# The authoring pipeline — v2

What it is, how it runs, and the rules every stage is built against. Started
2026-09-11 as a ground-up redesign; the previous pipeline is archived under
`research/v1/` and is not a baseline for anything here. All five stages are
designed and written up below.

**The goals it is built to.** Present each topic honestly to a general adult
reader, at about the depth a good encyclopedia entry reaches. Make a good-faith
effort that facts and figures are accurate, most of all in Basics. Present
every position and idea in its strongest and most honest light, without it
reading as advertising. Automation drafts, a human publishes.

---

## 1. Name

**The authoring pipeline.** Short form, "the pipeline". "Author" stays the verb,
so the command and the skill say what they do while the noun stops competing
with it. "Engine" is retired: it was carrying three other jobs in this repo at
once, and it named a machine rather than a job.

## 2. Scope — the bookends

The pipeline takes a topic file from `not_started` to `ready`, and does nothing
else. Both ends were fixed before it was designed, and they are its whole
contract.

**Before it** is the topic itself. `research/topics/<slug>/` is the set of
topics, one directory each, cradle to grave. The database is derived from the
directory and is disposable.

**After it** is the human. `mark_ready` certifies, and any content write
withdraws that certification, because what was verified is no longer what the
file says. `publish_topic` is a switch that refuses anything not sitting at
`ready`; it re-derives no readiness and knows nothing about how it was earned.

Automation drafts; a human publishes.

## 3. How it reaches Claude

The subscription requirement decides the architecture before anything else does.

| Approach | Billing |
|---|---|
| Anthropic API, manual loop or Tool Runner | API credits |
| Managed Agents | API credits |
| **Claude Agent SDK** | **whatever the CLI is logged into** |

Only the Agent SDK reaches the subscription, because it is not an API client —
it is Claude Code as a library, authenticating the way the terminal command
does. That eliminates three quarters of the design space before any other
consideration. Installed: `claude-agent-sdk` 0.2.152, Claude Code 2.1.265.

**The pipeline is a program, not a session.** Each agent call spawns a fresh
headless Claude Code process with its own context, system prompt, tool
allowlist, model and effort. You start the pipeline from a terminal; it runs for
hours; no interactive session is involved. A Claude Code window is for launching
and for fixing, never for watching.

What the SDK makes available: the built-in tools (Read, Write, Edit, Bash, Glob,
Grep, WebSearch, WebFetch), server-side tools (`web_search`, `web_fetch`,
`code_execution`, `advisor`, tool search), skills, subagents defined in code,
your own Python functions as in-process tools, hooks and permission callbacks,
sessions, structured output, sandboxing, and budgets. Not available: the
API-only surfaces — Batches, manual cache placement, the Files API, Managed
Agents.

## 4. Orchestration

**Control flow in code. Judgment in agents, at declared points. Rules in prose
the agents read.**

The orchestrator's job is bookkeeping: what has run, what succeeded, what runs
next, what happens when something fails. With well-specified stages there is
almost no judgment in that, so most of a run needs no model at all.

Where a decision is genuinely ambiguous — retry or route, is this stage
finished — the orchestrator may be a Claude session. Two conditions make that
safe rather than merely pleasant:

- **A closed tool surface.** Its only way to act is through tools that record
  the transition. State discipline is then the mechanism, not a rule it is
  trusted to follow, and it cannot drift because it has no other levers.
- **No reach into content.** It sees step names, statuses and short notes,
  never the draft or the renders. That keeps it cheap (a run costs tens of
  millions of tokens; a thin orchestrator is roughly two percent of that) and
  keeps it from becoming a reader of its own run.

The orchestrator is never a gate. An agent that watched the run is primed to
accept its output.

**Repeatability is general, not strict.** Research, editorial and art are
non-deterministic by nature; the same topic run twice should produce two good
topics, not the same topic. What must hold is that the same *guarantees* were
applied: every stage ran, every gate was enforced, every check was computed
rather than asserted.

## 5. State — stages are functions over the file

There is no separate run ledger that can disagree with reality. **The artifact
is the state.** A stage looks at the topic directory, sees whether its inputs
are present and its own outputs are not, and runs.

Every stage declares three things, all expressible as assertions about the
files:

| Declaration | Meaning |
|---|---|
| **requires** | what must already be present |
| **satisfied when** | how to tell this stage is done (must be a separate check, or a stage re-runs on its own output) |
| **produces** | what it writes |

No stage knows the run order. Stage 3 does not care how or when stage 1 ran,
only that what it needs is in the file.

**Granularity of the function is granularity of the loss.** A session limit
costs one unit of work, not one stage. If the unit is "write the case for one
position", a limit on a twelve-position topic costs eight percent of the
heaviest stage instead of all of it. Stage 1 will be decomposed furthest,
because it is by far the heaviest.

Item identity is the addressing scheme this depends on, and it already exists:
ids are assigned once from an item's text and then frozen, so rewording and
reordering never change them (`topics/item_ids.py`). All 591 items across all
136 topics carry them. The JSON key is `id`; `item_id` is the Django field name.

Findings live in the file too, as a work queue, so routing needs nobody to
remember anything.

**Agents never write the product files.** Each unit returns structured output
that the orchestrator writes to `run/<stage>/<unit>.json`; code merges into
`topic.json` and `evidence.json` at phase end. Parallel units therefore never
contend for a file, and "is this unit done" is "does its return file exist
and validate".

**A stage's gate verdict is recorded with a hash of the fields it certified**
(in `evidence.json`), and a later write to any of those fields invalidates
it — the mechanism `mark_ready` already uses. "Requires: stage N" is then a
file assertion rather than a memory of run order.

## 6. Budget and usage limits

The subscription is the budget, and it is a shared resource — an interactive
session draws on the same windows. Magnitudes are lopsided, though: a run is
tens of millions of tokens and a working conversation is a rounding error
against it. The thing to avoid is having an agent poll the run.

**Every SDK call returns both windows' utilization, for free.** Not only at
threshold crossings. The useful data is nested in the raw dict under
`unifiedWindows`; the modeled top-level `utilization` field comes back empty.

| Window | What it costs to hit |
|---|---|
| `five_hour` | a nap; a run can sleep through one and finish |
| `seven_day` | the better part of three days |

That asymmetry is why the guards are asymmetric: **pause at 80% of the weekly
window, 90% of the five-hour one.** Overage is disabled at the org level, so
hitting a wall means stopping rather than silently spending.

**Cost is for the record; utilization is for control.** Every call also returns
`total_cost_usd` and a per-model breakdown, but on a subscription that dollar
figure is API-equivalent notional. Utilization is the real currency.

**A pause is a stop you chose.** Because every unit of work is resumable from
the file, pausing is just declining to dispatch the next one. No in-flight loss,
no separate pause machinery. Resumability and limit-awareness are the same
mechanism seen twice.

The one constraint: you learn utilization only by making a call, so the reading
is always one unit stale. With fine-grained stages that is precise enough to be
irrelevant.

## 7. Storage

A topic is a directory, and the directory name is the slug.

```
research/topics/<slug>/
  topic.json      product; the only thing the loader reads
  evidence.json   map, claim ledger, crux placement, cut record, gate verdicts
  icon.md         art brief + generation prompt
  review.md       the packet for the human
  run/ renders/ candidates/     process, untracked
```

Shipped images stay at `static/img/{topics,social}/<slug>.png` because that is
where Django's static pipeline serves them from. That is the only artifact
outside the topic directory, and it is a real constraint.

**Evidence is not process.** The claim ledger is the only proof that "an
unverified claim may not be asserted" was honored, and later stages depend on
it, so it must be durable. Drawing the product/process line at the top-level
directory is what nearly lost it.

## 8. Schema decisions so far

**Out: `tier` and `fold`.** Array order already carries the ranking — the
existing rule is that you move an item across the fold by reordering it — so
`tier` was a second encoding of the same judgment, and `fold` became per-topic
data for what is really a design-system constant. Fixed per-section counts
replace both, chosen as multiples of each section's column count so the
row-snapping logic goes too. That removes two fields, one render algorithm, and
one stage 2 decision, and it lets every downstream surface *assert* a layout
instead of deriving one.

**The counts (decided 2026-09-13).** Before Go-deeper is hard and a multiple
of the section's column count; the total is a guideline stage 2 applies topic
by topic. A section with fewer items than its show-count shows them all and
gets no Go-deeper.

| Section | Shows before Go-deeper | Total, guideline | Layout |
|---|---|---|---|
| Basics | 6 cells (a wide tile is 2) | 8–12 | three columns |
| Questions | 4 | 5–8 | one column |
| Positions | 4 | 3–8 | two columns |
| Actions | 4 | 6–10 | two columns |

The totals sit on the corpus medians (10, 7, 6, 8 across 18 drafted topics);
the tails — twelve positions, fifteen actions — are what the editor cuts, and
a two-camp topic ships two. Four questions is one screen; the reader chooses
to see more, which is what Go-deeper is for.

**Out: `prevalence_weight`, `prevalence_basis`, `spectrum_position`,
`importance`, `reveal`, and the rule that positions render by prevalence
(decided 2026-09-13).** Every section renders in file order, most important
first; that is the whole mechanism for weight. `reveal` only ever decided
which side of Go-deeper an item fell on, which the show-count above now does
from array order.

**Site delta this implies**, to be built before stage 2's checks are written
against it: `Position.Meta.ordering` and the view's position sort become
`order` only; `Section._tier_lead_count`, `_basics_base_count` and the
`has_layer_*` properties reduce to the fixed show-counts over array order;
the loader stops reading `tier` and `reveal`; a migration drops `tier`,
`reveal`, `prevalence_weight`, `spectrum_position` and `importance`; the
`when-normal`/`when-deep` classes are replaced by one before/after Go-deeper
class. The CLAUDE.md invariant about positions rendering by
`prevalence_weight` is retired with it.

**In and already working:** stable item ids; the six sections and their fields
as the loader enforces them.

**The per-field ownership table** is under stage 1. It is what makes a stage's
contract checkable rather than trusted; stage 2's lock check is derived from it.

## 9. The exit-criteria principle

**Every stage's exit criteria are what guarantee the next stage finds nothing.**

If a later stage legitimately catches something, some earlier stage's criteria
are too weak. The fix is always to strengthen those, never to patch this topic.
That is a permanent fix instead of a recurring one.

It follows that **inter-stage fix loops should not exist.** Routing a stage 4
finding back to stage 2 is the wrong shape; the right answer is for stage 2 to
measure before it writes, so there is nothing to route. Same move as `tier` and `fold`: stop
routing a finding around a loop and make the producer get it right the first
time.

**The exception, and it is the reason stage 5 exists.** Taken literally the
principle makes a final review pointless. It is not, because every other stage
reads a *slice* and stage 5 reads the *whole*. No amount of strengthening a
slice-reader's criteria catches a property that only exists across slices. Stage
5 does not catch what earlier stages missed; it owns something they structurally
cannot see.

That gives a sharp test for where a finding belongs: **could any single-slice
reader have seen it?** If yes, it is an upstream gap and the note says so. If
no, it is stage 5's by right.

## 10. Failure semantics

A stage that cannot satisfy itself **stops the run and marks the topic blocked**,
naming the stage its failure implicates. No routing, no continuing to the next
stage.

**Two kinds of failure, treated differently.** A *transport* failure — a rate
limit, a killed process, a malformed structured output — is retried a fixed
number of times (§11 names the clean retry signal), then blocks. A *criteria*
failure — the stage ran and its exit check failed — blocks at once. Stage 1
has one named exception: a ledger claim still open after its repair round is
cut and logged rather than blocking, because it is a source that did not say
what the writer remembered, not a pipeline bug.

The reasoning is §9. If a stage fails, some earlier stage's criteria were too
weak to prevent it, which is a pipeline bug rather than a task for this topic.
Absorbing it silently would fix the symptom and hide the bug. Stopping makes it
loud, and the human decides whether to fix the topic by hand or fix the stage.

This does not conflict with "the engine decides, never escalates" (Jeff,
2026-08-27). That rule is about resolving editorial forks mid-run by the
engine's own rules rather than asking. It was never about continuing when
something is actually broken.

## 11. Machine-level findings that apply to every stage

From the 2026-09-12 meta-research. Stage-specific findings live in
`research/STAGE1_RESEARCH.md`; these are cross-cutting and belong here.

### WebSearch cannot ground a claim

**Claude Code's WebSearch returns titles and URLs only.** The CLI maps results
to `{title, url}` and discards the snippets; verified by probe against this
install. The API's web search returns cited text spans, and Claude Code throws
them away.

So it is a discovery tool. Any stage that must quote or verify needs a second
fetch:

| Step | Tool |
|---|---|
| discovery | WebSearch, with `allowed_domains` |
| grounding | Bash + curl to disk — raw bytes, no intermediating model, and the file persists for a checker |
| cheap triage | WebFetch prompted to quote verbatim (it is a local fetch plus a small model, so it summarizes unless told otherwise) |
| attribution | a separate citation pass over stored files plus the draft — the citer can only cite what it was handed |

Measured limits on this install: 200 searches per session
(`CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`), 8 `max_uses` per call,
`allowed_domains` and `blocked_domains` mutually exclusive.

### Rate limits come as typed events, not exception strings

`RateLimitEvent` arrives in the message stream with `status`, `resets_at`,
`rate_limit_type` and a raw dict carrying both windows' utilization under
`unifiedWindows`. Reading the event beats parsing an exception, which only
fires *after* a failure. `allowed_warning` lets a run stop dispatching before it
is rejected. `ResultMessage.api_error_status` is the clean retry signal.

### Separate `query()` calls per stage, not `AgentDefinition` subagents

`output_format` is a session-level option, so a code-defined subagent cannot
carry its own JSON schema. Separate calls also give a journal key and
independent replay, and rate-limit events arrive on the parent stream so one
worker can be slept and resumed. Concurrency cap is 20
(`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`). Default buffer is 1MB; image-reading
agents need it raised.

### Fan out on retrieval, never on synthesis

Multi-agent is documented as a poor fit where workers need shared context or
have dependencies between them, and one open-source team abandoned parallel
section-writers because "the reports were disjoint." Parallel workers return
**structured, pruned findings**; one writer composes. Prose hand-back is what
produces disjointness.

### Prompt register is causal

"An anxious prompt produces a cautious, hedging model." Prohibitions backfire —
"a prohibition against a failure the model wasn't going to make can anchor it
toward that failure." So instructions of the form *do not hedge, never
both-sides* are the wrong shape.

### Conservatism instructions in a gate suppress recall

Documented across four model generations: a review prompt saying "only report
high-severity issues" or "be conservative" is followed literally and the gate
reports less. Ask for everything, filter in a separate pass. A gate can lose
recall on a model upgrade purely from prompt text.

### Checkers get the sources, and are blind to provenance

Blind to the author's reasoning and to any "this passed gate N" label, because
self-preference and label deference are triggered by exposure to provenance.
**Not** blind to the sources: a checker denied the sources cannot verify, only
opine, and an opinion-generating checker produces confident passes.

### Scaffolds to delete

Prefill (a hard 400 on current models), "think step by step", `<thinking>`
scaffolds, "output ONLY valid JSON" plus regex extraction, and required
reasoning sections. Also: **remove** "verify your own work" from a writer's
prompt on Opus 5 rather than rewriting it — it causes over-verification.

### The meta-lesson

Anthropic dropped context resets from its own harness when a model made them
unnecessary, and wrote: "every component in a harness encodes an assumption
about what the model can't do on its own, and those assumptions are worth stress
testing." Every scaffold in this design is an assumption of that kind and
should be re-tested against the current model before it is kept.

---

# Stage 1 — research

**Find out what the debate actually is, write every section at research grade,
and prove every hard claim before handing on.**

Designed 2026-09-13 against `STAGE1_RESEARCH.md` and Anthropic's published
research-agent guidance, and revised the same day after two independent cold
reviews. Stage 1 is the heaviest stage and is decomposed furthest (§5):
roughly sixty calls, most of them small, every one resumable from its own
return file.

## Contract

**Requires:** the index fields of `topic.json` — slug, title, scope, categories.

**Produces:** every content field of `draft`, with item ids assigned; in
`evidence.json`, the **map**, the **claim ledger**, the **crux placement**,
and stage 1's gate verdict; under `run/sources/`, the fetched pages and their
extracted text (process — the ledger carries the quotes, so it survives
without them).

**Satisfied when:** stats, questions and actions are at or above the §8
minimum and positions cover every ranked camp in the map; the map check
passes; the coverage check passes; every hard claim in the ledger is closed
as supported, attributed, or cut-and-logged; every URL resolved when written;
lint is clean. Anything else blocks the topic per §10.

## Three principles that shape the stage

**Depth is Wikipedia's, not a literature review's.** The goal is an honest
presentation to a general reader. Sources are the encyclopedic and journalistic
layer: reference sites, major explainers, the camps' own public statements,
official and statistical bodies. Academic work appears when an explainer points
at it. "Cite reviews, don't write them." This also answers Anthropic's finding
that research agents "consistently chose SEO-optimized content farms over
authoritative but less highly-ranked sources": the allowed source classes are
named up front.

**Sourcing is two-tier, because accuracy matters most in some places and
intellectual honesty is the higher rule everywhere else** (Jeff, 2026-09-12).
A **hard claim** — a number, a date, a named event, a quote, any sentence of
the form "X said" or "X found", and the existence of a camp's adherents — gets
a fetched source and a check. Basics is entirely hard claims, which is where
the accuracy effort concentrates. **Everything else is written from the
model's own knowledge under the honesty rule**: how a camp reasons, what it
values, what is common knowledge in the debate, and the page's own voice in
questions and crux. The certainty bar for that tier is the one a good
encyclopedia entry or a good LLM answer meets today (Jeff, 2026-09-13, when
per-argument sourcing was proposed and declined: that is literature-review
certainty, and it would cut real arguments adherents make but no fetched page
happens to state). The one free guard: the position writer receives its
camp's adherent quotes from the map, which are checked against fetched pages,
and its case must be consistent with them.

**When a hard claim's check fails, the writer has three moves**: cut it,
soften it to what the source supports, or attribute it to whoever asserts it.
The good-faith standard is that a figure the page states in its own voice has
a source behind it; it is not that every sentence carries a footnote.

**Stage 1 writes research grade, stage 2 writes for the reader.** Length budgets
here are loose ceilings — about twice the render budget — not targets. A
position says everything the camp's case needs and stage 2 cuts; the crux unit
writes where the disagreement sits and stage 2 makes the lead line sing. The
one thing stage 1 must leave in a durable form is what each hard claim's
source actually said, because stage 2 will reword almost every sentence and
needs something to check its rewording against. That is stage 2's fidelity
check, and it needs the ledger's stored quotes — the one dependency this
stage creates.

## Open research first, and its output is a map

Every tradition in the meta-research converged on not asking "what are the
positions?" — that is the generative mode, and a model can always construct a
defensible camp. Ask instead who has publicly said what, and where. So the
stage opens with an unmotivated harvest whose output is a **map**, not prose,
and the section writers are required to build against it: a writer may not
introduce a camp, a fact or a source that is not in the map. If it needs one,
it adds it to the map with a fetched source first. That dissolves the
open-versus-directed question — open research is what the writers are allowed
to know, so it can be neither skipped nor overridden by a section's convenience.

STORM's ablation is the warrant: removing the perspective-discovery step nearly
halved unique references.

## How units interact

**Nothing talks to anything, and no agent writes the product files.** Every
unit is a separate SDK call that reads files and returns structured output;
the orchestrator (code, §4) writes each return to `run/<phase>/<unit>.json`
and merges into `topic.json` and `evidence.json` at the end of each phase.
Source ids are namespaced by the unit that fetched them (`s-crit-03`). That
is what makes parallel units safe and every unit resumable: "is this unit
done" is "does its return file exist and validate".

Two shared artifacts:

- **The map**, in `evidence.json`: ranked camps with adherents, agreed facts,
  the stat list, controversial statements, gaps.
- **The sources store**, `run/sources/<id>.{raw,txt}`: every fetched page as
  raw bytes plus text extracted by a deterministic extractor (PDF included),
  with HTTP status, title and fetch date in the index. **"Fetched" means
  extracted text over a floor length with a 200 status**; a bot wall, a
  paywall stub or a JS shell is not a source.

Retrieval units return structure, writing units return content, checking units
return verdicts. No unit returns prose to another agent — prose hand-back is
what produces disjointness (§11). **Every unit is blind to something on
purpose**, and the "sees" column below is part of the contract.

No unit gets the Agent tool (Opus 5 delegates readily, and the unit count is
the orchestrator's), and no writer's prompt carries "verify your work" (§11).
Rules in prompts are stated affirmatively — what a camp is, what a question
looks like — and the things to refuse are enforced by lint and code checks,
which cannot be anchored (§11, prompt register).

## Phase A — the map

| Unit | Count | Model, effort | Sees | Returns |
|---|---|---|---|---|
| Framer | 1 | Opus 5, medium | index fields | dimensions of variation, affected populations, the frame-rejection question, seed sources |
| Scouts | 4, parallel | Sonnet 5, medium | the frame, one **source class** each | claimants (name, org, verbatim claim, source id, date), facts with quotes, everyone each document argues against by name |
| Camp scout | 1, after the four | Sonnet 5, medium | the four returns' `argues_against` and claimant orgs | same shape, from the camps' own organizations |
| Cartographer | 1 | Opus 5, high | all scout returns, nothing else | the map, with a **gap list** |
| Gap scout | 1 | Sonnet 5, medium | the gap list only | same shape as a scout |
| Cartographer, final | 1 | Opus 5, high | map plus gap return | final map; gaps closed or recorded unfilled |

**The framer** names the dimensions along which views vary before any position
is named (SEP's move: you cannot see a missing camp in a list, you can see an
empty cell), lists the populations materially affected, asks whether a camp
rejects the question, and seeds the scouts with the Wikipedia article and two
or three landmark explainers.

**Scouts divide by source class, not by section** — encyclopedic and reference;
explainers and journalism; official and statistical bodies; critiques. That is
the context-centric split Anthropic recommends, and it is what makes the
harvest unmotivated: no scout is looking for support for a section. The
highest-yield single operation is harvesting everyone a document argues
against by name — critics have an incentive to find every opponent. **The
camp-class scout runs after the other four**, because its domain list cannot
exist before the camps do; it is seeded from the names the others harvested,
with `blocked_domains` for content farms. **Saturation is computed by code**,
not reported by the scout: distinct claimant names per returned source, base
four, run two, under 5% new ends the class, with a floor of six sources.
Scouts run at medium because a model at low effort searches less and answers
from memory, the one behaviour a scout must not have.

**The cartographer** is the highest-stakes judgment in the stage. It groups
claimants into camps under rules it does not get to relax, stated in the
prompt as what a camp *is*:

- **A camp exists when two independent, named adherents, at least one
  institutional, assert its claim in their own published words.** Wikipedia's
  version: a significant view is one where it is "easy to name prominent
  adherents". Adherence, not coherence — the model cannot construct two
  adherents with fetched pages.
- **Two camps are distinct when there is a proposition one affirms and the
  other denies** — "not merely emphasizes differently". Camps that differ only
  in instrument, magnitude or sequencing are **merged before any writer
  runs**, with the variation recorded. This is where the position count is
  controlled: not by a cap, but by refusing secondary-aspect splits.
- **A hybrid position and a reject-the-question position are looked for
  explicitly**, because the page title presupposes a frame.
- **Camps are named by what they want.** All camps in the same grammatical
  form; a name passes if the camp's strongest advocate and strongest critic
  would both call it *accurate*. (Skeptic, Realist, Pragmatist, Alarmist are
  posture labels — the nuclear file gave both pro camps Pragmatist and Advocate
  and both anti camps Skeptic. That check is lint.)
- **Camps are ranked most to least important, with a one-line reason each.**
  Decided (Jeff, 2026-09-13): order is the whole mechanism for weight, in
  every section — the most important basics first, the most central questions
  first, the camps most people hold first, the way an answer about US parties
  starts with the two big ones. No prevalence band, no population, no scalar,
  no display of weight; the rank is a seed and stage 2 makes the final order.
  Every camp gets equal length.

It also emits the agreed facts (cited across camps; the basics stat list is
chosen from these), and the controversial statements that questions will come
from (Kunz & Rittel: "the origins of issues are controversial statements").

**The map is a checked artifact.** Before Phase B, code runs the quote check
over every adherent quote, agreed fact and controversial statement, and
asserts per camp: two adherents with distinct source ids, one institutional,
a `wants` line, a `distinguishing` proposition, a rank. A map that fails
blocks the topic — a cartographer that invents an adherent is the failure the
whole phase exists to prevent.

**The gap round runs once.** It is Co-STORM's moderator move — search for what
the map says is missing (a second adherent, an affected population with no
voice, a camp on one source), not for more of what it has. A second round is
where loops start.

**Decoy calibration is a fixture test, not a run step.** A recorded scout
return with fabricated camps mixed in, run against the cartographer whenever
its prompt changes; if a decoy survives the adherence rule, the prompt is
broken. Prompt register is causal (§11), so prompt edits need a regression
test, and this is the only test of the cartographer.

## Phase B — the sections

| Unit | Count | Model, effort | Sees | Returns |
|---|---|---|---|---|
| Stat writers | 1 per source | Sonnet 5, low | the stat entries that cite one source, that source's text | stat fields, verbatim quote per stat |
| Questions | 1 | Opus 5, medium | controversial statements, dimensions, agreed facts with quotes and ids, the stat entries | the question set, hard-claim sidecar |
| Position writers | 1 per camp | Opus 5, medium | own map entry with adherent quotes, own sources, agreed facts, a shared style sheet | position fields, hard-claim sidecar |
| Crux | 1 | Opus 5, high | positions, questions, agreed facts with quotes and ids | crux substance, camp placement, hard-claim sidecar |
| Overview, actions | 1 | Sonnet 5, medium | map, the explainer-class scout return, WebFetch for action URLs only | overview, why_now, glyph hint, actions, hard-claim sidecar |

Before Phase B, code assigns item ids to the draft (`topics/item_ids.py` is
plain Python; the loader no longer has to be first). Stats, questions and
positions run in parallel; crux after them; overview last.

**Stat writers** have the text on disk and no search, so the task is read and
transcribe; grouping by source is one call per page instead of one per
number. A stat with no fetched source does not exist. Value, unit, note,
detail, source fields and the quote all come from that text. Presentation
numbers — `series[].pct`, `fill_pct`, `range_at` — are derived by code from
the values, never written by a model.

**Questions** are written under Conklin's rules — open, no embedded solution,
no "should we do X", no benefits — and each names the controversial statement
it came from. Kind is decided by the taboo test: ban the contested word and see
whether the disagreement survives; if it evaporates it was definitional. The
nuclear file carries a question whose own `why` contradicts its `kind`, so this
is a check, not a hope. Questions carry numbers, so the unit gets the agreed
facts with their quotes and ids and emits a sidecar like a position writer.
`lean_pct_a` is written only when the map holds a poll source; otherwise null,
which the model and template already handle.

**Position writers do not see the other camps' text.** A camp's own sources
already tell it what it argues against, and hiding the others is what keeps
"critics counter" and "the argument goes" out of a camp's voice. The writer
uses its own knowledge plus the camp's sources and its verified adherent
quotes; the pass condition is the ideological Turing test — would an adherent
say "yes, that is our case". The prompt says it affirmatively: state the
camp's case as its adherents make it, including what they say about the
alternatives. Self-rebuttal ("but the model's fragility is real too") is what
lint catches, not mention of other camps. Every number and every "X said" in
the prose goes in the sidecar with a source id and quote, which closes the
audit finding of thirteen unsourced figures in 1,133 words. Register symmetry
across camps comes from the same style sheet and the same ceiling, not from
seeing each other. Opus 5 rather than Sonnet because in-voice writing is what
it is for; medium rather than high because a page of prose does not need
over-deliberation.

**The crux** uses subtraction (what nobody holds — SEP's "no one defends the
status quo") and root divergence (the earliest point of conflict, which the
measured data says is usually definitional, causal or a forecast, and rarely
moral). It must place every camp relative to the crux, so nuclear's orphaned
camp cannot recur; the placement is an `evidence.json` artifact for the map
check, not page content. Highest effort in the stage: the hardest single write.

**Overview and actions** are short and low-stakes. The unit has WebFetch for
one purpose, resolving action URLs at the moment they are written, and every
URL is code-checked again. The meta-research questioned whether Actions
belongs on a contested topic. Decided (Jeff, 2026-09-13): it stays. Every
topic has actions; where an action set is split by the contest, each side's
actions appear, mapped to the position via `for_position`.

## Phase C — the ledger and the checks

| Unit | Count | Model, effort | Sees | Returns |
|---|---|---|---|---|
| Extractor | 1 per section | Sonnet 5, low | section text, sidecar | hard claims: verbatim quote, self-contained restatement, kind, source id |
| Coverage check | code | — | draft, ledger | every hard-claim pattern in the text falls inside some ledger quote |
| Quote and URL check | code | — | ledger, store | pass or fail per claim |
| Verifiers | 1 per source | Sonnet 5, low | the claims citing one source, that source's text, nothing else | per claim: supported, partial, unsupported, attributed |
| Repairers | 1 per failure | Opus 5, medium | claim, verdict, source text, the field's text | a patch: cut, soften, or attribute |
| Lint | code | — | draft | defects |

**Extraction recall is checked by code, because a claim the extractor skipped
would otherwise pass every gate.** Every numeric token, four-digit year,
quoted span and "Proper Noun said/found/estimates" pattern in each section's
text must fall inside some ledger claim's quote span. Unmatched spans fail
the stage.

**Code checks before any model judges.** The cited quote must be in the cited
source's extracted text, by normalised string match, and every URL must
resolve. This makes a hallucinated URL or an invented quote structurally
impossible. It does not make a true quote support a false claim impossible —
citation laundering, "linked to" cited as "causes" — which is what the
verifier stands against.

**Verifiers are blind to the draft and to provenance, not to the source.** A
checker denied the source can only opine, and opinion produces confident passes
(§11). "Does this quote support this claim" is a task a 770M model matched
GPT-4 on, so Sonnet at low is right-sized, and it is a different model from
the writers — cross-family is not available on the subscription, cross-model is
the nearest substitute. All claims citing one source are checked in one call,
which loses no blindness and cuts the call count by most of an order of
magnitude. A **fact** is checked against the source; an **inference** —
causal, comparative, predictive — is checked against who draws it. `partial`
is a failure. Verifiers run in batches under the concurrency cap; a limit
event on the parent stream pauses the batch.

**A camp's own number is attributed, not asserted.** A fact whose only source
is in the camp or critique class is written as "the X camp cites…" unless a
reference or official source corroborates it. The verifier confirms the quote;
nothing else asks whether an advocacy site's statistic is fit to state in the
page's voice, so the remedy is built into the rule.

**One repair round, grounded.** The remedies are the three above: cut, soften
to what the source supports, or attribute. Attribution
means different things by voice: inside a position, the camp is the
attribution; in basics, questions and crux the page speaks, so the remedy
names the proponent in the sentence and that claim goes in the ledger, or the
sentence is cut or softened. Changed fields go back through extract, coverage,
check and verify. **A claim still open after that is cut and logged** in
`evidence.json`, and the topic blocks only if
the cut drops a section below its §8 minimum. Decided (Jeff, 2026-09-13):
an open claim is a source that did not say what the writer remembered, not a
pipeline bug, and blocking on it would block most topics on every run. A
wrong repair is worse than none, hence Opus.

**Lint** is code, not a judge: hedge phrases ("the argument goes", "from this
view"), self-rebuttal patterns inside positions ("but… is real too", "critics
counter"), posture labels in camp names, UK spellings, HTML entities and
straight quotes, camp-name register, section minimums. A phrase list is cheap
and cannot be gamed. Whether one camp reads with more energy than another
needs the whole and is stage 5's.

**The gate verdict.** When everything above passes, code writes stage 1's
verdict to `evidence.json` with a hash of the fields it certified. A later
write to any of those fields invalidates it (the mechanism `mark_ready`
already uses), which is how stages 2 through 4 can require "stage 1 valid" as
a file assertion.

## Model mix

Fable is reserved for stage 5. The split here is judgment versus handling:
Opus 5 where the output changes the topic (framer, cartographer, questions,
positions, crux, repairs — about fifteen calls), Sonnet 5 where the task is
search, parse, transcribe, decompose or check (about forty, all small, after
batching stat writers and verifiers by source). No unit runs at low effort
except the ones whose input is already on disk. Effort names do not map to
the same thinking across models, so these are starting points; the sweeps
worth running once a topic goes through are cartographer and crux at medium
versus high, and position writers at low versus medium.

## What this stage deliberately lacks

**No critic panel.** Neutrality and steelman are enforced by construction —
own sources, no sight of other camps, a lint for self-rebuttal — and by
stage 5's whole read, not by a judge-shaped call, which the meta-research says
takes a side even when the same model hedges as a generator.

**No planner that locks positions before research.** Camps come out of the
harvest; deciding the positions first and then researching them is the
generative mode.

**No fix loop.** One grounded repair round, then cut and log.

**No prevalence field.** Rank is a seed for stage 2's order, nothing more.

**No orchestrator model.** Every branch is a file assertion (§4).

## The shapes the units share

Decided once, before any prompt, because a unit's output format is half its
prompt and these cross unit boundaries. Sketches, not schemas yet; the field
names are the decision.

**A source** (the store index, in `evidence.json`):

```
{ "id": "s-ref-03", "url": "…", "title": "…", "publisher": "…", "published": "2025-03-01",
  "fetched": "2026-09-13", "status": 200, "class": "reference|explainer|camp|official|critique",
  "raw": "run/sources/s-ref-03.raw", "text": "run/sources/s-ref-03.txt", "text_chars": 18400 }
```

**A scout return** (scouts, the camp scout, the gap scout):

```
{ "class": "critique",
  "claimants": [ { "name": "…", "org": "…", "claim": "verbatim sentence",
                   "source": "s-crit-01", "date": "…", "argues_against": ["…"] } ],
  "facts":     [ { "statement": "…", "quote": "verbatim", "source": "s-crit-01" } ],
  "sources": [ …store entries fetched… ] }
```

Saturation is not in the return; code computes it from `claimants[].name`
per source.

**The map** (in `evidence.json`; the cartographer owns it, writers read it):

```
{ "dimensions": [ { "axis": "…", "poles": ["…", "…"] } ],
  "affected": [ "…" ],
  "frame_rejection": { "exists": false, "note": "…" },
  "camps": [ { "key": "…", "name": "…", "wants": "one sentence, in the affirmative",
               "distinguishing": "a proposition this camp affirms and another denies",
               "rank": 1, "rank_reason": "one line",
               "adherents": [ { "name": "…", "org": "…", "kind": "institution|person",
                                "quote": "…", "source": "s-camp-02" } ],
               "sources": ["s-camp-02", "s-ref-03"],
               "variation": "secondary-aspect differences merged here, recorded, not split" } ],
  "agreed_facts": [ { "statement": "…", "quote": "…", "source": "s-ref-03",
                      "cited_by_camps": ["…", "…"] } ],
  "stat_list":   [ { "label": "…", "viz": "…", "from_fact": 3 } ],
  "controversial_statements": [ { "statement": "…", "held_by": ["…"], "denied_by": ["…"] } ],
  "gaps": [ { "kind": "second_adherent|affected_unvoiced|single_source|empty_cell",
              "about": "…", "filled": false } ] }
```

**Crux placement** (in `evidence.json`, for the map check):

```
{ "crux": "one line", "placement": [ { "camp": "<key>", "side": "empirical|values|both", "note": "…" } ] }
```

**A ledger claim** (the sidecar a writer attaches is this minus `verdict`):

```
{ "id": "c17", "section": "positions", "item": "<item id>", "field": "detail",
  "quote": "the sentence as it appears in the draft",
  "claim": "self-contained restatement",
  "kind": "fact|inference", "source": "s-ref-03", "source_quote": "verbatim from the text",
  "verdict": "supported|partial|unsupported|attributed|cut", "note": "…" }
```

**Per-field ownership.** Stage 2 rewords freely but does not change specific
facts (Jeff, 2026-09-13), so the fields that *are* the fact — values, units,
source fields, URLs — are marked locked and code checks they left stage 1
unchanged; everything else stage 2 may reword under the fidelity rule. `tier`, `fold`,
`prevalence_weight`, `prevalence_basis`, `spectrum_position`, `importance`
and `reveal` are gone (§8).

| Field | Owner | Note |
|---|---|---|
| slug, title, categories, scope, related, status, icon | index / human / stage 3 | before the pipeline; `icon` is stage 3's, stage 1 emits a hint |
| overview.summary, scope_covered, scope_excluded, why_now; volatility | stage 1 writes, stage 2 may reword | `why_now` is a hard claim; stage 2's own extraction covers it |
| basics.stats[].value, unit, series[].value, range_*, source_* | stage 1, **locked** | every one a ledger claim |
| basics.stats[].series[].pct, fill_pct, range_at | code | derived from values |
| basics.stats[].label, note, detail, viz, wide | stage 1 writes, stage 2 may reword | fidelity check on reworded text |
| basics.intro | stage 2, overview editor | |
| questions[].text, kind, why, detail, lean_label_*, lean_pct_a | stage 1 writes, stage 2 may reword | `lean_pct_a` null unless the map holds a poll |
| questions[].votes | participation | never the pipeline's |
| positions[].name, steelman, description, detail, representative_*, proponents | stage 1 writes, stage 2 may reword | a name may get shorter or friendlier, never change what the camp wants; the map's `wants` line is the check |
| positions[].color_key | code | assigned from order at load |
| crux.* | stage 1 writes, stage 2 may reword | `lead_highlight` is stage 2's |
| actions[].title, description, url, kind, for_position | stage 1, url **locked** | url resolved when written |
| array order, every section | stage 2 | seeded by stage 1's rank; the site renders every section in file order |
| id | code | assigned before Phase B, frozen |

---

# Stage 2 — editorial

**Turn research-grade text into the page a general reader meets, without
changing what it says.**

Designed 2026-09-13, revised the same day after two independent cold
reviews. Stage 1 owns substance; stage 2 owns the reader's experience: how much, in what order, at
what length, in what words. It does no research, and that is a mechanism
rather than a rule — its units can read the topic directory and nothing else.

## Contract

**Requires:** stage 1's gate verdict valid — `draft` at research grade with
ids, the map, the ledger with stored quotes.

**Produces:** the shipped text of every content field, the array order and
item count of every section, a **cut record** in `evidence.json`, and stage
2's gate verdict.

**Satisfied when:** every field is within its hard bound; every ledger claim
whose field changed passed fidelity; stage 2's own extraction and coverage
check found no hard claim that is not in the ledger; every item passed the
continuation test; every locked field is byte-identical to stage 1's; lint is
clean. Anything else blocks the topic per §10.

## What the reader actually sees

Every item has two tiers, and the templates fix what goes where:

| Item | Condensed — always visible | Expanded — appended on open |
|---|---|---|
| stat | value, unit, note | detail, source |
| question | text, why it is contested | detail |
| position | name, steelman line | description, detail, representative, proponents |
| crux | lead, subtitle | empirical branch, values branch |
| action | title, description | — (description hides on mobile until Go-deeper; no open state) |

**The expanded tier builds on the condensed tier.** When an item is open both
are on screen, the expanded text directly below the condensed, so the expanded
text is read as a continuation and never as a replacement. A description that
restates the steelman, or a detail that reopens with "the X camp believes",
is the failure. Two tests, both promptable:

- **The continuation test.** Concatenate condensed and expanded and read them
  as one passage. It must read without repetition or reintroduction.
- **The standalone test.** The condensed tier alone must make sense, because
  share cards, the poster and print show nothing else.

**There is no global depth control, and no `reveal`.** The Brief/Normal/Deep
toggle the design system described is gone from the product. What the page
has is two states per section — before Go-deeper and after — and which items
fall on which side is the §8 show-count applied to array order. The `reveal`
field is deleted along with `tier`; the site delta is listed in §8.

## Order is the whole mechanism for weight

Decided (Jeff, 2026-09-13). Every section displays in file order, most
important first: the basics that matter most, the most central questions, the
camps most people hold, the actions a reader would most want. Stage 1's rank
seeds it; stage 2 makes the final call and may depart from the seed with a
recorded reason. Nothing else encodes weight — no prevalence number, no band,
no size difference, and every camp gets equal length. The site's rule that
sorted positions by `prevalence_weight` goes (§8).

**Count is a judgment against guidelines, not a rule.** How many items show
before Go-deeper is the fixed per-section constant in §8; the total per
section is the editor's, topic by topic, against the §8 guideline range. The
position count is mostly settled upstream — the cartographer merges
near-duplicate camps before anything is written — so stage 2 orders the camps
and may drop from the bottom of the ranking when the topic does not need
them, never from the middle.

**Every cut is recorded.** The cut record names the item, its id, and the
reason, so a human can restore one and so the decision is visible. This is
PRISMA's near-miss rule: a wrongly kept item gets caught downstream, a wrongly
cut one is invisible forever.

## Fidelity — the one rule that matters most

Stage 2 will cut, condense and reword almost everything, and none of it may
change what stage 1 established. The rule, made checkable:

**A restatement may lose precision. It may never change direction, magnitude
class, or attribution.** 52% may become "about half" or "over half". It may
not become "under half", "a large majority", or lose who measured it.

The check is small and grounded. For every ledger claim whose field changed,
a no-web unit is handed the claim, its stored source quote, and **the whole
new text of that field** — after condensing, the claim may have moved or
merged, so "the sentence" has no referent — and returns where the claim now
lives and whether it is faithful, drifted, or absent. Stage 1 verified against
the world; stage 2 verifies against stage 1's record. This is the dependency
stage 1's design named, and the reason the ledger's quotes are durable.

**Stage 2 may not introduce a fact, and that is checked, not trusted.** The
overview editor writes `why_now` fresh, and condensing two sentences can mint a
number ("a fourfold gap") that was never a ledger sentence. So stage 1's
extractor and coverage check run again over stage 2's output; any hard claim
that does not map to an existing ledger claim fails the stage.

**Locked fields are asserted, not trusted.** Code diffs every field the
ownership table marks locked (stat values, units, series values, source
fields; action URLs) against stage 1's output. A byte differs, the stage fails.

**A camp may be renamed** to something shorter or friendlier, never to
something that changes what it wants. The map's `wants` line goes to the
fidelity checker with the new name.

**The same honesty applies to what is not a fact.** A position condensed to
its steelman line is still the strongest honest version of that camp's case,
not the most quotable. Cutting a camp's best argument to fit a budget is a
fidelity failure the continuation reader cannot see, which is why the
positions editor sees every camp at once: symmetry of length and register
across camps is exactly what an editor is for, and it is the one place in the
pipeline where seeing all camps together is the point rather than the hazard.
Length symmetry is code (a ratio across camps); register is one Sonnet read
of all the steelmen together.

## Length and reading level

**Two numbers per field, kept in one table.** We know roughly how much text
each slot holds (Jeff, 2026-09-13). So each field gets a **hard bound**, the
length at which the design visibly breaks or the loader truncates, and a
**target**, the length to write to. Hard bounds gate; targets are guidance,
because a lint that fails on guidance stops gating anything. The table is
derived from the templates and lives in one place; the editors' prompts are
assembled from it. The poster's longest-word bound is in the table, so stage
2's exit can guarantee stage 4's sheet checks rather than leaving overflow
for stage 4 to discover.

**Reading level is measured, reported, and never a gate.** The audience is
adults, not all of them patient. Guideline: Flesch-Kincaid grade 10–11 for
condensed text, 12–13 for expanded. Code computes it per section and the
number goes in the packet as one line. The style sheet carries the
qualitative version — "a great textbook or an Our World in Data explainer" —
which is what the editor actually writes to.

## Units

| Unit | Count | Model, effort | Sees | Returns |
|---|---|---|---|---|
| Section editor | 1 per section, parallel | Opus 5, medium | stage 1's section, the map, the budget table, count guidelines, style sheet | order, count, both tiers of every kept item, cut record |
| Crux editor | 1 | Opus 5, high | stage 1's crux, position names and steelmen | lead, highlight, subtitle, both branches |
| Overview editor | 1, last | Opus 5, medium | the whole condensed layer | summary, scope lines, why_now, basics intro |
| Budget, count, lock check | code | — | draft, stage 1's draft | hard-bound failures, locked-field diffs |
| Extractor + coverage check | Sonnet 5, low + code | | stage 2's text | hard claims not in the ledger |
| Fidelity checker | 1 per changed claim | Sonnet 5, low | claim, stored source quote, the field's new text | faithful, drifted or absent, and how |
| Continuation reader | 1 per section | Sonnet 5, low | each item's tiers, concatenated | per item: stands alone, continues, restates |
| Register reader | 1 | Sonnet 5, low | all steelmen and descriptions | per camp: same register or not, and how |
| Repairer | 1 per failure | Opus 5, medium | the item, the finding, stage 1's text | a patch |
| Readability, lint, verdict | code | — | draft | grades reported, defects, gate verdict with hash |

Sections run in parallel; the crux after positions and questions, because its
lead must not contradict a steelman it sits beside; the overview last, because
the summary describes the page that now exists. Then code checks, extraction,
fidelity, continuation and register in parallel, one repair round, recheck,
lint, verdict. About nine Opus calls and thirty small Sonnet calls.

**The crux gets the highest effort in the stage.** Its lead is the poster's
dark band and the share card's one line; it is the most-read sentence on the
page and the one stage 1 deliberately left for the editor.

## The shapes the units share

**A section editor's return** — the section as it will ship, plus what left it:

```
{ "section": "positions",
  "items": [ { "id": "<frozen id>", "name": "…",
               "condensed": { "steelman": "…" },
               "expanded":  { "description": "…", "detail": "…",
                              "representative_name": "…", "representative_note": "…",
                              "proponents": "…" } } ],
  "order_reason": "only if the order departs from stage 1's rank",
  "cuts": [ { "id": "<frozen id>", "name": "…", "reason": "…" } ] }
```

`condensed` and `expanded` carry exactly the fields the tier table above
assigns; the loader flattens them. Locked fields are absent — the editor never
emits them, and code copies them forward from stage 1 and diffs the result.

**A fidelity verdict**, one per ledger claim whose field changed:

```
{ "claim": "c17", "now_in": "positions/<id>/description", "verdict": "faithful|drifted|absent",
  "lost": "precision|direction|magnitude|attribution|none", "note": "…" }
```

**A continuation verdict**, one per item in a section:

```
{ "id": "<frozen id>", "standalone": true, "continues": "continues|restates|reintroduces" }
```

**The cut record** in `evidence.json` is the union of every editor's `cuts`.

## The budget table

One file, derived from the templates and the model's field lengths, with a
check that fails when a template or a field length changes so the table cannot
go stale silently. Each row: field, hard bound, target, and one line on which
render slot sets it. The §8 counts are not in it; they are a separate decision.

## The style sheet

The one document every editor reads. Its contents are decided; its prose is
written with the other prompts so all five stages share a voice.

- The design system's tone line: calm, precise, intellectually serious but
  plainspoken; explanatory, not persuasive; a great textbook or an Our World
  in Data explainer.
- The two reading-level targets, as intent rather than number.
- The fidelity rule: precision may go, direction, magnitude and attribution
  may not.
- What a steelman line is: the camp's case in one breath, the sentence an
  adherent would put on the banner — not a slogan, not a summary of the
  description.
- Every camp in the same register, to the same length. Weight is order, and
  only order.
- The continuation rule: expanded text continues the condensed text and never
  restates or reintroduces it; condensed text stands alone.
- Plain text only: `&`, typographic quotes, no markup; US spelling.

## What this stage deliberately lacks

**No web tools, on any unit.** "No new research" enforced by the tool surface.

**No critic panel.** Fidelity, continuation and register are the three checks,
all groundable, all cheap. Neutrality was enforced by construction in stage 1
and is read for whole in stage 5.

**No fix loop.** One grounded repair round, then block.

**No `reveal`, no `tier`, no `fold`, no prevalence.** Order, and the §8
show-count applied to it.

**No length decisions of its own.** The budget table is the single source;
stage 2 authors to it and stage 4 measures the result.

---

# Stage 3 — iconography

**Make the topic's two icons, and prove the art before finishing.**

Stages 4 and 5 ask almost nothing of stage 3 — the art present, and art that
composes into a card without breaking it. So the obligation is narrow: produce
art that is right, and do not hand on art that is not.

## Contract

**Requires:** stage 2's gate verdict valid, so the summary and position names
are the ones that ship; title, the first category's `color_key`, scope,
overview summary and position names from `topic.json`. Position names matter because one summary line cannot
tell a brief-writer what the topic's tension actually is.

**Produces:** `static/img/topics/<slug>.png` at 1035×690 on white; the Phosphor
glyph written into `topic.json`; `icon.md` with the brief, the generation
prompt and the selection note; every candidate kept under `candidates/` so a
human can override the pick.

**Satisfied when:** the art passes the judge and the glyph resolves to a real
Phosphor name.

The brief living at `research/topics/<slug>/icon.md` means the next load picks
up its generation prompt into `Topic.primary_image_prompt` with no flag; stage
4 loads the topic after stage 3 has run, so the provenance is always present.

## The prompt is assembled, not written

The style paragraphs in every existing brief are the same text with the hue
swapped. Every brief re-derives boilerplate it cannot improve and can only get
subtly wrong. So split it:

| Constant template | Per-topic slot |
|---|---|
| monoline, one stroke weight, rounded caps | the scene and its elements |
| duotone, 16–18% fill on every mass | the category hex, substituted |
| frameless, white ground, no text | what this topic's domain contains |
| universal negatives: gradients, 3D, texture, shadow | topic negatives |
| the composition rules below | |

The briefing agent then writes only the scene, which is the only part it is
qualified to invent. Style cannot drift, briefs get short and comparable, and
changing a style rule updates every future icon at once.

The **category hex is supplied, not hunted**: `color_key` maps to a `--cat-*`
token in `tokens.css`; the agent is never asked to find it by reading prose.

## Composition — what makes a scene rather than a lineup

Measured against the two worked examples. Nuclear does five things immigration
does not, and immigration's brief explicitly forbade all five: *"all standing on
a single ground line"*, *"placed symmetrically on either side"*, *"about the
same height as each other"*, *"equal visual weight"*, *"a single thin, straight
horizontal ground line… no landscape, no hill"*. The model complied exactly. It
produced a shelf of three objects because it was asked for one.

- **One dominant focal mass.** Not equal-weight objects.
- **At least one overlap.** Occlusion is what creates depth.
- **A shaped ground.** A curve, not a rule. A flat line makes a shelf.
- **Scale hierarchy.** Big, medium, small.
- **Something connective crossing the frame.** Power lines, steam, a horizon.

## Neutrality is a negative constraint

**The icon's job is recognition.** On a wall of 38 tiles it says which topic
this is. That is the primary and usually the whole job.

**Do not advocate.** No mushroom cloud, no sunlit meadow. Showing the domain
plainly is already neutral, and it is far easier to satisfy than balance.

**Opposing elements are welcome when the domain supplies them, never
manufactured.** Nuclear works because a real plant site plausibly holds cooling
towers and a waste drum; nobody invented the opposition. Immigration's brief
manufactured one — a door leaf covering exactly half its opening — and its own
notes admit the leaf kept drifting shut or wide and had to be measured against
the frame. A symbol was asked to carry an argument it could not carry.

**Never express neutrality as symmetry.** That is the trap a careful
brief-writer falls into by trying hard, and it is what produced the lineup.
Balance what the scene depicts, not the sizes and spacing of things in it.
Nuclear holds promise and peril while being wildly asymmetric.

## The loop

**Generation decides composition; refinement only fixes rendering.** Edit mode
preserves composition by design, which is why the spec prefers it — so editing
a lineup yields a better-rendered lineup. No number of refinement rounds would
have saved the immigration icon.

That makes four samples of one prompt the wrong first move: it buys four
near-identical compositions. The variation that matters is in the prompt, not
the seed.

- **Round 1** generates two or three genuinely different scene compositions,
  two samples each. Six images at $0.134 is about $0.80.
- **Later rounds** use edit mode on the incumbent, for rendering fixes the judge
  names in words — "the steam strokes are thinner than everything else" is
  exactly the note a human wrote by hand on nuclear.

**No measurement gate.** Fill weight, stroke uniformity, cohesion and hue are
the prompt's job, judged by eye. A cohesion metric based on connected components
would have flagged nuclear, whose atom floats free in the negative space beside
the towers — the exemplar fails the proxy. What stays mechanical is sanity, not
quality: the file is not blank or corrupt, it is 1035×690 on white, no text
crept in. Those catch API failures.

**The judge's job is therefore small**: is this the right scene for this topic,
and does it sit correctly beside its neighbours. It sees the candidates and
the neighbours only — not the brief, not the round notes, not which candidate
is the incumbent (§11: checkers are blind to provenance). Neighbours means *same
category*, because a shared hue is where a clash shows.

**Stops.** No cap on rounds. Stop on a pass. Stop when a round's best fails to
beat the incumbent, which says more rolls of this prompt will not converge and
the brief itself is the problem. **Hard stop at $3.00 per topic** — about five
rounds — as the backstop against a brief that never converges. Either stop
blocks the topic per §10, which hands a human a folder of candidates and a
brief to edit, exactly as the spec already intends. Spend is logged per round;
this is a separate bill on a separate account and nothing currently tallies it.

**Costs** (Gemini 3 Pro Image at 1K, confirmed against Google's pricing page):
$0.134 per image standard, $0.067 batch. Flash is half the price but the spec
chose Pro because it adheres best to the style constraints, so a cheaper model
fails more rounds. Batch halves the cost but needs submit-and-poll for a saving
of pennies on a topic that usually needs one round.

## The glyph

Stage 3 owns both icons. Stage 1 still emits a Phosphor hint, because the
planner knows the topic best, but the hint stops being authoritative: stage 3
validates it against the shipped Phosphor set and only reaches for an agent when
it does not resolve; an unvalidated name renders as nothing.

---

# Stage 4 — integration

**Build every surface from the content and the icon, then measure each one.**

Stage 4 is the first point at which content and icon both exist, which is what
makes it an integration stage in the ordinary sense. It is not a review. It
produces the files that ship and proves the contract held.

## Contract

**Requires:** stage 2's and stage 3's gate verdicts valid; the icon present at
`static/img/topics/<slug>.png`.

**Produces:**

| Output | Where |
|---|---|
| og card | `static/img/social/<slug>.png` — the file `og:image` actually serves |
| square, portrait cards | the packet, for manual posting |
| poster PDF | print-ready 18×24in |

Plus a pass, or a list of measured failures.

**Satisfied when:** all four files exist and every assertion below passed.

**Environment.** Stage 4 renders from the loaded site rather than from files, so
it needs the topic in the database and a server running. It does both itself —
loading the topic is its first act — which keeps it self-contained and
idempotent, and means no stage depends on another having left the server in some
state. Stage 5 is the same. Both need headless Chrome, the pipeline's only
non-Python dependency.

## The surface manifest

One table, one runner. A row is a route, params, a canvas, a class, and what it
emits. Adding a surface is adding a row, not writing another command.

| Surface | Route | Canvas | Class |
|---|---|---|---|
| topic desktop | `/<slug>/` | 1440 | flow |
| topic mobile | `/<slug>/` | 390 | flow |
| topic narrow | `/<slug>/` | 320 | flow |
| the same three, expanded | `?expanded=1` | as above | flow |
| og card | `/<slug>/share/?render=og` | 1200×630 @2x | sheet |
| square card | same route | 1080×1080 @2x | sheet |
| portrait card | same route | 1080×1350 @2x | sheet |
| poster | `/<slug>/poster/?fit=1` | 18×24in | sheet |

Category and site share cards fit the same shape and should be covered; one of
the standing defect-register entries is a share-card defect.

**`?expanded=1` is an artificial state, and only stage 4 may use it.** It is a
DEBUG-only flag that forces every Go-deeper layer open at once, built so a
capture rig could photograph deep content without clicking. It is gated on
`DEBUG`, so it does not exist on the live site, and no reader has ever been in
that state. For measuring individual elements it is a convenience — one page
load instead of N clicks — and the artificiality does not matter, because
per-element overflow does not care what else is open.

It does mean **stage 4 must never assert anything about total page height in
that state**, because nobody is ever in it and the number means nothing.
Measured on a real topic: a 320px expanded page runs 68,603px, and mobile
expanded 52,894px.

The deep content is in the served HTML all along, hidden by Alpine rather than
fetched, so the flag is not needed to read the text either. One page load and a
DOM walk gets every word in reading order, each block tagged with its layer.

## Two classes, two failure modes

This split is why one set of checks never fit stage 4. It was checking two
different things with one lens.

**Flow** surfaces scroll and reflow, so there is no canvas to overflow. Assert:
no horizontal page scroll; no element wider than its container; no clipped text
where overflow is hidden; the §8 show-counts exactly match what is above
Go-deeper; every interactive element clears 44px at ≤640px; no orphaned grid
row.

**Sheets** have a hard canvas and clip silently, so overflow is the whole
failure mode. Assert: content within the canvas, reported as a signed overflow
number; nothing positioned outside the bounds; no clipped text. Fold and touch
targets are meaningless here. The poster's `?fit=1` mode already stamps pixel
overflow onto the root element, and that mechanism generalizes to every sheet.

## What stage 4 does not do

**It does not review.** No agents, no screenshots for anyone to read.

**It does not check links.** A link is validated by whichever stage writes the
URL, at the moment it is recorded — not discovered dead hours later.

**It does not judge design conformance.** Token palette, spacing scale,
breakpoint rules and touch floors are properties of the templates, not of any
topic. See below.

**It does not route findings back into the run.** Per §9, it should never fail
on a run where every prior stage met its criteria. Not rarely — never. If it
does fail, the response is:

| What it found | What is actually broken |
|---|---|
| content overflows a surface | stage 2's measurement |
| icon missing or wrong | stage 3's exit criteria |
| off-palette token, wrong spacing, broken breakpoint | the templates |

A suite that never fails still earns its place: it is what tells you the moment
something changed.

## Design conformance leaves the pipeline

Every open entry in the standing defect register names a file and a line in
`templates/` or `static/css/`. Not one is about a topic's content, and several
say "every topic" outright. A per-topic stage was rediscovering site-wide bugs
topic after topic, and the register existed mainly to stop them being
re-reported — a cache in front of a question that should not be asked 136 times.

So conformance becomes a **test suite over fixture topics, run when templates or
CSS change.** The assertions come straight from the token file: 108 tokens, 12
spacing steps, 4 radii. Every computed color is in the palette; every radius is
one of four; every margin and padding is on the scale or zero; every breakpoint
rule holds at its width.

Fixtures are chosen to stress the layout, and the register says which stressors
matter: twelve positions to exhaust the palette, a ranked stat in a non-wide
tile, a bar stat with `fill_pct: 0`, the longest title, the longest word unit on
a poster value.

**Same manifest, two consumers.** Walk it per topic and you get stage 4. Walk it
over fixtures when templates change and you get conformance. That is what turns
"more surfaces" from more work into more rows.

Sheets must be covered too, not just web — two register entries are sheet
defects, and a web-only suite misses both.

## Sequencing

Build the conformance suite before deleting the critics, or coverage lapses in
the gap. Seed it from the open register entries as failing tests, which turns
the register from a list of complaints into a burndown that proves itself fixed.

## What this replaces

Three management commands that each re-implement headless Chrome and say so in
their own docstrings; three opus critics; the section-tiling machinery built to
make 50,000-pixel captures legible to an agent; the capture-cap check guarding a
capture that stops happening; and the stage-4-to-stage-2 fix loop.

---

# Stage 5 — the read

**One reader sees the finished topic the way a person would, and makes the
ready determination.**

Not a check — everything mechanical was settled upstream and stage 5 requires
stage 4 to have passed, so it needs no check lines and no shell. It reads.

Its justification is the exception in §9: every other stage reads a slice, and
this is the only reader that sees the whole. Tone drift across sections, the
same argument made twice by two camps, a crux that does not follow from the
questions above it, the icon working alone but not composed with copy on a
card — none of those are visible to any slice-reader, at any strength of exit
criteria.

## Contract

**Requires:** stage 4 passed.

**Produces:** a determination, everything it saw, and the three notes code
ranks to the top for the packet.

**Satisfied when:** the determination is recorded. If ready, the orchestrator
calls `mark_ready`.

## What it is handed

**The text, once.** All of it, condensed and deep, in reading order, each block
tagged with its layer. One page load and a DOM walk; the deep content is in the
HTML already. About 78k characters on a full topic. The text does not vary by
viewport, so it is read once, not per view.

**Screenshots of every view, at native resolution.** Not downscaled: a person
reads type at real size, and that is how a bad line break, an over-dense card
or a heading that reads as a label become visible. Downscaling destroys exactly
what is being judged.

| View | Shots |
|---|---|
| desktop 1440 | ~8, scrolled |
| mobile 390 | ~14, scrolled |
| og, square, portrait cards | 1 each |
| poster | 1 |

About 26 images. Deep-layer shots come from clicking a section open, not from
`?expanded=1`, because that is the state a person is actually in.

**320 is not read.** The design system names its design widths as desktop 1180
content max and mobile 390. There is no 320 mock, so "does this read well at
320" has no target to judge against. 320 is a must-not-break width, which is
measurement, which is stage 4's. And if 320 reads badly it reads badly on all
136 topics, which makes it site-wide and not a per-topic judgment.

**Fixed screenshots rather than a live browser.** What a browser adds is
interaction — the expand, the depth control, sticky chrome — and all of it is
template behavior identical on every topic, so it is the conformance suite's by
the same rule that moved design conformance out. And handing over 26 images at
once is a design wall: stage 5 exists to see everything together, which
sequential browsing is precisely not.

**It must be one agent, and it must not have watched the run.** One, because
the whole-artifact judgment cannot be split across parallel critics. Fresh,
because an agent that watched the run is primed to accept its output. No
verdicts, no ledger, no plan — the finished thing as a reader meets it.

Model and effort at the top of the range. This is the single call that gates
the pipeline; being cheap here is false economy.

## What it reads for

Only what no slice-reader can see (§9). Stage 2's continuation reader owns
"does Go-deeper restate"; stage 4's assertions own "does the card match the
page"; the cartographer owns duplicate camps. What is left is the whole:

**Structure and flow.** Does the crux follow from the questions. Does reading
order work on mobile, where the layout differs. Does the page, read top to
bottom, tell one story.

**Consistency.** Does a figure in Basics sit oddly beside a claim in a
position. Is one camp written with more energy than another. Is a camp given
prominence its place in the order does not explain.

**Plausibility, not verification.** Does this hold together. No sources, no
fact-checking, no web — that was stage 1's, and re-doing it here is the
duplicated judgment the pipeline caps. "Misled" therefore means internal
inconsistency, and the packet says so, so nobody reads a stage 5 pass as a
factual review.

## The determination

| Outcome | Meaning |
|---|---|
| ready, no notes | publish |
| ready, with notes | publish, and here is what you might change |
| not ready | a reader would be misled or confused |

The line between a note and a block is **whether the page would actively
mislead someone.** That is a bar an agent can apply consistently, unlike "is
this good enough."

Not-ready stops the run per §10. It does not route back, because a finding
stage 5 can make is either something no upstream stage could have owned, or
evidence that an upstream stage's criteria are too weak — and in the second
case the fix belongs there permanently, not in this topic.

**The bar for a note.** A stage told to check whether something "flows well"
will find something to say forever. So: a note must name **what the reader
experiences.** Not "the transition could be smoother" but "positions four and
seven argue the same thing, so a reader meets the same case twice." If you
cannot say what a reader does or thinks differently, it is not a note.

Three reach the packet. The reader reports everything it sees — a gate told
to say little says less than it saw (§11, conservatism suppresses recall) —
and code ranks and truncates to three, with the rest kept in `evidence.json`.

---

## Open questions

- Concurrency against a burn rate that is only sampled once per call (the
  one-file problem is settled in §5).
- Where stage 5's determination and notes are recorded — `evidence.json`,
  `review.md`, or both.
- Where the rules live and how a stage's prompt is assembled. One home,
  decided once, so a rule cannot drift between copies.
- Deliberate re-runs over a finished topic. The satisfied-when check handles the
  accident; deliberate regeneration is what killed refresh.
