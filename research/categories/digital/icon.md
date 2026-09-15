# Digital Society & Information — category art brief

The category's primary art, shown only on its own category page, in the same hero card as a topic page
(about 540px wide on desktop, 300px on
mobile) beside the title. It never sits next to another category's art. The scene sits at the full house
range, about 2.5-3.5x the complexity of one glyph, five or six elements, because it shows at hero size.

Style, composition rules and negatives common to every icon live in `research/pipeline/icon_prompt.py`;
this file supplies only the scene and this subject's own negatives. The prompt below is assembled by
that script (`icon_prompt.py brief research/categories/digital/icon.md`), never edited by hand.

Deliverable: `static/img/categories/digital.png`, square, normalized with
`icon_prompt.py normalize <candidate> static/img/categories/digital.png` (trim, 8% pad, 1:1, 512px, white).
Candidates go under `research/categories/digital/candidates/`.

## Scene
a large smartphone standing upright as the dominant focal mass; a rounded speech bubble
overlapping the phone's top edge and extending outside it; a smaller second speech bubble behind
the first; a closed padlock at the phone's base; a small open laptop low at the left; a small
eye-shaped camera lens at the right; three concentric broadcast arcs radiating from the upper-
left corner across toward the phone as the connective element; the ground is a gently curved
cable with three small nodes running beneath.

## Negatives
social-media logos, brand marks, cursors, keyboards, eyes, cameras, masks, hackers, hoodies.

## Prompt
> A minimalist flat vector-style icon illustration, in a clean editorial line-art style: a large smartphone standing upright as the dominant focal mass; a rounded speech bubble overlapping the phone's top edge and extending outside it; a small closed padlock at the phone's base; three concentric broadcast arcs radiating from the upper-left corner of the frame across toward the phone as the connective element; the ground is a gently curved cable with two small nodes on it running beneath the phone.
>
> Composition: one dominant focal mass with smaller supporting elements at clearly different scales (big, medium, small); at least one element overlaps another so the scene has depth; the ground is a gentle curve, never a flat line; one connective element runs across the frame to tie the pieces together. A single coherent scene, not a row of separate objects. Centered with generous, even padding.
>
> Style: monoline line art with ONE uniform stroke weight on every element, including the thinnest wisps and lines. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small. No fussy internal detail.
>
> Color: a single hue, two tones only. Draw all lines in solid #2f8f86, and give every major mass a clearly visible soft fill of the same hue at about 15-18% opacity, so the duotone is obviously present rather than white interiors. No other colors, no gradients, no shadows, no 3D, no texture.
>
> Important: NO border, NO frame, NO box or outline around the scene, just the illustration on a plain white background. No text, letters, or numbers. No human figures or faces. Calm, neutral, editorial mood: show the subject plainly, neither celebrating nor warning. Also avoid: social-media logos, brand marks, cursors, keyboards, eyes, cameras, masks, hackers, hoodies.

## Selection
Round 1, two samples of the one scene, judged by eye at tile size and full size. Picked `r1-a`: arcs stay a supporting element; in r1-b they wrap the whole scene and swamp the phone. Normalized to `static/img/categories/digital.png`.

Round 3 (scene expanded to hero complexity), two samples, judged against the round-1 incumbent. Picked `r3-a`: laptop, padlock, webcam and two bubbles on the cabled ground; r3-b arcs swamp the phone again. Replaced `static/img/categories/digital.png`.
