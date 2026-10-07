from django.contrib import admin, messages
from django.utils import timezone

from .models import (
    Action,
    Category,
    Crux,
    InputSummary,
    ParticipationEvent,
    Position,
    Prompt,
    PromptOption,
    Question,
    Response,
    Section,
    Stat,
    Topic,
    TopicEdge,
    Vote,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "color_key", "topic_count")
    list_filter = ("color_key",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("connects_to",)


class TopicSectionInline(admin.TabularInline):
    """The spine at a glance from the topic page; each row links to the
    section's own page where the typed children (stats, questions…) live."""

    model = Section
    extra = 0
    fields = ("kind",)
    show_change_link = True


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "review_status",
        "spine",
        "updated_at",
    )
    list_filter = ("status", "categories", "primary_category")
    # Readiness is set upstream and cleared by any content load; never editable here.
    search_fields = ("title", "summary")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("categories",)
    inlines = [TopicSectionInline]
    actions = ("publish", "unpublish", "mark_reviewed", "scaffold_sections")
    # `status` is deliberately NOT editable here. Publishing is one command with
    # one gate; a free-text dropdown beside it would be a second, ungated way to
    # do the same thing, and the ungated one always wins. Use the Publish action,
    # `manage.py publish_topic`, or `manage.py mark_ready`.
    readonly_fields = ("authored_at", "status", "review_due_display")
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
                    "Every topic is due for review 180 days after its last review, "
                    "else its authoring. Surfaced by the topics_due command."
                ),
                "fields": (
                                "review_due_display",
                    "authored_at",
                    "published_at",
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
        """Same gate as `manage.py publish_topic`: only a topic the engine
        certified READY can be made public, from here or anywhere, or the admin
        would be the hole in the rule."""
        ready = queryset.filter(status=Topic.READY)
        blocked = [t.slug for t in queryset.exclude(status=Topic.READY)]
        updated = ready.update(status=Topic.PUBLISHED, published_at=timezone.now())
        if updated:
            self.message_user(request, f"{updated} topic(s) published.")
        if blocked:
            self.message_user(
                request,
                "Not published — not READY: " + ", ".join(blocked),
                level=messages.WARNING,
            )

    @admin.action(description="Take selected topics off the site (back to ready)")
    def unpublish(self, request, queryset):
        """Back to READY, not to IN_PROGRESS: taking a page off the site says
        nothing about whether its content is still verified."""
        updated = queryset.filter(status=Topic.PUBLISHED).update(status=Topic.READY)
        self.message_user(request, f"{updated} topic(s) taken off the site.")

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

        stamp = timezone.now().isoformat()
        updated = 0
        for topic in queryset:
            topic.reviewed_at = list(topic.reviewed_at or []) + [stamp]
            topic.save(update_fields=["reviewed_at"])
            updated += 1
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
    search_fields = ("topic__title", "category__name")
    fields = ("topic", "category", "kind")

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


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "session_key", "created_at")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)


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


@admin.register(ParticipationEvent)
class ParticipationEventAdmin(admin.ModelAdmin):
    """The append-only participation record — browse and search, never edit."""

    list_display = (
        "created_at", "kind", "action", "topic_slug", "target_kind",
        "target_text", "prompt_text", "session_key",
    )
    list_filter = ("kind", "action", "target_kind", "trigger", "topic_slug")
    search_fields = ("target_text", "prompt_text", "session_key", "payload")
    date_hierarchy = "created_at"
    readonly_fields = [f.name for f in ParticipationEvent._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


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
