# Smartphones, Social Media & Youth Mental Health — primary icon art brief

Handoff brief for an illustrator or image/vector tool. Full style theme: `docs/DESIGN.md` (Topic art).
Template siblings: `nuclear-energy.md` (the tuned reference),
`birth-rate-decline-pronatalism.md` — the other **Society, Culture & Identity** topic and
the olive reference, this icon's nearest neighbor on the wall —
`content-moderation-free-speech.md` (the same open-question device), and
`economic-inequality.md` (current house weight, and the source of the no-figures rule).

**No human figures anywhere in this scene.** Not a lesson from this topic: the
economic-inequality round measured the generator drawing repeated figures at unequal
sizes in all ten candidates and refusing to correct them (see that brief's Notes). On a
topic about *young people*, a drawn child would also do editorial work no line of prompt
can take back. The young person is present as what they are growing into, never as a body.

## Use
The topic's **primary hero image**. Shows large on the topic page, poster, and social
cards; also reduced into a rounded-square tinted tile and shown on a dark band. Must
read both large and small, on light and dark.

## Style (non-negotiable)
- **Minimal monoline** — ONE consistent stroke weight across the whole image, rounded
  caps/joins. References: **Gorges Beer Co** menu icons, **Flaticon "Lineal."**
- **Duotone, single color, two tones** — line at full strength + a soft (~16–18%) fill
  of the **same hue** on the masses. No second color, no gradients, no shadows.
- **Color:** the category color (Society, Culture & Identity = **society olive**,
  `#7d8a4e`). Deliver single-color so it can be recolored per category.
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
The debate is whether smartphones and social platforms *caused* the rise in reported teen
distress since 2010, how large any effect is, what else could explain the trend, and what
should follow for platform design and minors' access. This is a live empirical fight with
several serious camps, so the art must render the **link as the open question** — two
things standing apart, under examination, with the connection between them deliberately
not drawn. The scene shows the question, never a finding:
- **A plain smartphone standing upright on the ground line** — face-on, a simple rounded
  rectangle body with one plain rounded screen area inside it and a short speaker slot
  above. The screen is **empty**: no app grid, no feed, no notification badges, no emoji,
  no crack. An intact, ordinary, unopinionated device. The topic's Phosphor
  `device-mobile` glyph already carries the bare-phone idea, so the phone here is one
  element in a scene, never the subject of it.
- **A small potted sapling standing on the same ground line** — a plain rounded pot, one
  straight stem, three simple leaves. The stand-in for a young person's development and
  wellbeing, and the reason no child is drawn. **Upright and healthy** — not wilting, not
  drooping, not shedding leaves, and equally not flowering, sprouting, or radiating: a
  plant in ordinary good order says neither "harmed" nor "fine."
- **The phone and the sapling at exactly the same overall height, with a clear gap
  between them** — the equality is the neutrality device. Neither is the accused and
  neither is the victim; they are two things a body of evidence is trying to relate.
- **A simple magnifying glass centered in the gap** — a plain circular lens with a short
  straight handle at its rim, held at mid height **exactly midway between the two,
  overlapping neither**. It is inquiry, not indictment: the lens is over the space where
  a link would be, not over the phone. What it frames is empty, because whether something
  is there is the topic.
- **A single straight horizontal ground line across the scene** — one plane under the
  phone and the pot alike (mirrors the sibling compositions): the device and the child's
  life are the same world, not two.

**The one thing this scene must never draw is a connector.** No arrow, cord, chain,
dashed line, or beam between the phone and the sapling. Drawing it asserts causation;
drawing it broken asserts the skeptics' case. The gap stays empty and the lens stays over
the gap.

## Mood
Neutral and editorial — an ordinary phone and a healthy young plant standing the same
height apart on one ground, with a lens held over the space between them. Whether
anything crosses that space, how much, and what should be done are the open questions the
scene holds. Not a screens-are-poisoning-our-children scene, not a reassurance that
nothing is happening.

## Avoid
Photorealism; more than one color; gradients/shadows; **human figures of any kind** —
no child, teenager, parent, silhouette, face, or hand, and no repeated figures in
particular (measured failure, see `economic-inequality.md`); **any connector between the
phone and the plant** — an arrow, chevron, cord, cable, wire, chain, broken chain, rope,
tendril, beam, or dashed line (verdict: causation asserted, or causation denied); a
cracked, shattered, or glitched screen; a sad face, frowning emoji, crying emoji, or any
face on the screen; notification badges, red dots, like counts, hearts, thumbs up or
down, or a scrolling feed rendered on the screen; a wilting, drooping, browning, or dead
plant, falling leaves, or a plant with cut or drained roots (verdict: harm proven); a
plant growing *out of* the phone or wrapped around it (verdict either way); a phone in a
cage, behind bars, padlocked, crossed out, slashed, X-ed, or in a trash can (verdict:
restriction is the answer); a thriving, flowering, or sparkling plant (verdict: nothing
to see); a falling or rising line chart, two curves rising together, a graph, an axis,
tick marks, or a trend line (verdict: the correlation *is* the finding — and the whole
fight is over what that graph means); brains, skulls, pills, beds, dark bedrooms,
clocks, hourglasses, timers, warning triangles, or exclamation marks; question marks or
any other lettering; platform logos, flags, party symbols, or government seals; fussy
internal detail (app icons or buttons on the phone, camera lenses, leaf veins, soil
texture or drainage holes on the pot, crosshairs or shine marks on the lens); clutter;
anything that reads as advocacy for or against phone bans.

## Deliverable
Ideally **vector (SVG)**, single-color, transparent ground. PNG accepted
(the pipeline is raster-primary).

## Generation prompt (Nano Banana / Gemini)
**Frameless** — the art has NO drawn border. The CSS tile renders the rounded-square
frame. Lessons carried over from the earlier generations: force the soft fill to
~15–18% (it renders near-invisible if unstressed), force uniform stroke weight (thin
secondary elements drift thinner), and make every major element a **filled mass** —
earlier linework-only elements nearly vanished at 40px. New this topic: the model will
try to editorialize an emotional topic (a crack, a sad face, a drooping leaf, a link
line), so the negative list is long and load-bearing.

**Fresh-generation prompt:**
> A minimalist flat vector-style icon illustration of an examination scene, in a clean editorial line-art style. Combine several simple symbols into one small, balanced composition: on one side, standing upright on the ground and resting on its short bottom edge, a simple smartphone drawn face-on — a plain rounded rectangle body with one plain rounded rectangle screen area inside it and a single short speaker slot above the screen — and the screen is completely EMPTY: no app icons, no app grid, no feed lines, no pictures, no notification badges or dots, no emoji or faces, no hearts, and no cracks, breaks or shatter lines anywhere on the phone; on the other side, standing on the same ground, a simple young potted plant — a plain rounded pot with one straight vertical stem rising from it and three simple leaves — upright, whole and healthy, with no drooping, wilting, curling, browning or falling leaves and no flowers, sparkles or fruit; the smartphone and the potted plant are drawn at EXACTLY the same overall height as each other, given equal visual weight, and separated by a clear empty gap; and centered in that gap, at mid height, a simple magnifying glass — a plain circular lens with a short straight handle attached at its rim, the handle extending up and to the right at an angle — placed exactly midway between the phone and the plant, touching and overlapping neither of them, so the lens frames only the empty space between the two objects; the lens is plain, with no crosshairs, no plus or minus sign, no reflection or shine lines, and nothing drawn inside it. A single thin, straight horizontal ground line runs across the whole scene — the phone and the plant pot both stand on it — no landscape, no hill, no grass.
>
> Important: NO border, NO frame, NO box or outline around the scene — just the illustration itself on a plain background. There are NO human figures, people, children, silhouettes, faces, heads, or hands anywhere in this image. There is NOTHING connecting the phone to the plant: no arrow, no chevron, no dashed or dotted line, no cord, cable, wire, chain, rope, vine or beam between them, and no arrow anywhere in the picture — the space between the two objects stays completely empty. Keep the composition compact and centered, not spread wide, and give the phone and the plant equal emphasis — neither larger, taller, bolder, darker, nor more detailed than the other.
>
> Style: monoline line art with ONE uniform stroke weight on every element — the phone's body and screen, the plant's pot, stem and leaves, the magnifying glass's lens circle and handle, and the ground line must all be exactly the same thickness. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small, about 2.5 to 3.5 times the complexity of one simple glyph — each element stays simple, the richness is the combination. No fussy internal detail — nothing drawn on the screen, no buttons, ports or camera lenses on the phone body, no veins on the leaves, no soil, texture or drainage holes on the pot, no hatching or shading anywhere.
>
> Color: a single olive-green hue, two tones only. Draw all lines in solid olive (#7d8a4e), and give EVERY major element a clearly visible soft fill of the same olive at about 16-18% opacity — fill the phone's body and its screen area, the plant pot, the three leaves, and the magnifying glass's lens circle with a light olive tint so the two-tone duotone is obviously present rather than white interiors; no major element may be left as unfilled outline-only linework. No other colors, no gradients, no shadows, no offset or misregistered fills, no 3D, no perspective, no texture.
>
> Composition: wide 3:2 aspect, centered with generous, even padding; balanced optical weight — the ground line runs level along the bottom, the upright phone stands on one side, the potted plant of identical height stands on the other, and the magnifying glass sits centered in the gap between them. Plain white background. Calm, neutral, editorial mood — a phone and a growing plant standing apart on the same ground with a lens held over the empty space between them, so the relationship between the two is an open question, neither asserted nor denied; not an anti-phone scene, not a reassurance. No cracked or shattered screens, no sad or crying faces or emoji, no notification badges or red dots, no hearts, likes or thumbs up or down, no falling or rising line charts, graph curves, trend lines, axes or tick marks, no arrows or chevrons, no wilting, dying or dead plants, no plant growing out of the phone, no cages, bars, padlocks, chains or broken chains, no prohibition slashes or X marks over the phone, no hands, no brains, no pills, no beds or bedrooms, no clocks, hourglasses or timers, no warning triangles, no flags or logos. No text, letters, words, numbers, question marks, exclamation marks, tick marks, percent signs, or scale markings anywhere in the image.

**Edit-mode instruction (after the first generation, feed the concept back in):**
> Using this image, keep the same composition, elements, and layout, but: (1) remove any border or frame around the scene entirely; (2) add a clearly visible soft light-olive fill (~16% opacity of the same hue) inside EVERY major element — the phone's body and screen area, the plant pot, the three leaves, and the magnifying glass's lens circle — so it reads as a two-tone duotone with no outline-only elements left; (3) make every line exactly the same thickness, matching the main outline weight — including the plant's stem, the magnifier's handle, and the ground line; (4) make the phone and the potted plant exactly the same overall height as each other, both standing on the single horizontal ground line, with a clear empty gap between them; (5) leave the phone's screen completely empty — no app icons, feed lines, notification dots, emoji or faces — and remove any crack, break or shatter line from the phone; (6) draw the plant upright, whole and healthy, with no drooping, wilting, browning or falling leaves, and no flowers or sparkles; (7) place the magnifying glass exactly midway between the phone and the plant at mid height, overlapping neither object, with a plain empty lens — no crosshairs, no shine lines, nothing inside it; (8) remove anything that connects the phone to the plant — any arrow, dashed line, cord, cable, chain, rope or vine — and leave the space between them empty; (9) remove any human figure, child, face, hand, or silhouette if one has appeared. Keep it flat, single olive hue, no gradients, shadows, extra colors, or text.

**Notes:**
- Over-generate on the **magnifier's placement** and the **empty screen**. The magnifier
  wants to drift over the phone, which converts the scene from inquiry into indictment —
  the whole neutrality of the concept lives in the lens being centered on the gap and
  touching neither object. The screen wants to fill with a feed, app grid, or
  notification dots, any of which imports a verdict about what phones do.
- Watch for the generator editorializing — a hairline crack on the screen, a single
  drooping leaf, a browning leaf tip, a downward arrow, or a small sad face are the
  likely intrusions on this topic, and each one takes a side in a live empirical
  dispute. Any of them disqualifies the candidate. The mirror failure disqualifies too:
  a flowering, sparkling, or thriving plant reading as "nothing to worry about."
- Watch for a **connector appearing between the phone and the plant** — a tendril, cable,
  arrow, or dotted line. This is the single most likely way a candidate silently answers
  the topic's question. The gap must be empty.
- Watch for the two objects rendering at different heights. Equal height is the
  neutrality device here, the way identical discs were on `economic-inequality`; a
  candidate whose phone towers over the plant reads as domination. Measure rather than
  eyeball it.
- Watch for the phone drifting into being the whole picture — the Phosphor
  `device-mobile` chip already carries the bare-phone idea, and the raster icon has to
  read as a scene, not as a bigger version of the glyph.
- Watch for outline-only elements — every major mass must carry the olive fill; a
  candidate whose phone or pot renders as bare linework fails the 40px test.
- White background is intentional — the primary sits on a neutral tile; the frame
  comes from the tile, not the art.
- After generating: save as `static/img/topics/social-media-youth-mental-health.png`,
  set `Topic.primary_art = "img/topics/social-media-youth-mental-health.png"`, and
  regenerate the social PNGs
  (`render_social --slug social-media-youth-mental-health --formats og,sq,pt`).

## Selection

**Winner: `social-media-youth-mental-health.gemini-3-pro-image.3.jpg`** →
`static/img/topics/social-media-youth-mental-health.png` (1035×690), promoted 2026-09-04.
One generation round, no edits — the disc-not-humans rule from economic-inequality held.

Chosen on the fill checklist: it is the only candidate where every major mass carries the
duotone fill — phone body, lens *and* handle, leaves and pot. Candidate 1 left the phone
body white; candidate 2 rendered the magnifier handle as a bare hairline; candidate 4
left the lens interior empty and ran to 38px of side padding. Three's 105px padding is
tighter than the others but symmetric and clear of the tile edge.

Equal height verified by measurement, not by eye: phone 166→675 and sapling 166→675,
**509px each, 0px delta**. Candidates 1 and 2 were also exactly equal (512/512 and
524/524), so the generator handles equal *objects* reliably — the scale drift that broke
the previous topic was specific to repeated human figures.

Neutrality check on the shipped image: no crack, no wilt, no arrow, chain or chart
between the two masses; the lens sits over the empty gap. Family fit checked against
`birth-rate-decline-pronatalism` (society olive, same weight and monoline).
