from django.db.models import Count, Q

from .models import Category


def navigation(request):
    """Categories for the global nav menu (rendered in base.html on every page)."""
    return {
        "nav_categories": Category.objects.annotate(
            num_topics=Count("topics", filter=Q(topics__status="published"))
        ),
    }
