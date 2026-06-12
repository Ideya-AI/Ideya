from django.contrib import admin

from .models import (
    Action,
    Category,
    Crux,
    Position,
    Question,
    Section,
    Stat,
    Submission,
    Topic,
    TopicEdge,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "color_key", "parent", "topic_count")
    list_filter = ("color_key", "parent")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("connects_to",)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "updated_at")
    list_filter = ("categories",)
    search_fields = ("title", "summary")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("categories",)
    fieldsets = (
        (None, {"fields": ("title", "slug", "icon", "summary", "categories")}),
        ("Overview", {"fields": ("scope_covered", "scope_excluded", "why_now")}),
    )


class StatInline(admin.TabularInline):
    model = Stat
    extra = 1
    fields = ("order", "label", "viz", "wide", "value", "unit", "fill_pct", "note")


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ("order", "text", "kind", "why", "votes")


class PositionInline(admin.TabularInline):
    model = Position
    extra = 1
    fields = ("order", "name", "color_key", "steelman", "importance")


class ActionInline(admin.TabularInline):
    model = Action
    extra = 1
    fields = ("order", "kind", "title", "url", "position")


class CruxInline(admin.StackedInline):
    model = Crux
    extra = 0
    fields = ("lead", "lead_highlight", "subtitle", "empirical", "values")


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("__str__", "kind", "topic", "category")
    list_filter = ("kind",)
    search_fields = ("topic__title", "category__name", "intro", "body")
    fieldsets = (
        (None, {"fields": ("topic", "category", "kind")}),
        ("Content", {"fields": ("intro", "body")}),
    )

    def get_inlines(self, request, obj=None):
        if obj is None:
            return []
        return {
            Section.BASICS: [StatInline],
            Section.QUESTIONS: [QuestionInline],
            Section.POSITIONS: [PositionInline],
            Section.CRUX: [CruxInline],
            Section.ACTIONS: [ActionInline],
        }.get(obj.kind, [])


@admin.register(TopicEdge)
class TopicEdgeAdmin(admin.ModelAdmin):
    list_display = ("source", "kind", "target")
    list_filter = ("kind",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("topic", "position", "stance", "importance", "created_at")
    list_filter = ("stance", "topic")
    readonly_fields = ("created_at",)
