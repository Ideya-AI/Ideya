# Existential & Global Catastrophic Risk — category art brief

The category's primary art, shown only on its own category page, in the same hero card as a topic page
(about 540px wide on desktop, 300px on
mobile) beside the title. It never sits next to another category's art. The scene sits at the full house
range, about 2.5-3.5x the complexity of one glyph, five or six elements, because it shows at hero size.

Style, composition rules and negatives common to every icon live in `research/pipeline/icon_prompt.py`;
this file supplies only the scene and this subject's own negatives. The prompt below is assembled by
that script (`icon_prompt.py brief research/categories/global-risk/icon.md`), never edited by hand.

Deliverable: `static/img/categories/global-risk.png`, square, normalized with
`icon_prompt.py normalize <candidate> static/img/categories/global-risk.png` (trim, 8% pad, 1:1, 512px, white).
Candidates go under `research/categories/global-risk/candidates/`.

## Scene
a large globe with simple continent shapes as the dominant focal mass; an asteroid with a
curving motion trail arcing across the frame from the upper-left and passing in front of the
globe's upper edge as the connective element; a rounded shield overlapping the globe's lower-
right edge; a radar dish low at the left pointed upward; a small satellite with two solar wings
at the upper-right; a small laboratory flask low at the right; the ground is a curved orbit arc
beneath the globe with a small moon on it.

## Negatives
mushroom clouds, explosions, fire, skulls, cracks in the earth, floods, viruses with spikes,
warning triangles, clocks.

## Prompt
> A minimalist flat vector-style icon illustration, in a clean editorial line-art style: a large globe with simple continent shapes as the dominant focal mass; a small asteroid with a curving motion trail arcing across the frame from the upper-left and passing in front of the globe's upper edge as the connective element; a rounded shield overlapping the globe's lower- right edge; a small radar dish low at the left pointed upward; the ground is a curved orbit arc beneath the globe.
>
> Composition: one dominant focal mass with smaller supporting elements at clearly different scales (big, medium, small); at least one element overlaps another so the scene has depth; the ground is a gentle curve, never a flat line; one connective element runs across the frame to tie the pieces together. A single coherent scene, not a row of separate objects. Centered with generous, even padding.
>
> Style: monoline line art with ONE uniform stroke weight on every element, including the thinnest wisps and lines. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small. No fussy internal detail.
>
> Color: a single hue, two tones only. Draw all lines in solid #b3404f, and give every major mass a clearly visible soft fill of the same hue at about 15-18% opacity, so the duotone is obviously present rather than white interiors. No other colors, no gradients, no shadows, no 3D, no texture.
>
> Important: NO border, NO frame, NO box or outline around the scene, just the illustration on a plain white background. No text, letters, or numbers. No human figures or faces. Calm, neutral, editorial mood: show the subject plainly, neither celebrating nor warning. Also avoid: mushroom clouds, explosions, fire, skulls, cracks in the earth, floods, viruses with spikes, warning triangles, clocks.

## Selection
Round 1, two samples of the one scene, judged by eye at tile size and full size. Picked `r1-a`: white orbit ground keeps the globe crisp; r1-b heavy fills merge globe, shield and ground at 92px. Normalized to `static/img/categories/global-risk.png`.

Round 3 (scene expanded to hero complexity), two samples, judged against the round-1 incumbent. Picked `r3-a`: satellite, moon and flask added, asteroid trail passes the globe; r3-b draws a Saturn-like ring. Replaced `static/img/categories/global-risk.png`.
