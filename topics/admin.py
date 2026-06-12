from django.contrib import admin

from .models import (
    Action,
    Category,
    Crux,
    Position,
    Question,
    Section,
    Stance,
    Stat,
    Submission,
    Topic,
    TopicEdge,
    Vote,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "color_key", "parent", "topic_count")
    list_filter = ("color_key", "parent")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("connects_to",)


class TopicSectionInline(admin.TabularInline):
    """The spine at a glance from the topic page; each row links to the
    section's own page where the typed children (stats, questions…) live."""

    model = Section
    extra = 0
    fields = ("kind", "intro")
    show_change_link = True


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "spine", "updated_at")
    list_filter = ("status", "categories")
    search_fields = ("title", "summary")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("categories",)
    inlines = [TopicSectionInline]
    actions = ("publish", "unpublish", "scaffold_sections")
    fieldsets = (
        (
            None,
            {"fields": ("title", "slug", "status", "icon", "summary", "categories")},
        ),
        ("Overview", {"fields": ("scope_covered", "scope_excluded", "why_now")}),
    )

    @admin.display(description="Spine")
    def spine(self, obj):
        missing = obj.missing_sections
        return "complete" if not missing else f"missing: {', '.join(missing)}"

    @admin.action(description="Publish selected topics")
    def publish(self, request, queryset):
        updated = queryset.update(status=Topic.PUBLISHED)
        self.message_user(request, f"{updated} topic(s) published.")

    @admin.action(description="Unpublish selected topics (back to draft)")
    def unpublish(self, request, queryset):
        updated = queryset.update(status=Topic.DRAFT)
        self.message_user(request, f"{updated} topic(s) back to draft.")

    @admin.action(description="Create missing spine sections")
    def scaffold_sections(self, request, queryset):
        created = 0
        for topic in queryset:
            for kind in topic.missing_sections:
                Section.objects.create(topic=topic, kind=kind)
                created += 1
        self.message_user(request, f"{created} section(s) created.")


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


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "session_key", "created_at")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)


@admin.register(Stance)
class StanceAdmin(admin.ModelAdmin):
    list_display = ("position", "value", "user", "session_key", "updated_at")
    list_filter = ("value",)
    readonly_fields = ("created_at", "updated_at")
