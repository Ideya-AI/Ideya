---
name: review-topic
description: Light, full-coverage review of ONE topic (draft or published) across content spot-checks, editorial/structure, and rendered views — then route fixes and feed generalizable lessons back into the authoring/refresh pipelines. Runs on simple models (sonnet); it is NOT a re-research pass. Use after authoring, after a refresh, or any time a topic deserves a look.
---

# review-topic

The standing in-between step of the project's core loop: **the human names the topic →
pipelines author/refresh it → this review inspects it → the human publishes.** It fully
inspects but stays light — the authoring pipeline already carries the research rigor and
its own adversarial gates; this pass looks for *obvious possible issues*, spot-checks,
and visual defects, then closes the loop by improving the pipelines themselves.

> **Iron rules.** review-topic never publishes and never edits templates/CSS. Topic
> fixes route through the existing flows (below). Pipeline improvements: **incremental
> changes (critic-prompt prose, added checks) are applied directly and logged**;
> **transformative changes (schema shape, loader contract, stage structure) are logged
> as PROPOSED in `research/PIPELINE_TUNING_LOG.md` and surfaced in the chat** — never
> auto-applied.

Model guidance: reviewers run on **sonnet** (this is spot-checking, not judgment-heavy
authoring); use opus/fable only if a finding is contested and needs one careful
adjudication. Total cost per review should be a small fraction of an authoring run.

| Step | Does | Output |
|---|---|---|
| 1 Ground | export/load current state, run deterministic checks | inputs for reviewers |
| 2 Inspect | 3 light reviewers: content spot-check · editorial · views | findings list |
| 3 Residual audit | prior blocking/advisory findings still open? | applied/open list |
| 4 Route + fix | topic fixes via existing flows; process lessons applied or proposed | fixes + log entries |
| 5 Packet | append a dated cycle to `research/reviews/<slug>/DEEP_REVIEW.md` | human-readable record |

## 1 · Ground

- Published topic: `export_topic --slug <slug> --out research/topics/<slug>.json` first
  (re-sync from live DB). Draft: use the existing JSON.
- Deterministic (no LLM): `check_links --topic <slug>`; the shape checks from
  `research_topic.js`'s `shapeCheck` (min counts, missing detail/crux, unit lengths).
- Render current views if stale or missing: `render_screens` / `render_social
  --formats og,sq,pt` / `render_poster` — **always pass `--base-url`** (they default to
  a dead localhost:8000).

## 2 · Inspect — three sonnet reviewers, in parallel (Agent tool, not a Workflow)

1. **Content spot-check** (`sonnet`, web enabled): obvious wrongness only — skim every
   stat/claim for internal contradictions, implausible or stale-looking figures, label/
   value scope mismatches, and web-spot-check the ~3-5 most load-bearing numbers
   against their cited source (EXACT claim: same population/threshold/measure). Check
   proponent names look right. Do NOT re-research the topic.
2. **Editorial** (`sonnet`): placement and both depth axes — is the most
   decision-relevant content above the "Go deeper" fold; is each compact line
   self-sufficient and register-appropriate (no bare jargon); does each expanded
   `detail` genuinely add over its compact line; are section/item orderings sensible;
   are summaries tight (steelman ≤~90 chars, why ≤~230, note one sentence)? Use the
   fold preview math from `distribute_topic.js` if fold questions arise.
3. **Views** (`sonnet`, vision): read the rendered images — desktop-1440, mobile-390/
   320, og/sq/pt cards, poster — for clipping, truncation, overflow, broken tiles, fold
   problems, icon/color correctness per `design/DESIGN_SYSTEM.md`. A browser (or Claude
   in Chrome) walk of the live/dev page is an acceptable substitute for re-rendering.
   **Coverage:** the default `render_screens` run captures the collapsed page state;
   add `render_screens --slug <slug> --expanded` (DEBUG dev server) to also capture
   `desktop-1440-expanded.png` etc. with every Go-deeper extra and detail region forced
   visible — review BOTH sets whenever below-fold or `detail`/expanded content changed.

Each reviewer returns findings as `{severity: blocking|advisory|note, item, issue,
evidence, fix, routing: content|presentation|code-css|process}`. For a **blocking**
finding, one quick second look (same model) before acting on it; advisories and notes
go straight to the packet.

## 3 · Residual audit

Read the topic's prior packet cycles (`research/reviews/<slug>/`) and stored verdicts
(`Topic.research_dossier`); check every prior blocking/advisory item against CURRENT
content: **applied or still open**. Still-open items re-enter today's findings. This
step exists because flagged findings have sat unapplied for weeks before (see
`PIPELINE_TUNING_LOG.md` Lesson 5).

## 4 · Route + fix

| Routing | Destination |
|---|---|
| content | Draft topic: apply directly to `research/topics/<slug>.json` (documented in the packet changelog) → reload → re-render affected views. Published topic: the `refresh-topic` flow (changelog → human approves → staging slug). |
| presentation | `distribute_topic.js --fix_only [findings]` → reload → re-render. |
| code-css | Log in the packet's Engineering issues section for the human. Never edit templates/CSS. |
| process | Generalize: would a pipeline prompt/schema change prevent this class of defect on future topics? Incremental → apply to the workflow `.js` file(s) now, entry in `PIPELINE_TUNING_LOG.md` (check the MIRROR siblings need the same edit). Transformative → PROPOSED entry + tell the human in chat. |

Process lesson-mining explicitly includes **model/effort cost-fit**: for each pipeline
run reviewed, ask whether any subtask burned a premium model or max reasoning effort on
mechanical work (web fetching, patch application, reformatting) — or, inversely,
whether a cheap/low-effort assignment produced a defect a stronger one would have
caught. Session overages are themselves review evidence of mis-fit routing. Route
findings like any other process lesson: incremental default changes to the workflow
`args.models`/`args.efforts` knobs apply directly; structural changes are PROPOSED.

## 5 · Packet

Append a dated cycle section to `research/reviews/<slug>/DEEP_REVIEW.md` (create if
absent): findings by severity, residual-audit results, fixes applied (topic + process),
open items for the human. Keep it scannable — this is what the human reads before
publishing.
