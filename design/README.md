# Handoff: Ideya — Design System & Product Surfaces

## Overview
**Ideya** (working name "Infinity" at handoff time) is a curated, navigable **atlas of hard human issues** (existential risk, governance, energy, economics, ethics) — "a visual wiki between an encyclopedia and a debate platform." Each issue is one structured infographic with **six sections in a fixed order**: Overview → Basics → Questions → Positions → Crux → Actions. The product is topic-first, neutral by intention, and explicitly *not* social media (no feed, follows, or recency).

This bundle contains the full design system (tokens, type, color, iconography), six reusable components, the data model, and high-fidelity mocks of every product surface across four mediums.

## About the design files
The files here are **design references authored in HTML/CSS/React** — prototypes that show the intended look, structure, and behavior. They are **not production code to ship directly**. Your task is to **recreate these designs in the target codebase's environment**, using its established patterns and libraries.

> Context: the original product is a **Django 5.1 + HTMX + Alpine.js + Tailwind** app (now `Ideya/`, SQLite). If you are building into that stack, translate these designs into Django templates + Tailwind + Alpine. If into a fresh stack, React is the natural fit — the components are already authored as React (`components/*.jsx`). Either way, reproduce the **tokens and component contracts** faithfully; adapt the implementation to the host environment.

## Fidelity
**High-fidelity.** Final colors, typography, spacing, iconography, and interactions are all specified. Recreate the UI pixel-faithfully using the codebase's libraries. All values come from `colors_and_type.css` (108 design tokens) — wire those into the host theme rather than hard-coding.

---

## Design language (the non-negotiables)
- **Type:** **Plus Jakarta Sans** for display (700/800 — titles, position names, stats, eyebrows) + **Inter** for body/UI. Hierarchy from weight + size + tracking, not extra families. Tabular figures for all numbers.
- **Icons:** **Phosphor Icons, duotone** weight (`<i class="ph-duotone ph-atom">`, CDN `@phosphor-icons/web`). Fill weight for heavy/poster contexts. No emoji, no custom icon set.
- **Color — three disciplined systems, never mixed:**
  1. **Ink ramp** — a green-tinted neutral scale carries *all* chrome (`--ink-50` `#f7f9f7` bg → `--ink-900` `#141813` text).
  2. **Brand green** `#4CB050` (`--green-500/600/700` + `--green-tint`) — the single accent: actions, links-as-action, active states, brand. Used throughout chrome.
  3. **Position colors** (`--pos-green/amber/blue/rust/purple/teal/slate`) — distinguish named positions *within a topic*; assigned per-topic, reused across topics, **no fixed meaning**.
  4. **Category colors** (`--cat-energy/tech/gov/econ/ethics/risk`) — identify top-level categories in **discovery tiers only** (Home, Category, Search) — **never on a Topic page**.
- **Cards:** flat — white, `1px var(--ink-100)` border, **no shadow**, ~14–18px radius. Hover may lift the border / translate slightly. Shadow exists *only* for transient overlays (dropdown, modal/sheet).
- **The Crux** is the one section that **inverts to a full dark band** (`--ink-900`, white text, green highlight) — the page's visual anchor.
- **Reading depth** (Brief / Normal / Deep) is a first-class, cross-cutting control. Every section degrades to a "condensed atom" for sharing/print; Normal adds context; Deep adds sources / "go further."
- **Motion:** quiet and short — `cubic-bezier(0.2,0,0,1)`, 120–280ms, fades + small position moves. No bounce/spring/parallax.
- **Voice:** sentence case (only the small tracked section eyebrow is uppercase); third-person, neutral; each position written as its own **steelman**; address the reader as "you" only at action points.

---

## Screens / views
> The `mocks/` and `preview/` HTML files were removed after the build shipped (the live app is now the reference implementation); they remain in git history. The surface descriptions below are the durable spec.

Widths: desktop content max 1180px; mobile 390px.

### 1. Home — `mocks/Home - Desktop.html`
- **Purpose:** orient a (often redirect-arriving) visitor and route them onward.
- **Parts:** (1) **Nav** — logo + center search + menu. (2) **Spotlight** — an editorial light/dark hero that mirrors the social share card (left "what it is": category badge, icon, Jakarta-800 title, summary, meta, "Explore" CTA; right dark "the debate": named position chips + the crux hook) + a 3-card bench of supporting picks. (3) **Purpose** — mission statement + a What/Why/How trio. (4) **Directory** — every topic grouped into category-colored columns with "X more" collapses and a By-category / A–Z toggle.

### 2. Category page — `mocks/Category Page - Energy.html`
- **Purpose:** funnel from a category to its topics (not a debate surface).
- **Parts:** section rail (Overview / Basics / Topics); **Overview** (category icon+title in its `--cat-*` color, description, parent/sibling "Connects to" chips); **meta-Basics** (facts about the *category itself* — topic count, institutions, how its debates split); **Topics grid** of `TopicNode`s.

### 3. Topic page — desktop `mocks/Desktop Topic - Nuclear Energy.html`, mobile `mocks/Mobile Topic - Nuclear Energy.html`
- **Purpose:** the core artifact — the six sections in fixed order. **This desktop/mobile pair is the reference implementation** for how every surface reflows.
- **Desktop:** sticky left section rail + visual depth toggle; side-by-side section layouts.
- **Mobile:** stacked accordions, sticky section-jump scroller, compact depth control, **bottom-sheet** position detail.

### 4. Search — `mocks/Search - Dropdown.html`
- **Purpose:** instant navigation. Live dropdown under the nav: grouped **Topics / Categories / Positions** with highlighted matches + debate dots; **suggested topics + browse-by-category** on empty query; keyboard nav (↑/↓/↵/esc). On mobile → full-screen search view.

### 5. Submit your view — `mocks/Submit Your View - Flow.html`
- **Purpose:** the one inbound participation surface. 3-step modal: (1) align with a position, (2) set stance + importance + optional reasoning, (3) identity (**anonymous by default**, optional email) → confirmation. On mobile → bottom sheet. Reasoning is **aggregated into the landscape, not posted as a comment.**

### 6. Poster & social — `mocks/Topic Poster - Nuclear Energy.html`, `mocks/Social Share Cards - Nuclear Energy.html`
- **Purpose:** the shareable/printable mediums. Poster = a 1280×3059 print one-sheet (dominant hero, Positions centerpiece, full-bleed dark Crux band). Social = OG / square / portrait share cards (light "what it is" + dark "the debate"), the visual DNA the Home Spotlight echoes.

---

## Components
The six reusable components — full typed source (props `.d.ts` + `.jsx` implementation) is in **`COMPONENTS.md`**. All are **depth-aware** (accept a `depth` prop). Authored as React; recreate in the target framework, preserving the prop contracts.

| Component | Role |
|---|---|
| `TopicNode` | Topic card for discovery tiers (Home, Category, Search, Spotlight bench). Category-tinted icon + name + summary + position "debate dots". Supports a dashed `stub`. |
| `PositionCard` | The heart. Color rail + dot + Jakarta-800 name, italic steelman (always), description + representative + proponents (by depth), agree/disagree + importance. |
| `QuestionCard` | One open question. Empirical/value tag drives the accent; importance vote; "why contested" at normal/deep. |
| `StatTile` | One Basics figure. Implements the **chart vocabulary**: fact shape → fixed viz (`ranked` / `radial` / `range` / `bar` / `sparkline`). Charts are ink + single green; subject is the only green element. |
| `DepthToggle` | The Brief/Normal/Deep reading-depth control (bar-height glyph). Drives every section's reveal. |
| `VoteControl` | The importance signal on Questions and Positions. Aggregates a count; surfaces salience but never reorders curated content. |

## Data model
**`DATA_MODEL.md`** holds the **canonical schema** — `Topic`, `Position`, `Question`, `Stat` (+ `VizKind`), `Action`, `Crux`, `Category`, `Depth` — plus a fully-populated **Nuclear Energy fixture** to build and test against.

## Interactions & behavior
- **Reading depth** — `condensed` shows each section's minimal atom (viz+value, name+steelman, etc.); `normal` adds one-line context + sources; `deep` adds methods / representative / "go further". Persist the user's choice.
- **Participation (two signals only)** — **stance** (agree↔disagree; on a Question, which way you lean) and **importance** (up/down vote). Both **aggregate** and surface salience; importance **reorders Questions** but **never reorders Positions**. Curation leads; participation refines.
- **Search** — debounced live filter; ↑/↓ move selection, ↵ opens, esc closes; scrim dims the page; empty query shows suggested + browse.
- **Submit flow** — stepper gates Continue until each step is valid; anonymous is preselected; confirmation recaps stance + position.
- **Navigation** — section rail / chips scroll-spy and jump (auto-expanding the target accordion on mobile). Category badges + related chips are navigation.
- **Responsive** — see `RESPONSIVE.md`. Rule of thumb: single column < 640; rails → horizontal scrollers; modals → bottom sheets; hover affordances become always-on at ≥44px touch targets.

## State management
- `depth: "condensed" | "normal" | "deep"` (persisted, app-global or per-page).
- Per-position `stance` and per-question/position `vote` (optimistic; reconciled with server aggregates).
- Search: `query`, derived `results`, `activeIndex`, `open`.
- Submit flow: `step`, `position`, `stance`, `importance`, `reasoning`, `identity`.
- Content (`Topic` and friends) is fetched per `types.d.ts`; one topic (Nuclear Energy) is fully authored.

## Design tokens
**All** values live in `colors_and_type.css` (108 tokens): ink ramp, brand green scale + tint, `--pos-*`, `--cat-*` (+ tints), the type scale and font vars, spacing (4px Tailwind scale), radii (`8 / 12 / 16 / 9999`), elevation (overlay shadows only), and motion (easing + durations). **Wire these into the host theme; do not hard-code.** Full prose rationale in `README.md` (VISUAL FOUNDATIONS) and `SKILL.md` (hard rules).

## Assets
- `assets/ideya-mark.png` — the square brand mark (app icon / nav bug). Keep on brand green; never recolor.
- Logos (horizontal/stacked/vector) are in the source project's `assets/`; in-product wordmark is the mark + "Ideya" in Plus Jakarta Sans Bold ink.
- **Icons:** Phosphor via CDN (`@phosphor-icons/web` duotone + fill) — not bundled here.
- **Fonts:** Plus Jakarta Sans + Inter via Google Fonts; self-host for production.

## Known gaps (intentionally not yet designed)
Flag these to the team — best refined against real implementation:
- **States:** empty / loading / error (404) and full interaction states (focus/disabled/validation) beyond the happy path.
- **Motion spec:** durations/easing are tokenized, but a per-interaction motion doc isn't written.
- **Accessibility pass:** focus order, ARIA roles, keyboard coverage, position-color contrast, reduced-motion — not yet audited.
- **Coverage:** one topic (Nuclear Energy) is fully authored; mobile exists only for the Topic page (others documented in `RESPONSIVE.md`).

## Files in this bundle
- `colors_and_type.css` — all design tokens (import everywhere). The source project also exposes a root `styles.css` that just `@import`s this.
- `DESIGN_SYSTEM.md` — full content + visual foundations, iconography, logo.
- `SKILL.md` — condensed hard-rules reference.
- `RESPONSIVE.md` — breakpoints + per-surface reflow.
- `COMPONENTS.md` — full source of the six components (props + implementation).
- `DATA_MODEL.md` — the schema + a populated fixture.
- `assets/` — brand mark.
- `mocks/` + `preview/` — removed post-build (see git history); the live app supersedes them.
