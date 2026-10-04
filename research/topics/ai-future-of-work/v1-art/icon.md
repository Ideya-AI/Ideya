# AI & the Future of Work — primary icon art brief

Handoff brief for an illustrator or image/vector tool. Full style theme: `docs/DESIGN.md` (Topic art).
Template siblings: `nuclear-energy.md` (the tuned reference), `universal-basic-income.md`,
`democratic-backsliding-populism.md`, `ai-takeoff-loss-of-control.md`.

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
- **Filled masses, not linework-only** — lesson from the last topic: thin unfilled
  curves nearly vanished at 40px. Every major element in this scene is a filled
  shape carrying the duotone tint; nothing important may be a bare line.

## Composition
A small bespoke **scene** combining several *simple* sub-icons in one frame — about
**2.5–3.5× the complexity of a single Gorges icon**. Generate wide (3:2); framing is
normalized in post (trim to content, ~8% pad, fit 3:2 on white). Legible from ~40px
to hero size, readable on a dark background.

## Elements — promise *and* peril
The debate is where AI taking on cognitive work **ends up** — augmented workers and
new roles, mass displacement, a post-labor economy, or an outcome institutions still
get to choose. The art must show work in transition with the relationship between
human and machine left ambiguous, never render a verdict:
- **A simple shared worktable** — the focal plane: one plain table, a single filled
  slab on simple legs, that both sides stand at. Sharing one surface is the
  neutrality: neither side owns the workspace.
- **A single simple human figure on one side of the table** — plain round head and
  simple filled body, no face; standing composed at the table, one hand resting on
  it. Neither slumped nor triumphant, not walking away, not being pushed out.
- **A simple abstract machine element on the other side** — a plain articulated
  machine arm rising from a small filled base unit on the same tabletop, its simple
  two-finger effector hovering near the shared document at the same height as the
  figure's hand. Abstract and tool-like, not a humanoid robot; equal visual weight
  to the figure. Whether it is helping, handing over, or taking over stays unreadable.
- **A single blank document or sheet at the table's center, between hand and
  effector** — the cognitive work itself, the thing in transition; a plain filled
  rectangle with no writing, claimed by neither side.
- **A briefcase standing on the ground beside the table, on the human's side** —
  echoing the topic's Phosphor `briefcase` glyph: work as livelihood and identity;
  upright and intact, simply present. Not dropped, not discarded, not carried out.
- **A low ground/horizon line** — one plane under figure, table, and briefcase alike
  (mirrors the sibling compositions): everything stands on the same ground.

## Mood
Neutral and editorial — a person and a machine at one table, the work between them,
the briefcase still standing. Whether this is augmentation, replacement, or something
institutions still get to decide is the open question the scene holds. Not a layoff
scene, not a utopia, not a duel.

## Avoid
Photorealism; more than one color; gradients/shadows; a robot seated in the human's
chair or the human shown leaving, shrunken, or displaced (verdict: replacement); the
figure raising arms, high-fiving the machine, or discarding tools (verdict: triumph);
unemployment-line, pink-slip, cardboard-box, or begging imagery (verdict:
displacement doom); a humanoid robot body, robot face, or red-eye motifs; the machine
arm looming over or dwarfing the figure; broken tools, crossed-out workers, downward
charts, alarm clocks; sad or angry posture; fussy internal detail (keyboard keys,
screen contents, facial features, panel lines on the arm); clutter; anything that
reads as pro- or anti-automation.

## Deliverable
Ideally **vector (SVG)**, single-color, transparent ground. PNG accepted
(the pipeline is raster-primary).

## Generation prompt (Nano Banana / Gemini)
**Frameless** — the art has NO drawn border. The CSS tile renders the rounded-square
frame. Lessons carried over from the earlier generations: force the soft fill to
~15–18% (it renders near-invisible if unstressed), force uniform stroke weight (thin
secondary elements drift thinner), and make every major element a **filled mass** —
the last topic's linework-only elements nearly vanished at 40px.

**Fresh-generation prompt:**
> A minimalist flat vector-style icon illustration of a work-in-transition scene, in a clean editorial line-art style. Combine several simple symbols into one small, balanced composition: at the center, a plain simple worktable — a single solid tabletop slab on simple legs; on the left side of the table, a single simple human figure — plain round head and simple body, no face — standing composed with one hand resting on the tabletop; on the right side of the table, a simple abstract machine arm rising from a small box-shaped base unit sitting on the same tabletop, its plain two-finger gripper hovering near the center of the table at the same height as the figure's hand — an abstract mechanical tool, NOT a humanoid robot, with no face and no body; between the hand and the gripper, a single blank rectangular sheet of paper lying flat on the tabletop, claimed by neither side; and on the ground beside the table on the figure's side, a simple upright briefcase with a handle, standing intact. A single thin, straight horizontal ground line runs under the whole scene — the figure, the table legs, and the briefcase all stand on the same line — no hill, no landscape.
>
> Important: NO border, NO frame, NO box or outline around the scene — just the illustration itself on a plain background. Keep the composition compact and centered, not spread wide, with the human figure and the machine arm at equal visual weight on either side of the table — neither larger, taller, nor more dominant than the other.
>
> Style: monoline line art with ONE uniform stroke weight on every element — the figure, the table, the machine arm and its base, the sheet of paper, the briefcase, and the ground line must all be exactly the same thickness. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small, about 2.5 to 3.5 times the complexity of one simple glyph — each element stays simple, the richness is the combination. No fussy internal detail — no facial features, no panel lines or bolts on the machine arm, no writing on the paper, no stitching on the briefcase.
>
> Color: a single amber hue, two tones only. Draw all lines in solid amber (#b98a35), and give EVERY major element a clearly visible soft fill of the same amber at about 16-18% opacity — fill the figure's body, the tabletop slab, the machine arm's base unit and arm segments, the sheet of paper, and the briefcase with a light amber tint so the two-tone duotone is obviously present rather than white interiors; no major element may be left as unfilled outline-only linework. No other colors, no gradients, no shadows, no offset or misregistered fills, no 3D, no texture.
>
> Composition: wide 3:2 aspect, centered with generous, even padding; balanced optical weight — the table anchors the middle, the figure and the machine arm balance each other across it. Plain white background. Calm, neutral, editorial mood — a person and a machine sharing one workspace with the work between them, and whether this is collaboration, handover, or takeover left an open question; not a layoff scene, not a celebration, not a confrontation. No humanoid robots, no empty chairs, no boxes of belongings, no downward charts, no crossed-out symbols, no raised fists. No text, letters, words, or numbers anywhere in the image, including on the paper and the briefcase.

**Edit-mode instruction (after the first generation, feed the concept back in):**
> Using this image, keep the same composition, elements, and layout, but: (1) remove any border or frame around the scene entirely; (2) add a clearly visible soft light-amber fill (~16% opacity of the same hue) inside EVERY major element — the figure's body, the tabletop, the machine arm's base and segments, the sheet of paper, and the briefcase — so it reads as a two-tone duotone with no outline-only elements left; (3) make every line exactly the same thickness, matching the main outline weight — including the machine arm's segments, the table legs, and the briefcase handle; (4) keep the figure and the machine arm at equal visual weight — neither taller nor more dominant. Keep it flat, single amber hue, no gradients, shadows, extra colors, or text.

**Notes:**
- Over-generate on the **machine arm** and the **hand/gripper meeting over the
  sheet**; the arm is the element most likely to render as a humanoid robot,
  over-detailed, or looming, and the generator tends to merge the gripper with the
  paper or the figure's hand.
- Watch for the generator editorializing — a robot with a face, the figure turned
  away or slumped, an empty chair, or the arm towering over the person sneak in
  easily on this topic; any of those breaks the required neutrality and disqualifies
  the candidate.
- Watch for text appearing on the paper or the briefcase — both must stay blank.
- Watch for outline-only elements — every major mass must carry the amber fill; a
  candidate whose paper, arm, or figure renders as bare linework fails the 40px test.
- White background is intentional — the primary sits on a neutral tile; the frame
  comes from the tile, not the art.
- After generating: save as `static/img/topics/ai-future-of-work.png`,
  set `Topic.primary_art = "img/topics/ai-future-of-work.png"`, and
  regenerate the social PNGs
  (`render_social --slug ai-future-of-work --formats og,sq,pt`).

## Selection

**Winner: candidate 4** (`ai-future-of-work.gemini-3-pro-image.4.jpg`), picked 2026-08-12.
All four render the shared-worktable scene. 4 wins on checklist fit: every major element carries the duotone fill and reads cleanly (2's briefcase is an unreadable slab, 3's gripper collapses into broken linework, 1's crane-style arm and table perspective are weaker); hand and gripper sit at equal distance from the unclaimed sheet, keeping the ambiguity structural.
