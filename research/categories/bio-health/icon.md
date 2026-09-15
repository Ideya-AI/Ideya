# Bio, Health & the Human Body — category art brief

The category's primary art, shown only on its own category page, in the same hero card as a topic page
(about 540px wide on desktop, 300px on
mobile) beside the title. It never sits next to another category's art. The scene sits at the full house
range, about 2.5-3.5x the complexity of one glyph, five or six elements, because it shows at hero size.

Style, composition rules and negatives common to every icon live in `research/pipeline/icon_prompt.py`;
this file supplies only the scene and this subject's own negatives. The prompt below is assembled by
that script (`icon_prompt.py brief research/categories/bio-health/icon.md`), never edited by hand.

Deliverable: `static/img/categories/bio-health.png`, square, normalized with
`icon_prompt.py normalize <candidate> static/img/categories/bio-health.png` (trim, 8% pad, 1:1, 512px, white).
Candidates go under `research/categories/bio-health/candidates/`.

## Scene
a tall DNA double helix rising on a diagonal from lower-left to upper-right as the dominant
focal mass and the connective element crossing the frame; a rounded medicine capsule overlapping
the lower rungs of the helix; a laboratory flask beside it at the base with a little liquid
inside; a small microscope low at the right; a small heart with a short pulse line tucked near
the upper-left; a small pill bottle behind the flask; the ground is the curved rim of a wide
petri dish holding the base of the scene.

## Negatives
syringes pointed at anything, skulls, blood, surgical tools, crosses, caducei with snakes,
skeletons.

## Prompt
> A minimalist flat vector-style icon illustration, in a clean editorial line-art style: a tall DNA double helix rising on a diagonal from lower-left to upper-right as the dominant focal mass and the connective element crossing the frame; a rounded medicine capsule overlapping the lower rungs of the helix; a small laboratory flask beside it at the base; a small heart shape with a short pulse line tucked near the upper-left; the ground is the curved rim of a petri dish.
>
> Composition: one dominant focal mass with smaller supporting elements at clearly different scales (big, medium, small); at least one element overlaps another so the scene has depth; the ground is a gentle curve, never a flat line; one connective element runs across the frame to tie the pieces together. A single coherent scene, not a row of separate objects. Centered with generous, even padding.
>
> Style: monoline line art with ONE uniform stroke weight on every element, including the thinnest wisps and lines. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small. No fussy internal detail.
>
> Color: a single hue, two tones only. Draw all lines in solid #b0567f, and give every major mass a clearly visible soft fill of the same hue at about 15-18% opacity, so the duotone is obviously present rather than white interiors. No other colors, no gradients, no shadows, no 3D, no texture.
>
> Important: NO border, NO frame, NO box or outline around the scene, just the illustration on a plain white background. No text, letters, or numbers. No human figures or faces. Calm, neutral, editorial mood: show the subject plainly, neither celebrating nor warning. Also avoid: syringes pointed at anything, skulls, blood, surgical tools, crosses, caducei with snakes, skeletons.

## Selection
Round 1, two samples of the one scene, judged by eye at tile size and full size. Picked `r1-a`: clean white dish and clear helix; r1-b adds motion lines and a filled dish that muddies the tile. Normalized to `static/img/categories/bio-health.png`.

Round 3 (scene expanded to hero complexity), two samples, judged against the round-1 incumbent. Picked `r3-a`: helix, capsule, flask, bottle, microscope on a filled dish; r3-b is thin and the dish floats. Replaced `static/img/categories/bio-health.png`.
