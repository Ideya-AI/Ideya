# Ideya

Part of the [Ideya-AI](https://github.com/Ideya-AI) project set.

A web app for considering and simply explaining major human problems and issues. Goal: take hard, sprawling topics and make the shape of them legible — what the core question actually is, what the trade-offs look like, and where the disagreement sits.

Django + HTMX + Alpine, token-native CSS, SQLite. Content is AI-drafted and human-published; `research/topics/<slug>.json` is the single source of truth per topic.

## Repo map

- `topics/` — the app: models, views, and the management commands that load, export, render (posters/social cards), and maintain content.
- `templates/`, `static/` — the built product surface (design tokens in `static/css/tokens.css`).
- `design/` — the locked design system: foundations, component specs, responsive rules, data model.
- `research/` — the content pipeline: topic universe catalog, per-topic JSON (source of truth), icon briefs + generator, authoring/refresh workflows, plus its two governing docs — `RESEARCH_PIPELINE.md` (the authoring engine's design + editorial quality bar, referenced by the workflows and skills) and `ICONOGRAPHY.md` (the locked topic-icon style).
- `DEPLOY.md` — how to go live (env vars, Docker/buildpack, content seeding).
- `accounts/` — shelved accounts app (kept by decision; no public entry points).
