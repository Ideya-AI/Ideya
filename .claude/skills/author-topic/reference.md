# author-topic — reference

Detail for the [SKILL](SKILL.md): artifact shapes, the dossier-injection recipe, the
presentation-patch contract, and the review-packet template.

## Artifact shapes

**Stage 1 dossier** `research/dossiers/<slug>.json`:
```
{ "dossier_version": 1, "generated": "YYYY-MM-DD", "slug": "...",
  "input": { "title": "...", "category": "..." },
  "draft": { overview, basics, questions, positions, crux, actions },
  "plan": { ...planner output incl. icon + positions },
  "verdicts": [ {critic, pass, blocking, notes} ],   // substance
  "shape_notes": [], "plan_positions": [ ... ] }
```
`draft` is substance-complete but presentation-provisional (tier/reveal are first-pass;
stage 2 finalizes them). The workflow returns this object; the orchestrator writes it.

**Stage 2 loadable draft** `research/topics/<slug>.json` — the existing loader contract,
unchanged: `{ draft, verdicts, plan_positions }`. Verdicts carry an additive
`stage: "substance" | "presentation"` tag (the loader stores verdicts opaquely into
`Topic.research_dossier`, so `refresh-topic` stays compatible). This is the same file
`export_topic` round-trips and `refresh-topic` reads.

Per-item draft fields are documented in `.claude/skills/refresh-topic/reference.md`
(the canonical schema) — nothing here changes them.

## Running a workflow with a large dossier arg

Workflow scripts can't read files and a 60KB+ dossier is impractical to pass inline. Bake
it into a run script (Python):
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
Then `Workflow({scriptPath: "<scratch>/run_distribute_<slug>.js"})`. Syntax-check first by
stripping the leading `export` keyword from the meta declaration (e.g.
`runner.replace("export const meta", "const meta")`) and then wrapping the body in a
function — top-level `return` won't parse bare in Node, and `export` won't parse inside
a function either, so both transforms are needed for the check.

For a **fix_only** view-feedback pass, add `"fix_only": [<finding objects or strings>]`
to `run_args`; the workflow skips distill/distribute and runs only the presentation fix
loop against the current `research/topics/<slug>.json` draft.

## Presentation-patch contract (stage 2)

`distribute_topic.js` edits **presentation only**. `applyPresentationPatch`:
- **edits**: field on the whitelist `{tier, reveal, wide, note, why, steelman,
  description, detail, intro, lead, subtitle, summary}` — anything else
  (value/unit/source_*/url/kind/name/text/label) is **rejected**, never applied. Facts
  are locked by stage 1.
- **reorder**: per-section full new order of item ids; rebuilds the array (omitted items
  append, keeping relative order). For stats/questions/actions this is how an item is
  moved across the fold — the loader assigns `order = array index`, and the fold math
  (`Section._tier_lead_count`, ported into the workflow's `foldPreview`) reads that
  order. `tier` alone only marks the drop-off within the current order. **Positions are
  the exception**: they render by `-prevalence_weight` first (array order only breaks
  ties), and prevalence is a locked fact — steer the position fold with `tier`, and keep
  the array sorted to match prevalence.

## Fold reference (must match `topics/models.py`)

BASICS min/max 3/9 (3-col grid, wide tiles span 2 cells); QUESTIONS 3/6 (1-col);
POSITIONS 2/6 (2-col). The workflow's `foldPreview` reproduces this exactly — validated
against the live nuclear-energy tiers (8/4/4).

## REVIEW.md template

```
# <Title> — review packet (<date>)

**Status:** DRAFT loaded as <slug>. Stages: research <n> fix rounds, distribute <n>,
icon <n> rounds, views <n> rounds.

## Substance gate (stage 1)
<4 critics: pass/fail + one line each; list any residual (e.g. a fact-source
citation-attribution note the human should confirm)>

## Presentation gate (stage 2)
<3 critics: pass/fail + one line each>
Fold above "Go deeper": basics <n>/<N>, questions <n>/<N>, positions <n>/<N>.

## Icon
Winner: <candidate>; <one line why>. Candidates in research/icons/candidates/<slug>/.

## Views
Desktop / mobile-390 / mobile-320 / OG / poster — <pass, or the content findings fixed>.
Poster fit: <slack>px.

## Engineering issues (for you — pipeline does not touch CSS)
- <code/CSS defects the view critics found>

## Check in 5 minutes
- <the few things most worth a human eye: close EDITORIAL calls (a fold choice, a
  contested framing, whether a camp deserves its own card). NOT unresolved facts —
  those are closed inside the pipeline before this packet is written. A fact appears
  here only when the RESOLUTION needs the human's judgment, and then it states the
  decision being asked for, never "please verify this".>

## To publish
load_topic_draft --slug <slug> --status published --image-brief research/icons/<slug>.md
→ set reviewed_at → check_links --topic <slug> (0/0) → commit artifacts.
```
