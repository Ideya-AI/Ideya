# Ethics & Philosophy — category art brief

The category's primary art, shown only on its own category page, in the same hero card as a topic page
(about 540px wide on desktop, 300px on
mobile) beside the title. It never sits next to another category's art. The scene sits at the full house
range, about 2.5-3.5x the complexity of one glyph, five or six elements, because it shows at hero size.

Style, composition rules and negatives common to every icon live in `research/pipeline/icon_prompt.py`;
this file supplies only the scene and this subject's own negatives. The prompt below is assembled by
that script (`icon_prompt.py brief research/categories/ethics/icon.md`), never edited by hand.

Deliverable: `static/img/categories/ethics.png`, square, normalized with
`icon_prompt.py normalize <candidate> static/img/categories/ethics.png` (trim, 8% pad, 1:1, 512px, white).
Candidates go under `research/categories/ethics/candidates/`.

## Scene
a balance scale with two hanging pans as the dominant focal mass, standing on a low curved
plinth; an open book overlapping the front of the plinth; an hourglass at the right foot of the
plinth; a small lantern with a flame at the left; a small feather quill resting across the book;
a winding path drawn as one curving ribbon running across the frame behind the scale from edge
to edge as the connective element, with a small tree standing on the path in the distance; the
ground is the gentle curve of the plinth's base.

## Negatives
human heads, busts, brains, halos, religious symbols, angels, devils, question marks,
lightbulbs.

## Prompt
> A minimalist flat vector-style icon illustration, in a clean editorial line-art style: a balance scale with two hanging pans as the dominant focal mass, standing on a low plinth; an open book overlapping the front of the plinth; a small hourglass at the right at the foot of the plinth; a winding path drawn as a single curving ribbon running across the frame behind the scale from left edge to right edge as the connective element; the ground is the gentle curve of the plinth's base.
>
> Composition: one dominant focal mass with smaller supporting elements at clearly different scales (big, medium, small); at least one element overlaps another so the scene has depth; the ground is a gentle curve, never a flat line; one connective element runs across the frame to tie the pieces together. A single coherent scene, not a row of separate objects. Centered with generous, even padding.
>
> Style: monoline line art with ONE uniform stroke weight on every element, including the thinnest wisps and lines. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small. No fussy internal detail.
>
> Color: a single hue, two tones only. Draw all lines in solid #b8653f, and give every major mass a clearly visible soft fill of the same hue at about 15-18% opacity, so the duotone is obviously present rather than white interiors. No other colors, no gradients, no shadows, no 3D, no texture.
>
> Important: NO border, NO frame, NO box or outline around the scene, just the illustration on a plain white background. No text, letters, or numbers. No human figures or faces. Calm, neutral, editorial mood: show the subject plainly, neither celebrating nor warning. Also avoid: human heads, busts, brains, halos, religious symbols, angels, devils, question marks, lightbulbs.

## Selection
Round 1, two samples of the one scene, judged by eye at tile size and full size. Picked `r1-b`: ribbon runs behind the scale on a curved plinth as briefed; in r1-a the ribbon dominates and the plinth is flat. Normalized to `static/img/categories/ethics.png`.

Round 3 (scene expanded to hero complexity), two samples, judged against the round-1 incumbent. Picked `r3-a`: path with a distant tree, lantern, quill and hourglass all sit on the plinth curve; r3-b is thinner and the book floats. Replaced `static/img/categories/ethics.png`.
