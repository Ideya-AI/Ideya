# Ideya — Design System

A curated, navigable **atlas of hard human issues** — existential/global risk, governance, economics, ethics. The product makes the *shape* of an issue legible: what the topic is, where the live disagreements sit, who holds which position and why, and how to engage. Positioning anchor: **"a visual wiki, between encyclopedia and debate platform"** — closer to Our World in Data or a well-designed textbook than to Wikipedia or Reddit.

- **Name:** Ideya (decided 2026-07-10; formerly working name "Infinity Project" — private framing: "humanity's last chance to understand its issues before AI takes over"). Public domains: ideya1.org (primary), ideya1.com.
- **Topic-first, not question-first.** Readers orient on what something *is* before being asked to take a side.
- **Neutral by intention**, not by audited performance. No bias-balance theater (no AllSides-style ratings).
- **Curation is the product; participation is feedback.** Votes/comments improve content, never destinations of their own.
- **Explicitly *not* social media** — no feed, friends, follows, profiles, recency bias.

## Sources (provided context)

- **Codebase:** `Ideya/` (named `Infinity_Project/` at handoff time) — a Django 5.1 + HTMX + Alpine.js + Tailwind (Play CDN) app, SQLite, one seeded topic (Nuclear Energy). The source of truth for UI patterns. Key files:
  - `DESIGN_BRIEF.md`, `PROJECT.md` — product shape, IA, the six-section topic spine, depth-as-axis model. (Both since retired — see git history; this folder is now the product-shape record.)
  - `templates/base.html` — the live Tailwind theme config (the `ink` palette, Inter, container widths).
  - `templates/topics/detail.html` — the canonical topic page; every component below is lifted from here.
  - `templates/topics/index.html` — the topic directory.
  - `topics/models.py` — the content model (Topic, Category, Section, BasicsCard, Question, Position, Action, TopicEdge).
- **Uploaded logos:** `0 Current Logo.png` (horizontal Ideya lockup), `Ideya Logo.png` (stacked), `IP logo2.png` / `IP logo2.jpg` (square mark), `IP Logo Vector.svg` (vector mark). Copied into `assets/`.
- **Org:** part of the [Ideya-AI](https://github.com/Ideya-AI) project set; sibling project `Explain_AI`.

> Note: the app is early-stage scaffolding. This system **codifies and lightly extends** its established direction (it adds the position palette, voting controls, search dropdown, and a navy-free accent discipline) without inventing a new look.

---

## Index — what's in this folder

| File / folder | What it is |
|---|---|
| `README.md` | This file — product context, content + visual foundations, iconography. |
| `colors_and_type.css` | All design tokens: ink ramp, position palette, brand accents, type scale, radii, spacing, elevation, motion + semantic element classes. Import this everywhere. |
| `assets/` | Ideya logos (horizontal lockup, stacked, square mark, vector). |
| `preview/` | Removed post-build (git history) — specimen cards + the six section specs; the live app supersedes them. |
| `components/` | The reusable React components (`.d.ts` + `.jsx`): `TopicNode`, `PositionCard`, `QuestionCard`, `StatTile`, `DepthToggle`, `VoteControl`. Plus `types.d.ts` (the canonical **data model**), `nuclear-energy.example.ts` (a populated fixture), and `Gallery.html` (live specimen). |
| Page mocks | Removed post-build (git history) — the shipped app is now the reference for **Home**, **Category Page**, **Desktop/Mobile/Poster/Social** Topic, **Search**, **Submit Your View**. |
| `RESPONSIVE.md` | Breakpoint + per-surface reflow intent for the desktop-only pages. |
| `SKILL.md` | Agent Skill manifest for reuse in Claude Code. |

---

## CONTENT FUNDAMENTALS

How Ideya writes. The voice is the product: editorially confident, neutral by posture, never preachy.

- **Tone:** calm, precise, intellectually serious but plainspoken. Explanatory, not persuasive. It earns trust by being *legible*, not by hedging. Think a great textbook or an Our World in Data explainer.
- **Person:** mostly **third-person and impersonal** ("most of the debate collapses onto…", "positions scramble partisan lines"). Addresses the reader as **"you"** only at action points ("submit your view", "where you can go further"). Never "we" in editorial copy — the product holds no house position.
- **Neutrality in language:** present each side via its **steelman** — the strongest, most sympathetic one-line case, written as that side would want it written. Describe what people *do* ("here's what people typically do"), never prescribe. No CTAs toward one side.
- **Casing:** sentence case everywhere for headings and UI. The only uppercase is the small tracked **section eyebrow** (`OVERVIEW`, `POSITIONS`). Title Case is reserved for proper nouns and named positions ("Climate Pragmatist").
- **Density:** Basics is terse and numeric (label / value / one-line note). Crux is the one place prose is allowed to breathe (1–3 full paragraphs). Everything else is tight.
- **Numbers:** tabular figures, lifecycle/qualified ("Deaths per TWh (lifecycle): 0.03"), always with a source link. Comparative context inline ("Coal ~24.6 · Gas ~2.8").
- **Citations:** inline, attached to the claim — "source ↗" links, never a separate references page.
- **Punctuation:** mid-dots (`·`) to pack comparisons; en-dashes for ranges; sparing italics for steelman lines and contested terms.
- **No emoji.** None in product copy or chrome. (The model's `icon` field permits an emoji fallback, but the design uses Phosphor glyphs.)
- **Vibe in one line:** *"Make the shape of hard issues legible."* Confident curation, zero theatrics.

**Specimen copy (from the Nuclear Energy topic):**
- Summary: *"Fission-based electricity generation — among the lowest-carbon and lowest-death-per-TWh sources, but with stubborn Western cost problems and a debate that scrambles partisan lines."*
- Steelman: *"Deep decarbonization on the timeline climate science demands cannot rely on weather-dependent renewables alone; nuclear is the only proven, scaled, firm low-carbon source."*
- Crux opener: *"Once the rhetorical heat is stripped away, most of the nuclear debate collapses onto a narrower disagreement…"*

---

## VISUAL FOUNDATIONS

**Overall:** modern, minimalistic, typography-driven, generously spaced. **Mobile-first**; desktop is a graceful expansion. Every page must also survive as a flat, printable/shareable static image (the "condensed" depth). The chrome is near-monochrome and quiet so that the *only* color a reader sees is meaningful — the per-topic position colors.

- **Color — three disciplined systems, never mixed:** a single **green-tinted neutral "ink" ramp** carries the chrome (`#f7f9f7` bg → `#141813` text). **(1) Brand:** the logo green `#4CB050` (`--green-500/600/700` + tint) is the one accent — action, links-as-action, active states, brand touches; used throughout product chrome. **(2) Positions** (`--pos-*`, muted equal-weight peers — green/blue/amber/rust/purple/teal) distinguish named positions *within a topic*; assigned per-topic, reused across topics, no fixed meaning. **(3) Categories** (`--cat-*`, one muted hue each) identify top-level categories in **discovery tiers only** (Home, Category pages, search) — never on a Topic page. No orange/lime (Ideya retired), no gradients, no decorative color.
- **Type:** **Plus Jakarta Sans — one family, the whole system.** Weights 400–800; hierarchy from **weight + size + tracking**, not a second face. Roles: **display = 800** (titles, section eyebrows, hero stats, tight tracking), **text = 400–600** (body/UI). **Inter** is kept only as a **tabular** utility for dense number tables (`--font-tabular`). Section eyebrows are uppercase with `+0.06em` tracking and `ink-400`. Body ~1.5–1.65 line-height, capped at a 68ch measure. **Optical scaling is by medium** — poster: huge/−3.5% tracking/0.98 leading; web: medium; mobile: compact — same family, different optical settings (see the "Type at Three Scales" card). Icon weight tracks type weight: fill (poster) → duotone (web) → line (mobile).
- **Spacing:** Tailwind 4px scale. Big rhythm between sections (`mt-14` = 56px); calm 16–20px card padding. Container is `max-w-5xl` (1024px) with 16–24px gutters.
- **Backgrounds:** flat fills only. Page is `ink-50`, cards are white. **No** images, gradients, textures, patterns, or hand illustration anywhere in chrome. (Topic content may include data charts via D3 / Observable Plot — line/bar, ink-on-white, color only when a series maps to a position.)
- **Cards:** white surface, **1px `ink-100` hairline border, no shadow**, `border-radius: 12px`. Hover lifts the border to `ink-200` (180ms). This flat, bordered card is the workhorse — stat cards, position cards, question rows, action cards all share it.
- **The Crux** is the one section that **inverts to a full dark band** (`--ink-900`, white text, green highlight) — the synthesis set apart as the page's visual anchor and tonal centerpiece. (This supersedes the earlier light-block-with-left-rule treatment.)
- **Borders:** hairline `1px ink-100` everywhere (dividers, card edges, section underlines). Stronger `ink-200` on hover/active. The biggest contrast move is the dark Crux band, not a rule.
- **Shadows:** essentially none. The system is flat. Shadow exists **only** for transient overlays — search dropdown (`shadow-pop`), modals/sheets (`shadow-overlay`). A card never casts a shadow.
- **Radii:** `8` (small controls) · `12` (cards) · `16` (crux/emphasis) · `9999` (chips, badges, search field, vote pills). Pills are used heavily for anything taxonomic or interactive-inline.
- **Transparency / blur:** not part of the language. No glassmorphism. Overlays are solid white with a hairline + soft shadow.
- **Hover states:** borders darken `ink-100 → ink-200`; ghost controls get an `ink-50` fill; links gain an underline (`text-underline-offset: 2px`). No color shifts.
- **Press states:** quiet — no scale/bounce. Active controls deepen fill by one ink step. Selected vote/agree states tint with the position color at ~8% (`color-mix`).
- **Motion:** quiet and short. `cubic-bezier(0.2,0,0,1)`, 120–280ms. Fades and small position moves only — **no bounce, no spring, no parallax.** Re-ordering (importance votes) animates list position; that's the most expressive motion in the product.
- **Imagery color vibe:** N/A for chrome (there is none). When data viz appears, it's ink-on-white, restrained, with position-color accents — never warm/cool photographic grading.
- **Layout rules:** single centered column (`max-w-5xl`); the topic page is **one vertically-sequenced artifact**, not a tabbed app — all six sections always render in fixed order when content exists. Sticky header is a candidate; nothing else is fixed. Related-topic chips and category badges fold *into* the Overview — never a separate footer band.
- **Focus:** visible 2px ring in `#3b7ea1` (the one functional blue), 2px offset — accessibility, kept distinct from position-blue's meaning.

---

## ICONOGRAPHY

- **System:** **Phosphor Icons**, **duotone** weight — a two-tone glyph (solid accent over a lighter ground) that reads as soft and editorial, not utilitarian. Drawn ~16–30px depending on context; they inherit `ink`/accent color from context. The model's `icon` fields name Phosphor icons (e.g. `atom`, `leaf`, `scales`, `flask`, `target`).
- **Weight by medium:** duotone is the default (web). Heavier surfaces can go **fill** (poster, emphasis); the smallest mobile contexts may drop to a lighter weight. Within one surface, stay on one weight.
- **Where icons appear:** topic/category glyph beside the title, search glyph, vote carets (fill when active), the `↗` on source/action links, menu, info affordance, the empirical/value tags (`flask` / `heart`), the Crux `target`, Basics chart glyphs, section eyebrow marks.
- **Delivery:** load from CDN — `https://unpkg.com/@phosphor-icons/web` (duotone + fill stylesheets), used as `<i class="ph-duotone ph-atom">`. No custom-drawn icon set.
- **Unicode as icon:** sparingly — the external-link `↗` and mid-dot `·` are used as typographic icons inline.
- **Emoji:** **not used.** The data model allows an emoji in `icon` as a fallback, but the language is Phosphor-only.
- **Brand mark:** the Ideya double-leaf / infinity glyph (`assets/ideya-mark.png`) is a *logo*, not an icon — never recolored, never used inline as a UI icon.

---

## Logo & brand usage

- **Primary logo:** the **Infinity Project** logo (`assets/infinity-logo.svg`, raster `assets/infinity-logo.jpg`) — the infinity glyph of two leaves reversed in white on the brand-green rounded badge, stacked over an all-caps geometric “INFINITY PROJECT” wordmark.
- **Mark:** the badge alone (`assets/ideya-mark.png`) is the app icon / favicon bug.
- **In-product wordmark:** drop “Project” — pair the mark with **“Ideya”** set in Plus Jakarta Sans Bold ink. This is what the nav and shareable artifacts use.
- **Construction:** white double-leaf / infinity symbol on the brand green (`#4CB050`).
- **Discipline:** keep the mark on the brand green; never recolor it. Chrome stays in the green-tinted ink ramp; the in-product wordmark is ink, not a colored logotype.

> The parent-org “Ideya” branding (orange wordmark, lime green) has been dropped from the system — the product brand is **Infinity**, using the Infinity Project mark.
