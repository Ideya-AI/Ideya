# Climate & Energy — category art brief

The category's primary art, shown only on its own category page, in the same hero card as a topic page
(about 540px wide on desktop, 300px on
mobile) beside the title. It never sits next to another category's art. The scene sits at the full house
range, about 2.5-3.5x the complexity of one glyph, five or six elements, because it shows at hero size.

Style, composition rules and negatives common to every icon live in `research/pipeline/icon_prompt.py`;
this file supplies only the scene and this subject's own negatives. The prompt below is assembled by
that script (`icon_prompt.py brief research/categories/climate-energy/icon.md`), never edited by hand.

Deliverable: `static/img/categories/climate-energy.png`, square, normalized with
`icon_prompt.py normalize <candidate> static/img/categories/climate-energy.png` (trim, 8% pad, 1:1, 512px, white).
Candidates go under `research/categories/climate-energy/candidates/`.

## Scene
a tall wind turbine as the dominant focal mass, blades mid-turn; an array of four tilted solar
panels overlapping the base of the turbine's tower so the panels sit in front of it; a small
cooling tower with a curl of steam far left behind the hills; a small battery block low at the
right with a charge mark; a sun half-risen at the horizon; power lines strung across the whole
frame from a pylon at the left edge as the connective element; the ground is a rolling hill with
a second lower hill behind.

## Negatives
smokestacks, oil derricks, fire, flooding, thermometers, melting ice, dead trees, mushroom
clouds.

## Prompt
> A minimalist flat vector-style icon illustration, in a clean editorial line-art style: a tall wind turbine as the dominant focal mass, its three blades mid-turn; a tilted solar panel array of three panels overlapping the base of the turbine's tower so panel sits in front of tower; a small sun half-risen at the horizon on the right; power lines strung across the frame from a small pylon at the left edge as the connective element; the ground is a rolling hill with a second, lower hill behind it.
>
> Composition: one dominant focal mass with smaller supporting elements at clearly different scales (big, medium, small); at least one element overlaps another so the scene has depth; the ground is a gentle curve, never a flat line; one connective element runs across the frame to tie the pieces together. A single coherent scene, not a row of separate objects. Centered with generous, even padding.
>
> Style: monoline line art with ONE uniform stroke weight on every element, including the thinnest wisps and lines. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small. No fussy internal detail.
>
> Color: a single hue, two tones only. Draw all lines in solid #3f9a6a, and give every major mass a clearly visible soft fill of the same hue at about 15-18% opacity, so the duotone is obviously present rather than white interiors. No other colors, no gradients, no shadows, no 3D, no texture.
>
> Important: NO border, NO frame, NO box or outline around the scene, just the illustration on a plain white background. No text, letters, or numbers. No human figures or faces. Calm, neutral, editorial mood: show the subject plainly, neither celebrating nor warning. Also avoid: smokestacks, oil derricks, fire, flooding, thermometers, melting ice, dead trees, mushroom clouds.

## Selection
Round 1, two samples of the one scene, judged by eye at tile size and full size. Picked `r1-a`: turbine dominant, panel overlaps the tower, two hills; r1-b is lower-contrast and flatter. Normalized to `static/img/categories/climate-energy.png`.

Round 3 (scene expanded to hero complexity), two samples, judged against the round-1 incumbent. Picked `r3-a`: turbine over panels with cooling tower steam, battery and sun; r3-b draws a circle around the blades. Replaced `static/img/categories/climate-energy.png`.
