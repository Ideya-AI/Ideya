from django.contrib import admin

from .models import Topic, TopicEdge


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "updated_at")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "summary")
    fieldsets = (
        (None, {"fields": ("title", "slug", "summary")}),
        ("L1 — Overview", {"fields": ("l1_content",)}),
        ("L2 — Comprehensive", {"fields": ("l2_content",)}),
        ("L3 — Learning map", {"fields": ("l3_content",)}),
    )


@admin.register(TopicEdge)
class TopicEdgeAdmin(admin.ModelAdmin):
    list_display = ("source", "kind", "target")
    list_filter = ("kind",)
