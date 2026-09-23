# Living With Wildfire — topic art brief

The topic's primary art, shown at hero size on the topic page, composed into share cards and the
poster, and reduced to a tile. Style, composition rules and negatives common to every icon live in
`topics/management/commands/generate_icon.py`; this file supplies only the scene and this subject's
own negatives.

Deliverable: `static/img/topics/wildfires.png`, 1035x690 on white, normalized with
`generate_icon normalize --slug wildfires --src <candidate>`. Candidates go under
`research/topics/wildfires/candidates/`.

## Scene
a forested ridge as the dominant focal mass, a curved hillside carrying a stand of simple conifers;
a low line of small flames running along the base of the stand; a broad band of smoke lifting from
the ridge and drifting across the whole frame as the connective element; a medium single-gable
house at the lower right, overlapping the foot of the ridge, with a cleared curved apron of open
ground around it; a small lookout tower on a far shoulder of the hill; the ground is the curve of
the slope falling toward the house, never a flat line.

## Negatives
orange or red glow, an inferno or wall of flame, firefighters, fire trucks, helicopters, sirens,
burning globes or burning earth, charred skeletons of trees, skulls, warning or hazard signs,
smoky faces, a bear or any mascot, matches, campfires, thermometers, graphs.

## Prompt
> A minimalist flat vector-style icon illustration, in a clean editorial line-art style: a forested ridge as the dominant focal mass, a curved hillside carrying a stand of simple conifers; a low line of small flames running along the base of the stand; a broad band of smoke lifting from the ridge and drifting across the whole frame as the connective element; a medium single-gable house at the lower right, overlapping the foot of the ridge, with a cleared curved apron of open ground around it; a small lookout tower on a far shoulder of the hill; the ground is the curve of the slope falling toward the house, never a flat line.
>
> Composition: one dominant focal mass with smaller supporting elements at clearly different scales (big, medium, small); at least one element overlaps another so the scene has depth; the ground is a gentle curve, never a flat line; one connective element runs across the frame to tie the pieces together. A single coherent scene, not a row of separate objects. Centered with generous, even padding.
>
> Style: monoline line art with ONE uniform stroke weight on every element, including the thinnest wisps and lines. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small. No fussy internal detail.
>
> Color: a single hue, two tones only. Draw all lines in solid #7d8a4e, and give every major mass a clearly visible soft fill of the same hue at about 15-18% opacity, so the duotone is obviously present rather than white interiors. No other colors, no gradients, no shadows, no 3D, no texture.
>
> Important: NO border, NO frame, NO box or outline around the scene, just the illustration on a plain white background. No text, letters, or numbers. No human figures or faces. Calm, neutral, editorial mood: show the subject plainly, neither celebrating nor warning. Also avoid: orange or red glow, an inferno or wall of flame, firefighters, fire trucks, helicopters, sirens, burning globes or burning earth, charred skeletons of trees, skulls, warning or hazard signs, smoky faces, a bear or any mascot, matches, campfires, thermometers, graphs.

## Selection
Round 1, two scenes at two samples each: ridge-dominant, fire at the treeline with the house below (`r1-a`, `r1-b`) and house-dominant with the stand behind (`r1-c`, `r1-d`). The house-led pair made the house a flat slab, turned the smoke into decorative ribbons and drew the hose as a squiggle; `r1-b` ran off all four edges with hollow trees. Incumbent `r1-a`: forested ridge dominant, flame line along its base, smoke crossing the frame, house overlapping the foot of the slope, lookout tower small at the left.

Round 2, one edit on `r1-a` naming the faults: hollow flames drawn thinner than the rest, the smoke band running off the right edge, a double-ellipse clearing around the house, an unfilled house. Both returns fixed all four; picked `r2-b` over `r2-a` for the simpler flame line.

Round 3, a simplified scene (six large conifers, a bolder flame line) to test whether the tree mass was too busy at tile size. Both returns came back hollow — white trees, white flames, a white house in `r3-b` — and `r3-a` made the smoke a swirl. Neither beat the incumbent, so `r2-b` stands. Normalized to `static/img/topics/wildfires.png`; the 40px tile reads as a filled forested hill with a small pale house at the right.

Spend: $1.07 of the $3.00 cap, 8 images.

Glyph: `fire`, the literal one, unused elsewhere in Food & Land.
