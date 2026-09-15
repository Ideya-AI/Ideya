# Nuclear Energy — primary icon art brief

Handoff brief for an illustrator or image/vector tool. Full style theme: `docs/DESIGN.md` (Topic art).

## Use
The topic's **primary hero image** (later: slide 1 of the topic's image carousel). Shows large on the topic page, poster, and social cards; also reduced into a rounded-square tinted tile and shown on a dark band. So it must read both large and small, on light and dark.

## Style (non-negotiable)
- **Minimal monoline** — ONE consistent stroke weight across the whole image, rounded caps/joins. References: **Gorges Beer Co** menu icons, **Flaticon "Lineal."**
- **Duotone, single color, two tones** — line at full strength + a soft (~16%) fill of the **same hue** on the masses (Phosphor-duotone logic). No second color, no gradients, no shadows.
- **Color:** the category color (Climate/Energy = **green**). Deliver single-color so it can be recolored per category.
- Flat, clean, editorial.

## Composition
A small bespoke **scene** that combines several *simple* sub-icons in one frame — about **2.5–3.5× the complexity of a single Gorges icon**. Each sub-icon stays simple; the richness is the combination, not detail on any one element. Balanced, consistent optical weight. Square (~256), legible from ~56px to hero size, and readable on a dark background.

## Elements — promise *and* peril
This topic scrambles partisan lines, so the art should hold both sides, not sell nuclear:
- **Cooling tower(s) with steam** — the signature form; the focal point.
- **An atom** — fission / clean energy.
- **A transmission pylon + power lines** — firm grid power.
- **A hill / horizon line** — grounds the scene.
- **A negative element: a radioactive-waste drum** (barrel with the trefoil) — signifies the waste & catastrophic-risk downside. *(Alt: the radiation trefoil alone.)* Matter-of-fact, not alarmist or gory.

## Mood
Neutral and editorial — neither pro- nor anti-nuclear; promise (clean firm power) and peril (waste/risk) held together in one calm image.

## Avoid
Photorealism; more than one color; gradients/shadows; fussy internal detail; clutter; alarmist/gory imagery.

## Deliverable
Ideally **vector (SVG)**, single-color, transparent ground.

## Generation prompt (Nano Banana / Gemini)
Tuned from the first generation (`nuclear-energy.concept.png`), which was close but: the soft fill came out almost invisible (~3% instead of ~16%) and the steam strokes were thinner than the rest. Energy green = `#4a9d6c`.

**Frameless** — the art has NO drawn border. The CSS tile renders the rounded-square frame, so it's consistent across topics, recolorable, and carousel-safe (a baked-in frame would double up and lock to green).

**Refined prompt (fresh generation):**
> A minimalist flat vector-style icon illustration of a nuclear energy scene, in a clean editorial line-art style. Combine several simple symbols into one small, balanced composition: two cooling towers with gently curling steam as the focal point, a small orbiting atom, a transmission pylon strung with power lines, a low rolling hill as the horizon, and a radioactive-waste barrel marked with a radiation trefoil.
>
> Important: NO border, NO frame, NO box or outline around the scene — just the illustration itself on a plain background.
>
> Style: monoline line art with ONE uniform stroke weight on every element — the outlines, the steam wisps, and the power lines must all be exactly the same thickness (do not let the steam or wires render thinner). Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small. No fussy internal detail.
>
> Color: a single green hue, two tones only. Draw all lines in solid green (#4a9d6c), and give the main masses a clearly visible soft fill of the same green at about 15–18% opacity — specifically fill the cooling towers, the hill/ground, and the waste drum with a light green tint, so the two-tone duotone is obviously present rather than white interiors. No other colors, no gradients, no shadows, no 3D, no texture.
>
> Composition: centered with generous, even padding; balanced optical weight. Plain white background. Calm, neutral, editorial mood — even-handed, neither promoting nor warning against nuclear power. No text or letters.

**Edit-mode instruction (recommended — feed `nuclear-energy.concept.png` back in):**
> Using this image, keep the same composition, elements, and layout, but make three changes: (1) Remove the rounded-square border/frame around the scene entirely — leave just the illustration on a plain white background. (2) Add a clearly visible soft light-green fill inside the cooling towers, the hill/ground, and the waste drum — about 15% opacity of the same green — so the icon reads as a two-tone duotone instead of mostly white. (3) Make every line exactly the same thickness, including the steam wisps and the power lines, which are currently too thin — match them to the main outline weight. Keep it flat, single green hue, no gradients, shadows, extra colors, or text.

**Notes:**
- Nano Banana is conversational, so constraints live in the prompt (no separate negative field). The editing path usually beats re-rolling — it preserves the composition you already liked.
- Still over-generate on the **atom** and the **radiation trefoil**; those are the elements most likely to come out wrong.
- White background is intentional — the primary sits on a **neutral tile**, not the green category tint (on green tint the soft fill disappears). The frame comes from the tile, not the art.
