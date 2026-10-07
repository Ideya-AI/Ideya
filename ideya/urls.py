from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.shortcuts import redirect
from django.templatetags.static import static
from django.urls import include, path

from topics.sitemaps import SITEMAPS
from topics.views import robots_txt

urlpatterns = [
    path("sitemap.xml", sitemap, {"sitemaps": SITEMAPS}, name="sitemap"),
    path("robots.txt", robots_txt, name="robots"),
    # Browsers and crawlers ask for these at the root regardless of <link> tags.
    # Resolved per request, so a missing manifest entry is a 500 here, not a
    # site that fails to start.
    path("favicon.ico", lambda r: redirect(static("img/favicon.ico"), permanent=True)),
    path(
        "apple-touch-icon.png",
        lambda r: redirect(static("img/apple-touch-icon.png"), permanent=True),
    ),
    path("", include("topics.urls", namespace="topics")),
]

# Admin only in DEBUG (local dev): nobody signs in on the live site, and its
# login form runs the slow password hasher on every attempt.
if settings.DEBUG:
    urlpatterns.insert(0, path("admin/", admin.site.urls))
