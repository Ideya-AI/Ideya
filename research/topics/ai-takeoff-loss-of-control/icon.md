# AI Takeoff Speed & Loss of Control — primary icon art brief

Handoff brief for an illustrator or image/vector tool. Full style theme: `docs/DESIGN.md` (Topic art).
Template siblings: `nuclear-energy.md` (the tuned reference), `universal-basic-income.md`,
`housing-affordability-crisis.md`, `democratic-backsliding-populism.md`.

## Use
The topic's **primary hero image**. Shows large on the topic page, poster, and social
cards; also reduced into a rounded-square tinted tile and shown on a dark band. Must
read both large and small, on light and dark.

## Style (non-negotiable)
- **Minimal monoline** — ONE consistent stroke weight across the whole image, rounded
  caps/joins. References: **Gorges Beer Co** menu icons, **Flaticon "Lineal."**
- **Duotone, single color, two tones** — line at full strength + a soft (~16–18%) fill
  of the **same hue** on the masses. No second color, no gradients, no shadows.
- **Color:** the category color (AI & Machine Intelligence = **tech blue**,
  `#3b7ea1`). Deliver single-color so it can be recolored per category.
- Flat, clean, editorial.

## Composition
A small bespoke **scene** combining several *simple* sub-icons in one frame — about
**2.5–3.5× the complexity of a single Gorges icon**. Generate wide (3:2); framing is
normalized in post (trim to content, ~8% pad, fit 3:2 on white). Legible from ~40px
to hero size, readable on a dark background.

## Elements — promise *and* peril
The debate is about the **shape of the arrival** — a sharp self-accelerating jump
versus gradual progress — and whether control is lost in one decisive moment, by slow
drift, or not at all. The art must hold both trajectories and the control question
open, never render a verdict:
- **Two trajectory curves rising from one shared origin point** — the focal point:
  one climbing steeply, nearly vertical; the other rising gently and gradually. Both
  end in plain open arrowheads at roughly the same visual weight. Neither curve is
  styled as the "real" one — the fork itself is the question.
- **A small simple rocket at the shared origin, nose up, not yet launched** —
  echoing the topic's Phosphor `rocket-launch` glyph: the thing whose path is
  contested. Sitting calmly at the fork, no exhaust, no blast.
- **A small human figure at ground level near the origin** — the human-scale
  reference point the curves are measured against; standing composed, looking up at
  the fork, neither panicking nor celebrating.
- **A simple control lever on a short pedestal beside the figure, the figure's hand
  resting on it** — the control question: a hand on the controls, held not lost.
  Plain and matter-of-fact; no snapped linkage, no crossed-out switch.
- **A low ground/horizon line** — one plane under figure, lever, and rocket alike
  (mirrors the sibling compositions).

## Mood
Neutral and editorial — a fork in a trajectory held calmly open, with a person at
human scale and a hand still on the lever. Whether the climb is sharp or slow, and
whether the hand stays on, are the open questions. Not a doom scene, not a launch
celebration.

## Avoid
Photorealism; more than one color; gradients/shadows; explosions, exhaust flames,
blast clouds, or smoke (verdict: violent takeoff); menacing or towering robots, robot
hands, or red-eye motifs (verdict: doom); broken chains, snapped tethers, or
crossed-out switches (verdict: control already lost); fireworks, trophies, or raised
arms (verdict: triumph); warning signs, skulls, mushroom clouds; a figure fleeing or
cowering; making one curve dashed, thinner, or fainter than the other (verdict on
which trajectory is real); fussy internal detail (rocket panel lines, dial numbers,
facial features); clutter; anything that reads as pro- or anti-AI.

## Deliverable
Ideally **vector (SVG)**, single-color, transparent ground. PNG accepted
(the pipeline is raster-primary).

## Generation prompt (Nano Banana / Gemini)
**Frameless** — the art has NO drawn border. The CSS tile renders the rounded-square
frame. Lessons carried over from the earlier generations: force the soft fill to
~15–18% (it renders near-invisible if unstressed) and force uniform stroke weight
(thin secondary elements drift thinner).

**Fresh-generation prompt:**
> A minimalist flat vector-style icon illustration of a technology-trajectory scene, in a clean editorial line-art style. Combine several simple symbols into one small, balanced composition: as the focal point, two smooth curved paths rising from one shared origin point near the ground — one climbing very steeply, almost vertical, the other rising gently and gradually — each ending in a plain simple arrowhead, both drawn with equal emphasis; at the shared origin, a small simple rocket standing nose-up on the ground, calm and unlaunched, with no exhaust and no flames; nearby at ground level, a single simple human figure — plain round head and simple body, no face — standing and looking up toward the fork of the two paths, with one hand resting on a simple control lever mounted on a short pedestal beside them. A single thin, straight horizontal ground line runs under the whole scene — the figure, the pedestal, and the rocket all stand on the same line — no hill, no landscape.
>
> Important: NO border, NO frame, NO box or outline around the scene — just the illustration itself on a plain background. Keep the composition compact and centered, not spread wide, with the two curves given equal visual weight so neither looks like the true path.
>
> Style: monoline line art with ONE uniform stroke weight on every element — the two curves, the arrowheads, the rocket, the figure, the lever, the pedestal, and the ground line must all be exactly the same thickness. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small, about 2.5 to 3.5 times the complexity of one simple glyph — each element stays simple, the richness is the combination. No fussy internal detail — no panel lines on the rocket, no dial markings, no facial features.
>
> Color: a single blue hue, two tones only. Draw all lines in solid blue (#3b7ea1), and give the main masses a clearly visible soft fill of the same blue at about 16-18% opacity — fill the rocket body, the figure's body, and the pedestal with a light blue tint so the two-tone duotone is obviously present rather than white interiors. No other colors, no gradients, no shadows, no offset or misregistered fills, no 3D, no texture.
>
> Composition: wide 3:2 aspect, centered with generous, even padding; balanced optical weight — the fork of paths dominates gently, the figure stays clearly human-scale beside it. Plain white background. Calm, neutral, editorial mood — an open question about how fast the climb is and whether the hand stays on the lever, neither a doom scene nor a celebration. No explosions, no flames, no smoke, no robots, no broken chains, no warning symbols. No text, letters, words, or numbers anywhere in the image.

**Edit-mode instruction (after the first generation, feed the concept back in):**
> Using this image, keep the same composition, elements, and layout, but: (1) remove any border or frame around the scene entirely; (2) add a clearly visible soft light-blue fill (~16% opacity of the same hue) inside the rocket body, the figure's body, and the pedestal so it reads as a two-tone duotone instead of mostly white; (3) make every line exactly the same thickness, matching the main outline weight — including both curves, the arrowheads, and the lever; (4) keep the two curves at equal emphasis — neither dashed, fainter, nor thinner than the other. Keep it flat, single blue hue, no gradients, shadows, extra colors, or text.

**Notes:**
- Over-generate on the **two-curve fork with arrowheads** and the **hand-on-lever**
  join; those are the elements most likely to come out malformed — the generator
  tends to merge the curves, drop an arrowhead, or detach the hand from the lever.
- Watch for the generator editorializing — exhaust flames under the rocket, a robot
  figure, a snapped lever, or one curve rendered dominant sneak in easily on this
  topic; any of those breaks the required neutrality and disqualifies the candidate.
- Watch for the rocket rendering mid-flight along the steep curve — it must stand on
  the ground at the fork, or the image picks the fast-takeoff side.
- White background is intentional — the primary sits on a neutral tile; the frame
  comes from the tile, not the art.
- After generating: save as `static/img/topics/ai-takeoff-loss-of-control.png`,
  set `Topic.primary_art = "img/topics/ai-takeoff-loss-of-control.png"`, and
  regenerate the social PNGs
  (`render_social --slug ai-takeoff-loss-of-control --formats og,sq,pt`).

## Selection

**Winner: candidate 3** (`ai-takeoff-loss-of-control.gemini-3-pro-image.3.jpg`), picked 2026-08-12.
1 and 4 sit on tinted grounds (style requires white) and 4's rocket loses its silhouette at small sizes. 2 and 3 both keep white ground with filled masses (rocket, figure, control pedestal) and linework trajectory arrows; 3 wins on the tighter fork springing directly from the rocket tip and cleaner curve strokes.

**Refine rounds:** candidate 3 → edit round 1 (image.8: arrows given duotone fill — kept) → edit round 2 (image.12: regressed to hollow arrows — rejected). **Final: image.8.** Honest note for review: the 40px thumb is legible but weaker than other topics' (linework-heavy scene); the human may prefer swapping candidates or re-briefing with a bolder scene.
