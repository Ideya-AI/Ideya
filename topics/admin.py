from django.contrib import admin

from .models import (
    Action,
    Category,
    Crux,
    InputSummary,
    Position,
    Prompt,
    PromptOption,
    Question,
    Response,
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
    list_display = (
        "title",
        "status",
        "volatility",
        "review_status",
        "spine",
        "updated_at",
    )
    list_filter = ("status", "volatility", "categories", "primary_category")
    search_fields = ("title", "summary")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("categories",)
    inlines = [TopicSectionInline]
    actions = ("publish", "unpublish", "mark_reviewed", "scaffold_sections")
    readonly_fields = ("researched_at", "research_dossier", "review_due_display")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "status",
                    "icon",
                    "summary",
                    "primary_category",
                    "categories",
                )
            },
        ),
        ("Overview", {"fields": ("scope_covered", "scope_excluded", "why_now")}),
        (
            "Primary art",
            {
                "classes": ("collapse",),
                "description": (
                    "The bespoke hero illustration is committed at "
                    "static/img/topics/&lt;slug&gt;.png. This field stores the "
                    "prompt used to generate it."
                ),
                "fields": ("primary_image_prompt",),
            },
        ),
        (
            "Review & freshness",
            {
                "description": (
                    "Volatility sets the review cadence (fast ~90d / medium ~180d "
                    "/ slow ~365d); the clock runs from the last review, else the "
                    "last research. Surfaced by the topics_due command."
                ),
                "fields": (
                    "volatility",
                    "reviewed_at",
                    "review_due_display",
                    "researched_at",
                    "research_dossier",
                ),
            },
        ),
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

    @admin.display(description="Review")
    def review_status(self, obj):
        if obj.last_touched is None:
            return "⚠ never reviewed"
        overdue = obj.days_overdue
        return f"⚠ {overdue}d overdue" if overdue >= 0 else f"ok · due in {-overdue}d"

    @admin.display(description="Next review due")
    def review_due_display(self, obj):
        due = obj.review_due_at
        if due is None:
            return "needs first review"
        return f"{due.date().isoformat()} — {self.review_status(obj)}"

    @admin.action(description="Mark reviewed now (reset the freshness clock)")
    def mark_reviewed(self, request, queryset):
        from django.utils import timezone

        updated = queryset.update(reviewed_at=timezone.now())
        self.message_user(request, f"{updated} topic(s) marked reviewed.")

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
    fields = (
        "order",
        "label",
        "viz",
        "wide",
        "value",
        "unit",
        "fill_pct",
        "note",
        "source_label",
        "source_published",
    )


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ("order", "text", "kind", "why", "votes")


class PositionInline(admin.TabularInline):
    model = Position
    extra = 1
    fields = (
        "order",
        "name",
        "color_key",
        "steelman",
        "prevalence_weight",
        "spectrum_position",
        "importance",
    )


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


class PromptOptionInline(admin.TabularInline):
    model = PromptOption
    extra = 2
    fields = ("order", "label", "position")


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ("text", "kind", "target_label", "active", "order", "n_responses")
    list_filter = ("kind", "active", "content_type")
    search_fields = ("text", "help_text")
    inlines = [PromptOptionInline]

    @admin.display(description="Responses")
    def n_responses(self, obj):
        return obj.responses.count()


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = (
        "prompt",
        "text_preview",
        "rating",
        "user",
        "session_key",
        "updated_at",
    )
    list_filter = ("prompt__kind", "prompt")
    search_fields = ("text",)
    readonly_fields = ("created_at", "updated_at")

    @admin.display(description="Text")
    def text_preview(self, obj):
        t = (obj.text or "").strip()
        return (t[:70] + "…") if len(t) > 70 else (t or "—")


@admin.register(InputSummary)
class InputSummaryAdmin(admin.ModelAdmin):
    list_display = (
        "prompt",
        "status",
        "n_responses",
        "model",
        "generated_at",
        "approved_at",
    )
    list_filter = ("status", "model")
    search_fields = ("body", "prompt__text")
    readonly_fields = (
        "generated_at",
        "approved_by",
        "approved_at",
        "n_responses",
        "model",
    )
    actions = ("approve_summaries", "reject_summaries")

    @admin.action(description="Approve selected summaries (publish to readers)")
    def approve_summaries(self, request, queryset):
        from django.utils import timezone

        updated = queryset.update(
            status=InputSummary.APPROVED,
            approved_by=request.user,
            approved_at=timezone.now(),
        )
        self.message_user(request, f"{updated} summary(ies) approved.")

    @admin.action(description="Reject selected summaries")
    def reject_summaries(self, request, queryset):
        updated = queryset.update(status=InputSummary.REJECTED)
        self.message_user(request, f"{updated} summary(ies) rejected.")
