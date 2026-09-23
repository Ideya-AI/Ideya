# Nuclear Energy — topic art brief

The topic's primary art, shown at hero size on the topic page, composed into share cards and the
poster, and reduced to a tile. Style, composition rules and negatives common to every icon live in
`topics/management/commands/generate_icon.py`; this file supplies only the scene and this subject's
own negatives.

Deliverable: `static/img/topics/nuclear-energy.png`, 1035x690 on white, normalized with
`generate_icon normalize --slug nuclear-energy --src <candidate>`. Candidates go under
`research/topics/nuclear-energy/candidates/`.

## Scene
a tall hyperbolic cooling tower as the dominant focal mass, waisted, with a soft curl of steam
rising from its rim; a domed containment building of medium size overlapping the foot of the
tower so the dome sits in front of it; a row of three small dry-cask cylinders low at the right;
a transmission pylon at the left edge with power lines strung across the whole frame as the
connective element; the ground is the curve of a riverbank with a low hill behind.

## Negatives
mushroom clouds, radiation trefoils, hazard or warning signs, skulls, the atom-with-orbits
symbol, green glow, leaking barrels, smoke, fire, cracked or ruined buildings, protest signs.

## Prompt
> A minimalist flat vector-style icon illustration, in a clean editorial line-art style: a tall hyperbolic cooling tower as the dominant focal mass, waisted, with a soft curl of steam rising from its rim; a domed containment building of medium size overlapping the foot of the tower so the dome sits in front of it; a row of three small dry-cask cylinders low at the right; a transmission pylon at the left edge with power lines strung across the whole frame as the connective element; the ground is the curve of a riverbank with a low hill behind.
>
> Composition: one dominant focal mass with smaller supporting elements at clearly different scales (big, medium, small); at least one element overlaps another so the scene has depth; the ground is a gentle curve, never a flat line; one connective element runs across the frame to tie the pieces together. A single coherent scene, not a row of separate objects. Centered with generous, even padding.
>
> Style: monoline line art with ONE uniform stroke weight on every element, including the thinnest wisps and lines. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small. No fussy internal detail.
>
> Color: a single hue, two tones only. Draw all lines in solid #3f9a6a, and give every major mass a clearly visible soft fill of the same hue at about 15-18% opacity, so the duotone is obviously present rather than white interiors. No other colors, no gradients, no shadows, no 3D, no texture.
>
> Important: NO border, NO frame, NO box or outline around the scene, just the illustration on a plain white background. No text, letters, or numbers. No human figures or faces. Calm, neutral, editorial mood: show the subject plainly, neither celebrating nor warning. Also avoid: mushroom clouds, radiation trefoils, hazard or warning signs, skulls, the atom-with-orbits symbol, green glow, leaking barrels, smoke, fire, cracked or ruined buildings, protest signs.

## Selection
Round 1, two scenes at two samples each: the cooling-tower plant on a riverbank (`r1-a`, `r1-b`) and a dome-dominant version with the tower behind (`r1-c`, `r1-d`). The dome scene reads as one blob with barrels and a smoke plume, so it was dropped. Incumbent `r1-b`: tower dominant, dome overlapping its foot, casks, pylon and lines.

Round 2, one edit on `r1-b` naming the faults: white tower interior, steam drawn thinner than the rest, casks floating at the edge, flat ground line. Picked `r2-b` — fills now read, steam matches weight, casks tuck against the dome; the straight horizontal behind the buildings survived.

Round 3, one more edit against that straight line. `r3-b` broke the power lines at the tower, so the connective element was lost; picked `r3-a`, which keeps the sweep across the frame. The short straight bank line remains and was accepted rather than spend another round. Normalized to `static/img/topics/nuclear-energy.png`; the 40px tile reads as tower plus dome.

Glyph: `nuclear-plant`, the literal one, unused elsewhere in Climate & Energy.
