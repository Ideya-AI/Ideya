# The authoring pipeline — v2

What it is, how it runs, and the rules every stage is built against. Started
2026-09-11 after v1 was archived to `research/v1/`. Stages 3, 4 and 5 are designed
and written up below; 1 and 2 are not.

Read `research/v1/RESEARCH_PIPELINE.md` for why a v1 rule existed. Do not treat
v1 as a baseline — it is evidence about the problem, not a constraint on the
solution.

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
A hook blocks automation from ever calling it.

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
| `five_hour` | a nap; v1 proved a run can sleep through one and finish |
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
  evidence.json   claim ledger, gate verdicts, prevalence basis, open findings
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

**In and already working:** stable item ids; the six sections and their fields
as the loader enforces them.

**Still open:** the per-field ownership and locking table — which stage writes
each field, and what freezes after which stage. v1 had the rule ("facts lock
after stage 1") but buried it in a patch whitelist. It belongs in the schema,
because that is what makes a stage's contract checkable rather than trusted.

## 9. The exit-criteria principle

**Every stage's exit criteria are what guarantee the next stage finds nothing.**

If a later stage legitimately catches something, some earlier stage's criteria
are too weak. The fix is always to strengthen those, never to patch this topic.
That is a permanent fix instead of a recurring one.

It follows that **inter-stage fix loops should not exist.** v1 routed findings
from stage 4 back to stage 2; the right answer is for stage 2 to measure before
it writes, so there is nothing to route. Same move as `tier` and `fold`: stop
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
naming the stage its failure implicates. No retry, no routing, no continuing to
the next stage.

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
`unifiedWindows`. v1 regexed a wait time out of an exception string, which only
fired *after* a failure. `allowed_warning` lets a run stop dispatching before it
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
testing." v1's scaffolding should be re-tested against the current model rather
than carried forward.

---

# Stage 3 — iconography

**Make the topic's two icons, and prove the art before finishing.**

Stages 4 and 5 ask almost nothing of stage 3 — the art present, and art that
composes into a card without breaking it. So the obligation is narrow: produce
art that is right, and do not hand on art that is not.

## Contract

**Requires:** title, category, scope, overview summary, and the position names,
all from `topic.json`. Position names matter because one summary line cannot
tell a brief-writer what the topic's tension actually is.

**Produces:** `static/img/topics/<slug>.png` at 1035×690 on white; the Phosphor
glyph written into `topic.json`; `icon.md` with the brief, the generation
prompt and the selection note; every candidate kept under `candidates/` so a
human can override the pick.

**Satisfied when:** the art passes the judge and the glyph resolves to a real
Phosphor name.

The brief living at `research/topics/<slug>/icon.md` means the next load picks
up its generation prompt into `Topic.primary_image_prompt` with no flag. v1
recorded that provenance as unfixable because stage 2 loaded before the brief
existed; stage 4 loading the topic itself after stage 3 has run closes it.

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
token in `tokens.css`. v1 asked the agent to find it by reading prose.

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
and does it sit correctly beside its neighbours. Neighbours means *same
category*, because a shared hue is where a clash shows; v1 handed it the first
three PNGs alphabetically.

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
it does not resolve. v1 validated nothing, so a wrong name rendered as nothing.

---

# Stage 4 — integration

**Build every surface from the content and the icon, then measure each one.**

Stage 4 is the first point at which content and icon both exist, which is what
makes it an integration stage in the ordinary sense. It is not a review. It
produces the files that ship and proves the contract held.

## Contract

**Requires:** `topic.json` complete; the icon present at
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
where overflow is hidden; the declared fold counts exactly match what is above
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
stage 4 to have passed, so unlike v1's gate it needs no check lines and no
shell. It reads.

Its justification is the exception in §9: every other stage reads a slice, and
this is the only reader that sees the whole. Tone drift across sections, the
same argument made twice by two camps, a crux that does not follow from the
questions above it, the icon working alone but not composed with copy on a
card — none of those are visible to any slice-reader, at any strength of exit
criteria.

## Contract

**Requires:** stage 4 passed.

**Produces:** a determination, and at most three notes.

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

**Structure and flow.** Does the condensed layer stand alone or only make sense
once expanded. Does Go-deeper add or restate. Does the crux follow from the
questions. Does reading order work on mobile, where the layout differs.

**Consistency.** Do two positions argue the same thing. Does a figure in Basics
sit oddly beside a claim in a position. Does a card promise what the page does
not. Is one camp written with more energy than another.

**Plausibility, not verification.** Does this hold together. No sources, no
fact-checking, no web — that was stage 1's, and re-doing it here is the
duplicated judgment the pipeline caps.

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

Capped at three. Brief only means something if it is enforced, and a cap forces
ranking instead of listing.

---

## Open questions

- The per-field ownership and locking table (§8).
- Concurrency: parallel units against one file, and against a burn rate that is
  only sampled once per call.
- Where stage 5's determination and notes are recorded — `evidence.json`,
  `review.md`, or both.
- Where the rules live and how a stage's prompt is assembled. v1 scattered this
  across agent definitions, inline strings and the manual, and grew a hook to
  check for drift. One home, decided once.
- Deliberate re-runs over a finished topic. The satisfied-when check handles the
  accident; deliberate regeneration is what killed refresh.
