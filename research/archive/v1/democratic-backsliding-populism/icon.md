# Democratic Backsliding & the Populism Debate — primary icon art brief

Handoff brief for an illustrator or image/vector tool. Full style theme: `docs/DESIGN.md` (Topic art).
Template siblings: `nuclear-energy.md` (the tuned reference), `universal-basic-income.md`,
`housing-affordability-crisis.md`, `wildfires.md`.

## Use
The topic's **primary hero image**. Shows large on the topic page, poster, and social
cards; also reduced into a rounded-square tinted tile and shown on a dark band. Must
read both large and small, on light and dark.

## Style (non-negotiable)
- **Minimal monoline** — ONE consistent stroke weight across the whole image, rounded
  caps/joins. References: **Gorges Beer Co** menu icons, **Flaticon "Lineal."**
- **Duotone, single color, two tones** — line at full strength + a soft (~16–18%) fill
  of the **same hue** on the masses. No second color, no gradients, no shadows.
- **Color:** the category color (Governance & Political Order = **gov purple**,
  `#7a6aa8`). Deliver single-color so it can be recolored per category.
- Flat, clean, editorial.

## Composition
A small bespoke **scene** combining several *simple* sub-icons in one frame — about
**2.5–3.5× the complexity of a single Gorges icon**. Generate wide (3:2); framing is
normalized in post (trim to content, ~8% pad, fit 3:2 on white). Legible from ~40px
to hero size, readable on a dark background.

## Elements — promise *and* peril
The debate is what the populist surge **means** for democracy — erosion of liberal
institutions, a corrective to unresponsive elites, or a diagnosis that is itself
contested. The art must hold the crowd and the institution in unresolved relation,
never render a verdict:
- **A cluster of three simple human figures** on one side — the popular movement;
  plain standing figures at equal height, echoing the topic's Phosphor `users-three`
  glyph. Present, composed, neither marching nor menacing.
- **A classical civic building with three or four columns and a plain pediment** on
  the other side — the liberal-democratic institution; intact, unadorned, at equal
  visual weight to the crowd. No cracks, no crumbling.
- **A ballot box with a slot and a single ballot slip entering it, exactly midway
  between crowd and building** — the focal point: the shared channel both sides claim,
  where the contest actually runs. Placing it in the middle is the neutrality.
- **A single speech bubble above the crowd** — voice and demand: the people saying
  something to the institution; empty, no text, matter-of-fact.
- **A low ground/horizon line** — one plane under crowd, box, and building alike
  (mirrors the sibling compositions): both stand on the same ground.

## Mood
Neutral and editorial — a crowd and an institution facing each other across a ballot
box, in tension and in balance at once. The question of which one democracy *is* held
open. Not a protest scene, not a fortress under siege, not a triumphal march.

## Avoid
Photorealism; more than one color; gradients/shadows; cracked, tilted, or crumbling
columns (verdict: erosion); raised fists, megaphones, torches, or placards (verdict:
menace or heroism); crowns, strongman figures, or podiums; any flag, national symbol,
or partisan iconography; angry or fleeing figures; barriers or fences between crowd
and building; crossed-out symbols; fussy internal detail (column fluting, brick
courses, facial features); clutter; anything that reads as pro- or anti-populist.

## Deliverable
Ideally **vector (SVG)**, single-color, transparent ground. PNG accepted
(the pipeline is raster-primary).

## Generation prompt (Nano Banana / Gemini)
**Frameless** — the art has NO drawn border. The CSS tile renders the rounded-square
frame. Lessons carried over from the earlier generations: force the soft fill to
~15–18% (it renders near-invisible if unstressed) and force uniform stroke weight
(thin secondary elements drift thinner).

**Fresh-generation prompt:**
> A minimalist flat vector-style icon illustration of a democracy-and-populism scene, in a clean editorial line-art style. Combine several simple symbols into one small, balanced composition: on the left, a cluster of three identical simple human figures standing together at the same height — plain round heads and simple bodies, no faces; on the right, a small classical civic building with three or four columns and a plain triangular pediment, intact and undamaged; exactly midway between them, as the focal point, a ballot box with a slot on top and a single ballot slip halfway into the slot; and one empty rounded speech bubble floating above the cluster of figures. A single thin, straight horizontal ground line runs under the whole scene — the figures, the ballot box, and the building all stand on the same line — no hill, no landscape.
>
> Important: NO border, NO frame, NO box or outline around the scene — just the illustration itself on a plain background. Keep the composition compact and centered, not spread wide, with the crowd and the building at equal visual weight on either side of the ballot box.
>
> Style: monoline line art with ONE uniform stroke weight on every element — the figures, the speech bubble, the ballot box, the ballot slip, the building's columns and pediment, and the ground line must all be exactly the same thickness. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small, about 2.5 to 3.5 times the complexity of one simple glyph — each element stays simple, the richness is the combination. No fussy internal detail — no column fluting, no brickwork, no steps, no facial features.
>
> Color: a single purple hue, two tones only. Draw all lines in solid purple (#7a6aa8), and give the main masses a clearly visible soft fill of the same purple at about 16-18% opacity — fill the figures' bodies, the ballot box, and the building's pediment and base with a light purple tint so the two-tone duotone is obviously present rather than white interiors. No other colors, no gradients, no shadows, no offset or misregistered fills, no 3D, no texture.
>
> Composition: wide 3:2 aspect, centered with generous, even padding; balanced optical weight — neither the crowd nor the building dominates. Plain white background. Calm, neutral, editorial mood — the crowd and the institution face each other across the ballot box in even-handed tension, neither side winning; not a protest scene, not a celebration. No flags, no raised fists, no placards, no megaphones, no crowns, no cracks in the building. No text, letters, words, or numbers anywhere in the image, including inside the speech bubble and on the ballot slip.

**Edit-mode instruction (after the first generation, feed the concept back in):**
> Using this image, keep the same composition, elements, and layout, but: (1) remove any border or frame around the scene entirely; (2) add a clearly visible soft light-purple fill (~16% opacity of the same hue) inside the figures' bodies, the ballot box, and the building's pediment and base so it reads as a two-tone duotone instead of mostly white; (3) make every line exactly the same thickness, matching the main outline weight — including the building's columns, the ballot slip, and the speech bubble. Keep it flat, single purple hue, no gradients, shadows, extra colors, or text.

**Notes:**
- Over-generate on the **ballot box with slip** and the **three-figure cluster**; those
  are the elements most likely to come out malformed, over-detailed, or (for the
  slip) dropped entirely.
- Watch for the generator editorializing — cracked columns, raised fists, placards, or
  a slumping building sneak in easily on this topic; any of those breaks the required
  neutrality and disqualifies the candidate.
- Watch for text appearing inside the speech bubble or on the ballot slip — both must
  stay blank.
- White background is intentional — the primary sits on a neutral tile; the frame
  comes from the tile, not the art.
- After generating: save as `static/img/topics/democratic-backsliding-populism.png`,
  set `Topic.primary_art = "img/topics/democratic-backsliding-populism.png"`, and
  regenerate the social PNGs
  (`render_social --slug democratic-backsliding-populism --formats og,sq,pt`).

## Selection

**Winner: candidate 2** (`democratic-backsliding-populism.gemini-3-pro-image.2.jpg`), picked 2026-08-11.
All four candidates hit the scene brief (crowd + speech bubble / ballot box mid-slip / columned building on one ground line). 2 wins on checklist fit: consistent same-hue duotone across every mass (1 leaves the middle figure unfilled, 3 leaves all heads unfilled), uniform monoline, and the most compact composition — the ballot box focal point stays legible at 40px where 4's smaller, wider-spaced box thins out. 4 also adds a double-outlined pediment that busies the building.
