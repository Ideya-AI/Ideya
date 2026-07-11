---
name: ideya-design
description: Use this skill to generate well-branded interfaces and assets for Ideya (the "atlas of hard issues" product), either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and reference page mocks for prototyping.
user-invocable: true
---

Read the `README.md` file within this skill, and explore the other available files.

Ideya is a curated, navigable atlas of hard human issues — "a visual wiki between encyclopedia and debate platform." The look is restrained, editorial, and mobile-first: a warm green-tinted **ink** palette for all chrome, **Plus Jakarta Sans** for display + **Inter** for body, flat bordered cards (no shadow), and color used with discipline — **positions** within a topic, **categories** in discovery tiers, and the **logo green** as the single brand accent.

Key files:
- `README.md` — product context, CONTENT FUNDAMENTALS (voice/tone), VISUAL FOUNDATIONS, ICONOGRAPHY, logo usage.
- `colors_and_type.css` — all design tokens (ink ramp, position palette, category palette, brand green, type scale, radii, spacing, elevation, motion) + semantic element classes. Import it.
- `assets/` — Ideya logos (horizontal/stacked lockups, square mark, vector).
- `preview/` + page mocks — removed post-build (recoverable from git history); the shipped app and the section rules in `README.md` are now the canonical reference for each section and surface.

If creating visual artifacts (slides, mocks, throwaway prototypes), copy assets out and create static HTML files for the user to view. If working on production code, copy assets and read the rules here to design like an Ideya expert.

If the user invokes this skill without other guidance, ask what they want to build, ask a few focused questions, and act as an expert designer who outputs HTML artifacts or production code as needed.

Hard rules to honor:
- **Type:** Plus Jakarta Sans (700/800) for display — titles, position names, numbers; Inter for body and UI. Tabular figures for all stats.
- **Icons:** Phosphor, **duotone** weight, sized generously. No emoji.
- **Color discipline (three independent systems):**
  - **Logo green** is the single brand accent — links-as-action, primary buttons, active states, brand touches. Used throughout product chrome (this supersedes the old "green on marketing only" rule).
  - **Position colors** (`--pos-*`) distinguish named positions *within a topic*; assigned per-topic, reused across topics, never carry fixed meaning.
  - **Category colors** (`--cat-*`) identify top-level categories in **discovery tiers only** (Home, Category pages, search) — never on a Topic page.
- **Cards** are flat: 1px `--ink-100` border, ~14–18px radius, no shadow (hover may lift slightly).
- **The Crux** is set apart as a full **dark inverted band** (`--ink-900`), the one place that goes dark — its visual anchor, not a side rule.
- **Reading depth** (Brief / Normal / Deep) is a first-class control; every section degrades gracefully to its condensed atom for sharing and print.
- **Voice:** sentence case everywhere except the small uppercase section eyebrow; third-person and neutral; each position written as its own steelman. Address the reader as "you" only at action points.
- **Participation** is two signals — stance + importance — that aggregate but never reorder curated content. Curation leads; participation refines.
