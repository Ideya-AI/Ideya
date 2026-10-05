# Gun Policy — topic art brief

The topic's primary art: `static/img/topics/gun-policy.png`, 1035x690 on white, shown at hero
size on the topic page, composed into the share cards and the poster, and reduced to a 40px tile.
Style, composition rules and the common negatives are supplied by `manage.py generate_icon`; this file
carries only the scene and this subject's own negatives, plus the selection log.

## Scene
the counter of a small gun shop seen from the front: a long low glass display case as the dominant focal mass, with two handguns lying flat on their sides inside it, pointing away from the viewer, given a clear fill; on top of the case a clipboard holding a blank lined paper form with a pen beside it, overlapping the case's top edge; behind the case a simple wall rack with three long rifles standing upright side by side, muzzles up, unloaded and at rest; a small closed box of cartridges on the case top; a curved rug-shaped floor under the case as the ground; a long wall shelf line running across the whole frame behind everything as the connective element.

## Negatives
people, hands, faces, blood, bullet holes, muzzle flash, smoke, bullets in flight, a gun pointed at the viewer, crosshairs, scopes aimed at anything, crossed guns, flags, national symbols, eagles, constitution scrolls, the number 2, candles, flowers, memorials, ribbons, crime scene tape, police, soldiers, handcuffs, prohibition signs, red circles, slashes, stop signs, school buses, schools, arrows, animals, deer.

## Prompt
> A minimalist flat vector-style icon illustration, in a clean editorial line-art style: the counter of a small gun shop seen from the front: a long low glass display case as the dominant focal mass, with two handguns lying flat on their sides inside it, pointing away from the viewer, given a clear fill; on top of the case a clipboard holding a blank lined paper form with a pen beside it, overlapping the case's top edge; behind the case a simple wall rack with three long rifles standing upright side by side, muzzles up, unloaded and at rest; a small closed box of cartridges on the case top; a curved rug-shaped floor under the case as the ground; a long wall shelf line running across the whole frame behind everything as the connective element.
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
Fix mode (audit: the rifle on a rest aimed at a target reads as sport shooting, the owner's side). Round 3, scenes C (gun shop counter: glass case with two handguns, clipboard purchase form, three rifles racked upright) and D (revolver in an open case on a hill, road to a domed legislature), two samples each, $0.57, total $1.37. D's revolver is huge and r3-d is flooded with fill, and the legislature reads as a camp's appeal to law. Picked r3-b: no gun in use, no target; the counter with its purchase form is where ownership and regulation meet, which every camp recognizes; even strokes, filled masses. r3-a has floating shelves and a stray glare. Normalized r3-b; at 40px it reads as a counter with racked long guns. Glyph kept: target (no gun glyph exists; crosshair aims, shield and vault each echo one camp).
