# Ideya

Django + HTMX + Alpine. A curated atlas of hard debates; depth is an axis, not a page.

## Commands

- Always `.venv/bin/python`, run from the repo root.
- Dev server: `DJANGO_DEBUG=true .venv/bin/python manage.py runserver 8641 --noreload`.
  **Never 8642** — that is the live container (a hook blocks it).
- **Restart the dev server after any template edit.** Django caches compiled templates
  even under DEBUG, and with `--noreload` nothing invalidates the cache — renders
  silently serve the pre-edit template. This has cost real debugging time twice.
- Lint a topic draft before rendering: `.venv/bin/python research/v1/workflows/lint_draft.py <file> --fix`.

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
- `research/runs/` and `research/reviews/` — process, not product, and untracked.
  How a topic was made; the topic itself is its file plus its shipped assets.
- `research/v1/` — **the retired v1 pipeline, archived 2026-09-11 and wired to
  nothing.** Its orchestrator, harness, stage scripts, measuring tools, agent
  definitions, `ENGINE.md` and `RESEARCH_PIPELINE.md` are kept for their
  rationale while v2 is built. Read it for why a rule exists; do not run it.
- `research/UI_DEFECTS.md` — the live register of code/CSS defects found while
  reviewing rendered topics. `design/` — the locked design system; treat it as
  authoritative over any prompt that contradicts it.

## Pipeline

**Being rebuilt (v2, from 2026-09-11).** Nothing authors a topic right now. v2
keeps five stages in the same order with the same goals; how each stage works is
being redesigned against the bookends below, stage by stage.

The bookends are fixed and are the pipeline's whole contract: it takes a topic
file from `not_started` to `ready`, and nothing else. Before it is the file.
After it is `publish_topic`, which is a switch a human throws.

There is **no upkeep engine**. A published topic stays as published until a human
deliberately edits its content file and reloads it.
