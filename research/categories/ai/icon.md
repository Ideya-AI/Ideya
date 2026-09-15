# AI & Machine Intelligence — category art brief

The category's primary art, shown only on its own category page, in the same hero card as a topic page
(about 540px wide on desktop, 300px on
mobile) beside the title. It never sits next to another category's art. The scene sits at the full house
range, about 2.5-3.5x the complexity of one glyph, five or six elements, because it shows at hero size.

Style, composition rules and negatives common to every icon live in `research/pipeline/icon_prompt.py`;
this file supplies only the scene and this subject's own negatives. The prompt below is assembled by
that script (`icon_prompt.py brief research/categories/ai/icon.md`), never edited by hand.

Deliverable: `static/img/categories/ai.png`, square, normalized with
`icon_prompt.py normalize <candidate> static/img/categories/ai.png` (trim, 8% pad, 1:1, 512px, white).
Candidates go under `research/categories/ai/candidates/`.

## Scene
a large square processor chip seen flat-on as the dominant focal mass, its pins along all four
edges; a cluster of five linked network nodes overlapping the chip's upper-right corner so the
graph sits partly on top of it; a stack of three server units low at the left with a small
status light on each; a small monitor on a stand low at the right showing a plain rising curve;
circuit traces with rounded bends running from the chip's pins across the frame to the servers
and the monitor as the connective element; the ground is a gentle curve of a circuit-board edge
with two small solder pads on it.

## Negatives
robot heads, humanoid robots, glowing eyes, brains, lightning bolts, binary digits, holograms.

## Prompt
> A minimalist flat vector-style icon illustration, in a clean editorial line-art style: a large square processor chip seen flat-on as the dominant focal mass, its pins along the edges; a small cluster of four linked network nodes overlapping the chip's upper-right corner so the graph sits partly on top of the chip; a small stack of two server units low at the left; circuit traces with rounded bends running from the chip's pins across the frame in both directions as the connective element; the ground is a gentle curve of a circuit-board edge beneath everything.
>
> Composition: one dominant focal mass with smaller supporting elements at clearly different scales (big, medium, small); at least one element overlaps another so the scene has depth; the ground is a gentle curve, never a flat line; one connective element runs across the frame to tie the pieces together. A single coherent scene, not a row of separate objects. Centered with generous, even padding.
>
> Style: monoline line art with ONE uniform stroke weight on every element, including the thinnest wisps and lines. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small. No fussy internal detail.
>
> Color: a single hue, two tones only. Draw all lines in solid #3b7ea1, and give every major mass a clearly visible soft fill of the same hue at about 15-18% opacity, so the duotone is obviously present rather than white interiors. No other colors, no gradients, no shadows, no 3D, no texture.
>
> Important: NO border, NO frame, NO box or outline around the scene, just the illustration on a plain white background. No text, letters, or numbers. No human figures or faces. Calm, neutral, editorial mood: show the subject plainly, neither celebrating nor warning. Also avoid: robot heads, humanoid robots, glowing eyes, brains, lightning bolts, binary digits, holograms.

## Selection
Round 1, two samples of the one scene, judged by eye at tile size and full size. Picked `r1-a`: bolder strokes and the node graph actually overlaps the chip; r1-b is thin and the graph floats free. Normalized to `static/img/categories/ai.png`.

Round 3 (scene expanded to hero complexity), two samples, judged against the round-1 incumbent. Picked `r3-a`: servers, monitor and node graph all tied by traces; r3-b is heavier and busier. Replaced `static/img/categories/ai.png`.
