# Content Moderation & Online Speech — primary icon art brief

Handoff brief for an illustrator or image/vector tool. Full style theme: `docs/DESIGN.md` (Topic art).
Template siblings: `nuclear-energy.md` (the tuned reference), `ai-future-of-work.md`,
`ai-takeoff-loss-of-control.md`, `democratic-backsliding-populism.md`.

## Use
The topic's **primary hero image**. Shows large on the topic page, poster, and social
cards; also reduced into a rounded-square tinted tile and shown on a dark band. Must
read both large and small, on light and dark.

## Style (non-negotiable)
- **Minimal monoline** — ONE consistent stroke weight across the whole image, rounded
  caps/joins. References: **Gorges Beer Co** menu icons, **Flaticon "Lineal."**
- **Duotone, single color, two tones** — line at full strength + a soft (~16–18%) fill
  of the **same hue** on the masses. No second color, no gradients, no shadows.
- **Color:** the category color (Digital Society & Information = **digital teal**,
  `#2f8f86`). Deliver single-color so it can be recolored per category.
- Flat, clean, editorial.
- **Filled masses, not linework-only** — lesson from earlier topics: thin unfilled
  curves nearly vanished at 40px. Every major element in this scene is a filled
  shape carrying the duotone tint; nothing important may be a bare line.

## Composition
A small bespoke **scene** combining several *simple* sub-icons in one frame — about
**2.5–3.5× the complexity of a single Gorges icon**. Generate wide (3:2); framing is
normalized in post (trim to content, ~8% pad, fit 3:2 on white). Legible from ~40px
to hero size, readable on a dark background.

## Elements — promise *and* peril
The debate is **who decides** which lawful-but-harmful posts stay online — platforms,
governments, courts, or users — and whether the liability shield behind the social
web should hold. The art must show speech passing through a contested governance
layer with the outcome left ambiguous, never render a verdict — neither "censorship
bad" nor "moderation good":
- **A simple open gateway** — the focal point: two plain upright posts and a flat
  lintel standing on the ground, the passage between them clearly **open**. The
  moderation layer itself — a structure speech moves through, not a wall or a barred
  door. No door leaf, no bars, no barrier.
- **A small level balance scale resting on top of the gateway's lintel** — the
  weighing built into the gate: pans exactly level, undecided. Who holds the scale
  is deliberately unshown — that is the topic's question.
- **Three simple rounded speech bubbles in transit along one line through the
  gateway** — echoing the topic's Phosphor `chat-centered-dots` glyph, each carrying
  three small dots: one already **past** the gate and continuing on, one **inside**
  the opening mid-passage, one **approaching** just before it. All three intact and
  identical — none crossed out, blocked, deflated, or turned away. The line of
  travel, not any bubble's fate, is the story.
- **A low ground/horizon line** — one plane under the gateway and the bubbles' path
  alike (mirrors the sibling compositions): everything happens on the same ground.

## Mood
Neutral and editorial — speech moving through an open gate with a level scale above
it. Whether the gate should exist, who should hold the scale, and what happens to the
next bubble are the open questions the scene holds. Not a censorship scene, not a
free-for-all celebration.

## Avoid
Photorealism; more than one color; gradients/shadows; a crossed-out, X-ed, or
prohibition-slashed speech bubble as any prominent motif (verdict: pro-censorship);
a closed, barred, or padlocked gate, a wall, or a bouncer figure (verdict: speech
suppressed); megaphones, especially triumphant or oversized ones (verdict: speech
maximalism); muzzles, gags, tape over mouths, zipped lips, or silenced faces; a
bubble bouncing off the gate, shattering, or piling up rejected; tilted or slammed
scale pans (verdict rendered); gavel-smashing imagery; national flags, party
symbols, or platform logos; fussy internal detail (letters inside bubbles, brick
texture on the gateway, ornament on the scale); clutter; anything that reads as pro-
or anti-moderation.

## Deliverable
Ideally **vector (SVG)**, single-color, transparent ground. PNG accepted
(the pipeline is raster-primary).

## Generation prompt (Nano Banana / Gemini)
**Frameless** — the art has NO drawn border. The CSS tile renders the rounded-square
frame. Lessons carried over from the earlier generations: force the soft fill to
~15–18% (it renders near-invisible if unstressed), force uniform stroke weight (thin
secondary elements drift thinner), and make every major element a **filled mass** —
earlier linework-only elements nearly vanished at 40px.

**Fresh-generation prompt:**
> A minimalist flat vector-style icon illustration of a speech-governance scene, in a clean editorial line-art style. Combine several simple symbols into one small, balanced composition: at the center, a simple open gateway standing on the ground — two plain upright posts and a flat horizontal lintel across the top, with the passage between the posts completely open — no door, no bars, no barrier of any kind; resting on top of the gateway's lintel, a small simple balance scale with two pans hanging exactly level, perfectly balanced; and three identical simple rounded speech bubbles, each containing three small round dots, traveling in a single line through the gateway at mid height — one bubble already past the gateway on one side moving away, one bubble inside the open passage exactly between the posts, and one bubble approaching the gateway from the other side — all three bubbles whole and intact, none blocked, crossed out, or turned away. A single thin, straight horizontal ground line runs under the whole scene — the gateway's posts stand on it — no hill, no landscape.
>
> Important: NO border, NO frame, NO box or outline around the scene — just the illustration itself on a plain background. Keep the composition compact and centered, not spread wide, with the three speech bubbles identical in size and shape and given equal emphasis — none larger, darker, or more dominant than the others.
>
> Style: monoline line art with ONE uniform stroke weight on every element — the gateway posts and lintel, the balance scale and its strings, all three speech bubbles, and the ground line must all be exactly the same thickness. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small, about 2.5 to 3.5 times the complexity of one simple glyph — each element stays simple, the richness is the combination. No fussy internal detail — no letters or words inside the bubbles (only the three dots), no brick or wood texture on the gateway, no ornament on the scale.
>
> Color: a single teal hue, two tones only. Draw all lines in solid teal (#2f8f86), and give EVERY major element a clearly visible soft fill of the same teal at about 16-18% opacity — fill all three speech bubbles, the gateway's posts and lintel, and the balance scale's pans with a light teal tint so the two-tone duotone is obviously present rather than white interiors; no major element may be left as unfilled outline-only linework. No other colors, no gradients, no shadows, no offset or misregistered fills, no 3D, no texture.
>
> Composition: wide 3:2 aspect, centered with generous, even padding; balanced optical weight — the gateway anchors the middle, the bubbles' line of travel runs level through it, the small scale sits centered on top. Plain white background. Calm, neutral, editorial mood — speech passing through an open gate with a level scale above it, and who should hold that scale left an open question; not a censorship scene, not a celebration. No crossed-out or X-ed bubbles, no closed doors or bars, no padlocks, no megaphones, no muzzles or tape, no gavels, no flags or logos. No text, letters, words, or numbers anywhere in the image, including inside the speech bubbles.

**Edit-mode instruction (after the first generation, feed the concept back in):**
> Using this image, keep the same composition, elements, and layout, but: (1) remove any border or frame around the scene entirely; (2) add a clearly visible soft light-teal fill (~16% opacity of the same hue) inside EVERY major element — all three speech bubbles, the gateway's posts and lintel, and the balance scale's pans — so it reads as a two-tone duotone with no outline-only elements left; (3) make every line exactly the same thickness, matching the main outline weight — including the scale's strings, the bubbles' outlines, and the ground line; (4) keep the gateway's passage completely open with no door or bars, the scale's pans exactly level, and all three bubbles identical, intact, and equally emphasized. Keep it flat, single teal hue, no gradients, shadows, extra colors, or text.

**Notes:**
- Over-generate on the **scale-on-lintel join** and the **bubble inside the open
  passage**; those are the elements most likely to come out malformed — the
  generator tends to merge the scale into the lintel, tilt the pans, or snag the
  mid-passage bubble on a gatepost.
- Watch for the generator editorializing — a door or bars appearing in the gateway,
  a bubble rendered crossed-out or bouncing back, tilted scale pans, or a guard
  figure at the gate sneak in easily on this topic; any of those breaks the required
  neutrality and disqualifies the candidate.
- Watch for letters or words appearing inside the speech bubbles — only the three
  dots are allowed; any text disqualifies the candidate.
- Watch for outline-only elements — every major mass must carry the teal fill; a
  candidate whose bubbles or gateway render as bare linework fails the 40px test.
- White background is intentional — the primary sits on a neutral tile; the frame
  comes from the tile, not the art.
- After generating: save as `static/img/topics/content-moderation-free-speech.png`,
  set `Topic.primary_art = "img/topics/content-moderation-free-speech.png"`, and
  regenerate the social PNGs
  (`render_social --slug content-moderation-free-speech --formats og,sq,pt`).

## Selection

**Winner: candidate 3** (`content-moderation-free-speech.gemini-3-pro-image.3.jpg`), picked 2026-08-12.
All four render the bubbles-through-gateway scene with the level scale. 3 wins: pure white ground (1 is tinted), no stroke artifacts (2 has a stray fragment on the right post, 4 doubles the ground line into a slab), every mass filled, scale perfectly level.
