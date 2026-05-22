from django.shortcuts import get_object_or_404, render

from .models import Topic


def topic_index(request):
    topics = Topic.objects.all()
    return render(request, "topics/index.html", {"topics": topics})


def topic_detail(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    related = topic.outgoing_edges.select_related("target").all()
    return render(
        request,
        "topics/detail.html",
        {"topic": topic, "related": related},
    )
