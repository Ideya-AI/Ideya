# Topic iconography — theme (decided 2026-06-20)

Two icons per topic:
- **Primary** — a unique, bespoke illustration; the topic's hero image (later the first slide of a per-topic image carousel).
- **Secondary** — a stock **Phosphor duotone** glyph for small UI spots (section rail, chips, discovery cards, search).

## Primary theme — "monoline duotone topic illustrations"
Synthesis of the references (Gorges Beer Co · Phosphor · Flaticon Lineal):
- **Line style (Gorges / Flaticon Lineal):** minimal, **one consistent stroke weight** across the whole set, rounded caps/joins; clean monoline with no fussy internal detail. **Uniform optical size + padding** so the set reads as one family.
- **Composition / complexity (decided 2026-06-20):** the primary is a small **scene** — about **2.5–3.5× the complexity of a single Gorges icon**, achieved by **combining several simple sub-icons in a larger space**, NOT by making any one element more detailed. Each sub-icon stays Gorges-simple; the richness is in the combination. (Nuclear = cooling towers + atom + transmission pylon + hill line.)
- **Duotone (from Phosphor):** single color, two tones — full-strength line + a soft (~16–18%) fill of the **same hue** on the main mass(es). Not multi-color.
- **Filled masses, never outline-only (2026-08 rule):** EVERY major element carries the soft fill — thin unfilled linework nearly vanished at 40px on ai-takeoff; since briefs demanded fills on all masses, winners have come from the first batch. Prompts should forbid "outline-only" major elements explicitly.
- **Color:** the topic's **category color**, two tones (energy = green, bio = rose, …). Lives in the existing rounded-square category-tinted tile.
- **Legibility:** reads from ~40px up to hero size.

## Approach (decided 2026-06-20)
Each topic's art is **bespoke** — its own composition, one at a time. This is **not** a fixed vocabulary / composition system; pieces may be reused across topics only when genuinely warranted. **Quality over coverage** — a topic ships only when its art is great; a weak one isn't worth having and a large count doesn't matter. The **pipeline proposes and a human can swap** — stage 3 of `author-topic` auto-generates and picks a winner, but every candidate is kept in `research/icons/candidates/<slug>/` so the owner can override the pick anytime.

## Automated generation (2026-07) — stage 3 of the authoring engine
The icon is produced automatically under the rules above; the operational procedure
(brief → generate → pick → post-process → provenance) lives in `research/ENGINE.md`
§5 stage 3. This file stays the visual spec the pipeline scores against.
