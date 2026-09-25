# Gun Policy — topic art brief

The topic's primary art: `static/img/topics/gun-policy.png`, 1035x690 on white, shown at hero
size on the topic page, composed into the share cards and the poster, and reduced to a 40px tile.
Style, composition rules and the common negatives are supplied by `manage.py generate_icon`; this file
carries only the scene and this subject's own negatives, plus the selection log.

## Scene
a large bolt-action hunting rifle in clean side profile spanning most of the frame's width as the dominant focal mass, its wooden stock and barrel given a clear fill, pointing away to the right and never toward the viewer, resting across a small rounded sandbag rest; the rest sits on the gentle curve of a low grassy mound that is the ground, and the rifle's stock overlaps the mound's edge; a small open box of cartridges on the mound near the stock; a small round bullseye target on a simple wooden stand far off to the upper right on a distant rise; a footpath that curves from the mound out to the target as the connective element. No table, no bench.

## Negatives
people, hands, faces, blood, bullet holes, muzzle flash, smoke, bullets in flight, a gun pointed at the viewer, crosshairs, scopes aimed at anything, crossed guns, flags, national symbols, eagles, constitution scrolls, the number 2, candles, flowers, memorials, ribbons, crime scene tape, police, soldiers, handcuffs, prohibition signs, red circles, slashes, stop signs, school buses, schools, arrows, animals, deer.

## Prompt
> A minimalist flat vector-style icon illustration, in a clean editorial line-art style: a large bolt-action hunting rifle in clean side profile spanning most of the frame's width as the dominant focal mass, its wooden stock and barrel given a clear fill, pointing away to the right and never toward the viewer, resting across a small rounded sandbag rest; the rest sits on the gentle curve of a low grassy mound that is the ground, and the rifle's stock overlaps the mound's edge; a small open box of cartridges on the mound near the stock; a small round bullseye target on a simple wooden stand far off to the upper right on a distant rise; a footpath that curves from the mound out to the target as the connective element. No table, no bench.
>
> Composition: one dominant focal mass with smaller supporting elements at clearly different scales (big, medium, small); at least one element overlaps another so the scene has depth; the ground is a gentle curve, never a flat line; one connective element runs across the frame to tie the pieces together. A single coherent scene, not a row of separate objects. Centered with generous, even padding.
>
> Style: monoline line art with ONE uniform stroke weight on every element, including the thinnest wisps and lines. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small. No fussy internal detail.
>
> Color: a single hue, two tones only. Draw all lines in solid #6a62b0, and give every major mass a clearly visible soft fill of the same hue at about 15-18% opacity, so the duotone is obviously present rather than white interiors. No other colors, no gradients, no shadows, no 3D, no texture.
>
> Important: NO border, NO frame, NO box or outline around the scene, just the illustration on a plain white background. No text, letters, or numbers. No human figures or faces. Calm, neutral, editorial mood: show the subject plainly, neither celebrating nor warning. Also avoid: people, hands, faces, blood, bullet holes, muzzle flash, smoke, bullets in flight, a gun pointed at the viewer, crosshairs, scopes aimed at anything, crossed guns, flags, national symbols, eagles, constitution scrolls, the number 2, candles, flowers, memorials, ribbons, crime scene tape, police, soldiers, handcuffs, prohibition signs, red circles, slashes, stop signs, school buses, schools, arrows, animals, deer.

## Selection
Round 1, scenes A (rifle on a shooting bench, target down a path) and B (gun safe with rifle leaning on it, revolver and key on a side table, rug), two samples each, $0.54. B reads as a safe, not guns, and r1-c has a hard rectangular fill block. Picked r1-a: rifle filled, target and path read; but at 40px the bench dominates and it reads as a table.
Round 2, scene A simplified (no bench; the rifle spans the frame on a sandbag rest atop a curved mound), two samples, $0.27, total $0.80. r2-a leaves the mound unfilled and cuts the path short; picked r2-b: rifle dominant, rest overlaps it, mound filled, path curves out to the target. The sandbag has faint soft shading, not worth an edit.
Normalized r2-b; the 40px thumbnail reads as a long gun resting on a mound. Glyph: target (Phosphor has no gun glyph; crosshair would read as aiming at something; no other governance topic uses target).
