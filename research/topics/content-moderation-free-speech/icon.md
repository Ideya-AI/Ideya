# Content Moderation — topic art brief

The topic's primary art: `static/img/topics/content-moderation-free-speech.png`, 1035x690 on white, shown at hero size on the topic page, composed into the share cards and the poster, and reduced to a 40px tile.
Style, composition rules and the common negatives are supplied by `manage.py generate_icon`; this file carries only the scene and this subject's own negatives, plus the selection log.

## Scene
a large open laptop seen from the front as the dominant focal mass, its screen showing a simple feed of three stacked post cards, each card a rounded rectangle with a plain filled circle dot and two short blank lines; the top card is lifted out of the column and tilted, overlapping the laptop's upper right frame, with a small triangular pennant flag on a short pole at its corner; everything flat, no drop shadow under any element; three small rounded speech bubbles with no text rise in a loose trail from behind the laptop to the upper left; the laptop sits on a low rounded mound, outlined and softly filled; one long thin rolling hill line runs across the whole width of the frame behind the mound as the connective element; a small cloud at the upper right.

## Negatives
people, hands, faces, text, letters, logos, platform logos, bird, thumbs up, likes, hearts, padlocks, gags, taped mouths, muzzles, chains, scissors, erasers, trash cans, red X marks, crossed-out bubbles, prohibition signs, slashes, stop signs, censored bars, megaphones, gavels, scales of justice, courthouses, flags of nations, shields, warning triangles, exclamation marks, fire, arrows.

## Prompt
> A minimalist flat vector-style icon illustration, in a clean editorial line-art style: a large open laptop seen from the front as the dominant focal mass, its screen showing a simple feed of three stacked post cards, each card a rounded rectangle with a plain filled circle dot and two short blank lines; the top card is lifted out of the column and tilted, overlapping the laptop's upper right frame, with a small triangular pennant flag on a short pole at its corner; everything flat, no drop shadow under any element; three small rounded speech bubbles with no text rise in a loose trail from behind the laptop to the upper left; the laptop sits on a low rounded mound, outlined and softly filled; one long thin rolling hill line runs across the whole width of the frame behind the mound as the connective element; a small cloud at the upper right.
>
> Composition: one dominant focal mass with smaller supporting elements at clearly different scales (big, medium, small); at least one element overlaps another so the scene has depth; the ground is a gentle curve, never a flat line; one connective element runs across the frame to tie the pieces together. A single coherent scene, not a row of separate objects. Centered with generous, even padding.
>
> Style: monoline line art with ONE uniform stroke weight on every element, including the thinnest wisps and lines. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small. No fussy internal detail.
>
> Color: a single hue, two tones only. Draw all lines in solid #2f8f86, and give every major mass a clearly visible soft fill of the same hue at about 15-18% opacity, so the duotone is obviously present rather than white interiors. No other colors, no gradients, no shadows, no 3D, no texture.
>
> Important: NO border, NO frame, NO box or outline around the scene, just the illustration on a plain white background. No text, letters, or numbers. No human figures or faces. Calm, neutral, editorial mood: show the subject plainly, neither celebrating nor warning. Also avoid: people, hands, faces, text, letters, logos, platform logos, bird, thumbs up, likes, hearts, padlocks, gags, taped mouths, muzzles, chains, scissors, erasers, trash cans, red X marks, crossed-out bubbles, prohibition signs, slashes, stop signs, censored bars, megaphones, gavels, scales of justice, courthouses, flags of nations, shields, warning triangles, exclamation marks, fire, arrows.

## Selection
Round 1, scenes A (laptop feed with one flagged card lifted out, speech bubbles, cable to a server) and B (public notice board of pinned speech-bubble notes, one hanging by a pin, phone at its post, path). Both calls failed before any image: Gemini returned RESOURCE_EXHAUSTED, prepayment credits depleted. Spend $0.00. Art blocked until billing is topped up; rerun round 1 as written.
Retry after billing top-up. Round 1, scenes A (laptop feed, flagged card lifted out, bubbles, cable to server) and B (notice board of pinned bubbles, phone, path), two samples each. Picked r1-b: flagged post lifted from the feed reads as moderation; B (r1-c, r1-d) reads as a bulletin board, not platforms. Faults: grey drop shadow under the card, cable drawn as a thick tube.
Round 2, edit of r1-b (remove shadow, thin cable). r2-a/b dropped the shadow but turned the mound into a gradient fade and kept the tube cable. Not better; kept r1-b.
Round 3, scene A rewritten with an explicit thin cable. r3-a lost the post lines (blank sticky note), r3-b drew person silhouettes as avatars; both kept shadow and tube. Cable is the problem, drop it.
Round 4, scene A with no cable: rolling hill line across the frame as connective, three small bubbles, cloud. Picked r4-a: no shadow, clear flagged post; faults: laptop screen unfilled, flat base line under the mound. r4-b's lifted card lost its lines.
Round 5, edit of r4-a (fill screen and base, remove flat base line). Picked r5-a: screen now filled, hills kept, mound a soft curve; small bubbles and cloud lost fill, mound has no outline, both minor. r5-b dropped the hill line. Normalized r5-a; 40px reads as a laptop with a flagged card. Spend $1.61.
Glyph: flag-pennant (the report flag every platform uses; no other digital topic has a glyph yet).
