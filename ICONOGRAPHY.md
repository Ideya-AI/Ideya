# Topic iconography — theme (decided 2026-06-20)

Two icons per topic:
- **Primary** — a unique, bespoke illustration; the topic's hero image (later the first slide of a per-topic image carousel).
- **Secondary** — a stock **Phosphor duotone** glyph for small UI spots (section rail, chips, discovery cards, search).

## Primary theme — "monoline duotone topic illustrations"
Synthesis of the references (Gorges Beer Co · Phosphor · Flaticon Lineal):
- **Line style (Gorges / Flaticon Lineal):** minimal, **one consistent stroke weight** across the whole set, rounded caps/joins; clean monoline with no fussy internal detail. **Uniform optical size + padding** so the set reads as one family.
- **Composition / complexity (decided 2026-06-20):** the primary is a small **scene** — about **2.5–3.5× the complexity of a single Gorges icon**, achieved by **combining several simple sub-icons in a larger space**, NOT by making any one element more detailed. Each sub-icon stays Gorges-simple; the richness is in the combination. (Nuclear = cooling towers + atom + transmission pylon + hill line.)
- **Duotone (from Phosphor):** single color, two tones — full-strength line + a soft (~16–18%) fill of the **same hue** on the main mass(es). Not multi-color.
- **Color:** the topic's **category color**, two tones (energy = green, bio = rose, …). Lives in the existing rounded-square category-tinted tile.
- **Legibility:** reads from ~40px up to hero size.

## Approach (decided 2026-06-20)
Each topic's art is **bespoke** — its own composition, one at a time. This is **not** a fixed vocabulary / composition system; pieces may be reused across topics only when genuinely warranted. **Quality over coverage** — a topic ships only when its art is great; a weak one isn't worth having and a large count doesn't matter. The **pipeline proposes and a human can swap** — stage 3 of `author-topic` auto-generates and picks a winner, but every candidate is kept in `research/icons/candidates/<slug>/` so the owner can override the pick anytime.

## Automated generation (2026-07) — stage 3 of the author-topic pipeline
The icon is now produced automatically inside the `author-topic` skill, but under the same rules above:
1. **Brief** — a `fable` agent writes `research/icons/<slug>.md` from these guidelines + `research/icons/categories.md` + the two exemplar briefs; the `## Generation prompt` blockquote is what the generator reads.
2. **Generate** — `python research/icons/generate_icons.py --slug <slug> --n 4` → candidates in `research/icons/candidates/<slug>/`. `--edit <candidate> --edit-prompt "..."` refines an existing candidate (Nano Banana edit mode) instead of drawing fresh.
3. **Pick** — Claude reads the candidates and scores them against the checklist above (uniform monoline, same-hue duotone, category colour, 2.5–3.5× scene, white ground, 40px legible); refine-and-regenerate up to ~3 rounds; the winner gets a `## Selection` note appended to the brief.
4. **Post-process** — `python research/icons/postprocess_icon.py --slug <slug> --src <winner.jpg>` flattens onto white, trims, re-pads, and fits to the committed **1035×690** PNG at `static/img/topics/<slug>.png`, plus a 40px legibility thumb. Requires Pillow.
5. **Provenance** — `load_topic_draft --image-brief research/icons/<slug>.md` stores the generation prompt in `Topic.primary_image_prompt` so the art can be re-run or refined later.
