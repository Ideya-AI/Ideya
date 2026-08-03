# Pipeline tuning log

One entry per generalized lesson learned from reviewing an authored/refreshed topic,
grouped under a dated cycle header. This is the durable record of WHY a critic prompt or
schema in `research/workflows/*.js` changed — the granular sibling of
`RESEARCH_PIPELINE.md`'s coarse design history (same dated-section idiom, different
granularity, like `ICONOGRAPHY.md`).

**Rules (decided 2026-08-01):**
- **Incremental changes** (critic-prompt prose, added checks, guidance wording) are
  applied directly by the review process — optimistic-and-logged; git-reviewable before
  any commit.
- **Transformative changes** (schema shape, new/removed required fields, patch-whitelist
  changes, loader contract, stage structure) are logged as **PROPOSED** and surfaced in
  the chat that initiated the topic run — never auto-applied. They alter the data
  contract for every future topic and the three workflow files are hand-synced
  (`MIRROR` comments), so they need an explicit human decision.
- A lesson that changes one workflow file must state whether its siblings need the same
  change (the mirror-drift failure mode — see Lesson 2's known-gap below).

---

## 2026-08-01 — housing-affordability-crisis, deep review cycle 1 (pre-skill, ad hoc)

Packet: `research/reviews/housing-affordability-crisis/DEEP_REVIEW.md`
(12 reviewers + per-finding adversarial verification; heavier than the standing
review-topic process that this cycle motivated — see `RESEARCH_PIPELINE.md` §13.)

### Lesson 1 — neutrality never checked for a MISSING camp

**Finding:** Blocking — the demand-restriction diagnosis (immigration/foreign-buyer/
second-home limits; live policy in Canada/NZ/Australia) is absent from Positions
despite being a real, currently-active camp.
**Why generalizable:** the neutrality critic only compared camps already ON the page
against each other; nothing asked it to check completeness. Any topic can ship missing
a whole camp and no critic would catch it.
**Applied diff:** `research_topic.js` `neutrality` critic ask — appended: "Given
scope_covered, use web search to check for a genuine, currently-active camp with real
proponents that isn't represented — omitting one is itself a neutrality failure, not
just an incompleteness."
**File(s) touched:** `research/workflows/research_topic.js`.
**Applied how:** optimistic-and-logged (prose-only).
**Status:** applied 2026-08-01.

### Lesson 2 — fact-source checked accuracy, not EXACT scope match

**Finding:** Blocking — the institutional-investor stat cited a CNBC/BatchData source
whose real figure is a ~2% STOCK share of investor-OWNED homes at a 1,000+-home
threshold (net sellers), presented as "bought under 2% of US home sales in 2024" at
100+ homes — different population, threshold, and stock-vs-flow measure. A second
blocking find (the Georgist Detroit ballot-measure claim) lived in position `detail`
text the critic never spot-checked.
**Why generalizable:** the critic asked "is it accurate, sourced, dated" and checked the
NUMBER, never whether the source supports the exact CLAIM (same population/threshold/
measure); and its scope was effectively Basics-only.
**Applied diff:** `research_topic.js` `fact-source` critic ask — appended: "Verify the
source supports the EXACT claim — same population, threshold, and measure (a stock
share is not a purchase share; a subset figure is not a total) — not just a
directionally-similar number found on the page. Also spot-check factual claims embedded
in position/question 'detail' and 'proponents' text, not only Basics stats."
**File(s) touched:** `research/workflows/research_topic.js`; ported to
`research/workflows/refresh_topic.js` `fact-source` critic 2026-08-01 (was initially
applied to research only — mirror drift caught by the pipeline audit).
**Applied how:** optimistic-and-logged.
**Status:** applied 2026-08-01 (both files).

### Lesson 3 — compact-layer labels can mis-scope their own denominator

**Finding:** Blocking — the "50%" cost-burdened stat is a share of RENTER households,
labeled "share of US households" — at the compact reading level (what cards and the
poster render) it claims roughly double the real population.
**Why generalizable:** compact-self-sufficiency checked whether facts were HIDDEN below
the fold, never whether a VISIBLE label's stated scope matches its value.
**Applied diff:** `distribute_topic.js` `compact-self-sufficiency` critic ask —
appended: "Also check each stat's label states the correct denominator/scope for its
value (e.g. a value that is '% of renters' must not be labeled '% of households') — a
label implying a broader or narrower scope than the value actually measures misleads
even if the note clarifies it."
**File(s) touched:** `research/workflows/distribute_topic.js`.
**Applied how:** optimistic-and-logged.
**Status:** applied 2026-08-01.

### Lesson 4 — ranked-stat rows have no per-row source (transformative; approved + applied 2026-08-02)

**Finding:** Blocking — the social/public-housing ranked stat carries ONE
source_label/source_url for the whole stat, but its series rows (Singapore 77% of
residents, Vienna 44% of city stock, Netherlands/US national stock) come from different
sources AND different denominators; one citation cannot support every row.
**Why generalizable:** `STAT.series` items are `{label, value, pct, highlight}` — no
per-row source/scope field exists, so ANY ranked stat spanning multiple sources is
structurally unable to attribute its rows. A prose-only critic fix only catches it
after the fact.
**Applied diff (2026-08-02, human-approved):** series rows now require
`source_label`/`source_url` (empty string when the stat-level source covers the row) in
the STAT schema across all three workflow mirrors, plus a prompt rule in the basics
research prompt (`research_topic.js`) and basics re-verify prompt (`refresh_topic.js`):
rows from different sources/denominators carry their own source fields and name their
denominator in the label. `scope_note` was dropped — the denominator-in-label rule
covers it without a third field.
**File(s) touched:** `research_topic.js`, `refresh_topic.js`, `distribute_topic.js`.
The loader needed NO change — `series` is stored raw as a JSONField, so the new row
keys pass through. The ranked-tile template does not yet display per-row sources; the
data is now carried so a template change stays display-only whenever wanted.
**Applied how:** approved in chat 2026-08-02 ("make your best choice"), then applied.
Existing topics keep the old row shape (valid — loader is shape-agnostic); rows gain
sources at their next refresh.
**Status:** applied 2026-08-02.

### Lesson 5 — gate verdicts flagged as blocking can sit unapplied indefinitely

**Finding:** all 4 fact-source residuals flagged blocking by author-topic's own stage-1
gate on 2026-07-11 were still unapplied on 2026-07-31.
**Why generalizable:** nothing tracks a flagged-but-unapplied finding across time; the
review packet is write-once and nothing re-checks it.
**Applied:** the standing `review-topic` process includes a **residual-audit** step —
every review cycle re-checks prior blocking/advisory findings against current content
and reports applied/still-open. (Process change, not a workflow-file diff.)
**Status:** applied 2026-08-01 (part of `.claude/skills/review-topic/`).

### Lesson 6 — a crux can binarize a multi-camp field

**Finding:** Advisory (confirmed) — the housing crux lead+subtitle offered only two
diagnoses (banned building vs turned-into-investments) over a five-camp field, leaving
the Demand-Side Skeptic diagnosis — which the draft itself calls foundational — with no
place in the axis. The crux critic passed it: its ask only tested house-verdict and
false-balance, not axis coverage.
**Why generalizable:** any topic with 3+ camps can produce a punchier binary crux that
orphans a camp; nothing checked that every camp's diagnosis can locate itself in the
lead/subtitle.
**Applied diff:** crux WRITER prompt (`research_topic.js`) and crux CRITIC ask
(`research_topic.js`) — added: a multi-diagnosis topic's lead/subtitle "must carve an
axis every camp can locate itself on — never compress the field into a two-way fork
that leaves a genuine camp's diagnosis unrepresented." Mirrored into
`refresh_topic.js`'s crux re-check prompt.
**File(s) touched:** `research/workflows/research_topic.js`,
`research/workflows/refresh_topic.js`.
**Applied how:** optimistic-and-logged (prose-only).
**Status:** applied 2026-08-01.

## 2026-08-01 — housing-affordability-crisis, review cycle 2 (first run of the light review-topic skill)

Packet: `research/reviews/housing-affordability-crisis/DEEP_REVIEW.md` (Cycle 2)

### Lesson 7 — view captures only cover the collapsed page state

**Finding:** Note/process — the topic's only range-viz stat (tier 3, reveal "deep")
appears in none of the seven rendered artifacts because `render_screens` captures the
default collapsed page; below-fold and expanded-detail content is never visually
inspected by the view step.
**Why generalizable:** every topic's Go-deeper and click-to-expand layers are invisible
to the current render set — a whole display axis escapes view review on every run.
**Applied (incremental, 2026-08-01):** review-topic SKILL.md view step carries the
coverage caveat — changed below-fold/expanded content must be inspected directly.
**Applied (tooling, approved + applied 2026-08-02):** `render_screens --expanded`
captures `?expanded=1` — a DEBUG-only page mode (`topic_detail` context flag + a
conditional style block in `detail.html`) that forces every Go-deeper extra
(`.tile-xtra`/`.q-xtra`/`.pos-xtra`) and detail region (`.tmore`/`.qmore`/`.pmore`/
`.csplit`) visible; files get an `-expanded` suffix. SKILL.md now says to capture and
review both sets when depth-layer content changed.
**File(s) touched:** `.claude/skills/review-topic/SKILL.md`,
`topics/management/commands/render_screens.py`, `topics/views.py`,
`templates/topics/detail.html`.
**Status:** applied 2026-08-02 (approved in chat: "make your best choice").

### Lesson 8 — a rewrite can re-attach a figure to the wrong population

**Finding:** Blocking (caught by the cycle-2 content spot-check, introduced by the
cycle-2 fix pass itself) — the mega-landlord detail rewrite spliced "small investors
make up about 91%" (a share of investor-owned STOCK) onto "25.7% of 2024 home sales"
as "of that total", silently converting a stock statistic into a purchases statistic
(the real 2024 small-investor purchases share is ~59%).
**Why generalizable:** any fixer/rewriter that reshapes prose around carried-over
figures can re-scope them; the existing fixer guardrails covered ADDED content and
not-weakening flagged parts, but said nothing about preserving each figure's own
population/denominator/measure during a rewrite.
**Applied diff:** stage-1 fixer prompt (`research_topic.js`) and refresh fixer prompt
(`refresh_topic.js`) — appended: "When you REWRITE prose around existing figures, each
figure must keep the exact population, denominator, and measure its source gives it —
never re-attach a number to a different total."
**File(s) touched:** `research/workflows/research_topic.js`,
`research/workflows/refresh_topic.js`.
**Applied how:** optimistic-and-logged (prose-only).
**Status:** applied 2026-08-01. (Also validates the review loop itself: the light
sonnet spot-check caught a defect the fix pass introduced minutes earlier.)

## 2026-08-01 — universal-basic-income, review cycle 1 (first published-topic run)

Packet: `research/reviews/universal-basic-income/DEEP_REVIEW.md`

### Lesson 9 — the loader can silently amputate prose at a length cap

**Finding:** Blocking (live site) — the Targeted-Transfer Economist's
representative_note ends mid-word at exactly 300 chars ("...a UBI gener"): the
loader slices prose fields to model max_lengths with no warning for most of
them (unit/note warned; representative_note, steelman, proponents, question
text, action description did not).
**Why generalizable:** any pipeline draft whose prose exceeds a cap ships broken
mid-sentence text to readers with zero signal at load time.
**Applied diff:** `load_topic_draft.py` — `_cap()` helper warns whenever a slice
actually truncates; routed the six at-risk prose fields through it.
**File(s) touched:** `topics/management/commands/load_topic_draft.py`.
**Applied how:** optimistic-and-logged (warning-only; no behavior change).
**Also applied (workflow half):** `research_topic.js` shapeCheck now flags
representative_note/proponents/action-description prose near their DB caps, so
truncation risk surfaces at authoring time, not after load.
**Status:** applied 2026-08-01. The truncated UBI note itself routes through the
refresh proposal (content fix, human-gated).

## 2026-08-02 — cross-pipeline cost review (session-overage evidence)

### Lesson 10 — premium models and inherited max effort on mechanical subtasks

**Finding:** Process/cost — repeated session overages during the housing/wildfires/UBI
runs. Two routing mis-fits identified: (a) the fact-source critic — the single most
token-hungry agent in both gates (fetches every source, compares each claim) — ran on
`fable` alongside the judgment critics, though its work is mechanical
claim-vs-source checking; (b) every sub-agent inherited the orchestrating session's
reasoning effort (often max), so ~10 web-grunt agents per authoring run and 5+ per
refresh each reasoned at max effort over mostly-mechanical work.
**Why generalizable:** cost-fit was never a routing dimension — models were assigned by
judgment-vs-grunt, but effort wasn't assigned at all, and the gates treated all four
critics as one tier. Every future run pays the same overhead until routed.
**Applied diff:** all three workflows — (1) per-critic model override in the gate
rosters (`model: FACT_MODEL` on fact-source, default `opus`; judgment critics stay
`CRITIQUE_MODEL`/fable; `runGate` uses `c.model ?? CRITIQUE_MODEL`); refresh's crux
re-check moved to its own `CRUX_MODEL` knob (fable) so overriding `critique` no longer
drags the crux with it. (2) `args.efforts` plumbing with explicit defaults:
research/re-verify agents, critics, and fixers pin `high`; distribute's fixer pins
`low` (it applies a whitelisted patch); judgment singletons (plan, crux, distribute)
inherit the session effort.
**File(s) touched:** `research/workflows/research_topic.js`,
`research/workflows/refresh_topic.js`, `research/workflows/distribute_topic.js`;
routing tables in `.claude/skills/author-topic/SKILL.md`.
**Also applied (review dimension):** `review-topic` SKILL.md lesson-mining now
explicitly asks the model/effort cost-fit question each cycle, treating session
overages as review evidence — so routing keeps getting tuned from real runs.
**Applied how:** optimistic-and-logged (default-knob changes; no schema/contract
change — `args.models`/`args.efforts` remain overridable per run).
**Status:** applied 2026-08-02.

## 2026-08-03 — loop upkeep (review-derived tooling closures)

### Lesson 11 — edge wiring existed but was never in the authoring runbook

**Finding:** Note (wildfires packet) — "related-topic edges are seeded only by
load_universe — the pipeline doesn't create them"; wildfires' three edges were wired
manually during its run.
**Why generalizable:** the machinery is complete (catalog `related_slugs` → idempotent
`load_universe` → `TopicEdge` rows; all 115 entries carry `related_slugs`) but no
authoring stage ever invoked it, so every future topic would ship with an empty
"Connects to" strip until someone noticed.
**Applied diff:** author-topic SKILL.md stage 5 now carries the edge-wiring step
(publish → `load_universe` → edges), plus the rule that a NEW catalog entry must
include 3-5 `related_slugs`.
**Also applied (same cycle):** `--base-url` is now REQUIRED on
`render_screens`/`render_social`/`render_poster` — the silent `localhost:8000`
default produced error-page captures twice in the 2026-08-01 runs.
**File(s) touched:** `.claude/skills/author-topic/SKILL.md`, the three render
commands in `topics/management/commands/`.
**Applied how:** optimistic-and-logged (runbook + fail-fast tooling; no contract change).
**Status:** applied 2026-08-03.
