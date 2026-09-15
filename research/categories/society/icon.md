# Society, Culture & Identity — category art brief

The category's primary art, shown only on its own category page, in the same hero card as a topic page
(about 540px wide on desktop, 300px on
mobile) beside the title. It never sits next to another category's art. The scene sits at the full house
range, about 2.5-3.5x the complexity of one glyph, five or six elements, because it shows at hero size.

Style, composition rules and negatives common to every icon live in `research/pipeline/icon_prompt.py`;
this file supplies only the scene and this subject's own negatives. The prompt below is assembled by
that script (`icon_prompt.py brief research/categories/society/icon.md`), never edited by hand.

Deliverable: `static/img/categories/society.png`, square, normalized with
`icon_prompt.py normalize <candidate> static/img/categories/society.png` (trim, 8% pad, 1:1, 512px, white).
Candidates go under `research/categories/society/candidates/`.

## Scene
a cluster of five simple houses of different heights on a rolling hill as the dominant focal
mass, the tallest in the middle with a small schoolhouse bell tower among them; a park bench
with a lamppost overlapping the front of the hill below the houses; an open book resting on the
bench; a small bicycle leaning beside the bench; a kite high in the upper-right with its string
running down across the frame to the bench as the connective element; a small tree between the
houses; the ground is the rolling hill with a gentle second hill behind.

## Negatives
people, silhouettes, crowds, hands, faces, religious buildings, flags, hearts, speech bubbles.

## Prompt
> A minimalist flat vector-style icon illustration, in a clean editorial line-art style: a cluster of three simple houses of different heights on a rolling hill as the dominant focal mass, the tallest in the middle; a park bench with a lamppost overlapping the front of the hill below the houses; a small kite high in the upper-right corner with its string running down across the frame to the bench as the connective element; a small open book resting on the bench; the ground is the rolling hill with a gentle second hill behind.
>
> Composition: one dominant focal mass with smaller supporting elements at clearly different scales (big, medium, small); at least one element overlaps another so the scene has depth; the ground is a gentle curve, never a flat line; one connective element runs across the frame to tie the pieces together. A single coherent scene, not a row of separate objects. Centered with generous, even padding.
>
> Style: monoline line art with ONE uniform stroke weight on every element, including the thinnest wisps and lines. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small. No fussy internal detail.
>
> Color: a single hue, two tones only. Draw all lines in solid #9459a2, and give every major mass a clearly visible soft fill of the same hue at about 15-18% opacity, so the duotone is obviously present rather than white interiors. No other colors, no gradients, no shadows, no 3D, no texture.
>
> Important: NO border, NO frame, NO box or outline around the scene, just the illustration on a plain white background. No text, letters, or numbers. No human figures or faces. Calm, neutral, editorial mood: show the subject plainly, neither celebrating nor warning. Also avoid: people, silhouettes, crowds, hands, faces, religious buildings, flags, hearts, speech bubbles.

## Selection
Round 1, two samples of the one scene, judged by eye at tile size and full size. Picked `r1-a`: houses read as one mass on the hill and the kite string crosses to the bench; r1-b is thinner and busier. Normalized to `static/img/categories/society.png`.

Round 3 (scene expanded to hero complexity), two samples, judged against the round-1 incumbent. Picked `r3-a`: five houses with bell tower and tree, bench, bike, lamp, kite string to the bench; r3-b is thinner. Replaced `static/img/categories/society.png`.
