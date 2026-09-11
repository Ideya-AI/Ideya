# Causes & Cures of Economic Inequality — primary icon art brief

Handoff brief for an illustrator or image/vector tool. Full style theme: `../ICONOGRAPHY.md`.
Template siblings: `nuclear-energy.md` (the tuned reference), `universal-basic-income.md`,
`housing-affordability-crisis.md`, `ai-future-of-work.md` — the other **Economy & Work**
topics, and this icon's nearest neighbors on the wall.

**Revised 2026-09-02 after a failed generation round** — the first version put three
identical human figures on the steps and the generator drew them at ascending sizes in
all ten candidates (see Notes). Figures are gone; the positions are marked by identical
plain discs.

## Use
The topic's **primary hero image**. Shows large on the topic page, poster, and social
cards; also reduced into a rounded-square tinted tile and shown on a dark band. Must
read both large and small, on light and dark.

## Style (non-negotiable)
- **Minimal monoline** — ONE consistent stroke weight across the whole image, rounded
  caps/joins. References: **Gorges Beer Co** menu icons, **Flaticon "Lineal."**
- **Duotone, single color, two tones** — line at full strength + a soft (~16–18%) fill
  of the **same hue** on the masses. No second color, no gradients, no shadows.
- **Color:** the category color (Economy & Work = **econ amber**, `#b98a35`).
  Deliver single-color so it can be recolored per category.
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
The debate is how far income and wealth gaps in rich democracies widened, what drove
them, whether the **gap itself** is the right target rather than the floor, and which
levers would close it. The art must render **positions on one shared structure** —
identical markers at different heights on the same regular form — and leave the verdict
open: no villain, no rescue, no direction of travel:
- **A three-step staircase as one continuous filled mass** — the focal point: a plain
  stepped block ascending across the scene, equal tread and equal rise on every step,
  standing on the ground line, drawn flat in side profile. The regularity is the
  neutrality device: the structure is not accused of anything, it is simply the thing
  the positions sit on. It nods at the topic's Phosphor `chart-bar-horizontal` glyph in
  profile only — it is a **staircase, not a chart**: no axis, no baseline ticks, no
  bars separated by gaps, no descending or ascending trend line.
- **Three identical plain discs, one resting on each step** — the positions in the
  distribution: simple filled circles, all three **exactly the same diameter**, one
  centered on each tread, each about half a tread wide. Same unit, different height —
  the difference in the scene belongs to the structure, not to what stands on it.
  Deliberately abstract markers, **not** people and **not** money: no rim ring, no
  double-ring edge, no slot, no markings, no stacking, no faces, no limbs. The circular
  form is doing legibility work too — round masses read instantly against the
  rectilinear steps at 40px, where a square token would merge into them.
- **A plain upright control lever beside the staircase** — a small filled rectangular
  base standing on the ground line, a short horizontal slot across it, and a straight
  vertical rod rising from the center of the slot, topped by a short horizontal grip
  bar (a T-shaped lever handle, not a ball). Held **exactly upright, centered in its
  travel** — the policy lever exists and has not been pushed either way. Which lever,
  and how far, is the topic's question.
- **A single straight horizontal ground line across the scene** — one plane under the
  staircase and the lever alike (mirrors the sibling compositions). The lowest step
  sits clearly above that line, so no disc rests at zero: the scene is about the
  distance between positions, not about a floor nobody reaches.

## Mood
Neutral and editorial — one regular structure, three identical markers at different
heights on it, and a control set at neither extreme. Whether the distance between them
is the problem, what opened it, and which lever should move are the open questions the
scene holds. Not a rich-versus-poor tableau, not a protest, not a prescription.

## Avoid
Photorealism; more than one color; gradients/shadows; **human figures of any kind** —
this scene has none, and repeated figures in particular are barred: the generator
cannot hold several of them at one size and will grow them with the steps, which
asserts that the people differ rather than their positions (measured failure, see
Notes); discs drawn at different sizes, or the top disc larger than the others (the
same defect in the marker); a bar chart, a descending or rising bar series, a Lorenz or
Gini curve, a pie chart, a trend line, an axis, tick marks, percent signs, or any arrow
or chevron indicating direction (verdict: which way the gap is going); coins,
double-ring coin rims, banknotes, dollar signs, stacked or piled money, money bags,
gold, top hats, mansions, yachts (money caricature — and the coin motif belongs to the
UBI icon on the same amber wall); a hand reaching down or pushing down, a ladder
against the steps, a rope or chain between the discs, a disc rolling or falling off the
stairs (verdict: the cure or the crime); cracked or crumbling steps, a broken stair, a
seesaw, a tipping scale, scissors cutting anything; a two-pan balance scale (owned by
the UBI icon and it renders a fairness verdict); protest signs, placards, raised fists,
crowds; flags, party symbols, or government seals; fussy internal detail (stair-tread
nosings, hatching or shading inside the steps, panel lines or screws on the lever
base); clutter; anything that reads as advocacy for or against redistribution.

## Deliverable
Ideally **vector (SVG)**, single-color, transparent ground. PNG accepted
(the pipeline is raster-primary).

## Generation prompt (Nano Banana / Gemini)
**Frameless** — the art has NO drawn border. The CSS tile renders the rounded-square
frame. Lessons carried over from the earlier generations: force the soft fill to
~15–18% (it renders near-invisible if unstressed), force uniform stroke weight (thin
secondary elements drift thinner), and make every major element a **filled mass** —
earlier linework-only elements nearly vanished at 40px. New this topic: repeated
elements must be a primitive the model can clone (identical circles), never repeated
figures — it silently scales those with their position and will not correct them.

**Fresh-generation prompt:**
> A minimalist flat vector-style icon illustration of a stepped-structure scene, in a clean editorial line-art style. Combine several simple symbols into one small, balanced composition: at the center, a simple three-step staircase drawn as ONE continuous solid stepped block, ascending from left to right, with every step exactly the same tread width and the same rise height as the others, standing on the ground and drawn flat in side profile — a plain staircase, NOT a bar chart, with no separated bars, no axis, no baseline, no tick marks and no labels; resting on each of the three steps, one plain simple circle — three circles in total, all three EXACTLY the same diameter as each other, each about half a step's tread wide, each sitting centered on its step; the circles are plain abstract discs, NOT coins and NOT people — no rim ring, no double ring, no slot, no markings, no faces, no heads, no arms or legs; to one side, standing on the ground beside the staircase, a plain upright control lever — a small solid rectangular base with a short horizontal slot across it, a straight vertical rod rising from the center of the slot, and a short horizontal grip bar across the top of the rod like a T-shaped lever handle, held perfectly upright and vertical, not tilted or pushed to either side. A single thin, straight horizontal ground line runs across the whole scene — the staircase and the lever base both stand on it — no landscape, no hill; the lowest step of the staircase sits clearly above that ground line.
>
> Important: NO border, NO frame, NO box or outline around the scene — just the illustration itself on a plain background. Keep the composition compact and centered, not spread wide. There are NO human figures, people, silhouettes, or characters anywhere in this image. Give the three circles equal emphasis — identical diameter, identical shape, none larger, smaller, or more detailed than the others; do not scale them with the height of the step they rest on.
>
> Style: monoline line art with ONE uniform stroke weight on every element — the staircase, the three circles, the lever's base, rod and grip bar, and the ground line must all be exactly the same thickness. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small, about 2.5 to 3.5 times the complexity of one simple glyph — each element stays simple, the richness is the combination. No fussy internal detail — no stair-tread edges or nosings, no hatching or shading inside the steps, no screws, bolts or panel lines on the lever.
>
> Color: a single warm amber hue, two tones only. Draw all lines in solid amber (#b98a35), and give EVERY major element a clearly visible soft fill of the same amber at about 16-18% opacity — fill the whole stepped staircase block, all three circles, and the lever's base and grip with a light amber tint so the two-tone duotone is obviously present rather than white interiors; no major element may be left as unfilled outline-only linework. No other colors, no gradients, no shadows, no offset or misregistered fills, no 3D, no perspective, no texture.
>
> Composition: wide 3:2 aspect, centered with generous, even padding; balanced optical weight — the ground line runs level along the bottom, the stepped block anchors the middle with one identical circle on each step, the upright lever stands to one side. Plain white background. Calm, neutral, editorial mood — identical markers resting at different heights on one regular structure, with a control set at neither extreme and the outcome left open; not a rich-versus-poor scene, not a protest, not a solution. No people or figures of any kind, no bar charts, graph curves or trend lines, no arrows or chevrons, no ladders, ropes, chains or broken steps, no hands, no coins, banknotes, dollar signs or money bags, no top hats, no mansions or shacks, no balance scales, no raised fists or placards, no flags. No text, letters, words, numbers, tick marks, percent signs, or scale markings anywhere in the image.

**Edit-mode instruction (after the first generation, feed the concept back in):**
> Using this image, keep the same composition, elements, and layout, but: (1) remove any border or frame around the scene entirely; (2) add a clearly visible soft light-amber fill (~16% opacity of the same hue) inside EVERY major element — the whole stepped staircase block, all three circles, and the lever's base and grip — so it reads as a two-tone duotone with no outline-only elements left; (3) make every line exactly the same thickness, matching the main outline weight — including the lever's rod, the slot in its base, and the ground line; (4) redraw the three circles as one identical circle repeated three times — same diameter, same shape, one centered on each step — and keep them plain discs with no rim ring, no double ring, no markings, and no faces or limbs; (5) make the staircase one continuous stepped block with equal tread and equal rise on every step, and remove any axis, baseline, tick marks, gaps between bars, arrows or labels so it cannot read as a bar chart; (6) stand the lever perfectly upright and vertical with a short horizontal grip bar across the top of its rod, not tilted and not a ball knob; (7) remove any human figure, silhouette, or character if one has appeared. Keep it flat, single amber hue, no gradients, shadows, extra colors, or text.

**Notes:**
- **Recorded failure (2026-09-02) — do not put repeated human figures on a structure in
  this pipeline.** The first version of this brief asked for three identical figures,
  one per step. Across ten candidates (4 fresh + 6 edit-mode) the generator drew them at
  ascending sizes, growing with step height; the residual defect measured a stable ~1.30×
  width / 1.25× height deficit on the figure at the bottom (95×72 px vs 124×89 and
  124×88). Edit mode fixed the top two relative to each other but never moved the third,
  including when told explicitly which figure was undersized, by how much, and with pixel
  dimensions supplied — three rounds, zero movement. Assume the model ties figure scale
  to vertical position and cannot be argued out of it. When a topic needs repeated
  equal-weight elements, use a primitive it can clone (identical circles) rather than
  figures; if a future topic truly needs a person, use exactly one.
- Over-generate on the **three equal circles** and the **lever**. The circles are the
  neutrality device — any candidate whose discs differ in size, or that scales them with
  step height, fails the same way the figures did. The lever wants to render as a
  lollipop, a lamp, a signpost, or a tilted joystick; the base-plus-slot came through
  cleanly last round, so it is the rod's top that needs watching (T grip bar, not a ball).
- Watch for the staircase drifting back into a **bar chart** — separated bars, an axis, a
  baseline, ticks, or a trend arrow sneak in easily on an inequality topic. This held up
  in every candidate last round, but the Phosphor chip already carries the chart idea and
  the raster icon must read as a scene.
- Watch for the discs reading as **coins** — a rim ring or a double-ring edge is what
  makes a circle money, and the coin motif belongs to the UBI icon on the same wall.
- Watch for the generator adding a **cure or a villain** — a hand reaching in, a ladder
  or rope between steps, a broken step. Any of those breaks the required neutrality.
- Watch for outline-only elements — every major mass must carry the amber fill; a
  candidate whose staircase or discs render as bare linework fails the 40px test.
- White background is intentional — the primary sits on a neutral tile; the frame
  comes from the tile, not the art.
- After generating: save as `static/img/topics/economic-inequality.png`,
  set `Topic.primary_art = "img/topics/economic-inequality.png"`, and
  regenerate the social PNGs
  (`render_social --slug economic-inequality --formats og,sq,pt`).

## Selection

**Winner: `economic-inequality.gemini-3-pro-image.14.jpg`** → `static/img/topics/economic-inequality.png`
(1035×690), promoted 2026-09-02.

Chosen on balance and disc placement: the three discs sit cleanly on the step tops
rather than tucking behind the risers (candidates 11 and 13), padding is even on both
sides, and the lever came through as a real lever — filled base block with its slot, a
straight rod at the house stroke weight, and a filled T-grip. Candidate 12 has larger
discs (174px vs 137px) and is marginally bolder at 40px, but its lever rod renders as a
single hairline thinner than every other stroke, which fails the uniform-monoline rule.

Disc equality verified by measurement, not by eye: 137 / 137 / 136 px across the three
(1.007× spread). The three sibling candidates measured 141/141/142, 174/174/174 and
141/141/141 — the revised disc concept fixed the defect that ten figure-based candidates
could not.

Family fit checked against the current house style rather than the oldest amber pair:
`encryption-vs-lawful-access` and `moral-status-of-animals` (both 2026-08) carry the same
saturated duotone fill as this one. The older `universal-basic-income` and
`housing-affordability-crisis` use a noticeably paler wash — the family has drifted
heavier, and this icon matches where it is now, not where it started. Worth a deliberate
call at some point about which weight the wall should settle on.
