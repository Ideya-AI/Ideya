from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from topics.sitemaps import SITEMAPS
from topics.views import robots_txt

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": SITEMAPS}, name="sitemap"),
    path("robots.txt", robots_txt, name="robots"),
    path("", include("topics.urls", namespace="topics")),
]
