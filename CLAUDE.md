# Ideya

Django + HTMX + Alpine. A curated atlas of hard debates; depth is an axis, not a page.

## Commands

- Always `.venv/bin/python`, run from the repo root.
- Dev server: `DJANGO_DEBUG=true .venv/bin/python manage.py runserver 8641 --noreload`.
  **Never 8642** — that is the live container (a hook blocks it).
- **Restart the dev server after any template edit.** Django caches compiled templates
  even under DEBUG, and with `--noreload` nothing invalidates the cache — renders
  silently serve the pre-edit template. This has cost real debugging time twice.
- Lint a topic draft before rendering: `.venv/bin/python research/workflows/lint_draft.py <file> --fix`.

## Invariants

- **Automation drafts; a human publishes.** Never `load_topic_draft --status published`
  and never `publish_topic` (a hook blocks both). Publishing is stage 5 and belongs
  to the human.
- **The pipeline never edits templates or CSS.** Log code/CSS defects in the review
  packet for the human instead.
- **Content fields are plain text**: write `&`, never `&amp;`; typographic quotes
  (’ “ ”), never straight; no markdown, no HTML. The renderer escapes literally, so
  markup surfaces as garbage on the page.
- **US spelling** throughout, except inside a proper noun ("Oxford Centre for the
  Governance of AI" keeps its spelling).
- **Display order = array order.** To move an item across the fold, REORDER it; `tier`
  only marks the drop-off within the current order. Positions are the exception — they
  render by `prevalence_weight`.
- **Facts are locked after stage 1.** Stage 2's patch whitelist rejects edits to
  value/unit/source_*/url/name/text; stage 1's does not, so fact corrections belong there.
- **An unverified claim may not be asserted.** If a claim cannot be sourced, it is cut,
  softened to what the source supports, or attributed in-voice to whoever asserts it —
  never handed to the human as "please verify this".

## Where things live

- `topics/` — the app. `templates/`, `static/` — the product surface (tokens in
  `static/css/tokens.css`).
- `research/topics/<slug>.json` — a topic's source of truth (the loader contract).
  `research/dossiers/` — stage-1 substance records. `research/reviews/<slug>/` — the
  human's review packet.
- `research/workflows/` — the engine: the three Workflow scripts plus `lint_draft.py`,
  `seed_defects.py` (gate calibration), `tally_tokens.py`, and `check_engine.py`.
- `research/ENGINE.md` — **the engine's operator manual and single source of truth
  for operations** (structure, runbooks, routing, contracts, failure modes). Any
  commit that changes the engine updates it in the same commit; `check_engine.py`
  verifies the checkable parts (hook-enforced on engine-file edits).
- `research/RESEARCH_PIPELINE.md` — the engine's design rationale + decision history
  (the "why"). `design/` — the locked design system; treat it as authoritative over
  any prompt that contradicts it.

## Pipeline

Authoring: `/author-topic <slug>` → `research/engine/engine.py author <slug>`, one
automated, resumable run to a loaded draft + packet (engine v3, 2026-09-06). Upkeep:
`/refresh-topic <slug>`. Both are human-invoked only — long, expensive, side-effectful.
