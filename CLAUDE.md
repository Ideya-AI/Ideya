# Ideya

Django + HTMX + Alpine. A curated atlas of hard debates; depth is an axis, not a page.

## Commands

- Always `.venv/bin/python`, run from the repo root.
- Dev server: `DJANGO_DEBUG=true .venv/bin/python manage.py runserver 8641 --noreload`.
  **Never 8642** — that is the live container.
- **Restart the dev server after any template edit.** Django caches compiled templates
  even under DEBUG, and with `--noreload` nothing invalidates the cache — renders
  silently serve the pre-edit template. This has cost real debugging time twice.

## Invariants

- **Automation drafts; a human publishes.** Never `load_topic_draft --status published`
  and never `publish_topic`. Publishing is stage 5 and belongs
  to the human. A topic's core status is one field with four stops —
  `not_started` → `in_progress` → `ready` → `published`. The engine's job ends at
  `ready`; only Jeff crosses the last line, and only `published` is public.
- **The pipeline never edits templates or CSS.** Log code/CSS defects in the topic's
  review packet for the human instead.
- **Content fields are plain text**: write `&`, never `&amp;`; typographic quotes
  (’ “ ”), never straight; no markdown, no HTML. The renderer escapes literally, so
  markup surfaces as garbage on the page.
- **US spelling** throughout, except inside a proper noun ("Oxford Centre for the
  Governance of AI" keeps its spelling).
- **Order is the whole mechanism for weight.** Every section lists its items most
  important first, and that is array order in `topic.json`. No prevalence numbers,
  no tiers. (The site still sorts positions by `prevalence_weight` until the §8 site
  delta in `research/pipeline/PIPELINE.md` is built; the pipeline design already assumes file order.)
- **Stage 2 rewords, it does not change facts.** Stat values, units, source fields and
  URLs leave stage 1 unchanged; everything else may be reworded so long as a
  restatement loses only precision, never direction, magnitude or attribution.
- **Hard claims get a source and a check.** A number, date, quote or "X said" in the
  page's own voice has a fetched source behind it. If the check fails it is cut,
  softened to what the source supports, or attributed to whoever asserts it — never
  handed to the human as "please verify this". Everything else is written from
  model knowledge at encyclopedia-level certainty.

## Where things live

- `topics/` — the app. `templates/`, `static/` — the product surface (tokens in
  `static/css/tokens.css`).
- `research/topics/<slug>/` — **the set of topics**, one directory each, cradle
  to grave: a topic with only a title and a published one are the same object at
  different stops. The directory name IS the slug.
  - `topic.json` — the product the loader reads. Index fields at the top (slug,
    title, status, scope, categories, related), `draft` under them once there is
    content. The source of truth for everything except participation.
  - `evidence.json` — what the pipeline knows: the map, the claim ledger, the cut
    record, gate verdicts. Durable, because later stages depend on it. (Not yet
    present on any topic; the v2 pipeline writes it.)
  - `icon.md` the art brief; `review.md` the packet for the human, written by stage 5.
  - `run/`, `renders/`, `candidates/` — process, and untracked.
  - Shipped images stay under `static/img/{topics,social}/<slug>.png`, because
    that is where Django serves them from.
- `research/categories.json` — the taxonomy.
- `docs/DESIGN.md` — the locked design system; treat it as authoritative over any
  prompt that contradicts it.

## The authoring pipeline

**v2, designed 2026-09-11 to 2026-09-14, not yet built.** Nothing authors a topic
right now. The previous pipeline was deleted on 2026-09-14; it is in git history
only and is not a baseline for anything.

- `research/pipeline/PIPELINE.md` — **the design**: goals, scope, how it reaches Claude,
  orchestration, state, budget, storage, schema, failure semantics, machine-level
  findings, and all five stages in full. Read it before touching the pipeline.

The bookends are fixed and are the pipeline's whole contract: it takes a topic
from `not_started` to `ready`, and nothing else. Before it is the topic
directory. After it is `publish_topic`, a switch a human throws.

There is **no upkeep engine**. A published topic stays as published until a human
deliberately edits its content file and reloads it.
