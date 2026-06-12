from django.db import transaction
from django.db.models import Count, F, Prefetch, Q
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from .models import (
    SECTION_ORDER,
    Action,
    Category,
    Position,
    Question,
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
    ).order_by("order", "id")
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
    voted_q, voted_p, stance_map = set(), set(), {}
    if request.user.is_authenticated or request.session.session_key:
        voted_q = set(
            Vote.objects.filter(question__section__topic=topic, **who).values_list(
                "question_id", flat=True
            )
        )
        voted_p = set(
            Vote.objects.filter(position__section__topic=topic, **who).values_list(
                "position_id", flat=True
            )
        )
        stance_map = dict(
            Stance.objects.filter(position__section__topic=topic, **who).values_list(
                "position_id", "value"
            )
        )
    for s in sections:
        if s.kind == "questions":
            for q in s.questions.all():
                q.voted = q.id in voted_q
        elif s.kind == "positions":
            for p in s.positions.all():
                p.voted = p.id in voted_p
                p.stance = stance_map.get(p.id, "")
    return render(
        request,
        "topics/detail.html",
        {
            "topic": topic,
            "sections": sections,
            "related": related,
            "positions": positions,
            "depths": [
                ("condensed", "Condensed"),
                ("normal", "Normal"),
                ("deep", "Deep"),
            ],
            "act_filters": [
                ("all", "All"),
                ("learn", "Learn"),
                ("donate", "Donate"),
                ("policy", "Policy"),
                ("local", "Local"),
            ],
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
    return render(
        request,
        "topics/share.html",
        {
            "topic": topic,
            "positions": pos_section.positions.all() if pos_section else [],
            "crux": getattr(crux_section, "crux", None) if crux_section else None,
        },
    )


# --------------------------------------------------------------------------- #
# Interactions
# --------------------------------------------------------------------------- #
def search(request):
    q = (request.GET.get("q") or "").strip()
    topics, categories, positions = [], [], []
    if q:
        topics = _decorate(
            Topic.published.filter(title__icontains=q).select_related(
                "primary_category"
            )[:6]
        )
        categories = Category.objects.filter(name__icontains=q)[:4]
        positions = (
            Position.objects.filter(name__icontains=q)
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
    """Toggle an importance vote: first POST casts it, a second retracts it.
    The Vote row is the truth; the counter on the model is a denormalized
    cache kept in step inside the same transaction."""
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

    who = _participant(request)
    with transaction.atomic():
        existing = Vote.objects.filter(**who, **lookup).first()
        if existing:
            existing.delete()
            delta = -1
        else:
            Vote.objects.create(**who, **lookup)
            delta = 1
        type(obj).objects.filter(pk=obj.pk).update(**{counter: F(counter) + delta})
    obj.refresh_from_db(fields=[counter])
    obj.voted = delta > 0
    return render(request, template, {ctx: obj})


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
    return render(request, "topics/components/_pfoot.html", {"p": position})


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
