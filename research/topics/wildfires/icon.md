# Living With Wildfire — primary icon art brief

Handoff brief for an illustrator or image/vector tool. Full style theme: `docs/DESIGN.md` (Topic art).
Template siblings: `nuclear-energy.md` (the tuned reference), `universal-basic-income.md`,
`housing-affordability-crisis.md`.

## Use
The topic's **primary hero image**. Shows large on the topic page, poster, and social
cards; also reduced into a rounded-square tinted tile and shown on a dark band. Must
read both large and small, on light and dark.

## Style (non-negotiable)
- **Minimal monoline** — ONE consistent stroke weight across the whole image, rounded
  caps/joins. References: **Gorges Beer Co** menu icons, **Flaticon "Lineal."**
- **Duotone, single color, two tones** — line at full strength + a soft (~16%) fill of
  the **same hue** on the masses. No second color, no gradients, no shadows.
- **Color:** the category color (Climate, Energy & Environment = **energy green**,
  `#4a9d6c`). Deliver single-color so it can be recolored per category.
- Flat, clean, editorial.

## Composition
A small bespoke **scene** combining several *simple* sub-icons in one frame — about
**2.5–3.5× the complexity of a single Gorges icon**. Generate wide (3:2); framing is
normalized in post (trim to content, ~8% pad, fit 3:2 on white). Legible from ~40px
to hero size, readable on a dark background.

## Elements — promise *and* peril
The debate is over the decisive lever against worsening wildfire — the landscape
(restored good fire, thinning), the built edge (ember-hardened homes), the firefight,
or the climate. The art should show the **contested relationship between fire, the
land, and the built edge** — fire as both tool and threat — not a disaster and not a
generic flame:
- **A stylized flame meeting a short treeline of two or three simple conifers** — the
  focal point: fire and forest in one image, the flame lapping at the first tree,
  matter-of-fact rather than raging.
- **A clear firebreak gap** between the trees and the house — a deliberate empty
  strip in the vegetation where the burn is meant to stop: the managed line.
- **A small gabled house with a plain solid roof** on the far side of the gap — the
  hardened built edge, simple and unadorned.
- **A dotted ember arc** — three or four small dots arcing from the flame over the
  firebreak toward the house's roof: the ember threat that hardening answers.
- **A drip torch** — a small handheld canister with a curved spout and a single tiny
  flame drop at its tip, standing near the firebreak — intentional fire: prescribed
  and cultural burning as stewardship, not accident.
- **A low ground/horizon line** — grounds the scene (mirrors the sibling
  compositions).

## Mood
Neutral and editorial — fire held calmly as ecological force, human tool, and threat
to the edge, all in one image. A question about where to work — the land, the home,
or the line between — not a catastrophe scene and not a pro-burning ad.

## Avoid
Photorealism; more than one color (no red/orange fire — the whole image is the single
green duotone); gradients/shadows; billowing smoke clouds dominating the scene; fire
trucks, helicopters, or airtankers as hero elements; burning or destroyed homes;
fleeing figures or any fear imagery; charred/blackened devastation; fussy internal
detail (bark texture, shingle lines, window grids); clutter; anything that reads as
advocacy for one lever.

## Deliverable
Ideally **vector (SVG)**, single-color, transparent ground. PNG accepted
(the pipeline is raster-primary).

## Generation prompt (Nano Banana / Gemini)
**Frameless** — the art has NO drawn border. The CSS tile renders the rounded-square
frame. Lessons carried over from the earlier generations: force the soft fill to
~15–18% (it renders near-invisible if unstressed) and force uniform stroke weight
(thin secondary elements drift thinner).

**Fresh-generation prompt:**
> A minimalist flat vector-style icon illustration of a living-with-wildfire scene, in a clean editorial line-art style. Combine several simple symbols into one small, balanced composition: on the left, a single stylized flame with two or three soft rounded tongues as the focal point, lapping at a short row of two or three simple triangular conifer trees; then a deliberate empty gap in the vegetation — a firebreak — with a small drip torch standing in it (a simple handheld canister with a curved downward spout and one tiny flame drop at its tip); on the right, a small simple gabled house with a plain solid roof and one door; and a gentle arc of three or four small round ember dots curving from the flame over the gap toward the house's roof. A single thin, straight horizontal ground line runs under the whole scene — no hill, no landscape.
>
> Important: NO border, NO frame, NO box or outline around the scene — just the illustration itself on a plain background. Keep the composition compact and centered, not spread wide.
>
> Style: monoline line art with ONE uniform stroke weight on every element — the flame, the trees, the drip torch, the house, the ember dots, and the ground line must all be exactly the same thickness. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small, about 2.5 to 3.5 times the complexity of one simple glyph — each element stays simple, the richness is the combination. No fussy internal detail — no bark texture, no shingle lines, no window grids.
>
> Color: a single green hue, two tones only. Draw all lines in solid green (#4a9d6c), and give the main masses a clearly visible soft fill of the same green at about 16-18% opacity — fill the flame body, the tree canopies, the house body, and the drip torch canister with a light green tint so the two-tone duotone is obviously present rather than white interiors. Absolutely no red, orange, or yellow on the flame — it stays the same green as everything else. No other colors, no gradients, no shadows, no offset or misregistered fills, no 3D, no texture.
>
> Composition: wide 3:2 aspect, centered with generous, even padding; balanced optical weight. Plain white background. Calm, neutral, editorial mood — fire, forest, and home held together matter-of-factly, neither a disaster scene nor an advocacy image. No smoke clouds, no fire trucks, no helicopters, no people. No text or letters anywhere in the image.

**Edit-mode instruction (after the first generation, feed the concept back in):**
> Using this image, keep the same composition, elements, and layout, but: (1) remove any border or frame around the scene entirely; (2) add a clearly visible soft light-green fill (~16% opacity of the same hue) inside the flame, the tree canopies, the house body, and the drip torch so it reads as a two-tone duotone instead of mostly white; (3) make every line exactly the same thickness, matching the main outline weight — including the ember dots and the drip torch spout. Keep it flat, single green hue, no gradients, shadows, extra colors, or text.

**Notes:**
- Over-generate on the **drip torch** and the **ember-dot arc**; those are the
  elements most likely to come out malformed, over-detailed, or (for the embers)
  dropped entirely.
- Watch for the generator recoloring the flame red/orange — the single-green
  constraint is the most likely one to break on this topic.
- White background is intentional — the primary sits on a neutral tile; the frame
  comes from the tile, not the art.
- After generating: save as `static/img/topics/wildfires.png`, set
  `Topic.primary_art = "img/topics/wildfires.png"`, and regenerate the social PNGs
  (`render_social --slug wildfires --formats og,sq,pt`).

## Selection

Winner: `candidates/wildfires/wildfires.gemini-3-pro-image.1.jpg` (2026-08-01, first
generation round — no edits needed). Cleanest uniform monoline of the four and the
clearest reading of the brief's story: flame at the treeline, drip torch in the
firebreak gap, four-dot ember arc landing on the hardened house — every element
grounded on the single horizon line. Rejected: #2 (thin stroke vs the sibling set;
falling droplets read as rain), #3 (solid-to-dotted arc inconsistency; flame
dominates toward disaster-imagery), #4 (full-width dashed dome reads as
rainbow/shield, not ember travel).
