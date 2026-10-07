import qrcode
import qrcode.image.svg

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import F, Prefetch
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from . import ratelimit
from . import search as fts


def _rate_ok(request):
    """Guard the accountless participation writes against scripted spam. Returns
    a 429 response when this IP is over the cap, else None to continue."""
    if not getattr(settings, "PARTICIPATION_RATELIMIT", True):
        return None
    if ratelimit.rate_limited(
        request,
        "participate",
        ratelimit.PARTICIPATE_LIMIT,
        ratelimit.PARTICIPATE_WINDOW,
    ) or ratelimit.rate_limited(
        request,
        "participate-day",
        ratelimit.PARTICIPATE_DAY_LIMIT,
        ratelimit.PARTICIPATE_DAY_WINDOW,
    ):
        return HttpResponse("Too many requests — slow down.", status=429)
    return None


from .models import (
    SECTION_ORDER,
    Action,
    Category,
    InputSummary,
    ParticipationEvent,
    Position,
    Prompt,
    Question,
    QuestionLean,
    Response,
    Section,
    Stat,
    Topic,
    Vote,
)


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _authored(qs):
    """Public listings show only fully-mapped topics (a positions section
    exists) — stubs and in-progress topics never appear in a public list."""
    return qs.filter(sections__kind="positions").distinct()


def _ordered_sections(parent_field, parent):
    # File order only: votes show as counts and never reorder (2026-10-06:
    # a reorder is an editorial decision).
    positions = Position.objects.order_by("order", "id")
    questions = Question.objects.order_by("order", "id")
    qs = Section.objects.filter(**{parent_field: parent}).prefetch_related(
        Prefetch("stats", queryset=Stat.objects.order_by("order", "id")),
        Prefetch("questions", queryset=questions),
        Prefetch("positions", queryset=positions),
        Prefetch(
            "actions",
            queryset=Action.objects.select_related("position").order_by("order", "id"),
        ),
        "crux",
    )
    by_kind = {s.kind: s for s in qs}
    return [by_kind[k] for k in SECTION_ORDER if k in by_kind]


def _participant_key(request) -> str:
    """The session key participation rows hang off. Created on first use so a
    reader only gets a session once they actually participate."""
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key


def _participant(request) -> dict:
    """Filter/create kwargs identifying this participant's rows (decision B:
    a user when logged in, the session otherwise)."""
    if request.user.is_authenticated:
        return {"user": request.user}
    return {"session_key": _participant_key(request)}


def _log_event(request, kind, action, target, payload=None, prompt=None):
    """Append one ParticipationEvent — the permanent record of a participation
    action (the current-state rows above it get edited, retracted and reset).
    `target` is the Topic / Section / Stat / Question / Position acted on (None
    for a prompt that is not attached to anything)."""
    if target is None:
        slug, text = "", ""
    elif isinstance(target, Topic):
        slug, text = target.slug, target.title
    elif isinstance(target, Section):
        slug, text = target.topic.slug, f"{target.get_kind_display()} section"
    else:
        slug = target.section.topic.slug
        text = (
            getattr(target, "text", None)
            or getattr(target, "name", None)
            or target.label
        )
    ParticipationEvent.objects.create(
        kind=kind,
        action=action,
        topic_slug=slug,
        target_kind=type(target).__name__.lower() if target else "",
        target_id=target.id if target else None,
        target_text=text[:400],
        prompt_id=prompt.id if prompt else None,
        prompt_text=prompt.text if prompt else "",
        trigger=prompt.trigger if prompt else "",
        payload=payload or {},
        user=request.user if request.user.is_authenticated else None,
        session_key=request.session.session_key or "",
    )


# Minimum responses before a prompt's live aggregate surfaces (mirrors the
# stance gate in spirit — avoids "1 vote = 100%" noise on the open layer).
MIN_PROMPT_SAMPLE = 5


def _decorate_prompt(prompt):
    """Attach render aids a prompt fragment needs that aren't plain fields.
    Currently: `ranked_options` — options in the participant's saved order (or
    the default option order) so the rank control renders in place."""
    if prompt.kind == Prompt.RANK:
        opts = list(prompt.options.all())
        resp = getattr(prompt, "user_response", None)
        if resp and resp.ranking:
            rank = {oid: i for i, oid in enumerate(resp.ranking)}
            opts.sort(key=lambda o: rank.get(o.id, len(rank)))
        prompt.ranked_options = opts
    return prompt


def _hydrate_prompts(request, prompts):
    """Attach to each prompt the participant's saved Response (`user_response`)
    and the latest approved InputSummary (`summary`), then decorate. One query
    for the summaries; responses are read off the prefetched rows so passive
    readers don't trigger a session (mirrors topic_detail's `who`)."""
    summary_map = {}
    for s in InputSummary.objects.filter(
        prompt_id__in=[p.id for p in prompts], status=InputSummary.APPROVED
    ).order_by("-generated_at"):
        summary_map.setdefault(s.prompt_id, s)

    user_id = request.user.id if request.user.is_authenticated else None
    skey = "" if user_id else (request.session.session_key or "")
    for p in prompts:
        ur = None
        for r in p.responses.all():
            if user_id and r.user_id == user_id:
                ur = r
                break
            if not user_id and skey and r.session_key == skey:
                ur = r
                break
        p.user_response = ur
        p.summary = summary_map.get(p.id)
        _decorate_prompt(p)
    return prompts


def _prompts_for(request, obj, trigger=""):
    """The active prompts attached to one object for one trigger (blank = the
    Add-your-view modal on a Topic; vote / lean_a / lean_b = the follow-up
    modal on a Question or Position), hydrated for rendering."""
    prompts = list(
        Prompt.objects.filter(
            active=True,
            trigger=trigger,
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id,
        ).prefetch_related("options", "responses")
    )
    return _hydrate_prompts(request, prompts)


def _with_follow_up(request, response, target, obj, trigger, eyebrow, icon):
    """Append the follow-up modal's body (and eyebrow) to a fragment response
    as out-of-band swaps and fire the "follow-up" event that opens it. A
    no-op when the item has no prompts for this trigger."""
    prompts = _prompts_for(request, obj, trigger)
    if prompts:
        body = render(
            request,
            "topics/components/_follow_body.html",
            {
                "target": target,
                "item": obj,
                "prompts": prompts,
                "eyebrow": eyebrow,
                "icon": icon,
                "min_prompt_sample": MIN_PROMPT_SAMPLE,
            },
        )
        response.content += body.content
        response["HX-Trigger"] = "follow-up"
    return response


# --------------------------------------------------------------------------- #
# Pages
# --------------------------------------------------------------------------- #
# Home spotlight and the four cards under it, chosen 2026-10-06. A slug
# that is not published is skipped and the slot falls back to file order.
SPOTLIGHT = "ai-future-of-work"
BENCH = [
    "nuclear-energy",
    "social-media-youth-mental-health",
    "ai-existential-risk",
    "housing-affordability-crisis",
]


def home(request):
    authored = (
        Topic.published.filter(sections__kind="positions")
        .select_related("primary_category")
        .distinct()
    )
    featured = (
        authored.filter(slug=SPOTLIGHT).first()
        or authored.prefetch_related("categories").first()
        or Topic.published.select_related("primary_category").first()
    )

    spotlight = None
    if featured:
        pos_section = (
            Section.objects.filter(topic=featured, kind="positions")
            .prefetch_related("positions")
            .first()
        )
        crux_section = Section.objects.filter(topic=featured, kind="crux").first()
        positions = list(pos_section.positions.all()) if pos_section else []
        spotlight = {
            "topic": featured,
            # Core positions only — mirrors the share cards and the detail
            # page's leading cards.
            "positions": positions[: Section.POSITIONS_DEFAULT_SHOWN],
            "crux": getattr(crux_section, "crux", None) if crux_section else None,
        }

    bench_ids = [featured.id] if featured else []
    rest = authored.exclude(id__in=bench_ids)
    chosen = {t.slug: t for t in rest.filter(slug__in=BENCH)}
    picked = [chosen[s] for s in BENCH if s in chosen]
    picked += list(rest.exclude(slug__in=BENCH)[: 4 - len(picked)])
    bench = picked

    categories = []
    for cat in Category.objects.prefetch_related(
        Prefetch(
            "topics",
            queryset=_authored(Topic.published.select_related("primary_category")),
        )
    ):
        # Include every category so the directory is genuinely complete; empty
        # ones render as browsable "coming soon" cards into their category page.
        categories.append({"category": cat, "topics": list(cat.topics.all())})
    # Populated categories lead; the not-yet-mapped ones cluster at the end.
    categories.sort(key=lambda g: 0 if g["topics"] else 1)

    all_topics = _authored(Topic.published.select_related("primary_category"))

    return render(
        request,
        "topics/home.html",
        {
            "spotlight": spotlight,
            "bench": bench,
            "categories": categories,
            "all_topics": all_topics,
        },
    )


def robots_txt(request):
    sitemap_url = request.build_absolute_uri("/sitemap.xml")
    return HttpResponse(
        f"User-agent: *\nAllow: /\nSitemap: {sitemap_url}\n",
        content_type="text/plain",
    )


def _visible_topics(request):
    """Drafts render in local dev (DEBUG) and for staff; the public sees
    published only. There are no reader accounts, so DEBUG is how drafts get
    previewed in practice."""
    if settings.DEBUG or request.user.is_staff:
        return Topic.objects
    return Topic.published


def topic_detail(request, slug):
    topic = get_object_or_404(
        Topic.objects.select_related("primary_category").prefetch_related("categories"),
        slug=slug,
    )
    # Drafts render in full for staff/DEBUG previews; the public gets the
    # coming-soon stub treatment (no sections, noindex) instead of a 404 —
    # related chips on published topics link to drafts as teasers.
    can_preview = settings.DEBUG or request.user.is_staff
    if topic.status != Topic.PUBLISHED and not can_preview:
        sections = []
    else:
        sections = _ordered_sections("topic", topic)
    related = topic.outgoing_edges.select_related(
        "target", "target__primary_category"
    ).all()
    if request.user.is_authenticated:
        who = {"user": request.user}
    else:
        who = {"session_key": request.session.session_key or ""}
    voted_q, voted_p, lean_map = {}, {}, {}
    if request.user.is_authenticated or request.session.session_key:
        voted_q = dict(
            Vote.objects.filter(question__section__topic=topic, **who).values_list(
                "question_id", "value"
            )
        )
        voted_p = dict(
            Vote.objects.filter(position__section__topic=topic, **who).values_list(
                "position_id", "value"
            )
        )
        lean_map = dict(
            QuestionLean.objects.filter(
                question__section__topic=topic, **who
            ).values_list("question_id", "value")
        )
    for s in sections:
        if s.kind == "questions":
            for q in s.questions.all():
                q.user_vote = voted_q.get(q.id, 0)
                q.user_lean = lean_map.get(q.id, "")
        elif s.kind == "positions":
            for p in s.positions.all():
                p.user_vote = voted_p.get(p.id, 0)
    topic_prompts = _prompts_for(request, topic)
    return render(
        request,
        "topics/detail.html",
        {
            "topic": topic,
            "sections": sections,
            "can_preview": can_preview,
            "related": related,
            "topic_prompts": topic_prompts,
            "min_prompt_sample": MIN_PROMPT_SAMPLE,
            # DEBUG-only capture aid: ?expanded=1 forces all depth layers
            # visible so render_screens --expanded can photograph them.
            "expanded": settings.DEBUG and request.GET.get("expanded") == "1",
        },
    )


def category_detail(request, slug):
    category = get_object_or_404(
        Category.objects.prefetch_related("connects_to"), slug=slug
    )
    topics = _authored(
        category.topics(manager="published").select_related("primary_category")
    )
    return render(
        request,
        "topics/category.html",
        {"category": category, "topics": topics},
    )


def site_share(request):
    """Bare 1200x630 OG card for the site itself, captured to a PNG
    (static/img/social/site.png → base.html's default og:image). Mirrors
    category_share: `?render=og` renders the card-only body for headless
    capture; anything else shows a framed dev preview."""
    return render(
        request,
        "topics/site_share.html",
        {
            "categories": Category.objects.all(),
            "render_card": request.GET.get("render") == "og",
        },
    )


def category_share(request, slug):
    """Bare 1200x630 OG card for a category, captured to a PNG (Category.social_card
    → og:image). `?render=og` renders the card-only body for headless capture; any
    other request shows the same card framed for a dev preview."""
    category = get_object_or_404(Category, slug=slug)
    topics = list(
        _authored(
            category.topics(manager="published").select_related("primary_category")
        )[:6]
    )
    return render(
        request,
        "topics/category_share.html",
        {
            "category": category,
            "topics": topics,
            "render_card": request.GET.get("render") == "og",
        },
    )


def poster(request, slug):
    topic = get_object_or_404(
        _visible_topics(request).select_related("primary_category"), slug=slug
    )
    sec = {s.kind: s for s in _ordered_sections("topic", topic)}
    origin = settings.PUBLIC_ORIGIN or request.build_absolute_uri("/").rstrip("/")
    topic_url = origin + topic.get_absolute_url()
    # Error correction H so the brand mark inset in the centre stays scannable.
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, border=2)
    qr.add_data(topic_url)
    qr.make(fit=True)
    qr_svg = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage).to_string(
        encoding="unicode"
    )
    return render(
        request,
        "topics/poster.html",
        {
            "topic": topic,
            "sec": sec,
            "topic_url_display": topic_url.split("://", 1)[-1],
            "qr_svg": qr_svg,
            "fitcheck": request.GET.get("fit") == "1",
        },
    )


def share_cards(request, slug):
    topic = get_object_or_404(
        _visible_topics(request).select_related("primary_category"), slug=slug
    )
    pos_section = (
        Section.objects.filter(topic=topic, kind="positions")
        .prefetch_related("positions")
        .first()
    )
    crux_section = Section.objects.filter(topic=topic, kind="crux").first()
    all_positions = list(pos_section.positions.all()) if pos_section else []
    return render(
        request,
        "topics/share.html",
        {
            "topic": topic,
            # Card shows only the primary positions (the leading cards on the
            # detail page).
            "positions": all_positions[: Section.POSITIONS_DEFAULT_SHOWN],
            "crux": getattr(crux_section, "crux", None) if crux_section else None,
            # Long titles step the card headline down a size bucket (mirrors
            # the poster's length buckets) so they never clip the layout. A
            # long single word ("Smartphones") can't wrap, so it steps down too.
            "title_class": (
                "t-long"
                if len(topic.title) > 40
                else (
                    "t-mid"
                    if len(topic.title) > 26
                    # measure the longest run that cannot wrap: "& Community"
                    # binds as one unit on the card (amp_nbsp)
                    else "t-word"
                    if max(map(len, topic.title.replace(" & ", " &_").split())) >= 11
                    else ""
                )
            ),
            "render_card": (
                request.GET.get("render")
                if request.GET.get("render") in ("og", "sq", "pt")
                else ""
            ),
            "render_unfurl": request.GET.get("render") == "unfurl",
        },
    )


# --------------------------------------------------------------------------- #
# Interactions
# --------------------------------------------------------------------------- #
def _in_order(qs, ids):
    """Materialize a queryset in the id order FTS ranked them."""
    by_id = {obj.id: obj for obj in qs}
    return [by_id[i] for i in ids if i in by_id]


def search(request):
    q = (request.GET.get("q") or "").strip()
    topics, categories = [], []
    if q and fts.available():
        tids = fts.search_ids(q, "topic", 6)
        cids = fts.search_ids(q, "category", 4)
        topics = _in_order(
            _authored(
                Topic.published.filter(id__in=tids).select_related("primary_category")
            ),
            tids,
        )
        categories = _in_order(Category.objects.filter(id__in=cids), cids)
    elif q:
        topics = _decorate(
            _authored(
                Topic.published.filter(title__icontains=q).select_related(
                    "primary_category"
                )
            )[:6]
        )
        categories = Category.objects.filter(name__icontains=q)[:4]
    return render(
        request,
        "topics/components/_search_results.html",
        {"q": q, "topics": topics, "categories": categories},
    )


@require_POST
def vote(request, target, pk):
    """Cast an upvote (the same participant again retracts). Downvotes were
    retired 2026-08-01 — the counter is a plain upvote count. The Vote row is
    the truth; the model's counter is a denormalized cache kept in step in one
    transaction."""
    if limited := _rate_ok(request):
        return limited
    if request.POST.get("dir") == "down":
        return HttpResponseBadRequest("downvotes are retired")
    # Only items on topics this reader can see: no voting on drafts by id.
    visible = {"section__topic__in": _visible_topics(request).all()}
    if target == "question":
        obj = get_object_or_404(Question, pk=pk, **visible)
        lookup, counter = {"question": obj}, "votes"
        template, ctx = "topics/components/_qvote.html", "q"
    elif target == "position":
        obj = get_object_or_404(Position, pk=pk, **visible)
        lookup, counter = {"position": obj}, "importance"
        template, ctx = "topics/components/_pimp.html", "p"
    else:
        return HttpResponseBadRequest("unknown vote target")

    direction = 1
    who = _participant(request)
    with transaction.atomic():
        existing = Vote.objects.filter(**who, **lookup).first()
        if existing:
            existing.delete()
            delta, user_vote = -direction, 0
        else:
            Vote.objects.create(**who, value=direction, **lookup)
            delta, user_vote = direction, direction
        type(obj).objects.filter(pk=obj.pk).update(**{counter: F(counter) + delta})
        _log_event(
            request, ParticipationEvent.VOTE, "cast" if delta > 0 else "retract", obj
        )
    obj.refresh_from_db(fields=[counter])
    obj.user_vote = user_vote
    # The control renders in the card and the mobile sheet under distinct ids.
    prefix = request.POST.get("prefix", "")
    context = {ctx: obj}
    if target == "position" and prefix in ("pimp", "spimp"):
        context["prefix"] = prefix
    response = render(request, template, context)
    # A cast (not a retract) opens the follow-up modal.
    if delta > 0:
        response = _with_follow_up(
            request,
            response,
            target,
            obj,
            Prompt.TRIGGER_VOTE,
            "",
            "",
        )
    return response


@require_POST
def question_lean(request, pk):
    """Cast a community direction vote (pole a|b) on a question. Same pole again
    retracts; the other pole switches. Returns the _qlean fragment."""
    if limited := _rate_ok(request):
        return limited
    question = get_object_or_404(
        Question, pk=pk, section__topic__in=_visible_topics(request).all()
    )
    value = request.POST.get("value")
    if value not in (QuestionLean.A, QuestionLean.B):
        return HttpResponseBadRequest("unknown lean value")

    who = _participant(request)
    existing = QuestionLean.objects.filter(question=question, **who).first()
    if existing and existing.value == value:
        existing.delete()
        question.user_lean = ""
        action = "retract"
    elif existing:
        existing.value = value
        existing.save(update_fields=["value", "updated_at"])
        question.user_lean = value
        action = "switch"
    else:
        QuestionLean.objects.create(question=question, value=value, **who)
        question.user_lean = value
        action = "cast"
    label = question.lean_label_a if value == QuestionLean.A else question.lean_label_b
    _log_event(
        request,
        ParticipationEvent.LEAN,
        action,
        question,
        {"value": value, "label": label},
    )
    response = render(request, "topics/components/_qlean.html", {"q": question})
    # A cast or switch (not a retract) opens the follow-up modal for that pole.
    if question.user_lean:
        label = (
            question.lean_label_a if value == QuestionLean.A else question.lean_label_b
        )
        response = _with_follow_up(
            request,
            response,
            "question",
            question,
            f"lean_{value}",
            f"You lean “{label}”",
            "arrows-left-right",
        )
    return response


FOLLOW_UP_TARGETS = {
    "stat": Stat,
    "question": Question,
    "position": Position,
    "section": Section,
}


def follow_up(request, target, pk):
    """Open the follow-up modal for one item from its respond button (no vote
    involved): an empty body whose out-of-band parts fill the modal."""
    model = FOLLOW_UP_TARGETS.get(target)
    if model is None:
        return HttpResponseBadRequest("unknown target")
    obj = get_object_or_404(model, pk=pk)
    if target == "section":
        trigger, eyebrow = Prompt.TRIGGER_MISSING, "Something missing?"
    else:
        noun = "fact" if target == "stat" else target
        trigger, eyebrow = Prompt.TRIGGER_RESPOND, f"Respond to this {noun}"
    return _with_follow_up(
        request, HttpResponse(""), target, obj, trigger, eyebrow, "chat-teardrop-text"
    )


# Reader text is cut to these lengths before it is stored, so a script cannot
# fill the disk through the respond endpoint.
MAX_TEXT = 4000
MAX_NOTE = 1000


def _response_payload(request, prompt):
    """Read the POST for `prompt`'s kind into Response field defaults. Returns
    (defaults, keep): `keep` is False when there's nothing worth storing (an
    empty answer → retract, mirroring the vote/stance clear semantics). Invalid
    option ids are dropped; ratings clamp to 1–5."""
    valid = set(prompt.options.values_list("id", flat=True))
    text = (request.POST.get("text") or "").strip()[:MAX_TEXT]
    defaults, structured = {}, False

    if prompt.kind == Prompt.FREE_TEXT:
        defaults["text"] = text
    elif prompt.kind == Prompt.CHOOSE_ONE:
        raw = request.POST.get("option") or ""
        sel = [int(raw)] if raw.isdigit() and int(raw) in valid else []
        defaults["selected_ids"] = sel
        structured = bool(sel)
    elif prompt.kind == Prompt.CHOOSE_MANY:
        sel = [
            int(o)
            for o in request.POST.getlist("option")
            if o.isdigit() and int(o) in valid
        ]
        sel = list(dict.fromkeys(sel))  # de-dupe, keep order
        defaults["selected_ids"] = sel
        structured = bool(sel)
        # Optional per-option note/answer, kept only for chosen options.
        notes = {}
        for oid in sel:
            note = (request.POST.get(f"note_{oid}") or "").strip()[:MAX_NOTE]
            if note:
                notes[str(oid)] = note
        defaults["option_texts"] = notes
    elif prompt.kind == Prompt.RATE:
        try:
            rating = max(1, min(5, int(request.POST.get("rating"))))
        except (TypeError, ValueError):
            rating = None
        defaults["rating"] = rating
        structured = rating is not None
    elif prompt.kind == Prompt.RANK:
        ranking, seen = [], set()
        for o in (request.POST.get("ranking") or "").split(","):
            o = o.strip()
            if o.isdigit() and int(o) in valid and int(o) not in seen:
                ranking.append(int(o))
                seen.add(int(o))
        defaults["ranking"] = ranking
        structured = bool(ranking)
    else:
        return None, False

    # Structured prompts may also collect an optional free-text "why".
    if prompt.collects_text and prompt.kind != Prompt.FREE_TEXT:
        defaults["text"] = text

    keep = structured or (prompt.collects_text and bool(text))
    return defaults, keep


@require_POST
def respond(request, pk):
    """Capture a reader's answer to an open-participation Prompt. One Response per
    participant, edited in place (upsert) like a vote; an empty answer retracts
    it. Returns the prompt fragment with the saved answer + live aggregate."""
    if limited := _rate_ok(request):
        return limited
    prompt = get_object_or_404(Prompt, pk=pk, active=True)
    defaults, keep = _response_payload(request, prompt)
    if defaults is None:
        return HttpResponseBadRequest("unknown prompt kind")

    who = _participant(request)
    with transaction.atomic():
        if keep:
            response, _ = Response.objects.update_or_create(
                prompt=prompt, **who, defaults=defaults
            )
        else:
            Response.objects.filter(prompt=prompt, **who).delete()
            response = None
        # The permanent record carries option labels, not ids, so it reads
        # without the (reseedable) PromptOption rows.
        labels = {o.id: o.label for o in prompt.options.all()}
        payload = {k: v for k, v in defaults.items() if v not in ("", None, [], {})}
        if "selected_ids" in payload:
            payload["selected"] = [
                labels.get(i, i) for i in payload.pop("selected_ids")
            ]
        if "ranking" in payload:
            payload["ranking"] = [labels.get(i, i) for i in payload["ranking"]]
        if "option_texts" in payload:
            payload["notes"] = {
                labels.get(int(i), i): t for i, t in payload.pop("option_texts").items()
            }
        _log_event(
            request,
            ParticipationEvent.RESPONSE,
            "save" if keep else "clear",
            prompt.target,
            payload,
            prompt,
        )

    prompt.user_response = response
    prompt.summary = (
        InputSummary.objects.filter(prompt=prompt, status=InputSummary.APPROVED)
        .order_by("-generated_at")
        .first()
    )
    _decorate_prompt(prompt)
    return render(
        request,
        "topics/components/_prompt.html",
        {"prompt": prompt, "min_prompt_sample": MIN_PROMPT_SAMPLE},
    )
