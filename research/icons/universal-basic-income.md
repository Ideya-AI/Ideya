# Universal Basic Income — primary icon art brief

Handoff brief for an illustrator or image/vector tool. Full style theme: `../../ICONOGRAPHY.md`.
Template sibling: `nuclear-energy.md` (the tuned reference).

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
**2.5–3.5× the complexity of a single Gorges icon**. Generate wide (3:2); framing is normalized in post (trim to content, ~8% pad,
fit 3:2 on white). Legible from ~56px to hero size, readable on a dark background.

## Elements — promise *and* peril
The debate is cash-for-everyone vs. targeting, jobs, and services — the art should
hold the whole design question, not sell UBI:
- **An open upturned hand with a coin above it** — the unconditional floor; the focal point.
- **A row of three identical small human figures, one coin over each** — universality:
  everyone gets the same, no test.
- **A tension element: a small two-pan balance scale weighing a coin against a wrench** —
  cash vs. work/services, and the cost question. Matter-of-fact, not editorializing.
- **A low ground/horizon line** — grounds the scene (mirrors the nuclear composition).

## Mood
Neutral and editorial — neither pro- nor anti-UBI; the guarantee (a floor under
everyone) and the contest (what a dollar should buy, and on what terms) held together
in one calm image.

## Avoid
Photorealism; more than one color; gradients/shadows; dollar-sign clichés piled up;
fussy internal detail; clutter; anything that reads as advocacy.

## Deliverable
Ideally **vector (SVG)**, single-color, transparent ground. PNG accepted
(the pipeline is raster-primary).

## Generation prompt (Nano Banana / Gemini)
**Frameless** — the art has NO drawn border. The CSS tile renders the rounded-square
frame. Lessons carried over from the nuclear generation: force the soft fill to
~15–18% (it renders near-invisible if unstressed) and force uniform stroke weight
(thin secondary elements drift thinner).

**Fresh-generation prompt:**
> A minimalist flat vector-style icon illustration of a universal basic income scene, in a clean editorial line-art style. Combine several simple symbols into one small, balanced composition: an open upturned hand with a single coin floating above the palm as the focal point, a row of three identical simple human figures each with a small coin above their head, a small two-pan balance scale weighing a coin on one pan against a wrench on the other, and a low horizon line grounding the scene.
>
> Important: NO border, NO frame, NO box or outline around the scene — just the illustration itself on a plain background.
>
> Style: monoline line art with ONE uniform stroke weight on every element — the hand, the figures, the coins, the scale, and the horizon must all be exactly the same thickness. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small. No fussy internal detail.
>
> Color: a single warm amber hue, two tones only. Draw all lines in solid amber (#b98a35), and give the main masses a clearly visible soft fill of the same amber at about 15–18% opacity — specifically fill the hand, the coins, the figures' bodies, and the scale pans with a light amber tint, so the two-tone duotone is obviously present rather than white interiors. No other colors, no gradients, no shadows, no 3D, no texture.
>
> Composition: centered with generous, even padding; balanced optical weight. Plain white background. Calm, neutral, editorial mood — even-handed, neither promoting nor criticizing basic income. No text, letters, or currency symbols other than the plain circular coins.

**Edit-mode instruction (after the first generation, feed the concept back in):**
> Using this image, keep the same composition, elements, and layout, but: (1) remove any border or frame around the scene entirely; (2) add a clearly visible soft light-amber fill (~15% opacity of the same hue) inside the hand, coins, figures, and scale pans so it reads as a two-tone duotone instead of mostly white; (3) make every line exactly the same thickness, matching the main outline weight. Keep it flat, single amber hue, no gradients, shadows, extra colors, or text.

**Notes:**
- Over-generate on the **balance scale** and the **coins-over-heads** row; those are
  the elements most likely to come out malformed or over-detailed.
- White background is intentional — the primary sits on a neutral tile; the frame
  comes from the tile, not the art.
- After generating: save as `static/img/topics/universal-basic-income.png` (match
  nuclear's location/naming), set `Topic.primary_art = "img/topics/universal-basic-income.png"`,
  and regenerate the social PNGs (`render_social --slug universal-basic-income --formats og,sq,pt`).
