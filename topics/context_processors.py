from django.conf import settings
from django.db.models import Count, Q

from .models import Category


def navigation(request):
    """Categories for the global nav menu (rendered in base.html on every page),
    and the public origin for canonical and share URLs, so they always name the
    canonical host whatever host the request came in on."""
    return {
        "origin": settings.PUBLIC_ORIGIN or f"{request.scheme}://{request.get_host()}",
        "nav_categories": Category.objects.annotate(
            num_topics=Count("topics", filter=Q(topics__status="published"))
        ),
    }
