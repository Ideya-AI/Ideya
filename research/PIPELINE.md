# The authoring pipeline — v2

What it is, how it runs, and the rules every stage is built against. Started
2026-09-11 after v1 was archived to `research/v1/`. Stages 1, 2, 3 and 5 are not
designed yet; stage 4 is, and is written up below.

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

---

# Stage 4 — integration

**Build every surface from the content and the icon, then measure each one.**

Stage 4 is the first point at which content and icon both exist, which is what
makes it an integration stage in the ordinary sense. It is not a review. It
produces the files that ship and proves the contract held.

## What it produces

| Output | Where |
|---|---|
| og card | `static/img/social/<slug>.png` — the file `og:image` actually serves |
| square, portrait cards | the packet, for manual posting |
| poster PDF | print-ready 18×24in |

Plus a pass, or a list of measured failures.

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

## Open questions

- The per-field ownership and locking table (§8).
- Failure semantics: does a stage that cannot satisfy itself halt the run, or
  mark itself blocked while other eligible work proceeds? The independence in §5
  points at the second.
- Concurrency: parallel units against one file, and against a burn rate that is
  only sampled once per call.
- Where the rules live and how a stage's prompt is assembled. v1 scattered this
  across agent definitions, inline strings and the manual, and grew a hook to
  check for drift. One home, decided once.
- Deliberate re-runs over a finished topic. The satisfied-when check handles the
  accident; deliberate regeneration is what killed refresh.
