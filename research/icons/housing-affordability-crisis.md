# What Drives the Housing Affordability Crisis — primary icon art brief

Handoff brief for an illustrator or image/vector tool. Full style theme: `../../ICONOGRAPHY.md`.
Template siblings: `nuclear-energy.md` (the tuned reference), `universal-basic-income.md`.

## Use
The topic's **primary hero image**. Shows large on the topic page, poster, and social
cards; also reduced into a rounded-square tinted tile and shown on a dark band. Must
read both large and small, on light and dark.

## Style (non-negotiable)
- **Minimal monoline** — ONE consistent stroke weight across the whole image, rounded
  caps/joins. References: **Gorges Beer Co** menu icons, **Flaticon "Lineal."**
- **Duotone, single color, two tones** — line at full strength + a soft (~16%) fill of
  the **same hue** on the masses. No second color, no gradients, no shadows.
- **Color:** the category color (Economy & Work = **amber**, `#b98a35`). Deliver
  single-color so it can be recolored per category.
- Flat, clean, editorial.

## Composition
A small bespoke **scene** combining several *simple* sub-icons in one frame — about
**2.5–3.5× the complexity of a single Gorges icon**. Generate wide (3:2); framing is
normalized in post (trim to content, ~8% pad, fit 3:2 on white). Legible from ~40px
to hero size, readable on a dark background.

## Elements — promise *and* peril
The debate is about **why** housing costs so much — restricted supply/zoning,
concentrated demand and inequality, investor/financialized ownership, rent rules,
land taxation. The art must hold the question, not sell any one diagnosis:
- **A simple gabled house raised on a tall rising bar/plinth** — the focal point:
  cost climbing out of reach.
- **An upward arrow beside the plinth** — the price trajectory, plain and
  matter-of-fact.
- **A small human figure at ground level, looking up at the raised house** — the
  affordability gap: the home is there, the reach isn't.
- **A tension element: a second, smaller house behind a simple fence/barrier
  segment, with a small padlock over its door** — gestures at the rival diagnoses
  (can't build it / can't buy it) without endorsing either. Neutral, not accusatory.
- **A low ground/horizon line** — grounds the scene (mirrors the nuclear and UBI
  compositions).

## Mood
Neutral and editorial — a diagnostic question held calmly: homes exist, prices climb,
people stand outside, and the causes are contested. Not an eviction scene, not a
developer ad.

## Avoid
Photorealism; more than one color; gradients/shadows; dollar signs or price tags with
text; crossed-out or "banned" symbols that pick a villain; sad/desperate figures;
fussy internal detail (window grids, brickwork); clutter; anything that reads as
advocacy for one fix.

## Deliverable
Ideally **vector (SVG)**, single-color, transparent ground. PNG accepted
(the pipeline is raster-primary).

## Generation prompt (Nano Banana / Gemini)
**Frameless** — the art has NO drawn border. The CSS tile renders the rounded-square
frame. Lessons carried over from the nuclear and UBI generations: force the soft fill
to ~15–18% (it renders near-invisible if unstressed) and force uniform stroke weight
(thin secondary elements drift thinner).

**Fresh-generation prompt:**
> A minimalist flat vector-style icon illustration of a housing affordability scene, in a clean editorial line-art style. Combine several simple symbols into one small, balanced composition: as the focal point, a simple gabled house with one door sitting on top of a tall vertical bar or plinth that rises from the ground, with a plain upward-pointing arrow alongside the bar showing the climb; at ground level, a single simple human figure standing and looking up toward the raised house; to one side, a second smaller gabled house behind a short simple fence segment, with a small padlock over its door. A single thin, straight horizontal ground line runs under the whole scene — no hill, no landscape.
>
> Important: NO border, NO frame, NO box or outline around the scene — just the illustration itself on a plain background. Keep the composition compact and centered, not spread wide.
>
> Style: monoline line art with ONE uniform stroke weight on every element — the houses, the bar, the arrow, the figure, the fence, the padlock, and the ground line must all be exactly the same thickness. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small. No fussy internal detail — no window grids, no brickwork, no roof tiles.
>
> Color: a single warm amber hue, two tones only. Draw all lines in solid amber (#b98a35), and give the main masses a clearly visible soft fill of the same amber at about 15-18% opacity — fill the house bodies, the rising bar, the figure, and the padlock with a light amber tint so the two-tone duotone is obviously present rather than white interiors. No other colors, no gradients, no shadows, no offset or misregistered fills, no 3D, no texture.
>
> Composition: wide 3:2 aspect, centered with generous, even padding; balanced optical weight. Plain white background. Calm, neutral, editorial mood — a question about why housing costs so much, neither blaming anyone nor promoting any fix. No text, letters, words, numbers, dollar signs, or price tags anywhere in the image.

**Edit-mode instruction (after the first generation, feed the concept back in):**
> Using this image, keep the same composition, elements, and layout, but: (1) remove any border or frame around the scene entirely; (2) add a clearly visible soft light-amber fill (~15% opacity of the same hue) inside the house bodies, the rising bar, the figure, and the padlock so it reads as a two-tone duotone instead of mostly white; (3) make every line exactly the same thickness, matching the main outline weight. Keep it flat, single amber hue, no gradients, shadows, extra colors, or text.

**Notes:**
- Over-generate on the **padlock** and the **house-on-plinth** join; those are the
  elements most likely to come out malformed or over-detailed.
- White background is intentional — the primary sits on a neutral tile; the frame
  comes from the tile, not the art.
- After generating: save as `static/img/topics/housing-affordability-crisis.png`,
  set `Topic.primary_art = "img/topics/housing-affordability-crisis.png"`,
  and regenerate the social PNGs (`render_social --slug housing-affordability-crisis --formats og,sq,pt`).

## Selection

Winner: `candidates/housing-affordability-crisis/housing-affordability-crisis.gemini-3-pro-image.1.jpg` (round 1 of 1, 4 candidates). Chosen for the cleanest uniform monoline stroke, an obvious same-hue duotone fill, and the best-spaced hierarchy — the raised house + climb arrow + person looking up + padlocked house behind a fence all read at a glance, and it holds up best at 40px. Candidates 2/4 had a heavy plinth mass; 3 had a slight 3D roof plane. Promoted via `postprocess_icon.py` to `static/img/topics/housing-affordability-crisis.png` (1035×690, white ground).
