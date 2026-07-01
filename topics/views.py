from collections import defaultdict

from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Count, F, Prefetch, Q
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from . import search as fts

from .models import (
    SECTION_ORDER,
    Action,
    Category,
    InputSummary,
    Position,
    Prompt,
    Question,
    QuestionLean,
    Response,
    Section,
    Stance,
    Stat,
    Submission,
    Topic,
    Vote,
)


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _decorate(topics):
    """Attach `dots` (position colours) and `is_stub` to topic cards in one sweep."""
    topics = list(topics)
    if not topics:
        return topics
    ids = [t.id for t in topics]
    dot_map = {}
    for p in (
        Position.objects.filter(section__topic_id__in=ids, section__kind="positions")
        .select_related("section")
        .order_by("order")
    ):
        dot_map.setdefault(p.section.topic_id, []).append(p.color_var)
    authored = set(
        Section.objects.filter(topic_id__in=ids).values_list("topic_id", flat=True)
    )
    for t in topics:
        t.dots = dot_map.get(t.id, [])
        t.is_stub = t.id not in authored
    return topics


def _ordered_sections(parent_field, parent):
    positions = Position.objects.annotate(
        agree_count=Count("stances", filter=Q(stances__value=Stance.AGREE)),
        disagree_count=Count("stances", filter=Q(stances__value=Stance.DISAGREE)),
    ).order_by("-importance", "-prevalence_weight", "order", "id")
    qs = Section.objects.filter(**{parent_field: parent}).prefetch_related(
        Prefetch("stats", queryset=Stat.objects.order_by("order", "id")),
        Prefetch(
            "questions", queryset=Question.objects.order_by("-votes", "order", "id")
        ),
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


def _attach_prompts(request, topic, sections):
    """Load the active prompts attached to a topic and its sub-pieces, attach to
    each the participant's saved Response (`user_response`) and the latest
    approved InputSummary (`summary`), and hang the child-attached ones off their
    object (`question.prompts` / `position.prompts` / `section.prompts`). Returns
    the topic-level prompts as a list. One query per concern — no per-prompt N+1."""
    question_ids, position_ids = [], []
    for s in sections:
        if s.kind == Section.QUESTIONS:
            question_ids += [q.id for q in s.questions.all()]
        elif s.kind == Section.POSITIONS:
            position_ids += [p.id for p in s.positions.all()]

    ct = ContentType.objects.get_for_model
    topic_ct = ct(Topic)
    section_ct = ct(Section)
    question_ct = ct(Question)
    position_ct = ct(Position)
    scopes = [
        (topic_ct.id, {topic.id}),
        (section_ct.id, {s.id for s in sections}),
        (question_ct.id, set(question_ids)),
        (position_ct.id, set(position_ids)),
    ]
    selector = Q()
    for ct_id, ids in scopes:
        if ids:
            selector |= Q(content_type_id=ct_id, object_id__in=ids)
    if not selector:
        return []

    prompts = list(
        Prompt.objects.filter(active=True)
        .filter(selector)
        .prefetch_related("options", "responses")
    )
    pids = [p.id for p in prompts]

    # Latest approved summary per prompt (the public "what readers think").
    summary_map = {}
    for s in InputSummary.objects.filter(
        prompt_id__in=pids, status=InputSummary.APPROVED
    ).order_by("-generated_at"):
        summary_map.setdefault(s.prompt_id, s)

    # The participant's own response — read off the prefetched rows so passive
    # readers don't trigger a session (mirrors topic_detail's `who`).
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

    topic_prompts = []
    by_section, by_question, by_position = (
        defaultdict(list),
        defaultdict(list),
        defaultdict(list),
    )
    for p in prompts:
        if p.content_type_id == topic_ct.id:
            topic_prompts.append(p)
        elif p.content_type_id == question_ct.id:
            by_question[p.object_id].append(p)
        elif p.content_type_id == position_ct.id:
            by_position[p.object_id].append(p)
        elif p.content_type_id == section_ct.id:
            by_section[p.object_id].append(p)

    for s in sections:
        s.prompts = by_section.get(s.id, [])
        if s.kind == Section.QUESTIONS:
            for q in s.questions.all():
                q.prompts = by_question.get(q.id, [])
        elif s.kind == Section.POSITIONS:
            for p in s.positions.all():
                p.prompts = by_position.get(p.id, [])
    return topic_prompts


# --------------------------------------------------------------------------- #
# Pages
# --------------------------------------------------------------------------- #
def home(request):
    authored = (
        Topic.published.filter(sections__kind="positions")
        .select_related("primary_category")
        .distinct()
    )
    featured = (
        authored.prefetch_related("categories").first()
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
            "positions": positions,
            "crux": getattr(crux_section, "crux", None) if crux_section else None,
            "counts": {
                "positions": len(positions),
                "questions": Question.objects.filter(section__topic=featured).count(),
                "stats": Stat.objects.filter(section__topic=featured).count(),
            },
        }

    bench_ids = [featured.id] if featured else []
    bench = _decorate(
        Topic.published.exclude(id__in=bench_ids).select_related("primary_category")[:3]
    )

    categories = []
    for cat in Category.objects.prefetch_related(
        Prefetch("topics", queryset=Topic.published.select_related("primary_category"))
    ):
        topic_list = _decorate(cat.topics.all())
        if topic_list:
            categories.append({"category": cat, "topics": topic_list})

    all_topics = _decorate(Topic.published.select_related("primary_category"))

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


def about(request):
    return render(
        request,
        "topics/about.html",
        {
            "counts": {
                "topics": Topic.published.count(),
                "mapped": Topic.published.filter(sections__isnull=False)
                .distinct()
                .count(),
                "categories": Category.objects.count(),
            }
        },
    )


def _visible_topics(request):
    """Drafts exist only for staff (preview); everyone else sees published."""
    return Topic.objects if request.user.is_staff else Topic.published


def topic_detail(request, slug):
    topic = get_object_or_404(
        _visible_topics(request)
        .select_related("primary_category")
        .prefetch_related("categories"),
        slug=slug,
    )
    sections = _ordered_sections("topic", topic)
    related = topic.outgoing_edges.select_related(
        "target", "target__primary_category"
    ).all()
    positions = next((s.positions.all() for s in sections if s.kind == "positions"), [])
    if request.user.is_authenticated:
        who = {"user": request.user}
    else:
        who = {"session_key": request.session.session_key or ""}
    voted_q, voted_p, stance_map, lean_map = {}, {}, {}, {}
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
        stance_map = dict(
            Stance.objects.filter(position__section__topic=topic, **who).values_list(
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
                p.stance = stance_map.get(p.id, "")
    topic_prompts = _attach_prompts(request, topic, sections)
    # Filter chips derived from the action kinds actually present, so a chip never
    # dead-ends to an empty grid. submit_view stays off the bar (it's the "add your
    # view" CTA, shown under All).
    actions_section = next((s for s in sections if s.kind == "actions"), None)
    present = (
        {a.kind for a in actions_section.actions.all()} if actions_section else set()
    )
    act_filters = [("all", "All")] + [
        (key, label)
        for key, kind, label in (
            ("learn", Action.LEARN_MORE, "Learn"),
            ("donate", Action.DONATE, "Donate"),
            ("volunteer", Action.VOLUNTEER, "Volunteer"),
            ("policy", Action.POLICY, "Policy"),
            ("local", Action.LOCAL, "Local"),
        )
        if kind in present
    ]
    return render(
        request,
        "topics/detail.html",
        {
            "topic": topic,
            "sections": sections,
            "related": related,
            "positions": positions,
            "topic_prompts": topic_prompts,
            "min_prompt_sample": MIN_PROMPT_SAMPLE,
            "act_filters": act_filters,
        },
    )


def category_detail(request, slug):
    category = get_object_or_404(
        Category.objects.prefetch_related("connects_to"), slug=slug
    )
    sections = _ordered_sections("category", category)
    topics = _decorate(
        category.topics(manager="published").select_related("primary_category").all()
    )
    return render(
        request,
        "topics/category.html",
        {"category": category, "sections": sections, "topics": topics},
    )


def poster(request, slug):
    topic = get_object_or_404(
        _visible_topics(request).select_related("primary_category"), slug=slug
    )
    sec = {s.kind: s for s in _ordered_sections("topic", topic)}
    return render(request, "topics/poster.html", {"topic": topic, "sec": sec})


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
            # detail page); the header still reports the debate's full size.
            "positions": all_positions[: Section.POSITIONS_DEFAULT_SHOWN],
            "positions_total": len(all_positions),
            "crux": getattr(crux_section, "crux", None) if crux_section else None,
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
    topics, categories, positions = [], [], []
    if q and fts.available():
        tids = fts.search_ids(q, "topic", 6)
        cids = fts.search_ids(q, "category", 4)
        pids = fts.search_ids(q, "position", 4)
        topics = _decorate(
            _in_order(
                Topic.published.filter(id__in=tids).select_related("primary_category"),
                tids,
            )
        )
        categories = _in_order(Category.objects.filter(id__in=cids), cids)
        positions = _in_order(
            Position.objects.filter(
                id__in=pids, section__topic__status=Topic.PUBLISHED
            ).select_related("section", "section__topic"),
            pids,
        )
    elif q:
        topics = _decorate(
            Topic.published.filter(title__icontains=q).select_related(
                "primary_category"
            )[:6]
        )
        categories = Category.objects.filter(name__icontains=q)[:4]
        positions = (
            Position.objects.filter(
                name__icontains=q, section__topic__status=Topic.PUBLISHED
            )
            .select_related("section", "section__topic")
            .order_by("-importance")[:4]
        )
    return render(
        request,
        "topics/components/_search_results.html",
        {"q": q, "topics": topics, "categories": categories, "positions": positions},
    )


@require_POST
def vote(request, target, pk):
    """Cast an up/down importance vote (POST dir=up|down): the same direction
    again retracts, the opposite switches. The Vote row is the truth; the
    model's net counter is a denormalized cache kept in step in one transaction."""
    if target == "question":
        obj = get_object_or_404(Question, pk=pk)
        lookup, counter = {"question": obj}, "votes"
        template, ctx = "topics/components/_qvote.html", "q"
    elif target == "position":
        obj = get_object_or_404(Position, pk=pk)
        lookup, counter = {"position": obj}, "importance"
        template, ctx = "topics/components/_pimp.html", "p"
    else:
        return HttpResponseBadRequest("unknown vote target")

    direction = -1 if request.POST.get("dir") == "down" else 1
    who = _participant(request)
    with transaction.atomic():
        existing = Vote.objects.filter(**who, **lookup).first()
        if existing and existing.value == direction:
            existing.delete()
            delta, user_vote = -direction, 0
        elif existing:
            delta = direction - existing.value
            existing.value = direction
            existing.save(update_fields=["value"])
            user_vote = direction
        else:
            Vote.objects.create(**who, value=direction, **lookup)
            delta, user_vote = direction, direction
        type(obj).objects.filter(pk=obj.pk).update(**{counter: F(counter) + delta})
    obj.refresh_from_db(fields=[counter])
    obj.user_vote = user_vote
    # The control renders in the card and the mobile sheet under distinct ids.
    prefix = request.POST.get("prefix", "")
    context = {ctx: obj}
    if target == "position" and prefix in ("pimp", "spimp"):
        context["prefix"] = prefix
    return render(request, template, context)


@require_POST
def stance(request, pk):
    """Toggle/switch an agree-disagree stance on a position. Same value again
    retracts; the other value switches. Returns the position foot fragment."""
    position = get_object_or_404(Position, pk=pk)
    value = request.POST.get("value")
    if value not in (Stance.AGREE, Stance.DISAGREE):
        return HttpResponseBadRequest("unknown stance value")

    who = _participant(request)
    existing = Stance.objects.filter(position=position, **who).first()
    if existing and existing.value == value:
        existing.delete()
        position.stance = ""
    elif existing:
        existing.value = value
        existing.save(update_fields=["value", "updated_at"])
        position.stance = value
    else:
        Stance.objects.create(position=position, value=value, **who)
        position.stance = value

    position.voted = Vote.objects.filter(position=position, **who).exists()
    context = {"p": position}
    prefix = request.POST.get("prefix", "")
    if prefix in ("pfoot", "spfoot"):
        context["prefix"] = prefix
    return render(request, "topics/components/_pfoot.html", context)


@require_POST
def question_lean(request, pk):
    """Cast a community direction vote (pole a|b) on a question. Same pole again
    retracts; the other pole switches. Returns the _qlean fragment."""
    question = get_object_or_404(Question, pk=pk)
    value = request.POST.get("value")
    if value not in (QuestionLean.A, QuestionLean.B):
        return HttpResponseBadRequest("unknown lean value")

    who = _participant(request)
    existing = QuestionLean.objects.filter(question=question, **who).first()
    if existing and existing.value == value:
        existing.delete()
        question.user_lean = ""
    elif existing:
        existing.value = value
        existing.save(update_fields=["value", "updated_at"])
        question.user_lean = value
    else:
        QuestionLean.objects.create(question=question, value=value, **who)
        question.user_lean = value
    return render(request, "topics/components/_qlean.html", {"q": question})


@require_POST
def submit(request):
    topic = get_object_or_404(Topic, pk=request.POST.get("topic"))
    # The flow posts "none" for "None of these" — anything non-numeric means
    # no position alignment.
    pos_id = request.POST.get("position") or ""
    position = Position.objects.filter(pk=pos_id).first() if pos_id.isdigit() else None
    try:
        importance = max(1, min(5, int(request.POST.get("importance", 3))))
    except (TypeError, ValueError):
        importance = 3

    stance_value = request.POST.get("stance", "agree")
    who = _participant(request)
    Submission.objects.create(
        topic=topic,
        position=position,
        stance=stance_value,
        importance=importance,
        reasoning=request.POST.get("reasoning", "").strip(),
        email=request.POST.get("email", "").strip(),
        **who,
    )
    # A submission's agree/disagree is the same signal as the card toggle —
    # upsert the participant's Stance so aggregates stay one pool. (It no
    # longer bumps importance; that's a separate, explicit vote.)
    if position and stance_value in (Stance.AGREE, Stance.DISAGREE):
        Stance.objects.update_or_create(
            position=position, **who, defaults={"value": stance_value}
        )

    return render(
        request,
        "topics/components/_submit_done.html",
        {
            "topic": topic,
            "position": position,
            "stance": request.POST.get("stance", "agree"),
        },
    )


def _response_payload(request, prompt):
    """Read the POST for `prompt`'s kind into Response field defaults. Returns
    (defaults, keep): `keep` is False when there's nothing worth storing (an
    empty answer → retract, mirroring the vote/stance clear semantics). Invalid
    option ids are dropped; ratings clamp to 1–5."""
    valid = set(prompt.options.values_list("id", flat=True))
    text = (request.POST.get("text") or "").strip()
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
            note = (request.POST.get(f"note_{oid}") or "").strip()
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
