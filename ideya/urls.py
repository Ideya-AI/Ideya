from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from topics.sitemaps import SITEMAPS
from topics.views import robots_txt

urlpatterns = [
    path("sitemap.xml", sitemap, {"sitemaps": SITEMAPS}, name="sitemap"),
    path("robots.txt", robots_txt, name="robots"),
    path("", include("topics.urls", namespace="topics")),
]

# Admin only in DEBUG (local dev): nobody signs in on the live site, and its
# login form runs the slow password hasher on every attempt.
if settings.DEBUG:
    urlpatterns.insert(0, path("admin/", admin.site.urls))
