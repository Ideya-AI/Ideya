# Food, Land & the Living World — category art brief

The category's primary art, shown only on its own category page, in the same hero card as a topic page
(about 540px wide on desktop, 300px on
mobile) beside the title. It never sits next to another category's art. The scene sits at the full house
range, about 2.5-3.5x the complexity of one glyph, five or six elements, because it shows at hero size.

Style, composition rules and negatives common to every icon live in `research/pipeline/icon_prompt.py`;
this file supplies only the scene and this subject's own negatives. The prompt below is assembled by
that script (`icon_prompt.py brief research/categories/food-land/icon.md`), never edited by hand.

Deliverable: `static/img/categories/food-land.png`, square, normalized with
`icon_prompt.py normalize <candidate> static/img/categories/food-land.png` (trim, 8% pad, 1:1, 512px, white).
Candidates go under `research/categories/food-land/candidates/`.

## Scene
a broad round-canopied tree as the dominant focal mass on the crest of a rolling hill; a barn
with a rounded roof overlapping the hill's slope in front of the tree; a small windmill or water
pump at the right on the far hill; a few wheat stalks in a bunch at the left in front of the
hill; four curved crop furrows sweeping across the lower frame from edge to edge as the
connective element; a short winding stream at the lower-left with a single water droplet above
it; the ground is the rolling hill itself with a second hill and a distant treeline behind.

## Negatives
cows, animals of any kind, tractors, fences with barbed wire, dead crops, fire, forks and
knives, plates.

## Prompt
> A minimalist flat vector-style icon illustration, in a clean editorial line-art style: a broad round-canopied tree as the dominant focal mass on the crest of a rolling hill; a small barn with a rounded roof overlapping the hill's slope in front of the tree; three curved crop furrows sweeping across the lower frame from edge to edge as the connective element; a small water droplet or a short winding stream near the left; the ground is the rolling hill itself with a second hill behind.
>
> Composition: one dominant focal mass with smaller supporting elements at clearly different scales (big, medium, small); at least one element overlaps another so the scene has depth; the ground is a gentle curve, never a flat line; one connective element runs across the frame to tie the pieces together. A single coherent scene, not a row of separate objects. Centered with generous, even padding.
>
> Style: monoline line art with ONE uniform stroke weight on every element, including the thinnest wisps and lines. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small. No fussy internal detail.
>
> Color: a single hue, two tones only. Draw all lines in solid #7d8a4e, and give every major mass a clearly visible soft fill of the same hue at about 15-18% opacity, so the duotone is obviously present rather than white interiors. No other colors, no gradients, no shadows, no 3D, no texture.
>
> Important: NO border, NO frame, NO box or outline around the scene, just the illustration on a plain white background. No text, letters, or numbers. No human figures or faces. Calm, neutral, editorial mood: show the subject plainly, neither celebrating nor warning. Also avoid: cows, animals of any kind, tractors, fences with barbed wire, dead crops, fire, forks and knives, plates.

## Selection
Round 1, two samples of the one scene, judged by eye at tile size and full size. Picked `r1-a`: fuller duotone and the barn sits on the slope; r2-a is linework-heavy and fades at tile size. Normalized to `static/img/categories/food-land.png`.

Round 3 (scene expanded to hero complexity), two samples, judged against the round-1 incumbent. Picked `r3-a`: wheat, windmill and treeline with the barn on the slope; r3-b fills the stream and loses the furrow rhythm. Replaced `static/img/categories/food-land.png`.
