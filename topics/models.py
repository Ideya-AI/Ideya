import datetime
import re

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime

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
    ("berry", "Berry"),
    ("indigo", "Indigo"),
    ("cocoa", "Cocoa"),
    ("slate", "Slate"),  # last resort: gray reads as disabled next to peers
]

# Minimum community lean votes before a question's reader-poll bar is displayed
# (decision C: counts live, lean bars gated — avoids "2 votes = 100%" noise).
# Also gates the bar itself: below the sample, poles render without % or bar.
MIN_STANCE_SAMPLE = 10

# Importance-vote reorder gate (questions + positions). Counts votes CAST
# (Vote rows), not the net score. Research seeds the initial order; vote order
# takes over once real participation accrues. Counts themselves always show.
MIN_VOTES_REORDER = 25  # per list: vote order replaces research order


class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.CharField(max_length=400, blank=True)
    icon = models.CharField(
        max_length=80, blank=True, help_text="Phosphor icon name, e.g. 'leaf'."
    )
    color_key = models.CharField(
        max_length=40,
        blank=True,
        help_text="Equals the slug: maps to the --cat-<slug> token. Discovery tiers only.",
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
    # A topic's core status — where it is in its life, one value, four stops.
    # NOT_STARTED is a topic file with nothing authored against it yet;
    # IN_PROGRESS is being worked on and not fit to publish; READY is the
    # engine's certification that it passed everything; PUBLISHED is live.
    # Only the last is visible to the public.
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    READY = "ready"
    PUBLISHED = "published"
    STATUS_CHOICES = [
        (NOT_STARTED, "Not started"),
        (IN_PROGRESS, "In progress"),
        (READY, "Ready to publish"),
        (PUBLISHED, "Published"),
    ]

    # One cadence for every topic. Per-topic volatility was a field the author
    # guessed and nothing validated; a single interval says the same thing.
    REVIEW_INTERVAL_DAYS = 180

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default=NOT_STARTED,
        db_index=True,
        help_text="Where this topic is in its life. Only PUBLISHED is visible "
        "to the public; everything else is staff-only. READY means the engine "
        "certified it — loading content withdraws that, because what was "
        "verified is then no longer what is loaded.",
    )
    scope = models.TextField(
        blank=True,
        help_text="One line fixing what this topic covers, written when it is "
        "added and used to brief the research planner. A SEED, never reader "
        "copy — nothing renders it. The public summary is written by the "
        "engine and lives on `summary`.",
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
    why_now_source_label = models.CharField(max_length=120, blank=True)
    why_now_source_url = models.URLField(max_length=500, blank=True)
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

    # --- lifecycle, mirrored from the topic file ---
    authored_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the authoring skill last finished this topic.",
    )
    published_at = models.DateTimeField(
        null=True, blank=True, help_text="When a human published this topic."
    )
    reviewed_at = models.JSONField(
        default=list,
        blank=True,
        help_text="One ISO 8601 timestamp per review-skill run, oldest first.",
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
        return self.REVIEW_INTERVAL_DAYS

    @property
    def last_reviewed_at(self):
        """The most recent review-skill run, as a datetime, else None."""
        stamps = [s for s in (self.reviewed_at or []) if s]
        if not stamps:
            return None
        parsed = [d for d in (parse_datetime(str(s)) for s in stamps) if d]
        return max(parsed) if parsed else None

    @property
    def last_touched(self):
        """The clock staleness runs from: most recent review, else authoring."""
        return self.last_reviewed_at or self.authored_at

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
        """Primary category first, then the rest."""
        cats = list(self.categories.all())
        primary = self.primary_category
        if primary:
            cats = [primary] + [c for c in cats if c.pk != primary.pk]
        return cats

    @property
    def glyph(self):
        """The Phosphor name every small slot draws: the topic's own icon
        (stage 3's), else its primary category's, so an unauthored topic wears
        its category rather than a bullet."""
        cat = self.color_category
        return self.icon or (cat.icon if cat else "") or "squares-four"

    @property
    def secondary_categories(self):
        """Everything but the primary — the Overview's chip row, not the header."""
        return self.category_badges[1:]


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

    BASICS_ROWS_SHOWN = 3  # desktop rows before Go deeper

    @property
    def basics_tiles(self):
        """Importance-ordered Stats annotated for the two-axis Basics grid:
        `is_extra` (revealed only when Go-deeper is open). Fixed fold: the
        first BASICS_ROWS_SHOWN packed rows show; the rest is Go deeper. A
        trailing tile keeps its own width; it does not stretch across the row."""
        stats = list(self.stats.all())
        # Pack into desktop rows of 3 cells. A cell count that is a multiple of
        # 3 does not guarantee the rows pack (1,1,W,W is six cells but leaves
        # the right column empty twice), so a tile that does not fit the open
        # row is deferred and the next one that fits is pulled forward. The
        # first BASICS_ROWS_SHOWN rows are the fold.
        rows, pending = [], list(stats)
        while pending:
            row, cells = [], 0
            i = 0
            while i < len(pending) and cells < 3:
                w = 2 if pending[i].wide else 1
                if cells + w <= 3:
                    row.append(pending.pop(i))
                    cells += w
                else:
                    i += 1
            rows.append(row)
        stats = [s for row in rows for s in row]
        shown = sum(len(row) for row in rows[: self.BASICS_ROWS_SHOWN])
        for i, s in enumerate(stats):
            s.is_extra = i >= shown
        return stats

    @property
    def basics_has_extra(self):
        return any(s.is_extra for s in self.basics_tiles)

    QUESTIONS_SHOWN = 4  # fixed fold; the rest is Go deeper

    @property
    def questions_tiles(self):
        """Ranked Questions annotated for the two-axis list: `is_extra`
        questions (beyond QUESTIONS_SHOWN) appear only when Go-deeper is open.
        Uses the prefetched queryset (research order, or vote order once the
        list passes MIN_VOTES_REORDER)."""
        questions = list(self.questions.all())
        for i, q in enumerate(questions):
            q.is_extra = i >= self.QUESTIONS_SHOWN
        return questions

    @property
    def questions_has_extra(self):
        return self.questions.count() > self.QUESTIONS_SHOWN

    POSITIONS_DEFAULT_SHOWN = 4  # fixed-layout surfaces (share cards, spotlight)
    POSITIONS_SHOWN = 4  # fixed fold; the rest is Go deeper

    @property
    def positions_tiles(self):
        """Ranked Positions, one per row: `is_extra` cards (beyond
        POSITIONS_SHOWN) are revealed only when the section's Go-deeper is open."""
        positions = list(self.positions.all())
        for i, p in enumerate(positions):
            p.is_extra = i >= self.POSITIONS_SHOWN
        return positions

    @property
    def positions_has_extra(self):
        return self.positions.count() > self.POSITIONS_SHOWN

    ACTIONS_SHOWN = 6  # fixed fold; the rest is Go deeper

    @property
    def actions_tiles(self):
        """Actions in file order: `is_extra` cards (beyond ACTIONS_SHOWN) are
        revealed only when the section's Go-deeper is open."""
        actions = list(self.actions.all())
        for i, a in enumerate(actions):
            a.is_extra = i >= self.ACTIONS_SHOWN
        return actions

    @property
    def actions_has_extra(self):
        return self.actions.count() > self.ACTIONS_SHOWN


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
    item_id = models.SlugField(
        max_length=80,
        blank=True,
        db_index=True,
        help_text="Stable identity, assigned once and never changed. Reader votes, leans and prompts attach to this, so rewording an item keeps them.",
    )
    order = models.PositiveSmallIntegerField(default=0)
    label = models.CharField(max_length=120, help_text="The metric, not a sentence.")
    viz = models.CharField(max_length=12, choices=VIZ_CHOICES, default=BAR)
    wide = models.BooleanField(default=False, help_text="Span two columns (ranked).")
    value = models.CharField(max_length=24, blank=True, help_text="Headline number.")
    unit = models.CharField(
        max_length=24,
        blank=True,
        help_text="Spelled out for the glance layer, e.g. %, ' tonnes', ' trillion/yr'.",
    )
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["section", "item_id"],
                condition=~models.Q(item_id=""),
                name="unique_stat_item_id",
            ),
        ]
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return f"{self.label}: {self.value}"

    @property
    def unit_is_word(self):
        """A unit that is a word ("million tonnes", " reactors") sits a space
        off the number; a symbol ("%", "$/MWh") sits tight. Decided here so
        no topic file has to remember a leading space."""
        u = self.unit or ""
        return u[:1] == " " or u[:1].isalpha()

    @property
    def range_band(self):
        """For a range viz whose VALUE is itself a numeric span ("60–90"),
        the track should mark the span, not a single midpoint pin (a pin at
        75 misreads "60–90%" as ~75). Returns {left, width} percentages when
        value parses as a span inside numeric range_min/range_max, else None
        (point values keep the pin)."""
        m = re.match(
            r"\s*~?(-?\d+(?:\.\d+)?)\s*[–—-]\s*~?(-?\d+(?:\.\d+)?)\s*$",
            (self.value or "").replace(",", ""),
        )
        if not m:
            return None
        ends = []
        for bound in (self.range_min, self.range_max):
            n = re.search(r"-?\d+(?:\.\d+)?", (bound or "").replace(",", ""))
            if not n:
                return None
            ends.append(float(n.group()))
        mn, mx = ends
        if mx <= mn:
            return None
        pct = lambda v: max(0.0, min(100.0, (v - mn) / (mx - mn) * 100))
        lo, hi = pct(float(m.group(1))), pct(float(m.group(2)))
        if hi <= lo:
            return None
        return {"left": round(lo, 1), "width": round(hi - lo, 1)}


class Question(models.Model):
    EMPIRICAL = "empirical"
    VALUE = "value"
    KIND_CHOICES = [(EMPIRICAL, "Empirical"), (VALUE, "Value")]

    section = models.ForeignKey(
        Section, related_name="questions", on_delete=models.CASCADE
    )
    item_id = models.SlugField(
        max_length=80,
        blank=True,
        db_index=True,
        help_text="Stable identity, assigned once and never changed. Reader votes, leans and prompts attach to this, so rewording an item keeps them.",
    )
    order = models.PositiveSmallIntegerField(default=0)
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["section", "item_id"],
                condition=~models.Q(item_id=""),
                name="unique_question_item_id",
            ),
        ]
        # Research order by default; the view layer switches to vote order once
        # a topic's questions pass MIN_VOTES_REORDER real votes.
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return self.text

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
        """Community direction-vote aggregate (the reader poll). Counts
        QuestionLean rows for poles a/b."""
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
        threshold, otherwise an even split (the page asserts no editorial lean)."""
        ls = self.lean_stats
        if ls["shown"]:
            return {
                "pct_a": ls["pct_a"],
                "pct_b": ls["pct_b"],
                "source": "community",
                "total": ls["total"],
            }
        return {"pct_a": 50, "pct_b": 50, "source": "research", "total": ls["total"]}


class Position(models.Model):
    section = models.ForeignKey(
        Section, related_name="positions", on_delete=models.CASCADE
    )
    item_id = models.SlugField(
        max_length=80,
        blank=True,
        db_index=True,
        help_text="Stable identity, assigned once and never changed. Reader votes, leans and prompts attach to this, so rewording an item keeps them.",
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
    detail = models.TextField(
        blank=True,
        help_text="The camp's case in its own voice, revealed when the position is expanded.",
    )
    proponents = models.CharField(
        max_length=400, blank=True, help_text="Comma-separated notable proponents."
    )
    importance = models.IntegerField(
        default=0, help_text="Net importance (upvotes minus downvotes)."
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["section", "item_id"],
                condition=~models.Q(item_id=""),
                name="unique_position_item_id",
            ),
        ]
        # File order is the whole mechanism for weight (§8); the view layer
        # switches to importance-vote order once the topic's positions pass
        # MIN_VOTES_REORDER real votes.
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
    def has_more(self) -> bool:
        """Any expandable detail behind the card's click-to-expand (axis 2)."""
        return bool(self.detail or self.proponents)


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

    @property
    def poster_size(self) -> str:
        """Size bucket for the poster's crux band, by total length, the way the
        poster title steps down by length. The sheet is fixed; the web crux is
        not held to it."""
        n = len(self.lead) + len(self.subtitle) + len(self.empirical) + len(self.values)
        return "c-xs" if n > 1050 else "c-sm" if n > 750 else ""


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
    item_id = models.SlugField(
        max_length=80,
        blank=True,
        db_index=True,
        help_text="Stable identity, assigned once and never changed. Reader votes, leans and prompts attach to this, so rewording an item keeps them.",
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["section", "item_id"],
                condition=~models.Q(item_id=""),
                name="unique_action_item_id",
            ),
        ]
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return self.title

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
    order = models.PositiveSmallIntegerField(
        default=0,
        help_text="Position in the topic file's `related` list; order is weight.",
    )

    class Meta:
        unique_together = [("source", "target", "kind")]
        ordering = ["order", "id"]

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
class ParticipationEvent(models.Model):
    """Append-only log of every participation action — each vote, lean and
    prompt response as it happened, including retracts, switches and edits.
    Everything is denormalized (topic slug, item text, prompt text, option
    labels) and nothing cascades, so the record survives content reloads and
    prompt reseeds that reset the current-state tables. Read later; never
    updated."""

    VOTE, LEAN, RESPONSE = "vote", "lean", "response"
    KIND_CHOICES = [(VOTE, "Vote"), (LEAN, "Lean"), (RESPONSE, "Response")]

    kind = models.CharField(max_length=8, choices=KIND_CHOICES)
    action = models.CharField(
        max_length=8,
        help_text="cast / retract / switch (votes, leans); save / clear (responses).",
    )
    topic_slug = models.CharField(max_length=200, blank=True, db_index=True)
    target_kind = models.CharField(
        max_length=12, blank=True, help_text="topic / stat / question / position"
    )
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target_text = models.CharField(max_length=400, blank=True)
    prompt_id = models.PositiveIntegerField(null=True, blank=True)
    prompt_text = models.CharField(max_length=300, blank=True)
    trigger = models.CharField(max_length=8, blank=True)
    payload = models.JSONField(
        default=dict,
        blank=True,
        help_text="The answer: value / selected labels / notes / rating / ranking / text.",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    session_key = models.CharField(max_length=40, blank=True, db_index=True)
    ip = models.CharField(max_length=45, blank=True)
    user_agent = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.kind} {self.action} · {self.target_text[:40]}"


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

    # What surfaces this prompt. Blank = the Add-your-view modal (topic level);
    # the rest open the follow-up modal after that interaction on the target.
    TRIGGER_VOTE = "vote"
    TRIGGER_LEAN_A = "lean_a"
    TRIGGER_LEAN_B = "lean_b"
    TRIGGER_RESPOND = "respond"
    TRIGGER_MISSING = "missing"
    TRIGGER_CHOICES = [
        ("", "None"),
        (TRIGGER_VOTE, "After an upvote"),
        (TRIGGER_LEAN_A, "After leaning to pole A"),
        (TRIGGER_LEAN_B, "After leaning to pole B"),
        (TRIGGER_RESPOND, "From the item's respond button"),
        (TRIGGER_MISSING, "From a section's Something-missing button"),
    ]

    kind = models.CharField(max_length=12, choices=KIND_CHOICES, default=FREE_TEXT)
    trigger = models.CharField(
        max_length=8, choices=TRIGGER_CHOICES, default="", blank=True
    )
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
