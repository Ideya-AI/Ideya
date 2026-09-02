# Refresh — the upkeep engine

**This file is the refresh engine's operator's manual.** It is separate from
`research/ENGINE.md` (authoring) because the two run on different clocks:
authoring is under active development and runs often; refresh runs a few times a
year and should sit still between times. Splitting them means weeks of authoring
work never touch this file, and a frozen refresh stays legible instead of
drifting inside a document being edited around it.

What that separation costs, and how it is paid: **run
`research/workflows/check_refresh_drift.py` before any refresh** (step 0 below).
It reports what refresh has fallen behind on — shared editorial rules, the
stage-2 `fix_only` seam, its own locks, the model fields it writes. It is
deliberately NOT in the authoring test path: a refresh that is a few weeks behind
must not block work on the system it is behind.

- **Authoring a new topic** → `research/ENGINE.md` §5.
- **Why the engine is shaped this way** → `research/RESEARCH_PIPELINE.md`.
- **The invariants** (publish rule, plain-text fields, fact locking) → project
  `CLAUDE.md`.

---

## The runbook

Upkeep mirror. A refresh answers three questions, in this order, and the engine
is shaped around them:

1. **Is there new information to incorporate?** → the scout (stage 2)
2. **What needs updating, refining, or deprecating?** → the scan + targeted
   re-verify (stages 1 and 3)
3. **Is the topic still accurate, fair, and intellectually honest?** → the
   deterministic floor, one grounded critic, and the reader (stages 4–5)

**A refresh corrects what moved. It never re-authors.** That is enforced in code,
not asked for in a prompt — see "The three locks" below, and the failure that
earned them. Automation may OPEN a proposal; a human approves every content
change.

### 0 · Drift check — is refresh level with the engine?
```
.venv/bin/python research/workflows/check_refresh_drift.py
```
Non-optional, and it is the price of keeping the two systems apart. Anything it
reports as BEHIND gets caught up in `refresh_topic.js` before the run, because a
refresh that writes to an older editorial bar puts the corpus out of register
with itself and the human gate cannot see it.

### 1 · Scan — take stock for free
```
manage.py refresh_scan --slug <slug>            # read it
manage.py refresh_scan --slug <slug> --json     # feed it to the run
```
Four signals and a work order: the volatility clock, `check_links` on every URL,
`lint_draft` on the topic JSON (plus a JSON-vs-DB drift warning), and every
stat's `source_accessed` age against a floor of **2× the review interval**.
Costs nothing and scopes everything downstream.

Run `manage.py export_topic --slug <slug> --out research/topics/<slug>.json`
first if the scan reports drift — admin edits do not reach the JSON on their own.

Then read what readers did: `/participation-review <slug>` (or the latest
`research/refresh/<slug>.PARTICIPATION.*.md` if it is recent). Its part 3,
once the human has ticked the decisions, goes into the run as `args.findings`
alongside any editor findings — proposals, not instructions: the locks below
still decide what a refresh may change. Manual: `research/PARTICIPATION.md`.

**Light path.** `deterministic_verdict: "clean"` and a scout that finds nothing
material is a complete refresh: stamp `reviewed_at` and stop. "Checked, nothing
changed" is the expected outcome on most runs, and forcing a load to show effort
is how a topic gets worse.

### 2 · Scout — what has moved (Q1)
`refresh_topic.js` opens with one cheap web agent that sees the topic's **shape**
(summary, question texts, position names, stat labels) and the date of the last
review, and answers: what has materially changed in this debate since then, and
**what here has been overtaken and should be cut?** Nothing else in the run asks
the deprecation question, and no section-scoped agent can — a real development
lands in `why_now` and a stat and a position at once, and five section agents
each see a fragment of it.

Its output plus the scan's work order becomes the run's **work order**, and every
id on it (`w1`, `d3`, `editor`) is a warrant an edit must cite.

### 3 · Re-verify — only what was flagged (Q2)
One agent per section **that has work**; a section nothing flagged gets no agent
and is reported as not-checked rather than padded with re-confirmations. Each
returns a PATCH, never a section.

Bake the export in as `args.current` and the scan as `args.scan` (the `__ARGS`
recipe, ENGINE.md §10), plus `args.today` and `args.findings` for anything the editor wants
verified this run. Grunt research on cheaper models; judgment on the strong model
(`args.models` / `args.efforts`).

Confirmations stamp `source_accessed`, and so does any edit to an item that
carries it. That stamp is the only thing that lets the next scan skip an item, so
a run that verifies without dating leaves the next one just as blind.

#### The three locks
Each is independent, and all three are code:

| Lock | What it stops | Where |
|---|---|---|
| **Whitelist** | `viz`, `wide`, `tier`, `reveal`, `prevalence_weight`, and every identifier (`name`, `text`, `label`, `title`) are not writable. Shape is stage 2's budget; identity is what reader votes re-attach by. | `LOCKED` / `sanitizeEdits` |
| **Grounding** | An edit whose `because` is not on the work order is dropped. A refresh corrects what was asked about; it does not improve prose it wandered into. | `validReasons` / `sanitizeEdits` |
| **Regression** | Any item that comes back with a dropped field, fewer series rows, a removed source or date, a backwards `source_accessed`, or prose cut by more than a quarter is **restored whole** from the live topic. An unsourced removal is refused outright. | `regressionCheck` / `applyReverts` |

Everything the locks refuse lands in the proposal's `refused` array and in the
changelog as `refused` / `reverted` rows. **Read those first** — they are the
only evidence the locks held.

> **Why this exists.** Nuclear Energy was refreshed twice and lost work both
> times: 12 stats to 8 on 2026-07-03 with two rich visualizations flattened to
> bars, then rich viz 5 to 1 on 2026-07-08 — the second run with
> *"PRESERVE the topic's existing stats"* and *"never flatten a ranked or range
> viz to a bar"* already in its prompt. The richness on the live page today is
> there because a human rebuilt it by hand. The root cause was the output shape:
> an agent asked to re-emit a section emits **its** section, and dropping,
> flattening and re-prosing are what regeneration is. Patch-only output plus the
> three locks close it; `RefreshCannotRewriteTests` pins all of it, and both
> historical runs replay clean against the current layer.

### 4 · Gate — the floor and one grounded critic (Q3, part 1)
Inside the script: typography autofix on what the run wrote, a deterministic
check (plain text, register, `lead_highlight` verbatim, placeholder URLs) rebuilt
from the current draft every round, and **one** fact-source critic that reads the
**diff**, not the draft. The judgment dimensions moved to the reader in step 7.5 —
they need the whole topic, which no critic in the script ever sees.

Fix loop: one round, a second only for externally-grounded findings, keep-best
with a blocking-count tie-break. The fixer runs under the same locks.

### 5 · Propose — the human gate
Persist `research/refresh/<slug>.refresh-proposal.<YYYY-MM-DD>.json` and snapshot
the pre-refresh export beside it. **No DB writes yet.** The proposal carries
`{draft, changelog, verdicts, unverified, not_flagged, developments,
scout_assessment, refused, shipped}`. `shipped: false` means the run produced no
surviving change — a legitimate and common result.

### 6 · Re-lint and re-fold — the JSON work
```
lint_draft.py research/topics/<slug>.json --fix     # then --json for the rest
# route what is left, plus any view findings, through stage 2:
#   re-run distribute_topic.js with args.fix_only = [<findings>]
```
Run the `fix_only` pass when the refresh rewrote prose or changed an item count.
Stage 2 owns the budgets, the two-register check, claim fidelity, and the fold,
and **refresh never moves the fold itself** — its `reorder` is dropped and `tier`
is locked, so an added or removed item leaves the fold where the old item count
put it. Skip this step only for a run that changed no prose.

This is JSON work and it has to happen BEFORE the load: everything after this
point reads a loaded topic.

> `claim_ledger` is absent from every topic authored before 2026-08-28, which is
> all three published ones. Stage 2's fidelity check reports itself **not run**
> there rather than passing — expect that and do not read it as a pass. Refresh
> emits a ledger for the claims it touches, so coverage grows one refresh at a
> time.

### 7 · Apply — staged load
Commit the step-1 export FIRST ("checkpoint: live state") so the final diff is
exactly this refresh. Write the merged content to `research/topics/<slug>.json`
in loader shape, including the workflow's `changelog` array as a top-level key
(the loader ignores it; it is the refresh's durable provenance).

Load to a **staging slug** so the live topic stays online:
```
manage.py load_topic_draft --file research/topics/<slug>.json \
  --slug <slug>-draft --title '<Title>' --category <cat> --status draft
```
Why: the loader upserts by slug and rebuilds sections atomically — loading onto
the live slug with `--status draft` would flip the published topic to draft
(offline) and destroy the version you wanted to diff against. For an unpublished
topic, load straight onto the real slug.

### 7.5 · Read — is it still honest? (Q3, part 2)
The PM gate, in its refresh form — numbered 7.5 for the same reason authoring's
is stage 4.5: it is the one pass that reads the finished thing whole, after the
pieces are assembled and before a human spends time on it.
Now that the topic is loaded, render it — **only if the item count or the fold
moved** (`render_screens --base-url …`, desktop + mobile-320; a run that changed
no shape has nothing new to look at) — and spawn `topic-pm` on the result.

Its fourth question in a refresh is the one no critic in the script can ask,
because none of them sees the topic whole: **did this lose anything the authored
version had?** — judged against the pre-refresh snapshot from step 5. Its packet
goes to `research/refresh/<slug>.REVIEW.<date>.md`.

### 8 · Review & publish
1. **Compare** staging vs live as staff.
2. **Publish** onto the canonical slug (atomic in-place rebuild; participation
   re-attaches by exact question text / position name, with a warning for dropped
   rows), then delete staging:
   ```
   manage.py load_topic_draft --file research/topics/<slug>.json \
     --slug <slug> --title '<Title>' --category <cat> --status published --reviewed
   manage.py shell -c "from topics.models import Topic; \
     Topic.objects.filter(slug='<slug>-draft').delete()"
   ```
   Or for light changes: Django admin (`TopicAdmin` → Publish action — sets
   status only, still set `reviewed_at` yourself).
3. **`reviewed_at`** is stamped by `--reviewed` in the same transaction (the
   loader sets `researched_at`, the machine's clock; `reviewed_at` records human
   approval and resets the cadence). Doing it afterwards was a separate
   `shell -c` that is easy to forget, and forgetting it is silent: `topics_due`
   just re-queues the topic early.
4. **`check_links --topic <slug>`** — 0 dead / 0 placeholder. Non-optional; a
   piecemeal admin apply is exactly how the 2026-07-03 nuclear refresh shipped
   `#` placeholders live.
5. **Commit** the JSON — the diff is the content history.
6. **Push to live** per `DEPLOY.md` §3 (`docker exec` loader + `load_universe` +
   `rebuild_search` + `reviewed_at` inside the container).

### Account the refresh
Same rule as authoring: tally the refresh workflow's run
(`tally_tokens.py refresh=wf_<id> > research/refresh/<slug>.tokens.<date>.md`)
and commit it beside the proposal. No refresh has ever written this file; the
rule is not new, the compliance is.

### Cost shape
A refresh is scoped, so its bill is proportional to what moved: 1 scout + one
agent per flagged section (0–5) + 1 diff-scoped critic + at most 1 fixer —
**typically 4–8 calls, mostly sonnet**, against the old fixed 10–22 with four
opus critics re-reading the whole draft every round. The gate phase is ~85% of a
run's cache reads (ENGINE.md §9), which is why the panel is one critic reading a diff.

### Cadence
Links: continuous (weekly scheduled sweep + on change). Full re-research: event-
driven first (a position obsolesced, a key fact moved a lot), volatility cadence
as the backstop, occasional light review for fast movers (AI). The gate never
moves: scheduled runs stop at the proposal. Display concerns are out of scope
(`topics_due` measures content/link freshness only).

**Lint debt is not refresh's job.** The topics authored before the current lint
rules carry real findings (nuclear-energy: 33). The scan reports the number; the
burn-down is separate one-time work. Mixing "fix 2026-era prose rules" into "the
world moved" makes the human's diff unreadable.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Published topic went offline during refresh | loaded onto the live slug with `--status draft` | always stage at `<slug>-draft`; publish by re-running onto the canonical slug |
| A `research/topics/*.json` key vanishes after a refresh | `export_topic` writes only `draft` + `verdicts`; step 1 exports onto the same path step 7 wrote | fixed 2026-08-27 — the export now carries forward every top-level key it does not itself produce (`changelog`, `plan_positions`) and names them in its output line |
| A refresh returns fewer stats, a flattened viz, or thinner prose | an agent was asked to re-emit a whole section, so it emitted ITS section | fixed 2026-09-01 — re-verify is patch-only behind three locks (whitelist / grounding / regression gate). If it reappears, check `refused` and `reverted` in the proposal FIRST: a lock that fired is working, a lock that did not is the bug. `RefreshCannotRewriteTests` pins the shape |
| A refresh's changelog is padded with re-confirmations, or claims a change that did not happen | the changelog was self-reported alongside the draft, and a reverted item kept its `updated` row | fixed 2026-09-01 — rows are derived from what applied; no-op edits are discarded and a revert scrubs the rows it undoes |
| Every scan re-flags the same stats as undated | a `verified_current` verdict wrote no date | fixed 2026-09-01 — confirmations AND edits stamp `source_accessed`. nuclear-energy carried 5 of 12 undated stats through two refreshes this way |
| A refresh's second fix round never runs, even on fact findings | the grounded-round test read `v.key`, which the critic verdicts never carried | fixed 2026-09-01 — `key` is attached in `runGate` |

Engine-wide failure modes (renders, resume, classifier limits, the loader) are
in `research/ENGINE.md` §11.
