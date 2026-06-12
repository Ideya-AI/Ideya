from django.conf import settings
from django.db import models
from django.urls import reverse

# Fixed render order of a topic's (and category's) section spine.
SECTION_ORDER = [
    "overview",
    "basics",
    "questions",
    "positions",
    "crux",
    "actions",
    "topics",  # category pages only
]

# Position palette — keys map to --pos-* tokens. Assigned per-topic; no fixed meaning.
POS_COLORS = [
    ("green", "Green"),
    ("blue", "Blue"),
    ("amber", "Amber"),
    ("rust", "Rust"),
    ("purple", "Purple"),
    ("teal", "Teal"),
    ("slate", "Slate"),
]

# Minimum agree+disagree stances before a position's ratio is displayed
# (decision C: counts live, lean bars gated — avoids "2 votes = 100%" noise).
MIN_STANCE_SAMPLE = 10

# Reading-depth at which an item first appears. Shown when current depth >= reveal.
REVEAL_CHOICES = [
    ("condensed", "Always"),
    ("normal", "Normal+"),
    ("deep", "Deep only"),
]


def _reveal_class(value: str) -> str:
    """CSS class that makes an element appear at the right reading depth."""
    return {"condensed": "", "normal": "when-normal", "deep": "when-deep"}.get(
        value, ""
    )


# Category palette — keys map to --cat-* tokens. Discovery tiers only.
CAT_COLORS = [
    ("energy", "Energy & Environment"),
    ("tech", "AI & Technology"),
    ("gov", "Political & Governance"),
    ("econ", "Economic & Social"),
    ("ethics", "Ethics & Philosophy"),
    ("risk", "Existential & Global Risk"),
]


class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.CharField(max_length=400, blank=True)
    icon = models.CharField(
        max_length=80, blank=True, help_text="Phosphor icon name, e.g. 'leaf'."
    )
    color_key = models.CharField(
        max_length=10,
        choices=CAT_COLORS,
        default="energy",
        help_text="Maps to a --cat-* token. Used in discovery tiers only.",
    )
    parent = models.ForeignKey(
        "self",
        related_name="children",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    connects_to = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=True,
        help_text="Sibling categories surfaced as 'Connects to' chips.",
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("topics:category", args=[self.slug])

    @property
    def color_var(self) -> str:
        return f"var(--cat-{self.color_key})"

    @property
    def tint_var(self) -> str:
        return f"var(--cat-{self.color_key}-tint)"

    @property
    def topic_count(self) -> int:
        return self.topics.count()


class Topic(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    summary = models.CharField(
        max_length=400,
        blank=True,
        help_text="One-sentence framing for cards, previews, and the Overview hero.",
    )
    icon = models.CharField(
        max_length=80, blank=True, help_text="Phosphor icon name, e.g. 'atom'."
    )
    scope_covered = models.CharField(
        max_length=400, blank=True, help_text="What this topic covers."
    )
    scope_excluded = models.CharField(
        max_length=400, blank=True, help_text="What it deliberately excludes."
    )
    why_now = models.TextField(blank=True, help_text="Why it matters now.")
    categories = models.ManyToManyField(Category, related_name="topics", blank=True)
    primary_category = models.ForeignKey(
        Category,
        related_name="primary_topics",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Drives the topic's badge colour and category-page ordering.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("topics:detail", args=[self.slug])

    @property
    def color_category(self):
        """The category whose --cat-* colour tints this topic in discovery tiers."""
        return self.primary_category or self.categories.first()

    @property
    def category_badges(self):
        """Primary category first, then the rest — for the Overview badges."""
        cats = list(self.categories.all())
        primary = self.primary_category
        if primary:
            cats = [primary] + [c for c in cats if c.pk != primary.pk]
        return cats


class Section(models.Model):
    """One slot in a topic or category's section spine."""

    OVERVIEW = "overview"
    BASICS = "basics"
    QUESTIONS = "questions"
    POSITIONS = "positions"
    CRUX = "crux"
    ACTIONS = "actions"
    TOPICS = "topics"  # category-only

    KIND_CHOICES = [
        (OVERVIEW, "Overview"),
        (BASICS, "Basics"),
        (QUESTIONS, "Questions"),
        (POSITIONS, "Positions"),
        (CRUX, "Crux"),
        (ACTIONS, "Actions"),
        (TOPICS, "Topics"),
    ]

    # Per-section eyebrow icon + caption shown on the topic page.
    META = {
        OVERVIEW: ("compass-rose", "the orientation"),
        BASICS: ("chart-bar", "the numbers"),
        QUESTIONS: ("question", "what's contested · vote to reorder"),
        POSITIONS: ("scales", "the debate"),
        CRUX: ("target", "where it actually sits"),
        ACTIONS: ("compass", "paths forward, across the landscape"),
        TOPICS: ("squares-four", "explore the topics"),
    }

    topic = models.ForeignKey(
        Topic, related_name="sections", on_delete=models.CASCADE, null=True, blank=True
    )
    category = models.ForeignKey(
        Category,
        related_name="sections",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    intro = models.TextField(
        blank=True, help_text="Lead-in copy for sections that have typed children."
    )
    body = models.TextField(
        blank=True, help_text="Content body for Overview when used as free text."
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["topic", "kind"],
                condition=models.Q(topic__isnull=False),
                name="unique_topic_section_kind",
            ),
            models.UniqueConstraint(
                fields=["category", "kind"],
                condition=models.Q(category__isnull=False),
                name="unique_category_section_kind",
            ),
            models.CheckConstraint(
                check=(
                    models.Q(topic__isnull=False, category__isnull=True)
                    | models.Q(topic__isnull=True, category__isnull=False)
                ),
                name="section_belongs_to_exactly_one_parent",
            ),
        ]

    def __str__(self) -> str:
        parent = self.topic or self.category
        return f"{parent} — {self.get_kind_display()}"

    @property
    def eyebrow_icon(self) -> str:
        return self.META.get(self.kind, ("circle", ""))[0]

    @property
    def eyebrow_sub(self) -> str:
        return self.META.get(self.kind, ("", ""))[1]

    @property
    def step(self) -> str:
        try:
            return f"{SECTION_ORDER.index(self.kind) + 1:02d}"
        except ValueError:
            return ""


class Stat(models.Model):
    """One Basics figure. `viz` maps the fact's shape to a fixed visualization."""

    RANKED = "ranked"
    RADIAL = "radial"
    RANGE = "range"
    BAR = "bar"
    SPARKLINE = "sparkline"
    VIZ_CHOICES = [
        (RANKED, "Ranked bars"),
        (RADIAL, "Radial"),
        (RANGE, "Range marker"),
        (BAR, "Single bar"),
        (SPARKLINE, "Sparkline"),
    ]

    section = models.ForeignKey(Section, related_name="stats", on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=0)
    label = models.CharField(max_length=120, help_text="The metric, not a sentence.")
    viz = models.CharField(max_length=12, choices=VIZ_CHOICES, default=BAR)
    wide = models.BooleanField(default=False, help_text="Span two columns (ranked).")
    value = models.CharField(max_length=24, blank=True, help_text="Headline number.")
    unit = models.CharField(max_length=12, blank=True, help_text="e.g. %, g, ×, kt.")
    fill_pct = models.PositiveSmallIntegerField(
        null=True, blank=True, help_text="0–100 bar/radial fill."
    )
    series = models.JSONField(
        default=list,
        blank=True,
        help_text="Ranked/sparkline rows: [{label, value, pct, highlight}].",
    )
    range_min = models.CharField(max_length=40, blank=True)
    range_max = models.CharField(max_length=40, blank=True)
    range_at = models.PositiveSmallIntegerField(
        null=True, blank=True, help_text="0–100 marker position."
    )
    note = models.CharField(max_length=400, blank=True)
    source_url = models.URLField(blank=True)
    source_label = models.CharField(max_length=120, blank=True)
    reveal = models.CharField(
        max_length=10, choices=REVEAL_CHOICES, default="condensed"
    )

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return f"{self.label}: {self.value}"

    @property
    def reveal_class(self) -> str:
        return _reveal_class(self.reveal)


class Question(models.Model):
    EMPIRICAL = "empirical"
    VALUE = "value"
    KIND_CHOICES = [(EMPIRICAL, "Empirical"), (VALUE, "Value")]

    section = models.ForeignKey(
        Section, related_name="questions", on_delete=models.CASCADE
    )
    order = models.PositiveSmallIntegerField(default=0)
    text = models.CharField(max_length=400)
    kind = models.CharField(max_length=12, choices=KIND_CHOICES, default=EMPIRICAL)
    why = models.TextField(blank=True, help_text="Why this question is contested.")
    votes = models.PositiveIntegerField(default=0, help_text="Importance aggregate.")
    # Optional aggregated lean (shown at deep depth).
    lean_label_a = models.CharField(max_length=40, blank=True)
    lean_label_b = models.CharField(max_length=40, blank=True)
    lean_pct_a = models.PositiveSmallIntegerField(null=True, blank=True)
    reveal = models.CharField(
        max_length=10, choices=REVEAL_CHOICES, default="condensed"
    )

    class Meta:
        ordering = ["-votes", "order", "id"]

    def __str__(self) -> str:
        return self.text

    @property
    def reveal_class(self) -> str:
        return _reveal_class(self.reveal)

    @property
    def tag_icon(self) -> str:
        return "flask" if self.kind == self.EMPIRICAL else "heart"

    @property
    def lean_pct_b(self):
        return None if self.lean_pct_a is None else 100 - self.lean_pct_a


class Position(models.Model):
    section = models.ForeignKey(
        Section, related_name="positions", on_delete=models.CASCADE
    )
    order = models.PositiveSmallIntegerField(default=0)
    name = models.CharField(max_length=120)
    color_key = models.CharField(
        max_length=10,
        choices=POS_COLORS,
        default="green",
        help_text="Maps to a --pos-* token, unique within the topic.",
    )
    steelman = models.CharField(
        max_length=400, help_text="One-line strongest case, in the side's own voice."
    )
    description = models.TextField(blank=True)
    representative_name = models.CharField(max_length=120, blank=True)
    representative_note = models.CharField(max_length=300, blank=True)
    proponents = models.CharField(
        max_length=400, blank=True, help_text="Comma-separated notable proponents."
    )
    importance = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return self.name

    @property
    def color_var(self) -> str:
        return f"var(--pos-{self.color_key})"

    @property
    def proponent_list(self):
        return [p.strip() for p in self.proponents.split(",") if p.strip()]

    @property
    def stance_stats(self):
        """Agree/disagree aggregate. Uses agree_count/disagree_count annotations
        when the queryset provides them; falls back to queries for fragments."""
        agree = getattr(self, "agree_count", None)
        disagree = getattr(self, "disagree_count", None)
        if agree is None or disagree is None:
            agree = self.stances.filter(value="agree").count()
            disagree = self.stances.filter(value="disagree").count()
        total = agree + disagree
        return {
            "agree": agree,
            "disagree": disagree,
            "total": total,
            "pct_agree": round(100 * agree / total) if total else None,
            "shown": total >= MIN_STANCE_SAMPLE,
        }


class Crux(models.Model):
    """The synthesis — one per Crux section. The page's dark anchor."""

    section = models.OneToOneField(
        Section, related_name="crux", on_delete=models.CASCADE
    )
    lead = models.CharField(max_length=240, help_text="The narrowing, in display type.")
    lead_highlight = models.CharField(
        max_length=80, blank=True, help_text="Phrase inside lead to highlight green."
    )
    subtitle = models.TextField(blank=True, help_text="The framing.")
    empirical = models.TextField(blank=True, help_text="If empirical, then…")
    values = models.TextField(blank=True, help_text="If values, then…")

    def __str__(self) -> str:
        return f"Crux — {self.section.topic}"


class Action(models.Model):
    LEARN_MORE = "learn_more"
    DONATE = "donate"
    VOLUNTEER = "volunteer"
    POLICY = "policy"
    LOCAL = "local"
    SUBMIT_VIEW = "submit_view"

    KIND_CHOICES = [
        (LEARN_MORE, "Learn more"),
        (DONATE, "Donate"),
        (VOLUNTEER, "Volunteer"),
        (POLICY, "Policy"),
        (LOCAL, "Local"),
        (SUBMIT_VIEW, "Your view"),
    ]

    ICONS = {
        LEARN_MORE: "book-open",
        DONATE: "hand-coins",
        VOLUNTEER: "hand-heart",
        POLICY: "bank",
        LOCAL: "map-pin",
        SUBMIT_VIEW: "paper-plane-tilt",
    }

    section = models.ForeignKey(
        Section, related_name="actions", on_delete=models.CASCADE
    )
    order = models.PositiveSmallIntegerField(default=0)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default=LEARN_MORE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=400, blank=True)
    url = models.URLField(blank=True)
    position = models.ForeignKey(
        Position,
        related_name="aligned_actions",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Optional alignment to a specific position.",
    )
    reveal = models.CharField(
        max_length=10, choices=REVEAL_CHOICES, default="condensed"
    )

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return self.title

    @property
    def reveal_class(self) -> str:
        return _reveal_class(self.reveal)

    @property
    def phosphor_icon(self) -> str:
        return self.ICONS.get(self.kind, "arrow-up-right")


class TopicEdge(models.Model):
    DEPENDS_ON = "depends_on"
    RELATES_TO = "relates_to"
    EDGE_TYPES = [(DEPENDS_ON, "Depends on"), (RELATES_TO, "Relates to")]

    source = models.ForeignKey(
        Topic, related_name="outgoing_edges", on_delete=models.CASCADE
    )
    target = models.ForeignKey(
        Topic, related_name="incoming_edges", on_delete=models.CASCADE
    )
    kind = models.CharField(max_length=20, choices=EDGE_TYPES, default=RELATES_TO)
    note = models.CharField(max_length=300, blank=True)

    class Meta:
        unique_together = [("source", "target", "kind")]

    def __str__(self) -> str:
        return f"{self.source} -[{self.kind}]-> {self.target}"


class ParticipationBase(models.Model):
    """Shared keying for participation rows: a session now, a user once
    accounts land (decision B: hybrid — session rows merge into the user)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="+",
    )
    session_key = models.CharField(max_length=40, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Vote(ParticipationBase):
    """One importance vote on a question or a position. Idempotent (unique per
    participant per target) and retractable (the row is deleted)."""

    question = models.ForeignKey(
        Question,
        related_name="importance_votes",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    position = models.ForeignKey(
        Position,
        related_name="importance_votes",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(question__isnull=False, position__isnull=True)
                    | models.Q(question__isnull=True, position__isnull=False)
                ),
                name="vote_has_exactly_one_target",
            ),
            models.UniqueConstraint(
                fields=["question", "session_key"],
                condition=models.Q(question__isnull=False) & ~models.Q(session_key=""),
                name="unique_question_vote_per_session",
            ),
            models.UniqueConstraint(
                fields=["position", "session_key"],
                condition=models.Q(position__isnull=False) & ~models.Q(session_key=""),
                name="unique_position_vote_per_session",
            ),
            models.UniqueConstraint(
                fields=["question", "user"],
                condition=models.Q(question__isnull=False, user__isnull=False),
                name="unique_question_vote_per_user",
            ),
            models.UniqueConstraint(
                fields=["position", "user"],
                condition=models.Q(position__isnull=False, user__isnull=False),
                name="unique_position_vote_per_user",
            ),
        ]

    def __str__(self) -> str:
        return f"Vote · {self.question or self.position}"


class Stance(ParticipationBase):
    """One agree/disagree on a position. One row per participant per position;
    re-clicking the same value retracts it, the other value switches it."""

    AGREE = "agree"
    DISAGREE = "disagree"
    VALUE_CHOICES = [(AGREE, "Agree"), (DISAGREE, "Disagree")]

    position = models.ForeignKey(
        Position, related_name="stances", on_delete=models.CASCADE
    )
    value = models.CharField(max_length=10, choices=VALUE_CHOICES)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["position", "session_key"],
                condition=~models.Q(session_key=""),
                name="unique_stance_per_session",
            ),
            models.UniqueConstraint(
                fields=["position", "user"],
                condition=models.Q(user__isnull=False),
                name="unique_stance_per_user",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.get_value_display()} · {self.position}"


class Submission(models.Model):
    """One inbound 'submit your view' — anonymous by default, aggregated, never a comment."""

    AGREE = "agree"
    DISAGREE = "disagree"
    NEUTRAL = "neutral"
    STANCE_CHOICES = [(AGREE, "Agree"), (DISAGREE, "Disagree"), (NEUTRAL, "Neutral")]

    topic = models.ForeignKey(
        Topic, related_name="submissions", on_delete=models.CASCADE
    )
    position = models.ForeignKey(
        Position,
        related_name="submissions",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    stance = models.CharField(max_length=10, choices=STANCE_CHOICES, default=AGREE)
    importance = models.PositiveSmallIntegerField(default=3, help_text="1–5.")
    reasoning = models.TextField(blank=True)
    email = models.EmailField(blank=True, help_text="Optional; anonymous by default.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return (
            f"{self.get_stance_display()} · {self.topic} · {self.created_at:%Y-%m-%d}"
        )
