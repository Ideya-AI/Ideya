# The Ideya authoring engine — operator's manual

**This file is the single source of truth for operating the engine**: its structure,
order of operations, runbooks, routing, contracts, and failure modes. The rule that
keeps it true: **any commit that changes the engine updates this manual in the same
commit** — and `research/workflows/check_engine.py` verifies the machine-checkable
parts (inventory paths exist, the routing table matches the scripts' actual
constants), wired to run automatically after engine-file edits.

Which doc do I want?
- **Operate the engine** (run, resume, calibrate, debug) → this file.
- **Understand or change the design** (why the gates are shaped this way, decision
  history) → `research/RESEARCH_PIPELINE.md`.
- **The invariants** (publish rule, plain-text fields, fact locking…) →
  project `CLAUDE.md`. It is auto-loaded into every session and enforced by hooks;
  this manual references it rather than restating it.
- **Design system** (tokens, type, color discipline) → `design/`. **Icon spec** →
  `research/ICONOGRAPHY.md`.

The skills `/author-topic` and `/refresh-topic` are thin launchers into §5 (Runbook
A) and §6 (Runbook B) — the procedure lives here, once.

---

## 1. What the engine is

A staged pipeline that turns a catalog entry into a publish-ready topic draft
(authoring), and keeps published topics accurate as the world moves (refresh). AI
drafts; a human publishes — always. Each stage writes a durable artifact and is
independently re-runnable; a stage that already has its artifact is skipped unless
redone deliberately.

Iron rules (enforced, not advisory — see `CLAUDE.md` Invariants for the full list):
- **Automation drafts; a human publishes.** `--status published` from automation is
  blocked by `.claude/hooks/pipeline-guard.sh`.
- **The pipeline never edits templates or CSS** — code defects go in the review
  packet.
- **An unverified claim may not be asserted** — cut, soften, or attribute in-voice;
  never "please verify this".
- **Facts are locked after stage 1** — stage 2's patch whitelist rejects fact edits.
- Dev server on **8641, never 8642** (the live container; hook-blocked).

## 2. The map

```mermaid
flowchart TD
    C[research/catalog/topic-universe.json<br/>stage 0 · catalog entry] -->|research_topic.js| D[research/dossiers/slug.json<br/>stage 1 · substance dossier]
    D -->|distribute_topic.js + lint_draft.py| J[research/topics/slug.json<br/>stage 2 · loader contract]
    J -->|load_topic_draft| DB[(authoring DB · DRAFT)]
    D -->|icon brief + generate + postprocess| I[static/img/topics/slug.png<br/>stage 3 · primary icon]
    DB -->|render_screens / social / poster + view critics| R[research/reviews/slug/<br/>stage 4 · rendered views]
    R -->|topic-pm: verify, route back, write the packet| Q[REVIEW.md<br/>stage 4.5 · one-page packet]
    Q -.->|routed findings| DB
    Q -->|HUMAN reviews + publishes| P[stage 5 · published topic]
    P -->|DEPLOY.md §3 docker exec| L[(live container DB)]
    P -.->|export_topic re-syncs| J
    J -->|refresh_topic.js, upkeep mirror| J
```

## 3. Order of operations

| Stage | Engine piece | Does | Gate | Artifact |
|---|---|---|---|---|
| 0 Catalog | hand-authored entry + `load_universe` | register the topic stub + taxonomy edges | — | entry in `research/catalog/topic-universe.json` |
| 1 Research | `research/workflows/research_topic.js` | plan (+icon, prevalence_basis) → parallel section research (basics facts→shape + questions + one agent per position + actions) → crux → **claim ledger + isolated per-claim verification** → 3-critic substance gate → fix loop → verbatim prescribed-fix pass | substance gate 3/3, shape_notes empty, ledger closed | `research/dossiers/<slug>.json` |
| 2 Distribute | `research/workflows/distribute_topic.js` + `lint_draft.py` | distill compact layer → tier/reveal/fold → reorder → 2-critic presentation gate → whitelisted fix loop | gate 2/2 + lint at 0 findings + loader loads with 0 warnings | `research/topics/<slug>.json` |
| 3 Iconography | brief agent + `research/icons/generate_icons.py` + `postprocess_icon.py` | brief → 4 Nano Banana candidates → pick vs checklist → normalize | checklist pass at 40px | `static/img/topics/<slug>.png` + `research/icons/<slug>.md` |
| 4 Views | `render_screens/social/poster` + view critics | render all surfaces → critique → content-fix loop (`fix_only`) | poster fit exit 0 + all 3 social formats + no blocking content findings | `research/reviews/<slug>/` + `REVIEW.md` |
| 4.5 PM gate | `.claude/agents/topic-pm.md` | fresh-context read of the FINISHED topic: deterministic pass (lint/links/artifacts) → reads every render → routes findings to the owning stage → writes the packet | every deterministic check green + no open routed finding | `research/reviews/<slug>/REVIEW.md` |
| 5 Publish | **human** | review packet → publish → live push | human judgment | live topic |

Refresh (`refresh_topic.js`) is the upkeep mirror: detect → re-verify everything →
cited old→new changelog → **human approves the diff** → staged load → publish.
§Runbook B.

## 4. Parts inventory

<!-- inventory:begin — check_engine.py verifies each backticked path exists -->
| Piece | Role |
|---|---|
| `research/workflows/research_topic.js` | stage 1: substance research + claim ledger + substance gate |
| `research/workflows/distribute_topic.js` | stage 2: presentation distill/fold + gate; also `fix_only` view-feedback passes |
| `research/workflows/refresh_topic.js` | upkeep mirror: re-verify + changelog + gate, stops at the human |
| `research/workflows/lint_draft.py` | deterministic lint of a draft JSON; `--fix` applies safe rewrites |
| `research/workflows/seed_defects.py` | gate calibration: inject known defects, score detection |
| `research/workflows/tally_tokens.py` | per-run token/cost accounting |
| `research/workflows/check_engine.py` | verifies this manual against the code (routing + inventory) |
| `topics/tests/test_workflow_mirrors.py` | guard on the hand-mirrored workflow contracts (run after ANY workflow-script edit: `manage.py test topics.tests.test_workflow_mirrors`) |
| `.claude/agents/claim-verifier.md` | stage-1 ledger verifier: `tools: WebFetch, WebSearch` only — the blindness is structural, not a prompt |
| `.claude/agents/topic-pm.md` | stage-4.5 PM gate: verifies the finished topic, routes findings, writes the packet. Fable (allowlisted), falls back to opus |
| `.claude/skills/author-topic/SKILL.md` | launcher for Runbook A (user-invoked only) |
| `.claude/skills/refresh-topic/SKILL.md` | launcher for Runbook B (user-invoked only) |
| `.claude/hooks/pipeline-guard.sh` | blocks automated publishing + dev-server-on-8642 |
| `.claude/hooks/engine-doc-guard.sh` | runs check_engine.py after engine-file edits |
| `topics/management/commands/load_topic_draft.py` | the loader: JSON → DB topic; wires catalog edges; idempotent |
| `topics/management/commands/load_universe.py` | catalog → DB stubs + taxonomy + all related edges |
| `topics/management/commands/export_topic.py` | DB → canonical JSON re-sync |
| `topics/management/commands/check_links.py` | dead/placeholder/redirect audit (stat sources + action URLs + series rows) |
| `topics/management/commands/topics_due.py` | refresh queue by volatility cadence |
| `topics/management/commands/render_screens.py` | full-height page renders (1440/390/320, `--expanded`) |
| `topics/management/commands/render_social.py` | OG / square / portrait share cards |
| `topics/management/commands/render_poster.py` | print one-sheet; fit-check exit code is a hard gate |
| `research/icons/generate_icons.py` | Nano Banana candidate generation (`--edit` refines) |
| `research/icons/postprocess_icon.py` | winner → 1035×690 white-ground PNG + 40px thumb |
| `research/catalog/topic-universe.json` | stage 0: taxonomy + draft universe (edges' source of truth) |
| `research/dossiers/` | stage-1 substance records |
| `research/topics/` | canonical per-topic JSON (the loader contract) |
| `research/reviews/` | per-topic human review packets |
| `research/reviews/UI_DEFECTS.md` | standing site-wide UI-defect register (critics consult; human burns down) |
| `research/refresh/` | refresh proposals + pre-refresh snapshots (`<slug>.refresh-proposal.<date>.json`) |
| `research/icons/` | briefs, exemplars, candidates |
| `research/RESEARCH_PIPELINE.md` | design rationale + decision history (the "why") |
| `research/ICONOGRAPHY.md` | icon visual spec |
| `design/` | locked design system (authoritative over any prompt) |
<!-- inventory:end -->

## 5. Runbook A — author a topic

One run = one topic through stages 0–4, then the stage-5 human hard stop. Run from
the repo root; always `.venv/bin/python`. Category slugs: `global-risk · ai ·
digital · climate-env · bio-health · economy · governance · society · ethics`.

> **Dual-use note.** Some catalog topics (engineered pathogens and similar) are
> blocked by content policy — stage-1 research agents error out. Author those via an
> external-research path onto the same `research/topics/<slug>.json` contract
> ("path B") and resume at stage 3.

### Stage 0 — catalog entry (only if not yet cataloged)

Author an entry in `research/catalog/topic-universe.json` matching the existing
shape: `{title, slug, summary, why_now, primary_category_slug,
secondary_category_slugs, suggested_icon, position_names, related_slugs}`.
`related_slugs` is this topic's **best 3–5 related topics, from its own
perspective** — the site shows **outgoing** edges only, and asymmetry is deliberate
(decided 2026-08-26): a niche topic may point at a hub without being one of the
hub's own best five, so never force reciprocity. When adding a new entry, also
review 1–2 neighboring entries and add this slug there only where it genuinely
belongs in *their* best 3–5. Then `manage.py load_universe` (idempotent) registers
the stub; it warns on any `related_slugs` entry that matches no topic (a renamed
slug once left a dangling reference that silently created no edge).

### Stage 1 — research (substance)

Pull the catalog entry and run `research_topic.js` via the Workflow tool with inline
args `{title, slug, summary, why_now, category, suggested_icon, positionNames,
questionsSeed:[], today:"YYYY-MM-DD"}` (map `primary_category_slug`→`category`,
`position_names`→`positionNames`). Stage-1 args are small — no baking needed.

Persist the return (`{draft, plan, verdicts, shape_notes, plan_positions,
claim_ledger}`) to `research/dossiers/<slug>.json` wrapped as `{dossier_version:1,
generated, slug, input, ...}`. Check: gate 3/3, `shape_notes` empty. Verdicts carry
`checks_run`; a check with `ran=false` fails its critic and re-runs once — a clean
gate means the checks actually happened.

**Basics is researched in two calls** — the facts (label/value/unit/note/detail/
tier/source_*), then the chart shape for those same facts (viz/wide/series/
range_*/fill_pct) — merged locally by exact label. A shape that arrives without
its data (ranked with no rows, range with no endpoints) is demoted to `bar` in
code, and an unmatched label defaults to `bar`; both are logged, never silent.
*Why:* one whole-section schema carrying both halves serialized to ~4.5KB and
the safety classifier refused it twice in `[basics]` on a large topic
("output schema too large to classify safely"). **Operating budget: keep any one
output schema under ~3KB.** Every schema in the engine now sits under that except
`refresh_topic.js`'s `reverify(BASICS_SCHEMA)` (~4.7KB) — the same trap, unsprung
so far because refresh edits an existing Basics rather than researching one.

The plan emits the Phosphor `icon` and, per position, `prevalence_weight` **with a
one-line `prevalence_basis`** (the evidence behind the weight — capture only, no
critic judges it yet; the dossier records it so the weight is checkable).

**The claim ledger** (between crux and gate): an extraction agent enumerates every
load-bearing claim — figures, dates, statute/EO names, "X did Y" — sweeping
position/question prose as hard as stats, because only stats carry `source_*` fields
and unsourced prose is where wrong claims hide behind a clean gate. Verifiers check
each claim in parallel seeing **only the claim + cited URL, never the draft** (a
draft primes rationalization). That blindness is **structural**: they run as the
custom `claim-verifier` agent (`.claude/agents/claim-verifier.md`), whose
`tools: WebFetch, WebSearch` frontmatter leaves them no way to open the draft or
the dossier — until 2026-08-27 they were general-purpose agents that inherited
`Read` and were merely *asked* not to look. A missing `source_quote` forces
`unverifiable` in code, and a claim that comes back with **no verdict at all** is
filed as blocking — an empty results array has no failures in it, so a
verification batch that died would otherwise report a clean ledger. `contradicted`/`unverifiable` are blocking; failing claims re-verify each fix
round **and are first checked against the revised draft**: a claim whose verbatim
`quote` no longer appears in the draft is marked `resolved-by-revision` in code
and stops blocking, because a claim the draft no longer asserts is not a live
defect. Without that, a landed fix kept scoring blocking for the rest of the run
(ai-alignment, 2026-08-27: 5 of 6 "blocking" ledger items were stale). Report
ledger coverage (supported/total, plus resolved-by-revision) in the packet — it
replaces asserting that facts were checked.

**Prescribed fixes are applied in code once the fix loop is spent.** A blocking
finding that quotes BOTH the target and its replacement ("replace “X” with “Y”")
is a repair the critic already wrote; after the loop, any such prescription whose
target still appears verbatim in the draft is applied as a literal string swap and
the finding is retired. Deliberately narrow — a fix that quotes only its
replacement leaves the target ambiguous and is left alone. Applied swaps are
recorded in the dossier's `prescribed_fixes` (no fixer agent authored them, so the
packet says so). *Why:* the loop is capped and judgment findings get one round,
so a prescription could expire unapplied and reach the human as a blocking defect
with its own fix printed beside it — democratic-backsliding, then ai-alignment.

**Fact residuals are the pipeline's to close, never the human's.** Stage 1's
`applyPatch` has no field whitelist, so fact fields are fixable here. Re-run the
fact critic or apply its prescribed resolution (cut / soften / attribute in-voice).

**Nothing escalates mid-run (Jeff, 2026-08-27) — the engine decides editorial
forks itself**, by its own rules: a verified genuine missing camp is ADDED
(omission is a neutrality failure); when a critic offers alternatives, take its
primary prescription. Every such decision is flagged in the packet's "Check in 5
minutes" for the stage-5 human, who can override before publishing. The run never
stops to ask.

### Stage 2 — distribute (presentation)

Run `distribute_topic.js` with `{slug, title, today, dossier:<stage-1 return>}`.
The dossier is 60KB+ — bake it in via the `__ARGS` recipe (§10). Distill → tier
(the "Go deeper" fold) → reveal → reorder (most decision-relevant first) → 2-critic
gate (compact-self-sufficiency incl. above-fold selection; reading-level fit).
**Display order = array order; `tier` marks the drop-off — move an item across the
fold by REORDERING. Positions are the exception: they render by `prevalence_weight`
(locked); steer their fold with `tier`.** Facts are whitelist-locked here.

Persist the return as `research/topics/<slug>.json` (`{draft, verdicts,
plan_positions}`; verdicts stage-tagged). Before persisting, write
`draft.categories = [primary_category_slug, ...secondary_category_slugs]` from the
catalog — the workflows don't emit it and the loader would drop secondaries.

Then, in order:
1. `lint_draft.py research/topics/<slug>.json --fix` — drive to **0 findings**
   (exits 1 while judgment findings remain; it catches what eyeballing misses).
2. Load and confirm zero loader warnings:
   `manage.py load_topic_draft --file research/topics/<slug>.json --slug <slug>
   --title "<Title>" --category <cat> --status draft`
   (no `--image-brief` yet — the brief doesn't exist until stage 3 and the loader
   hard-errors on a missing path). Use the real slug for a new topic; use
   `<slug>-draft` only when a published version must stay online. The loader wires
   this slug's related-topic edges from the catalog automatically (idempotent, both
   directions).

### Stage 3 — iconography

Loop, capped at ~3 refine rounds (spec: `research/ICONOGRAPHY.md`):
1. An `opus` sub-agent writes `research/icons/<slug>.md` from the spec +
   `research/icons/categories.md` + existing briefs as exemplars (match their
   headings; the `## Generation prompt` blockquote is what the generator reads).
2. `python research/icons/generate_icons.py --slug <slug> --n 4` → candidates in
   `research/icons/candidates/<slug>/`.
3. **Read** the candidates; score against the checklist (uniform monoline stroke,
   same-hue ~16–18% duotone fill on EVERY major element — outline-only linework
   vanishes at 40px, category color, 2.5–3.5× scene complexity, white ground, no
   text/frame, 40px legibility). Judge family fit too: view the strongest
   candidate next to 2–3 existing winners in `static/img/topics/` — 38 tiles will
   sit on one wall, and per-icon quality does not guarantee the set reads as one
   hand. None pass → refine the prompt or `--edit <candidate> --edit-prompt
   "..."`. One passes → append a `## Selection` note to the brief.
4. `python research/icons/postprocess_icon.py --slug <slug> --src <winner.jpg>` →
   `static/img/topics/<slug>.png` (1035×690) + 40px thumb; Read the thumb to
   confirm legibility. Keep all candidates for human swaps.

### Stage 4 — views

Dev server up (`DJANGO_DEBUG=true … runserver 8641 --noreload`; **restart after any
template edit** — the compiled-template cache silently serves stale renders).
Render + critique, capped at ~3 rounds:
1. `render_screens --slug <slug> --base-url <dev>` plus an `--expanded` run
   (`?expanded=1` forces every Go-deeper extra visible — the depth layers get no
   coverage otherwise); then social in **two** calls, and
   `render_poster --slug <slug> --base-url <dev> --out research/reviews/<slug>`.
   `--base-url` is required on all three.

   ```
   render_social --slug <slug> --formats og      --base-url <dev>          # NO --out
   render_social --slug <slug> --formats sq,pt   --base-url <dev> --out research/reviews/<slug>
   ```

   **The `og` call takes no `--out` on purpose.** Its default is
   `static/img/social/<slug>.png`, which is the file `Topic.social_card` and the
   page's `og:image` actually serve; a copy in the review folder is a review
   artifact and reaches no reader. Redirecting all three formats there — as this
   runbook did until 2026-08-27 — ships every topic with the generic site image
   for link previews and shares. The three published topics have real cards only
   because someone installed them by hand. `sq`/`pt` are for manual posting and
   belong in the packet. The stage-4.5 PM checks for the installed file.
2. `opus` sub-agents **Read** every image against `design/DESIGN_SYSTEM.md` +
   `design/RESPONSIVE.md`, **with `research/reviews/UI_DEFECTS.md` in hand**.
   Findings split:
   - **content-fixable** (overlong text, bad fold, poster overflow) → re-run
     `distribute_topic.js` with `args.fix_only:[findings]` (runs only the
     presentation fix loop) → reload → re-render.
   - **code/CSS defect** → check the register first: matches an OPEN entry →
     cite it, don't re-report; matches a FIXED entry → report as a REGRESSION;
     genuinely new and site-wide → log in `REVIEW.md` AND append to the
     register. Never edit templates/CSS.
3. Pass = poster fit exit 0 + all three social formats + **the og card installed at
   `static/img/social/<slug>.png`** + no blocking content findings.

Assemble `research/reviews/<slug>/REVIEW.md` from the template in §12.

### Stage 4.5 — the PM gate

The last engine step before the human. Invoke `topic-pm` (Agent tool,
`subagent_type: "topic-pm"`) with the slug, the title, the counts, the stage
verdicts and the ledger coverage. **Give it nothing from the dossier** — it judges
the finished artifact, not the research.

It is the only agent in the engine that sees the topic whole. Every other critic
reads one slice; a defect that only shows up when the page, the cards and the
poster are read together has, until now, had no reader but you.

Three properties make it a gate rather than a second opinion:

- **Fresh context.** It did not watch the run. An agent that watched the pipeline
  work is primed to accept its output — the same reason ledger verifiers are blind
  to the draft. This is why the PM must NOT also be the orchestrator: a context
  that ran the pipeline and then certifies it is marking its own homework.
- **Grounded findings only.** It may file what it can point at — a failed check, a
  missing artifact, text truncated mid-word, a card contradicting the page. Not
  "this could be sharper". Judgment findings are capped at one fix round for a
  reason (`RESEARCH_PIPELINE.md` §6); an unconstrained PM re-opens exactly that loop.
- **It routes, it does not repair.** Each finding names the owning stage. Its only
  repair is `lint_draft.py --fix`, which is deterministic and reversible.

Its deterministic pass is the checklist in the agent definition — lint at 0, links
0/0, the icon at 1035×690, **the OG card present at `static/img/social/<slug>.png`**
(not the review-folder copy), all three social formats, the poster, and all six
renders. Anything failing there is decidable and must never reach you.

Re-run the routed stages, then re-run the PM. Exit: every deterministic check
green and no open routed finding. It returns ROUTING plus the packet markdown; the
orchestrator writes `research/reviews/<slug>/REVIEW.md` (§12) — the PM has no Write
tool, so the artifact stays under the orchestrator's hand.

> **Honest limit:** the PM's blindness to the dossier is a prompt rule, not a tool
> restriction — it needs Bash for the deterministic pass, and Bash can read
> anything. Unlike `claim-verifier`, this one is convention.

### Stage 5 — human review & publish (the hard stop)

The human: preview the draft as staff → publish (`load_topic_draft … --status
published --image-brief research/icons/<slug>.md`) → set `reviewed_at = now()` →
`check_links --topic <slug>` (0 dead / 0 placeholder) → commit the dossier, topic
JSON, icon assets, and review packet. **Then push to live** — the live DB is
separate; follow "Publish one topic to the live site" in `DEPLOY.md` §3 (a
`docker exec` load against the live container — never copy the whole DB over it).

## 6. Runbook B — refresh a topic

Upkeep mirror: detect → re-verify → **cited diff for human approval** → staged load
→ publish. Automation may OPEN a proposal; a human approves every content change.

### 1 · Detect
- `manage.py topics_due` — queue by volatility cadence (fast 90 / medium 180 / slow
  365 days from `reviewed_at`, else `researched_at`; never-touched always due).
  Flags: `--all`, `--status published`, `--json`. Confirm the slug is actually due.
- `manage.py check_links --topic <slug>` — cheap, run first.
- `manage.py export_topic --slug <slug> --out research/topics/<slug>.json` —
  re-sync from the live DB (admin edits may have drifted); its `research_dossier`
  is the provenance you re-verify against.

**Light path (barely-stale):** cadence-due, clean links, no material event → skim
`why_now` + crux, spot-check the 2–3 most perishable stats, fix links via admin,
set `reviewed_at = now()`. "Checked, nothing changed" is a legitimate outcome —
record it by resetting `reviewed_at`, not by forcing a load.

### 2 · Research & verify
Run `refresh_topic.js`: re-verifies every element in parallel, re-checks the crux,
runs the severity gate + fix loop, returns `{draft, changelog, verdicts,
unverified}` in loader shape. Bake the stage-1 export in as `args.current` (the
`__ARGS` recipe, §10), plus `args.today`, `args.link_report`, and `args.findings`
for anything the editor wants verified this run. If `unverified` names sections,
say so in the proposal — those were NOT checked. Editorial bar: §10 "Editorial
rules". Grunt research on cheaper models; judgment on the strong model
(`args.models` / `args.efforts`).

### 3 · Propose — the human gate
A changelog the reviewer can act on, grouped by section: **old → new** with source
URL + date + confidence + the driving verdict. Call out anything unverifiable or
needing an editorial call. Persist it as
`research/refresh/<slug>.refresh-proposal.<YYYY-MM-DD>.json` (snapshot the
pre-refresh export beside it). No DB writes yet.

### 4 · Apply — staged load
On approval, write the merged content to `research/topics/<slug>.json` in loader
shape, including the workflow's `changelog` array as a top-level key (the loader
ignores it; it is the refresh's durable provenance). Commit the stage-1 export
FIRST ("checkpoint: live state") so the final diff is exactly this refresh.

Load to a **staging slug** so the live topic stays online:
```
manage.py load_topic_draft --file research/topics/<slug>.json \
  --slug <slug>-draft --title '<Title>' --category <cat> --status draft
```
Why: the loader upserts by slug and rebuilds sections atomically — loading onto the
live slug with `--status draft` would flip the published topic to draft (offline)
and destroy the version you wanted to diff against. For an unpublished topic, load
straight onto the real slug.

### 5 · Review & publish
1. **Compare** staging vs live as staff. If the changelog added/removed items or
   grew compact-layer text, run `distribute_topic.js` with `args.fix_only` first —
   refresh preserves tier/reveal but never re-balances the fold.
2. **Publish** onto the canonical slug (atomic in-place rebuild; participation
   re-attaches by exact question text / position name, with a warning for dropped
   rows), then delete staging:
   ```
   manage.py load_topic_draft --file research/topics/<slug>.json \
     --slug <slug> --title '<Title>' --category <cat> --status published
   manage.py shell -c "from topics.models import Topic; \
     Topic.objects.filter(slug='<slug>-draft').delete()"
   ```
   Or for light changes: Django admin (`TopicAdmin` → Publish action — sets status
   only, still set `reviewed_at` yourself).
3. **Set `reviewed_at`** (the loader sets `researched_at`, not `reviewed_at`;
   this records human approval and resets the cadence clock; internal only):
   ```
   manage.py shell -c "from django.utils import timezone; from topics.models import Topic; \
     Topic.objects.filter(slug='<slug>').update(reviewed_at=timezone.now())"
   ```
4. **`check_links --topic <slug>`** — 0 dead / 0 placeholder. Non-optional; a
   piecemeal admin apply is exactly how the 2026-07-03 nuclear refresh shipped `#`
   placeholders live.
5. **Commit** the JSON — the diff is the content history.
6. **Push to live** per `DEPLOY.md` §3 (`docker exec` loader + `load_universe` +
   `rebuild_search` + `reviewed_at` inside the container).

### Cadence
Links: continuous (weekly scheduled sweep + on change). Full re-research: event-
driven first (a position obsolesced, a key fact moved a lot), volatility cadence as
the backstop, occasional light review for fast movers (AI). The gate never moves:
scheduled runs stop at the proposal. Display concerns are out of scope
(`topics_due` measures content/link freshness only).

## 7. Runbook C — resume & recover

- **A workflow died or was checkpointed mid-run:** relaunch with
  `Workflow({scriptPath, resumeFromRunId})` and the SAME args — the unchanged
  prefix of agent calls returns cached. Inspect `journal.jsonl` in the transcript
  dir before assuming a cached result is non-empty.
- **A gate critic reported a check it could not run** (search pool spent): re-run
  that critic alone in a fresh workflow invocation — a new run gets a fresh pool.
  Verification should lean on WebFetch of primary sources anyway (separate,
  uncapped pool); search is for discovery.
- **A stage already has its artifact:** it is skipped on re-run; redo deliberately
  by regenerating the artifact.
- **Renders look stale after a template edit:** restart the dev server; the
  compiled-template cache does not invalidate under `--noreload`.

## 8. Runbook D — calibrate the gate

Clean gates are self-reported; a run of them is equally consistent with "good
drafts" and "agreeable judges". Inject known defects and count what comes back:
```
.venv/bin/python research/workflows/seed_defects.py \
  --src research/topics/<clean-topic>.json --out <scratch>/seeded.json
# run stage 1's gate against the seeded draft, save verdicts, then:
.venv/bin/python research/workflows/seed_defects.py \
  --score <scratch>/seeded.manifest.json <verdicts.json>
```
Seed from a topic that lints at 0 so every finding is attributable. Injection
targets are disjoint; classes span easy (`fact-wrong-10x`, `dead-link` — expect
~100%) to discriminating (`source-misattributed`, `unsupported-precision`). A class
at 0% is a blind spot to close with a rule, not a prompt nudge. Last calibration
(2026-08): 7/7 detected, plus real defects the gate had previously passed.

## 9. Cost, models, budgets

Judgment on **opus**, web grunt on **sonnet**, never below sonnet (defaults are
baked in the scripts — an `args.models` override alone does NOT reliably reach a
script).

**Fable: barred from the workflow scripts, allowed for the PM gate** (Jeff,
2026-08-27). The 2026-08-13 exhaustion came from putting Fable on the engine's
highest-call-count work — plan, crux, distribute and the stage-1 gate — not from
Fable being a poor fit. It is the most capable model and the most expensive
($10/$50 per MTok, twice opus), so the rule is about **call count, not tier**:
Fable is for high-level, low-call-count roles only. `topic-pm` is the only agent
allowlisted, and `topics/tests/test_workflow_mirrors.py` enforces both halves —
no `?? "fable"` in the scripts, and no un-allowlisted `.claude/agents/*.md` naming
Fable (the scripts-only check missed agent definitions entirely).

**Fable → opus fallback.** If Fable's weekly allowance is spent, re-invoke the PM
with `model: "opus"` and change nothing else: `topic-pm.md` declares
`model: fable`, and an explicit `model` on the Agent call overrides the
definition. The prompt is model-agnostic, so the fallback is a one-line retry, not
a reconfiguration — but it is a retry the orchestrator performs, not something the
platform does for you.

<!-- routing:begin — check_engine.py verifies this table against the scripts -->
| Script | Model defaults | Effort pins |
|---|---|---|
| `research_topic.js` | plan=opus research=sonnet crux=opus critique=opus fact=opus fix=opus | research=high critique=high fix=high |
| `distribute_topic.js` | distill=opus distribute=opus critique=opus fix=sonnet | distill=high critique=high fix=low |
| `refresh_topic.js` | research=sonnet distill=research critique=opus fact=opus crux=opus fix=opus | research=high critique=high fix=high |
<!-- routing:end -->

High-volume subtasks pin efforts instead of inheriting the session's (often max) —
the main overage lever. Judgment singletons (plan, crux, distribute) inherit.

- **Web-search pool**: `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` (default 200,
  raised to 1500 in `.claude/settings.json`), shared across the session and all
  subagents. WebFetch draws on a separate pool the search cap does not touch —
  verification leans on it; search is for discovery.
- **Accounting**: `research/workflows/tally_tokens.py` per run. Reference points:
  fable-era topic ~285k opus-equivalent output; first opus+sonnet-only run ~553k
  (inflated by a resumed double-gate + largest topic yet).
- **HARD STOP**: the moment any usage signal shows 90% of weekly limits — cease all
  runs and report.

## 10. Contracts & shapes

**Stage-1 dossier** `research/dossiers/<slug>.json`:
```
{ "dossier_version": 1, "generated": "YYYY-MM-DD", "slug": "...",
  "input": { "title": "...", "category": "..." },
  "draft": { overview, basics, questions, positions, crux, actions },
  "plan": { ...planner output incl. icon + positions (prevalence_basis lives here) },
  "verdicts": [ {critic, pass, blocking, notes, checks_run} ],
  "shape_notes": [], "plan_positions": [...],
  "claim_ledger": { claims, results },
  "prescribed_fixes": [ {critic, from, to, fields} ] }
```
A ledger `result.status` is `supported` | `contradicted` | `unverifiable` |
`resolved-by-revision` (the fix loop removed the sentence the claim was extracted
from, so it is closed rather than checked). A claim that got **no** result at all
is filed as blocking, never passed.
```
```
`draft` is substance-complete, presentation-provisional (stage 2 finalizes
tier/reveal).

**Loader contract** `research/topics/<slug>.json`: `{draft, verdicts,
plan_positions}` (bare `draft` also works; refresh adds a top-level `changelog`).
The loader stores verdicts opaquely on `Topic.research_dossier`; the additive
`stage:` tag is harmless everywhere. Per-item fields the loader actually maps:

```jsonc
{
  "draft": {
    "overview": { "summary", "scope_covered", "scope_excluded", "why_now" },
    "basics": {
      "intro": "lead-in copy",
      "stats": [{
        "label", "value",
        "unit",                                       // <= 24 chars, spelled out; leading space before word units; currency goes in value
        "viz": "bar|ranked|radial|range|sparkline",  // default bar
        "wide": true,                                 // ranked tiles span two columns
        "series": [{ "label", "value", "pct", "highlight", "source_label", "source_url" }],
        "range_min", "range_max", "range_at",         // range viz track + marker (0-100)
        "fill_pct",                                   // ONLY a true share of a whole the tile names; null otherwise
        "note",                                       // one tight sentence (visible layer)
        "detail",                                     // deeper analysis on tile expand
        "tier",                                       // 1 = leading; new tier at a natural drop-off
        "source_label", "source_url",
        "source_published",                           // when the data is from
        "source_accessed",                            // when you verified it (YYYY-MM-DD)
        "reveal": "condensed|normal|deep"
      }]
    },
    "questions": [{ "text", "kind": "empirical|value", "why", "detail",
      "lean_label_a", "lean_label_b", "lean_pct_a", "tier", "reveal" }],
    "positions": [{ "name", "steelman", "description", "detail", "tier",
      "proponents", "representative_name", "representative_note",
      "prevalence_weight", "spectrum_position" }],    // color auto-assigned by index
    "crux": { "lead", "lead_highlight", "subtitle", "empirical", "values" },
    "actions": [{ "kind": "learn_more|donate|volunteer|policy|local|submit_view",
      "title", "description", "url", "for_position", "tier", "reveal" }]
  },
  "verdicts": [{ "pass": true, "issues": ["..."], "fixes": ["..."] }],
  "plan_positions": []
}
```
A rich viz arriving without its data falls back to `bar` with a warning. The loader
(re)seeds the 3 Add-your-view prompts each load, warns on placeholder action URLs
and truncated stat units/notes, and wires this slug's related-topic edges from the
catalog.

> **Shape caveat:** `nuclear-energy.gold.json` is in **export shape** — the content
> quality bar, not loadable. Loadable-shape example:
> `nuclear-energy-pipeline.json`.

**Presentation-patch whitelist (stage 2).** Edits allowed only on `{tier, reveal,
wide, note, why, steelman, description, detail, intro, lead, subtitle, summary}` —
anything else (value/unit/source_*/url/kind/name/text/label) is rejected. `reorder`
takes a per-section full order of item ids (omitted items append). Stats/questions/
actions cross the fold by reorder; positions by `tier` (prevalence is locked).

**Fold reference** (must match `topics/models.py`): BASICS min/max 3/9 (3-col grid,
wide spans 2), QUESTIONS 3/6 (1-col), POSITIONS 2/6 (2-col). The workflows'
`foldPreview` reproduces `Section._tier_lead_count` exactly.

**Verdict contract:** each pipeline critic returns `{critic, pass, blocking, notes,
checks_run}`; `pass=false` only on a blocking defect ("parity with a strong
published topic, not perfection"); an unperformed check is filed as blocking, never
passed with a caveat. VERDICT_SCHEMA is hand-mirrored across the three scripts —
**change it in all three or the guard test fails** (`manage.py test
topics.tests.test_workflow_mirrors`; run it after any workflow-script edit). (The loader sample above shows
the older per-element `{pass, issues, fixes}` shape from manual refresh verdicts;
the loader stores either opaquely, so both round-trip.)

**The `__ARGS` recipe** (workflow scripts can't read files; 60KB+ args must be
baked into a run script):
```python
import json, re
dj = json.load(open("research/dossiers/<slug>.json"))
run_args = {"slug": "<slug>", "title": "<Title>", "today": "YYYY-MM-DD",
            "dossier": {"draft": dj["draft"], "verdicts": dj["verdicts"],
                        "plan_positions": dj["plan_positions"], "plan": dj["plan"]}}
body = open("research/workflows/distribute_topic.js").read()
runner = re.sub(r"\bargs\b", "__ARGS", body)                 # rewire the global
idx = runner.index("};\n") + 3                               # after meta
runner = runner[:idx] + "\nconst __ARGS = " + json.dumps(run_args) + ";\n" + runner[idx:]
open("<scratch>/run_distribute_<slug>.js", "w").write(runner)
```
Then `Workflow({scriptPath: "<scratch>/run_…js"})`. To syntax-check: strip the
leading `export` AND wrap the body in an **async** function (top-level `return`
won't parse bare; `export` won't parse inside a function; the scripts `await` at
top level, so a plain function won't parse either). For a view-feedback pass add
`"fix_only": [<findings>]` — skips distill/distribute, runs only the fix loop.

**Editorial rules** (the bar all content must meet; rationale in
`RESEARCH_PIPELINE.md` §8): neutral by intention; genuine steelman in each side's
own voice; honest non-balance (every genuine position, never forced 50/50, no
fringe-exclusion-by-omission); crux must narrow (no new facts, never "both sides
have a point"); every stat verified + sourced + dated (`source_published` +
`source_accessed`); recency pass on time-sensitive figures; durable by default
(isolate + date the perishable); source tiers (primary/peer-reviewed > journalism >
advocacy; the proponent is a position's source); depth = distill down (same
six-section skeleton at every depth; more room adds evidence, never sections).

## 11. Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Critic reports a check it couldn't run | shared search pool spent (the research fan-out runs first) | re-run that critic alone in a fresh workflow (fresh pool); lean on WebFetch |
| Render doesn't show your template edit | compiled-template cache + `--noreload` | restart the dev server — always, after any template edit |
| `args.models` override seems ignored | args don't reliably reach a script's `??` defaults | defaults are baked in the scripts; edit them there |
| Empty topic loaded, no error | fed an export-shape file (gold) to the loader | loader wants `{draft:{overview,…}}`; use a pipeline-emitted file |
| Published topic went offline during refresh | loaded onto the live slug with `--status draft` | always stage at `<slug>-draft`; publish by re-running onto the canonical slug |
| Poster stamp/fit silently wrong | render commands default to dead `localhost:8000` | `--base-url` is required on all three render commands |
| Fact errors surviving a clean 4/4 gate | wrong claims hide in unsourced position/question prose | the claim ledger exists for this; check its coverage number in the packet |
| Packet lists ledger defects the run already fixed | a failing claim was re-verified against its SOURCE each round but never against the REVISED draft | fixed 2026-08-27 — a claim whose verbatim quote is gone from the draft is `resolved-by-revision`; if stale items reappear, check that the fixer edited the quoted sentence rather than adding a second one |
| Workflow "could not be resumed" after session restart | background fork checkpoint | relaunch with `resumeFromRunId` + identical args; cached prefix returns |
| `render_screens` dies "within 200px of the capture window" | the page is taller than the capture height (long topics at 320px expanded) | raise `CAPTURE_HEIGHT_EXPANDED` in `render_screens.py` and re-capture — the hard error exists because a clipped capture handed to the view critics reads as a complete render (ai-alignment, 2026-08-27) |
| Stage-1 agents error out on a topic | dual-use content policy | path B: external research onto the loader contract, resume at stage 3 |
| `output schema too large to classify safely` | an output schema over ~3KB (worst with a long prompt) | split the call and merge locally, or move rich sub-objects to JSON-encoded strings (what stage 2's `add_*` does); stage 1's basics is split facts→shape for this reason |
| `agent type '<name>' not found` mid-run | the custom-agent registry picks up a new `.claude/agents/*.md` on a **lag**, not instantly | wait and retry before doing anything drastic — 2026-08-27: a just-written definition failed to resolve, and the same file resolved later in the same session with its tool restriction intact. Restarting the session also works but is rarely needed |
| Link previews show the generic Ideya mark | the og card was rendered into the review folder, not `static/img/social/` | stage 4 runs the `og` format with NO `--out`; the review-folder copy is not what `og:image` serves |
| Live site missing a just-published topic | authoring DB ≠ live DB | `DEPLOY.md` §3 docker-exec load; never copy the whole DB |

## 12. Appendix — REVIEW.md template

Written by the stage-4.5 PM, persisted by the orchestrator. **One page, hard.**
Links first — the point is one click to each view.

Nothing mechanical reaches this file. Facts, links, lint, missing artifacts and
truncation are closed inside the pipeline; if one shows up here, the gate leaked.
Engine-development narrative does not belong here either — that goes in
`RESEARCH_PIPELINE.md`. Packets drifted to 50–259 lines (mean ~94) by absorbing
calibration findings and engine notes, which is how a review packet becomes a
build log the human has to mine.

```
# <Title> — review packet (<date>)

**DRAFT `<slug>`** · <n> stats · <n> questions · <n> positions · <n> actions
Fold above "Go deeper": basics <n>/<N> · questions <n>/<N> · positions <n>/<N>

## Look
[page](http://localhost:8641/<slug>/) · [expanded](http://localhost:8641/<slug>/?expanded=1)
[1440](desktop-1440.png) · [390](mobile-390.png) · [320](mobile-320.png)
[OG](<slug>.png) · [square](<slug>-sq.png) · [portrait](<slug>-pt.png) · [poster](<slug>.pdf)
<the first two need the dev server up on 8641>

## Run
substance <n>/3 · presentation <n>/2 · ledger <supported>/<total> · lint 0 · links 0/0 · poster fits (<n>px)
Rounds: research <n> · distribute <n> · icon <n> · views <n> · PM <n> (<n> routed, all closed)

## Decided for you
<editorial forks the engine resolved by its own rules, one line each, naming the
 rule it applied. "None this run" is a valid and common answer.>

## Check in 5 minutes
<at most THREE, editorial only — a call you might make differently. Never a fact,
 never a mechanical defect. Empty is a good packet, not a suspicious one.>

## Engineering (the pipeline may not touch CSS)
<new site-wide defects, or "none — <n> open entries cited from UI_DEFECTS.md">

## Publish
Runbook A stage 5 — the loader invocation, then reviewed_at, then
check_links --topic <slug> (0/0), then commit, then DEPLOY.md §3.
```
