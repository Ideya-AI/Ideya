import datetime

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils import timezone

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

# Minimum community lean votes before a question's reader-poll bar is displayed
# (decision C: counts live, lean bars gated — avoids "2 votes = 100%" noise).
# Also gates the bar itself: below the sample, poles render without % or bar.
MIN_STANCE_SAMPLE = 10

# Importance-vote reveal gates (questions + positions). Both count votes CAST
# (Vote rows), not the net score. Research seeds the initial experience; the
# community takes over in stages as real participation accrues.
MIN_VOTES_SHOW_COUNT = 5  # per item: the net number appears
MIN_VOTES_REORDER = 25  # per list: vote order replaces research order

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

    @property
    def social_card(self):
        """Static path to this category's 1200x630 OG link-preview card, generated
        to static/img/social/cat-<slug>.png (via `?render=og` on the category
        share view + headless Chrome); else None so the page falls back to the
        generic Ideya mark."""
        rel = f"img/social/cat-{self.slug}.png"
        return rel if (settings.BASE_DIR / "static" / rel).exists() else None

    @property
    def primary_art(self):
        """Static path to this category's bespoke hero illustration, when one has
        been added at static/img/categories/<slug>.png; else None so the page
        falls back to the Phosphor glyph tile. Same convention as
        Topic.primary_art — the committed asset rides the WhiteNoise pipeline."""
        rel = f"img/categories/{self.slug}.png"
        return rel if (settings.BASE_DIR / "static" / rel).exists() else None


class PublishedTopicManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="published")


class Topic(models.Model):
    DRAFT = "draft"
    PUBLISHED = "published"
    STATUS_CHOICES = [(DRAFT, "Draft"), (PUBLISHED, "Published")]

    FAST = "fast"
    MEDIUM = "medium"
    SLOW = "slow"
    VOLATILITY_CHOICES = [
        (FAST, "Fast — review ~quarterly"),
        (MEDIUM, "Medium — review ~twice a year"),
        (SLOW, "Slow — review ~yearly"),
    ]
    REVIEW_INTERVAL_DAYS = {FAST: 90, MEDIUM: 180, SLOW: 365}

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
    volatility = models.CharField(
        max_length=10,
        choices=VOLATILITY_CHOICES,
        default=MEDIUM,
        help_text="How fast this topic's content goes stale — drives the review cadence.",
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

    # --- content freshness / review cadence ---
    @property
    def review_interval_days(self) -> int:
        return self.REVIEW_INTERVAL_DAYS.get(self.volatility, 180)

    @property
    def last_touched(self):
        """The clock staleness runs from: most recent human review, else research."""
        return self.reviewed_at or self.researched_at

    @property
    def review_due_at(self):
        """When this topic next falls due for review (None if never touched)."""
        base = self.last_touched
        return (
            base + datetime.timedelta(days=self.review_interval_days) if base else None
        )

    @property
    def is_review_due(self) -> bool:
        """True when overdue — or never researched (which always needs attention)."""
        due = self.review_due_at
        return due is None or due <= timezone.now()

    @property
    def days_overdue(self) -> int:
        """Days past the due date; large sentinel if never touched (sorts first)."""
        due = self.review_due_at
        return 10**6 if due is None else (timezone.now() - due).days

    @property
    def primary_art(self):
        """Static path to this topic's bespoke primary illustration, when one
        has been added at static/img/topics/<slug>.png; else None so callers
        fall back to the Phosphor glyph tile. The committed asset rides the
        existing WhiteNoise/manifest static pipeline."""
        rel = f"img/topics/{self.slug}.png"
        return rel if (settings.BASE_DIR / "static" / rel).exists() else None

    @property
    def social_card(self):
        """Static path to this topic's 1200x630 OG link-preview card, generated to
        static/img/social/<slug>.png (via `?render=og` on the share view + headless
        Chrome); else None so the page falls back to the generic Ideya mark."""
        rel = f"img/social/{self.slug}.png"
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

    @staticmethod
    def _tier_lead_count(items, cols, min_show, max_show):
        """How many leading (rank-ordered) items show before Go-deeper.

        The research picks the natural cutoff: items carry a quality `tier`
        (a new tier starts at a clear drop-off), and the lead set is the
        smallest whole-tier prefix that reaches `min_show`, capped at
        `max_show`. The display then snaps to full desktop rows (visual only):
        round down, unless that would demote a tier-1 item or dip below the
        minimum — then promote the next-ranked item(s) to complete the row
        (tier 1 of 3 in a 2-up grid grabs a 4th; a 7-item lead set drops to 6).
        """
        total = len(items)
        if total <= min_show:
            return total
        boundaries = [
            i
            for i in range(1, total)
            if getattr(items[i], "tier", 1) != getattr(items[i - 1], "tier", 1)
        ] + [total]
        raw = next((b for b in boundaries if b >= min_show), total)
        raw = min(raw, max_show, total)
        if cols > 1 and raw % cols and raw != total:
            floor = min(max(min_show, boundaries[0]), raw)
            down = raw - raw % cols
            up = min(raw + cols - raw % cols, total)
            raw = down if down >= floor else up
        return raw

    BASICS_MIN_SHOWN = 3  # at least one full desktop row
    BASICS_MAX_SHOWN = 9  # three desktop rows before Go-deeper takes over

    def _basics_base_count(self, stats):
        """How many leading tiles to show before Go-deeper: the research tiers
        pick the cutoff (via _tier_lead_count), then the count is snapped to a
        clean desktop cell boundary (wide tiles span 2 of the 3 columns) so the
        default never orphans."""
        cols = 3
        n = self._tier_lead_count(
            stats, 1, self.BASICS_MIN_SHOWN, self.BASICS_MAX_SHOWN
        )
        if n >= len(stats):
            return len(stats)

        def cells(k):
            return sum(2 if s.wide else 1 for s in stats[:k])

        # Snap to a full row (same rule as _tier_lead_count): round down unless
        # that demotes a tier-1 tile or dips below the minimum, else promote
        # next-ranked tiles to complete the row.
        first_tier = getattr(stats[0], "tier", 1)
        tier1 = next(
            (i for i, s in enumerate(stats) if getattr(s, "tier", 1) != first_tier),
            len(stats),
        )
        floor = min(max(self.BASICS_MIN_SHOWN, tier1), n)
        down = n
        while down > 0 and cells(down) % cols != 0:
            down -= 1
        if down >= floor:
            return down
        up = n
        while up < len(stats) and cells(up) % cols != 0:
            up += 1
        return up if cells(up) % cols == 0 else len(stats)

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

    QUESTIONS_MIN_SHOWN = 3
    QUESTIONS_MAX_SHOWN = 6

    def _questions_base_count(self, questions):
        # Single-column list — the tier cutoff needs no row snapping.
        return self._tier_lead_count(
            questions, 1, self.QUESTIONS_MIN_SHOWN, self.QUESTIONS_MAX_SHOWN
        )

    @property
    def questions_tiles(self):
        """Ranked Questions annotated for the two-axis list: `is_extra`
        questions (beyond the tier cutoff) appear only when Go-deeper is open.
        Uses the prefetched queryset (research order, or vote order once the
        list passes MIN_VOTES_REORDER)."""
        questions = list(self.questions.all())
        base_n = self._questions_base_count(questions)
        for i, q in enumerate(questions):
            q.is_extra = i >= base_n
        return questions

    @property
    def questions_has_extra(self):
        questions = list(self.questions.all())
        return self._questions_base_count(questions) < len(questions)

    POSITIONS_DEFAULT_SHOWN = 4  # fixed-layout surfaces (share cards, spotlight)
    POSITIONS_MIN_SHOWN = 2
    POSITIONS_MAX_SHOWN = 6

    def _positions_base_count(self, positions):
        # 2-column desktop grid — snap the tier cutoff to full rows.
        return self._tier_lead_count(
            positions, 2, self.POSITIONS_MIN_SHOWN, self.POSITIONS_MAX_SHOWN
        )

    @property
    def positions_tiles(self):
        """Ranked Positions annotated for the two-axis grid: `is_extra` cards
        (revealed only when the section's Go-deeper is open) come after the
        tier cutoff. Mirrors basics_tiles (breadth axis)."""
        positions = list(self.positions.all())
        base_n = self._positions_base_count(positions)
        for i, p in enumerate(positions):
            p.is_extra = i >= base_n
        return positions

    @property
    def positions_has_extra(self):
        positions = list(self.positions.all())
        return self._positions_base_count(positions) < len(positions)


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
    tier = models.PositiveSmallIntegerField(
        default=1,
        help_text="Quality tier from research (1 = leading). A new tier starts at a "
        "natural drop-off; tier 1 leads the section before Go-deeper.",
    )
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


class Question(models.Model):
    EMPIRICAL = "empirical"
    VALUE = "value"
    KIND_CHOICES = [(EMPIRICAL, "Empirical"), (VALUE, "Value")]

    section = models.ForeignKey(
        Section, related_name="questions", on_delete=models.CASCADE
    )
    order = models.PositiveSmallIntegerField(default=0)
    tier = models.PositiveSmallIntegerField(
        default=1,
        help_text="Quality tier from research (1 = leading); drives the Go-deeper split.",
    )
    text = models.CharField(max_length=400)
    kind = models.CharField(max_length=12, choices=KIND_CHOICES, default=EMPIRICAL)
    why = models.TextField(blank=True, help_text="Why this question is contested.")
    detail = models.TextField(
        blank=True,
        help_text="Deeper follow-up revealed when the question is expanded.",
    )
    votes = models.IntegerField(
        default=0, help_text="Net importance (upvotes minus downvotes)."
    )
    # Optional aggregated lean (shown at deep depth).
    lean_label_a = models.CharField(max_length=40, blank=True)
    lean_label_b = models.CharField(max_length=40, blank=True)
    lean_pct_a = models.PositiveSmallIntegerField(null=True, blank=True)
    reveal = models.CharField(
        max_length=10, choices=REVEAL_CHOICES, default="condensed"
    )

    class Meta:
        # Research order by default; the view layer switches to vote order once
        # a topic's questions pass MIN_VOTES_REORDER real votes.
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return self.text

    @property
    def show_count(self):
        """Gate the net number behind real participation (MIN_VOTES_SHOW_COUNT
        votes cast). Uses the `votes_cast` annotation when the queryset
        provides it; falls back to a query for HTMX fragments."""
        n = getattr(self, "votes_cast", None)
        if n is None:
            n = self.importance_votes.count()
        return n >= MIN_VOTES_SHOW_COUNT

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
    def lean_stats(self):
        """Community direction-vote aggregate (the reader poll) — distinct from the
        editorial lean_pct_a. Counts QuestionLean rows for poles a/b."""
        a = getattr(self, "lean_a_count", None)
        b = getattr(self, "lean_b_count", None)
        if a is None or b is None:
            a = self.community_leans.filter(value="a").count()
            b = self.community_leans.filter(value="b").count()
        total = a + b
        return {
            "a": a,
            "b": b,
            "total": total,
            "pct_a": round(100 * a / total) if total else None,
            "pct_b": round(100 * b / total) if total else None,
            "shown": total >= MIN_STANCE_SAMPLE,
        }

    @property
    def lean_display(self):
        """The single direction bar: community % once reader votes reach the
        threshold, otherwise the research/editorial estimate (lean_pct_a)."""
        ls = self.lean_stats
        if ls["shown"]:
            return {
                "pct_a": ls["pct_a"],
                "pct_b": ls["pct_b"],
                "source": "community",
                "total": ls["total"],
            }
        pa = self.lean_pct_a if self.lean_pct_a is not None else 50
        return {
            "pct_a": pa,
            "pct_b": 100 - pa,
            "source": "research",
            "total": ls["total"],
        }


class Position(models.Model):
    section = models.ForeignKey(
        Section, related_name="positions", on_delete=models.CASCADE
    )
    order = models.PositiveSmallIntegerField(default=0)
    tier = models.PositiveSmallIntegerField(
        default=1,
        help_text="Quality tier from research (1 = leading); drives the Go-deeper split.",
    )
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
    importance = models.IntegerField(
        default=0, help_text="Net importance (upvotes minus downvotes)."
    )
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
        # Prevalence-seeded (research) by default; the view layer switches to
        # importance-vote order once the topic's positions pass
        # MIN_VOTES_REORDER real votes (supersedes decision 2026-06-17).
        ordering = ["-prevalence_weight", "order", "id"]

    def __str__(self) -> str:
        return self.name

    @property
    def show_count(self):
        """Gate the net number behind real participation (MIN_VOTES_SHOW_COUNT
        votes cast). Mirrors Question.show_count."""
        n = getattr(self, "votes_cast", None)
        if n is None:
            n = self.importance_votes.count()
        return n >= MIN_VOTES_SHOW_COUNT

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
    tier = models.PositiveSmallIntegerField(
        default=1,
        help_text="Quality tier from research (1 = leading). Recorded for future "
        "tier-driven display; actions currently split by reveal level.",
    )
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

    value = models.SmallIntegerField(
        default=1, help_text="+1 upvote (downvotes retired 2026-08-01)."
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


class QuestionLean(ParticipationBase):
    """One reader's direction on a question (pole A or B) — the community poll,
    distinct from the editorial lean. One row per participant per question;
    re-clicking the same pole retracts it, the other pole switches it."""

    A = "a"
    B = "b"
    VALUE_CHOICES = [(A, "Pole A"), (B, "Pole B")]

    question = models.ForeignKey(
        Question, related_name="community_leans", on_delete=models.CASCADE
    )
    value = models.CharField(max_length=1, choices=VALUE_CHOICES)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["question", "session_key"],
                condition=~models.Q(session_key=""),
                name="unique_qlean_per_session",
            ),
            models.UniqueConstraint(
                fields=["question", "user"],
                condition=models.Q(user__isnull=False),
                name="unique_qlean_per_user",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.value} · {self.question}"


# --------------------------------------------------------------------------- #
# Open participation layer — free-form + structured prompts, attachable at any
# scale, with GenAI summaries that publish only after editorial approval.
# Distinct from the core Question/Position votes above.
# --------------------------------------------------------------------------- #
class Prompt(models.Model):
    """A reader-input prompt — free-form or structured (choose/rate/rank) — that can
    attach to anything at any scale (a Topic overall, or a sub-piece: Section,
    Question, Position) via a generic relation. The open participation layer:
    structured answers aggregate into `response_stats`; text answers feed the
    editor-gated GenAI summaries (`InputSummary`)."""

    FREE_TEXT = "free_text"
    CHOOSE_ONE = "choose_one"
    CHOOSE_MANY = "choose_many"
    RATE = "rate"
    RANK = "rank"
    KIND_CHOICES = [
        (FREE_TEXT, "Free text"),
        (CHOOSE_ONE, "Choose one"),
        (CHOOSE_MANY, "Choose many"),
        (RATE, "Rating (1–5)"),
        (RANK, "Ranking"),
    ]

    kind = models.CharField(max_length=12, choices=KIND_CHOICES, default=FREE_TEXT)
    text = models.CharField(max_length=300, help_text="The prompt shown to readers.")
    help_text = models.CharField(max_length=300, blank=True)
    allow_text = models.BooleanField(
        default=False,
        help_text="For structured prompts: also collect an optional free-text 'why'.",
    )

    # Generic attachment — overarching (Topic) or a sub-piece (Section/Question/Position).
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="What this attaches to (Topic / Section / Question / Position).",
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey("content_type", "object_id")

    order = models.PositiveSmallIntegerField(default=0)
    active = models.BooleanField(
        default=True, help_text="Inactive prompts are hidden and accept no responses."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]
        indexes = [models.Index(fields=["content_type", "object_id"])]

    def __str__(self) -> str:
        return f"{self.get_kind_display()} · {self.text[:50]}"

    @property
    def is_structured(self) -> bool:
        return self.kind in (self.CHOOSE_ONE, self.CHOOSE_MANY, self.RATE, self.RANK)

    @property
    def collects_text(self) -> bool:
        return self.kind == self.FREE_TEXT or self.allow_text

    @property
    def target_label(self) -> str:
        t = self.target
        return f"{t.__class__.__name__}: {t}" if t is not None else "(unattached)"

    @property
    def response_stats(self):
        """Aggregate of structured answers + a text-answer count. by_option counts
        for choose; Borda points for rank; mean for rate. Drives any live display."""
        responses = list(self.responses.all())
        out = {
            "total": len(responses),
            "text_count": sum(1 for r in responses if (r.text or "").strip()),
        }
        if self.kind in (self.CHOOSE_ONE, self.CHOOSE_MANY):
            from collections import Counter

            counter = Counter()
            for r in responses:
                for oid in r.selected_ids or []:
                    counter[oid] += 1
            out["by_option"] = {
                o.id: {"label": o.label, "count": counter.get(o.id, 0)}
                for o in self.options.all()
            }
        elif self.kind == self.RATE:
            vals = [r.rating for r in responses if r.rating is not None]
            out["mean"] = round(sum(vals) / len(vals), 2) if vals else None
            out["n"] = len(vals)
        elif self.kind == self.RANK:
            from collections import defaultdict

            points = defaultdict(int)
            for r in responses:
                order = r.ranking or []
                for i, oid in enumerate(order):
                    points[oid] += len(order) - i  # first = most points
            out["by_option"] = {
                o.id: {"label": o.label, "points": points.get(o.id, 0)}
                for o in self.options.all()
            }
        return out


class PromptOption(models.Model):
    """An option for a structured prompt (choose/rank). May reference a Position so
    'which do you agree with most?' can point at the real mapped positions."""

    prompt = models.ForeignKey(Prompt, related_name="options", on_delete=models.CASCADE)
    label = models.CharField(max_length=200)
    position = models.ForeignKey(
        Position,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="prompt_options",
        help_text="Optional — tie this option to a mapped Position.",
    )
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return self.label


class Response(ParticipationBase):
    """One participant's answer to a Prompt — one row per (prompt, participant),
    edited in place (upsert) like a vote. `text` feeds GenAI summaries; the
    structured fields feed `Prompt.response_stats`."""

    prompt = models.ForeignKey(
        Prompt, related_name="responses", on_delete=models.CASCADE
    )
    text = models.TextField(blank=True)
    selected_ids = models.JSONField(
        default=list, blank=True, help_text="Chosen PromptOption ids (choose_*)."
    )
    rating = models.PositiveSmallIntegerField(
        null=True, blank=True, help_text="1–5 for rate prompts."
    )
    ranking = models.JSONField(
        default=list, blank=True, help_text="Ordered PromptOption ids for rank prompts."
    )
    option_texts = models.JSONField(
        default=dict,
        blank=True,
        help_text="Optional per-option note/answer for choose_many: {option_id: text}.",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["prompt", "session_key"],
                condition=~models.Q(session_key=""),
                name="unique_response_per_session",
            ),
            models.UniqueConstraint(
                fields=["prompt", "user"],
                condition=models.Q(user__isnull=False),
                name="unique_response_per_user",
            ),
        ]

    def __str__(self) -> str:
        return f"Response · prompt {self.prompt_id}"


class InputSummary(models.Model):
    """A GenAI digest of the responses to a Prompt — Amazon-review-style "what
    readers think". Draft by default; it surfaces publicly only after editorial
    approval (Decision D: AI drafts, a human publishes). It never edits the topic
    content itself — it is a separate, clearly-labelled reader-opinion digest."""

    DRAFT = "draft"
    APPROVED = "approved"
    REJECTED = "rejected"
    STATUS_CHOICES = [(DRAFT, "Draft"), (APPROVED, "Approved"), (REJECTED, "Rejected")]

    prompt = models.ForeignKey(
        Prompt, related_name="summaries", on_delete=models.CASCADE
    )
    body = models.TextField(help_text="The generated digest.")
    themes = models.JSONField(
        default=list, blank=True, help_text="Optional structured themes / learnings."
    )
    n_responses = models.PositiveIntegerField(
        default=0, help_text="How many responses this digest summarized."
    )
    model = models.CharField(
        max_length=60, blank=True, help_text="The model that generated it."
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-generated_at"]
        verbose_name_plural = "input summaries"

    def __str__(self) -> str:
        return f"[{self.status}] summary · prompt {self.prompt_id}"
