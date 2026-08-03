---
name: author-topic
description: Author ONE new Ideya topic end to end through the staged pipeline — research (substance) → distribute (presentation) → iconography → views → a review packet for the human. Use when turning a catalog entry into a publish-ready draft. AI drafts → a human publishes.
---

# author-topic

Turn a catalog skeleton into a publish-ready topic. One run = one topic through five
stages, each an automated create-and-refine step with its own gate; the human reviews
only at the end. This is the forward pipeline; `refresh-topic` is its upkeep mirror.

> **Iron rule — automation drafts; a human publishes.** Stages 1–4 run unattended and
> produce a DRAFT topic + a review packet. Publishing (stage 5) is a human hard stop.

Run from the repo root in the project venv (`.venv/bin/python`). `<slug>` is the topic
slug; `<cat>` is a category slug (`global-risk · ai · digital · climate-env ·
bio-health · economy · governance · society · ethics`). Each stage writes a durable
artifact so stages are independently re-runnable — a stage that already has its
artifact is skipped unless you pass `--redo`.

| Stage | Does | Artifact |
|---|---|---|
| 1 Research | substance: plan (+icon) → parallel research → crux → substance gate | `research/dossiers/<slug>.json` |
| 2 Distribute | presentation: distill → tier/reveal/fold → presentation gate | `research/topics/<slug>.json` (loader contract) |
| 3 Iconography | brief → Nano Banana candidates → pick → post-process | `static/img/topics/<slug>.png` + `research/icons/<slug>.md` + candidates |
| 4 Views | render desktop/mobile/social/poster → critique → content-fix loop | `research/reviews/<slug>/` (+ `REVIEW.md`) |
| 5 Publish | **human** reviews the packet, then publishes | live topic |

> **Dual-use content note.** Some catalog topics (engineered pathogens / bioweapons and
> similar) are blocked by content policy — the deep-research agents error out. If stage 1
> fails that way, the topic is not automatable through Claude agents; author it via an
> external-research path onto the same `research/topics/<slug>.json` contract (path B in
> `research/RESEARCH_PIPELINE.md §11`) and resume at stage 3.

---

## Model + effort routing (baked as workflow defaults; override via `args.models` / `args.efforts`)

Judgment on **fable**; web grunt on **sonnet**/**opus**; never below sonnet.
- Stage 1: plan `fable` · research `sonnet` · crux `fable` · gate `fable`
  (EXCEPT fact-source critic: `opus` — token-heavy mechanical web checking) · fix `opus`
- Stage 2: distill `opus` · distribute `fable` · gate `fable` · fix `sonnet`
- Stages 3–4: brief/pick and view critics on `fable` (main session + sub-agents)

High-volume subtasks also pin an explicit reasoning **effort** instead of inheriting
the session's (often max) effort — the main session-overage lever: stage-1
research/critics/fix `high`; stage-2 distill/critics `high`, fix `low` (whitelisted
patch application). Judgment singletons (plan, crux, distribute) inherit.

---

## Stage 1 · Research (substance)

Pull the catalog entry from `research/catalog/topic-universe.json` and run the
`research_topic.js` workflow with args `{title, slug, summary, why_now, category,
suggested_icon, positionNames, questionsSeed:[], today:"YYYY-MM-DD"}`.

Persist the return (`{draft, plan, verdicts, shape_notes, plan_positions}`) to
`research/dossiers/<slug>.json` wrapped in `{dossier_version:1, generated, slug, input,
...}`. Check: substance gate 4/4 (or logged residuals — the fact-source critic often
leaves a citation-attribution note; that's a human-review item, not a blocker), and
`shape_notes` empty. The plan emits the Phosphor `icon`, so `--icon` at load is optional.

## Stage 2 · Distribute (presentation)

Run `distribute_topic.js` with args `{slug, title, today, dossier:<the stage-1 return>,
models}`. It distills the compact layer, assigns tier (the "Go deeper" fold) and reveal
(compact vs expanded), and reorders items so the most decision-relevant lead — then a
3-critic presentation gate (compact-self-sufficiency, reading-level-fit,
above-fold-selection). **Display order = array order; `tier` marks the drop-off within
that order — to move an item across the fold you REORDER, not just re-tier.** Persist the
return as `research/topics/<slug>.json` (`{draft, verdicts, plan_positions}` — the loader
contract; verdicts are stage-tagged). Facts are never changed here (the patch whitelist
rejects edits to value/unit/source/url/name/text).

> Passing a 64KB+ dossier as a tool arg is impractical and workflow scripts can't read
> files. Bake it in: copy the workflow to a run script, whole-word replace `args` →
> `__ARGS`, and inject `const __ARGS = {...}` after the meta block. See `reference.md`.

Load to a staging draft and confirm zero loader warnings:
```
.venv/bin/python manage.py load_topic_draft --file research/topics/<slug>.json \
  --slug <slug> --title "<Title>" --category <cat> --status draft \
  --image-brief research/icons/<slug>.md
```
(For a brand-new topic use the real slug — it's already an unpublished catalog draft.
Use `<slug>-draft` only when a published version is live and must stay online.)

## Stage 3 · Iconography

Loop, capped at ~3 refine rounds:
1. A `fable` sub-agent writes `research/icons/<slug>.md` from `research/ICONOGRAPHY.md` +
   `research/icons/categories.md` + the existing briefs as exemplars (match their
   headings; the `## Generation prompt` blockquote is what the generator reads).
2. `python research/icons/generate_icons.py --slug <slug> --n 4` → candidates land in
   `research/icons/candidates/<slug>/`.
3. **Read** the candidates; score against the `research/ICONOGRAPHY.md` checklist (uniform
   monoline stroke, same-hue ~16–18% duotone fill, category colour, 2.5–3.5× scene
   complexity, white ground, no text/frame, 40px legibility). None pass → refine the
   prompt or `generate_icons.py --edit <candidate> --edit-prompt "..."`; one passes →
   pick it and append a `## Selection` note to the brief.
4. `python research/icons/postprocess_icon.py --slug <slug> --src <winner.jpg>` →
   normalizes to `static/img/topics/<slug>.png` (1035×690 white ground) + a 40px thumb;
   Read the thumb to confirm legibility. All candidates are kept for later human swaps.

## Stage 4 · Views

With the draft loaded and a dev server up (`DJANGO_DEBUG=true … runserver`; drafts render
under DEBUG), render + critique, capped at ~3 rounds:
1. `render_screens --slug <slug> --base-url <dev>` (1440/390/320, full height),
   `render_social --slug <slug> --formats og,sq,pt --out research/reviews/<slug>`,
   `render_poster --slug <slug> --out research/reviews/<slug>` (its fit-check exit code
   is a hard gate).
2. `fable` sub-agents **Read** every image against `design/DESIGN_SYSTEM.md` +
   `design/RESPONSIVE.md`. Classify findings:
   - **content-fixable** (overlong text, bad fold, poster overflow) → re-run
     `distribute_topic.js` with `args.fix_only:[findings]` (skips distill/distribute, runs
     only the presentation fix loop) → reload → re-render.
   - **code/CSS defect** → log in `REVIEW.md` for the human; the pipeline never edits
     templates/CSS.
3. Pass = poster fit exit 0 + all three social formats + no blocking content findings.

> **After stage 4, run the `review-topic` skill** (light, sonnet-based) before handing
> the packet to the human: stage 4's view critique is one-shot and self-reported, while
> review-topic also spot-checks content and editorial structure, audits prior residuals,
> and feeds generalizable lessons back into the pipelines
> (`research/PIPELINE_TUNING_LOG.md`). Unlike stage 4 it can be re-run any time,
> including against a published topic.

## Stage 5 · Human review & publish

Assemble `research/reviews/<slug>/REVIEW.md` (template in `reference.md`): stage
timings/rounds, substance + presentation verdict summaries, the fold preview, icon winner
+ candidates, screenshot/card/poster links, and the engineering issues found. Then the
human: preview the draft as staff → publish
(`load_topic_draft … --slug <slug> --status published --image-brief …`) → **wire
related-topic edges**: the catalog entry's `related_slugs` (every entry carries 3-5;
add them when creating a new entry) feed `manage.py load_universe` (idempotent) which
creates the `TopicEdge` rows — without this step the new topic ships with an empty
"Connects to" strip → set
`reviewed_at = now()` → `check_links --topic <slug>` (0 dead / 0 placeholder) → commit
`research/dossiers/<slug>.json`, `research/topics/<slug>.json`, the icon assets, and the
review packet.
