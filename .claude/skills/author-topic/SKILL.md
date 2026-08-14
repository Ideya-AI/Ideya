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

Judgment on **opus**; web grunt on **sonnet**; never below sonnet.
- Stage 1: plan `opus` · research `sonnet` · crux `opus` · gate `opus` (3 critics) · fix `opus`
- Two critics were retired on evidence, not taste: across the corpus the **crux** critic
  produced 0 blocking findings in 21 verdicts and **above-fold-selection** 0 in 9, while
  `fact-source` blocked 71% of the time. Both remits were folded into the neighbouring
  critic that reads the same material; the saving goes to verification, which is where
  the failures actually are.
- Stage 2: distill `opus` · distribute `opus` · gate `opus` · fix `sonnet`
- Stages 3–4: icon brief/pick and view critics on `opus` (main session + sub-agents)

> **No Fable anywhere (2026-08-13).** The weekly Fable limit was exhausted mid-run on
> `frontier-ai-regulation`, killing three of the four gate critics. `args.models` alone
> was NOT enough to prevent it — the override silently did not reach the workflow script,
> so the old `?? "fable"` defaults won. Every Fable default has been removed from all
> three workflow scripts; do not reintroduce one on the assumption an arg will override it.
> First Opus-only run held quality: stage-1 gate 4/4 with zero blocking findings.

High-volume subtasks also pin an explicit reasoning **effort** instead of inheriting
the session's (often max) effort — the main session-overage lever: stage-1
research/critics/fix `high`; stage-2 distill/critics `high`, fix `low` (whitelisted
patch application). Judgment singletons (plan, crux, distribute) inherit.

---

## Stage 0 · Catalog entry (only if the topic isn't cataloged yet)

If the named topic has no entry in `research/catalog/topic-universe.json`, author one
first (match the existing entries' shape): `{title, slug, summary, why_now,
primary_category_slug, secondary_category_slugs, suggested_icon, position_names,
related_slugs}` — `related_slugs` is 3-5 existing catalog slugs, and add this new slug
to 1-2 neighbouring entries' `related_slugs` so edges point both ways. Then
`manage.py load_universe` registers the stub (idempotent).

## Stage 1 · Research (substance)

Pull the catalog entry from `research/catalog/topic-universe.json` and run the
`research_topic.js` workflow with args `{title, slug, summary, why_now, category,
suggested_icon, positionNames, questionsSeed:[], today:"YYYY-MM-DD"}` — mapping the
catalog keys `primary_category_slug`→`category` and `position_names`→`positionNames`
(`questionsSeed` is `[]` unless seeding). Stage-1 args are small: pass them inline as
the Workflow tool's `args` (no baking needed — the `__ARGS` recipe below is only for
stage 2's 60KB+ dossier).

Persist the return (`{draft, plan, verdicts, shape_notes, plan_positions}`) to
`research/dossiers/<slug>.json` wrapped in `{dossier_version:1, generated, slug, input,
...}`. Check: substance gate 3/3 and `shape_notes` empty. A verdict now carries `checks_run`;
a check with `ran=false` fails that critic and re-runs it once automatically, so a gate
reported as clean means the checks actually happened. **Fact residuals are NOT a
human-review item.** If a verdict leaves any factual matter unresolved — a wrong number,
a shaky citation, a claim the critic could not verify — it is the pipeline's to close
before the packet is written: re-run the fact critic on that claim, or apply the
resolution it prescribed (cut / soften to what the source supports / attribute in-voice).
Stage 1's `applyPatch` has NO field whitelist, so fact fields (`value`, `label`,
`source_*`) ARE fixable here — the whitelist that rejects them exists only in stage 2.
Escalate a fact to the human only when the resolution needs a judgment they alone can
make (e.g. cutting the claim would change which camps the topic can represent), and then
state the decision being asked for, never "please verify this".
The plan emits the Phosphor `icon`, so `--icon` at load is optional.

> **Web-search budget is a shared, non-configurable pool.** There is no setting for it
> (checked against the Claude Code settings docs, 2026-08-13). Stage 1 runs 7 web-enabled
> research agents BEFORE the gate, so the critics arrive last and can find the pool empty —
> on `frontier-ai-regulation` both the neutrality and fact-source critics reported it spent
> before their first search. **WebFetch is NOT affected** and kept working throughout; that
> is why fact-source could still verify every URL directly. Verification should therefore
> lean on WebFetch of primary sources, with search reserved for discovery. If a gate critic
> reports a check it could not run, re-run that critic alone in a fresh workflow invocation
> (a new run gets a fresh pool) rather than accepting the caveat.

## Stage 2 · Distribute (presentation)

Run `distribute_topic.js` with args `{slug, title, today, dossier:<the stage-1 return>,
models}`. It distills the compact layer, assigns tier (the "Go deeper" fold) and reveal
(compact vs expanded), and reorders items so the most decision-relevant lead — then a
2-critic presentation gate (compact-self-sufficiency — which now also judges above-fold
selection — and reading-level-fit). **Display order = array order; `tier` marks the drop-off within
that order — to move an item across the fold you REORDER, not just re-tier.** Persist the
return as `research/topics/<slug>.json` (`{draft, verdicts, plan_positions}` — the loader
contract; verdicts are stage-tagged). Facts are never changed here (the patch whitelist
rejects edits to value/unit/source/url/name/text).

> Passing a 64KB+ dossier as a tool arg is impractical and workflow scripts can't read
> files. Bake it in: copy the workflow to a run script, whole-word replace `args` →
> `__ARGS`, and inject `const __ARGS = {...}` after the meta block. See `reference.md`.

**Lint before the gate.** Run the deterministic lint on the persisted JSON — mechanical
defects (straight quotes, entities, double spaces, over-cap fields, wrapped lean chips,
one-paragraph details, over-long poster-band units) are decidable and must never consume
critic attention or reach the human:
```
.venv/bin/python research/workflows/lint_draft.py research/topics/<slug>.json --fix
```
`--fix` applies only the safe deterministic rewrites (typography/spacing/entities); it
exits 1 while any judgment finding remains. Drive it to **0 findings** before rendering.
It catches things eyeballing misses — it found a capitalised `Honouring` that a manual
case-sensitive sweep had walked straight past.

Before persisting, write the catalog entry's categories into the draft:
`draft.categories = [primary_category_slug, ...secondary_category_slugs]` — the
workflows don't emit this key and the loader would otherwise drop the topic's
secondary categories. Then load to a staging draft and confirm zero loader warnings:
```
.venv/bin/python manage.py load_topic_draft --file research/topics/<slug>.json \
  --slug <slug> --title "<Title>" --category <cat> --status draft
```
(`--image-brief research/icons/<slug>.md` is added from stage 3 on — the brief doesn't
exist yet at this point and the loader hard-errors on a missing path.)
(For a brand-new topic use the real slug — it's already an unpublished catalog draft.
Use `<slug>-draft` only when a published version is live and must stay online.)

## Stage 3 · Iconography

Loop, capped at ~3 refine rounds:
1. An `opus` sub-agent writes `research/icons/<slug>.md` from `research/ICONOGRAPHY.md` +
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

With the draft loaded and a dev server up (`DJANGO_DEBUG=true … runserver 8641` — one
pinned dev port everywhere below, deliberately not 8642, the live container; drafts render
under DEBUG), render + critique, capped at ~3 rounds. **Restart the dev server after any
template edit**: Django 4.1+ caches compiled templates even under DEBUG, and with
`--noreload` nothing invalidates the cache — renders silently serve the pre-edit template:
1. `render_screens --slug <slug> --base-url <dev>` (1440/390/320, full height) —
   add a `--expanded` run too (captures `?expanded=1` with every Go-deeper extra and
   detail region forced visible; the depth layers get no visual coverage otherwise),
   `render_social --slug <slug> --formats og,sq,pt --base-url <dev> --out
   research/reviews/<slug>`, `render_poster --slug <slug> --base-url <dev> --out
   research/reviews/<slug>` (its fit-check exit code is a hard gate; `--base-url` is
   required on all three render commands).
2. `opus` sub-agents **Read** every image against `design/DESIGN_SYSTEM.md` +
   `design/RESPONSIVE.md`. Classify findings:
   - **content-fixable** (overlong text, bad fold, poster overflow) → re-run
     `distribute_topic.js` with `args.fix_only:[findings]` (skips distill/distribute, runs
     only the presentation fix loop) → reload → re-render.
   - **code/CSS defect** → log in `REVIEW.md` for the human; the pipeline never edits
     templates/CSS.
3. Pass = poster fit exit 0 + all three social formats + no blocking content findings.


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
review packet. **Then put it on the live site** — the live DB is separate from this
authoring DB; follow "Publish one topic to the live site" in `DEPLOY.md` §3 (a
`docker exec` load against the live container — never copy the whole DB over it).
