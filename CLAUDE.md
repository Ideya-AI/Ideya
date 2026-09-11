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
  to the human. A topic's core status is one field with four stops —
  `not_started` → `in_progress` → `ready` → `published`. The engine's job ends at
  `ready`; only Jeff crosses the last line, and only `published` is public.
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
- `research/topics/` — **the set of topics**, one file each, cradle to grave: a
  topic with only a title and a published one are the same object at different
  stops. Index fields at the top (slug, title, status, scope, categories,
  related), `draft` under them once there is content. The source of truth for
  everything except participation. `research/categories.json` — the taxonomy.
  `research/runs/<slug>/record.json` — everything the engine produced getting
  there. `research/reviews/<slug>/` — the human's review packet.
- `research/workflows/` — the engine: the two Workflow scripts plus `lint_draft.py`,
  `topic_ids.py`, `seed_defects.py` (gate calibration), `tally_tokens.py`, and
  `check_engine.py`.
- `research/ENGINE.md` — **the engine's operator manual and single source of truth
  for operations** (structure, runbooks, routing, contracts, failure modes). Any
  commit that changes the engine updates it in the same commit; `check_engine.py`
  verifies the checkable parts (hook-enforced on engine-file edits).
- `research/RESEARCH_PIPELINE.md` — the engine's design rationale + decision history
  (the "why"). `design/` — the locked design system; treat it as authoritative over
  any prompt that contradicts it.

## Pipeline

Authoring: `/author-topic <slug>` → `research/engine/engine.py author <slug>`, one
automated, resumable run to a loaded draft + packet (engine v3, 2026-09-06).
Human-invoked only — long, expensive, side-effectful.

There is **no upkeep engine**. A published topic stays as published until a human
deliberately edits its content file and reloads it, or re-runs the engine on it.
