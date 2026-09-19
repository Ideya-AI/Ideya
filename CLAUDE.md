# Ideya

Django + HTMX + Alpine. One page per issue: Overview, Basics, Questions,
Positions, Crux, Actions, each opening at a glance and expanding in place.

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
  no tiers, no reveal levels: the site renders file order and a fixed count per
  section before Go deeper (`research/SCHEMA.md`).
- **Rewording never changes a fact.** A restatement may lose precision; it may not
  change direction, magnitude or attribution. Stat values, units, source fields and
  URLs are not reworded at all.
- **A number, date, quote or "X said" in the page's own voice names a source a
  reader can follow, and the URL resolves.** Everything else — how a camp
  reasons, what it values, what is common knowledge in the debate — is written
  without a source.

## Where things live

- `topics/` — the app. `templates/`, `static/` — the product surface (tokens in
  `static/css/tokens.css`).
- `research/topics/<slug>/` — **the set of topics**, one directory each, cradle
  to grave: a topic with only a title and a published one are the same object at
  different stops. The directory name IS the slug.
  - `topic.json` — the product the loader reads. Index fields at the top (slug,
    title, status, authored_at, published_at, reviewed_at, scope, primary_category,
    categories, related), `content` under them once there is content. The source of truth for everything except participation.
  - `evidence.json` — whatever the rebuilt pipeline needs to keep. Nothing writes
    it today; v2's ledger is not a template for it.
  - `icon.md` the art brief; `review.md` the packet for the human, written by stage 5.
  - `run/`, `renders/`, `candidates/` — process, and untracked.
  - Shipped images stay under `static/img/{topics,social}/<slug>.png`, because
    that is where Django serves them from.
- `research/categories.json` — the taxonomy, including each category's page copy.
- `research/SCHEMA.md` — **the topic file schema**. Authoritative.
- `docs/DESIGN.md` — the design system as notes: useful context, not a rule that
  overrides anything. The app itself is the real spec — `templates/` and
  `static/css/tokens.css` are closer to the truth than the doc, and what Jeff
  asks for wins over both.

## The authoring pipeline

**Nothing authors a topic right now.** Being rebuilt from
`research/pipeline/BRIEF.md`; v1 and v2 are gone and neither is a baseline.
