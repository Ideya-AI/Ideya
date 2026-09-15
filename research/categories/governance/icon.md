# Governance & Political Order — category art brief

The category's primary art, shown only on its own category page, in the same hero card as a topic page
(about 540px wide on desktop, 300px on
mobile) beside the title. It never sits next to another category's art. The scene sits at the full house
range, about 2.5-3.5x the complexity of one glyph, five or six elements, because it shows at hero size.

Style, composition rules and negatives common to every icon live in `research/pipeline/icon_prompt.py`;
this file supplies only the scene and this subject's own negatives. The prompt below is assembled by
that script (`icon_prompt.py brief research/categories/governance/icon.md`), never edited by hand.

Deliverable: `static/img/categories/governance.png`, square, normalized with
`icon_prompt.py normalize <candidate> static/img/categories/governance.png` (trim, 8% pad, 1:1, 512px, white).
Candidates go under `research/categories/governance/candidates/`.

## Scene
a domed building with a columned front as the dominant focal mass, set on a low curved flight of
steps; a gavel leaning against the base of the steps and overlapping their front edge; a ballot
box with a slot at the right; a small scroll tied with a band at the left; a small courthouse-
style lamp post beside the steps; a long banner or ribbon drawn as one smooth curve running
across the frame behind the dome from edge to edge as the connective element; the ground is the
curve of the steps continuing into a low path.

## Negatives
flags of any nation, crowns, eagles, stars, fists, chains, barbed wire, podiums, microphones.

## Prompt
> A minimalist flat vector-style icon illustration, in a clean editorial line-art style: a domed building with a columned front as the dominant focal mass, set on a low curved flight of steps; a gavel leaning against the base of the steps and overlapping their front edge; a small ballot box with a slot at the right; a long banner or ribbon drawn as one smooth curve running across the frame behind the dome from edge to edge as the connective element; the ground is the curve of the steps.
>
> Composition: one dominant focal mass with smaller supporting elements at clearly different scales (big, medium, small); at least one element overlaps another so the scene has depth; the ground is a gentle curve, never a flat line; one connective element runs across the frame to tie the pieces together. A single coherent scene, not a row of separate objects. Centered with generous, even padding.
>
> Style: monoline line art with ONE uniform stroke weight on every element, including the thinnest wisps and lines. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small. No fussy internal detail.
>
> Color: a single hue, two tones only. Draw all lines in solid #6a62b0, and give every major mass a clearly visible soft fill of the same hue at about 15-18% opacity, so the duotone is obviously present rather than white interiors. No other colors, no gradients, no shadows, no 3D, no texture.
>
> Important: NO border, NO frame, NO box or outline around the scene, just the illustration on a plain white background. No text, letters, or numbers. No human figures or faces. Calm, neutral, editorial mood: show the subject plainly, neither celebrating nor warning. Also avoid: flags of any nation, crowns, eagles, stars, fists, chains, barbed wire, podiums, microphones.

## Selection
Round 1, two samples of the one scene, judged by eye at tile size and full size. Picked `r1-a`: columns and dome read at tile size; r1-b columns turn into arches and the banner is a flat band. Normalized to `static/img/categories/governance.png`.

Round 3 (scene expanded to hero complexity), two samples, judged against the round-1 incumbent. Picked `r3-a`: banner behind the capitol, scroll, lamp, ballot box and gavel; r3-b banner cuts through the columns. Replaced `static/img/categories/governance.png`.
