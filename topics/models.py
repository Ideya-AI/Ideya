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
    ("energy", "Green (energy/climate)"),
    ("tech", "Blue (AI/tech)"),
    ("gov", "Purple (governance)"),
    ("econ", "Amber (economy)"),
    ("ethics", "Rust (ethics)"),
    ("risk", "Slate (global risk)"),
    ("digital", "Teal (digital society)"),
    ("bio", "Rose (bio/health)"),
    ("society", "Olive (society/culture)"),
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


class PublishedTopicManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="published")


class Topic(models.Model):
    DRAFT = "draft"
    PUBLISHED = "published"
    STATUS_CHOICES = [(DRAFT, "Draft"), (PUBLISHED, "Published")]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text="Drafts are invisible everywhere except to staff.",
    )
    summary = models.CharField(
        max_length=400,
        blank=True,
        help_text="One-sentence framing for cards, previews, and the Overview hero.",
    )
    icon = models.CharField(
        max_length=80, blank=True, help_text="Phosphor icon name, e.g. 'atom'."
    )
    primary_image_prompt = models.TextField(
        blank=True,
        help_text=(
            "Generation prompt (Nano Banana / Gemini) for the topic's bespoke "
            "primary illustration. The image itself is committed at "
            "static/img/topics/<slug>.png; this keeps its provenance so the art "
            "can be re-run or refined."
        ),
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

    # --- research provenance (pipeline) ---
    researched_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the research pipeline last authored this.",
    )
    reviewed_at = models.DateTimeField(
        null=True, blank=True, help_text="When a human last reviewed/approved this."
    )
    research_dossier = models.JSONField(
        default=dict,
        blank=True,
        help_text="Pipeline dossier — sources, raw research, notes. Reviewer-facing, not public.",
    )

    objects = models.Manager()
    published = PublishedTopicManager()

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("topics:detail", args=[self.slug])

    @property
    def missing_sections(self):
        """Spine kinds this topic hasn't authored yet (order preserved)."""
        have = set(self.sections.values_list("kind", flat=True))
        return [k for k in SECTION_ORDER if k != Section.TOPICS and k not in have]

    @property
    def primary_art(self):
        """Static path to this topic's bespoke primary illustration, when one
        has been added at static/img/topics/<slug>.png; else None so callers
        fall back to the Phosphor glyph tile. The committed asset rides the
        existing WhiteNoise/manifest static pipeline."""
        rel = f"img/topics/{self.slug}.png"
        return rel if (settings.BASE_DIR / "static" / rel).exists() else None

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
        QUESTIONS: ("question", "what's contested"),
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

    def _crux_or_none(self):
        try:
            return self.crux
        except Crux.DoesNotExist:
            return None

    @property
    def has_layer_normal(self) -> bool:
        """Any normal-layer content — part of the base read on desktop, behind
        the section's Go-deeper on mobile (decision A: medium sets the base)."""
        if self.kind == self.BASICS:
            # Breadth axis only: extra tiles tagged to appear at normal depth.
            # The lead note now always shows; per-tile detail is its own axis.
            return any(s.reveal == "normal" for s in self.stats.all())
        if self.kind == self.QUESTIONS:
            return any(q.why or q.reveal == "normal" for q in self.questions.all())
        if self.kind == self.POSITIONS:
            return any(p.description for p in self.positions.all())
        if self.kind == self.CRUX:
            crux = self._crux_or_none()
            return bool(crux and crux.subtitle)
        if self.kind == self.ACTIONS:
            return any(
                a.description or a.reveal == "normal" for a in self.actions.all()
            )
        return False

    @property
    def has_layer_deep(self) -> bool:
        """Any deep-layer content — always behind the section's Go-deeper."""
        if self.kind == self.BASICS:
            # Breadth axis only: extra tiles tagged to appear at deep depth.
            # Source moved into the per-tile More expander.
            return any(s.reveal == "deep" for s in self.stats.all())
        if self.kind == self.QUESTIONS:
            return any(
                q.lean_pct_a is not None or q.reveal == "deep"
                for q in self.questions.all()
            )
        if self.kind == self.POSITIONS:
            return any(
                p.representative_name or p.proponents for p in self.positions.all()
            )
        if self.kind == self.CRUX:
            crux = self._crux_or_none()
            return bool(crux and (crux.empirical or crux.values))
        if self.kind == self.ACTIONS:
            return any(a.reveal == "deep" for a in self.actions.all())
        return False

    BASICS_DEFAULT_ROWS = 2  # desktop rows (3-col grid) shown before Go-deeper

    def _basics_base_count(self, stats):
        """How many leading (importance-ordered) tiles to show before Go-deeper,
        snapped to a clean desktop-row boundary so the default never orphans."""
        cols = 3
        cap = cols * self.BASICS_DEFAULT_ROWS

        def span(s):
            return 2 if s.wide else 1

        if sum(span(s) for s in stats) <= cap:
            return len(stats)
        cells = n = 0
        for s in stats:
            if cells + span(s) > cap:
                break
            cells += span(s)
            n += 1
        while n > 0 and sum(span(s) for s in stats[:n]) % cols != 0:
            n -= 1
        return n or len(stats)

    @property
    def basics_tiles(self):
        """Importance-ordered Stats annotated for the two-axis Basics grid:
        `is_extra` (revealed only when Go-deeper is open) and `fill_row` (a
        trailing orphan spans the full row so rows stay clean)."""
        stats = list(self.stats.all())
        base_n = self._basics_base_count(stats)
        for i, s in enumerate(stats):
            s.is_extra = i >= base_n
            s.fill_row = False
        if stats and sum(2 if s.wide else 1 for s in stats) % 3 == 1:
            stats[-1].fill_row = True
        return stats

    @property
    def basics_has_extra(self):
        stats = list(self.stats.all())
        return self._basics_base_count(stats) < len(stats)

    QUESTIONS_DEFAULT_SHOWN = 4  # leading questions shown before Go-deeper

    @property
    def questions_tiles(self):
        """Vote-ordered Questions annotated for the two-axis list: `is_extra`
        questions (beyond the default shown) appear only when Go-deeper is open.
        Uses the prefetched queryset (ordered by -votes, order, id)."""
        questions = list(self.questions.all())
        for i, q in enumerate(questions):
            q.is_extra = i >= self.QUESTIONS_DEFAULT_SHOWN
        return questions

    @property
    def questions_has_extra(self):
        return len(self.questions.all()) > self.QUESTIONS_DEFAULT_SHOWN

    POSITIONS_DEFAULT_SHOWN = 4  # leading position cards shown before Go-deeper

    @property
    def positions_tiles(self):
        """Order-ranked Positions annotated for the two-axis grid: `is_extra`
        cards (revealed only when the section's Go-deeper is open) come after the
        leading POSITIONS_DEFAULT_SHOWN. Mirrors basics_tiles (breadth axis)."""
        positions = list(self.positions.all())
        for i, p in enumerate(positions):
            p.is_extra = i >= self.POSITIONS_DEFAULT_SHOWN
        return positions

    @property
    def positions_has_extra(self):
        return len(self.positions.all()) > self.POSITIONS_DEFAULT_SHOWN


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
    note = models.CharField(
        max_length=400,
        blank=True,
        help_text="Lead line on the tile — simple, 1–2 sentences.",
    )
    detail = models.TextField(
        blank=True,
        help_text="Deeper follow-up revealed when the tile is expanded. More depth/complexity allowed here.",
    )
    source_url = models.URLField(blank=True)
    source_label = models.CharField(max_length=120, blank=True)
    source_published = models.CharField(
        max_length=40,
        blank=True,
        help_text="When the source data is from, e.g. '2024' or 'Q1 2025'.",
    )
    source_accessed = models.DateField(
        null=True,
        blank=True,
        help_text="When the figure was last verified during research.",
    )
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
    detail = models.TextField(
        blank=True,
        help_text="Deeper follow-up revealed when the question is expanded.",
    )
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
    def kind_tip(self) -> str:
        """Hover explainer for the Empirical/Value badge."""
        if self.kind == self.EMPIRICAL:
            return (
                "An empirical question — answerable in principle by evidence and "
                "data, even if the answer is currently uncertain or contested."
            )
        return (
            "A value question — the disagreement is about priorities and ethics, "
            "not facts. Evidence informs it but can't settle it alone."
        )

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
    detail = models.TextField(
        blank=True,
        help_text="Deeper detail revealed when the position is expanded.",
    )
    representative_name = models.CharField(max_length=120, blank=True)
    representative_note = models.CharField(max_length=300, blank=True)
    proponents = models.CharField(
        max_length=400, blank=True, help_text="Comma-separated notable proponents."
    )
    importance = models.PositiveIntegerField(default=0)
    prevalence_weight = models.PositiveSmallIntegerField(
        default=0,
        help_text="How widely held / influential (0–100). Seeds default order so the "
        "mainstream leads; importance votes reorder over time.",
    )
    spectrum_position = models.SmallIntegerField(
        null=True,
        blank=True,
        help_text="Optional ordinal on the debate's main axis (metadata, not the default order).",
    )

    class Meta:
        # Prevalence-seeded, vote-reordered (decision 2026-06-17): when unvoted
        # (importance 0) prevalence decides; importance votes take over as they accrue.
        ordering = ["-importance", "-prevalence_weight", "order", "id"]

    def __str__(self) -> str:
        return self.name

    @property
    def color_var(self) -> str:
        return f"var(--pos-{self.color_key})"

    @property
    def proponent_list(self):
        return [p.strip() for p in self.proponents.split(",") if p.strip()]

    @property
    def has_more(self) -> bool:
        """Any expandable detail behind the card's click-to-expand (axis 2)."""
        return bool(
            self.description
            or self.detail
            or self.representative_name
            or self.proponents
        )

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
    # Hybrid participant keying (decision B). The user link anonymizes to NULL
    # on account deletion — the view itself stays as aggregate content.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="submissions",
    )
    session_key = models.CharField(max_length=40, blank=True, db_index=True)
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
