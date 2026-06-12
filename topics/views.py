from django.db.models import Prefetch
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
    Stat,
    Submission,
    Topic,
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
    qs = Section.objects.filter(**{parent_field: parent}).prefetch_related(
        Prefetch("stats", queryset=Stat.objects.order_by("order", "id")),
        Prefetch(
            "questions", queryset=Question.objects.order_by("-votes", "order", "id")
        ),
        Prefetch("positions", queryset=Position.objects.order_by("order", "id")),
        Prefetch(
            "actions",
            queryset=Action.objects.select_related("position").order_by("order", "id"),
        ),
        "crux",
    )
    by_kind = {s.kind: s for s in qs}
    return [by_kind[k] for k in SECTION_ORDER if k in by_kind]


# --------------------------------------------------------------------------- #
# Pages
# --------------------------------------------------------------------------- #
def home(request):
    authored = (
        Topic.objects.filter(sections__kind="positions")
        .select_related("primary_category")
        .distinct()
    )
    featured = (
        authored.prefetch_related("categories").first()
        or Topic.objects.select_related("primary_category").first()
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
        Topic.objects.exclude(id__in=bench_ids).select_related("primary_category")[:3]
    )

    categories = []
    for cat in Category.objects.prefetch_related(
        Prefetch("topics", queryset=Topic.objects.select_related("primary_category"))
    ):
        topic_list = _decorate(cat.topics.all())
        if topic_list:
            categories.append({"category": cat, "topics": topic_list})

    all_topics = _decorate(Topic.objects.select_related("primary_category"))

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
                "topics": Topic.objects.count(),
                "mapped": Topic.objects.filter(sections__isnull=False)
                .distinct()
                .count(),
                "categories": Category.objects.count(),
            }
        },
    )


def topic_detail(request, slug):
    topic = get_object_or_404(
        Topic.objects.select_related("primary_category").prefetch_related("categories"),
        slug=slug,
    )
    sections = _ordered_sections("topic", topic)
    related = topic.outgoing_edges.select_related(
        "target", "target__primary_category"
    ).all()
    positions = next((s.positions.all() for s in sections if s.kind == "positions"), [])
    voted = request.session.get("voted", {})
    for s in sections:
        if s.kind == "questions":
            for q in s.questions.all():
                q.voted = voted.get(f"question:{q.id}", False)
        elif s.kind == "positions":
            for p in s.positions.all():
                p.voted = voted.get(f"position:{p.id}", False)
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
    topics = _decorate(category.topics.select_related("primary_category").all())
    return render(
        request,
        "topics/category.html",
        {"category": category, "sections": sections, "topics": topics},
    )


def poster(request, slug):
    topic = get_object_or_404(
        Topic.objects.select_related("primary_category"), slug=slug
    )
    sec = {s.kind: s for s in _ordered_sections("topic", topic)}
    return render(request, "topics/poster.html", {"topic": topic, "sec": sec})


def share_cards(request, slug):
    topic = get_object_or_404(
        Topic.objects.select_related("primary_category"), slug=slug
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
            Topic.objects.filter(title__icontains=q).select_related("primary_category")[
                :6
            ]
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
    voted = request.session.setdefault("voted", {})
    key = f"{target}:{pk}"
    already = voted.get(key)

    if target == "question":
        obj = get_object_or_404(Question, pk=pk)
        if not already:
            obj.votes += 1
            obj.save(update_fields=["votes"])
            voted[key] = True
            request.session.modified = True
        obj.voted = True
        return render(request, "topics/components/_qvote.html", {"q": obj})

    if target == "position":
        obj = get_object_or_404(Position, pk=pk)
        if not already:
            obj.importance += 1
            obj.save(update_fields=["importance"])
            voted[key] = True
            request.session.modified = True
        obj.voted = True
        return render(request, "topics/components/_pimp.html", {"p": obj})

    return HttpResponseBadRequest("unknown vote target")


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

    Submission.objects.create(
        topic=topic,
        position=position,
        stance=request.POST.get("stance", "agree"),
        importance=importance,
        reasoning=request.POST.get("reasoning", "").strip(),
        email=request.POST.get("email", "").strip(),
    )
    if position:
        position.importance += 1
        position.save(update_fields=["importance"])

    return render(
        request,
        "topics/components/_submit_done.html",
        {
            "topic": topic,
            "position": position,
            "stance": request.POST.get("stance", "agree"),
        },
    )
