from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Category, Topic


class TopicSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Topic.published.all()

    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Category.objects.all()


class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return ["topics:home", "topics:about"]

    def location(self, item):
        return reverse(item)


SITEMAPS = {
    "topics": TopicSitemap,
    "categories": CategorySitemap,
    "static": StaticSitemap,
}
