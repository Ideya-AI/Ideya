# Economy & Work — category art brief

The category's primary art, shown only on its own category page, in the same hero card as a topic page
(about 540px wide on desktop, 300px on
mobile) beside the title. It never sits next to another category's art. The scene sits at the full house
range, about 2.5-3.5x the complexity of one glyph, five or six elements, because it shows at hero size.

Style, composition rules and negatives common to every icon live in `research/pipeline/icon_prompt.py`;
this file supplies only the scene and this subject's own negatives. The prompt below is assembled by
that script (`icon_prompt.py brief research/categories/economy/icon.md`), never edited by hand.

Deliverable: `static/img/categories/economy.png`, square, normalized with
`icon_prompt.py normalize <candidate> static/img/categories/economy.png` (trim, 8% pad, 1:1, 512px, white).
Candidates go under `research/categories/economy/candidates/`.

## Scene
a tall rising bar chart of five bars as the dominant focal mass; a stack of four coins
overlapping the foot of the shortest bar; a briefcase set low at the right; a small factory with
a sawtooth roof and no smoke behind the tallest bars; a small shopping cart low at the left; a
single smooth trend line with an arrowhead sweeping up across the whole frame from lower-left to
upper-right as the connective element; the ground is the curved edge of a table beneath the
chart.

## Negatives
currency symbols, dollar signs, banknotes, piggy banks, handshakes, ties, top hats, factories
with smoke.

## Prompt
> A minimalist flat vector-style icon illustration, in a clean editorial line-art style: a tall rising bar chart of four bars as the dominant focal mass; a stack of three coins overlapping the foot of the shortest bar; a small briefcase set low at the right; a single smooth trend line with an arrowhead sweeping up across the whole frame from lower-left to upper- right as the connective element; the ground is the curved edge of a table beneath the chart.
>
> Composition: one dominant focal mass with smaller supporting elements at clearly different scales (big, medium, small); at least one element overlaps another so the scene has depth; the ground is a gentle curve, never a flat line; one connective element runs across the frame to tie the pieces together. A single coherent scene, not a row of separate objects. Centered with generous, even padding.
>
> Style: monoline line art with ONE uniform stroke weight on every element, including the thinnest wisps and lines. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small. No fussy internal detail.
>
> Color: a single hue, two tones only. Draw all lines in solid #b48f2c, and give every major mass a clearly visible soft fill of the same hue at about 15-18% opacity, so the duotone is obviously present rather than white interiors. No other colors, no gradients, no shadows, no 3D, no texture.
>
> Important: NO border, NO frame, NO box or outline around the scene, just the illustration on a plain white background. No text, letters, or numbers. No human figures or faces. Calm, neutral, editorial mood: show the subject plainly, neither celebrating nor warning. Also avoid: currency symbols, dollar signs, banknotes, piggy banks, handshakes, ties, top hats, factories with smoke.

## Selection
Round 1, two samples of the one scene, judged by eye at tile size and full size. Picked `r1-a`: proper arrowhead and coins overlapping the first bar; r1-b arrow is a blob. Normalized to `static/img/categories/economy.png`.

Round 3 (scene expanded to hero complexity), two samples, judged against the round-1 incumbent. Picked `r3-b`: factory without smoke, coins and cart at the foot; r3-a puts a smoke curl on the chimney, which the brief excludes. Replaced `static/img/categories/economy.png`.
