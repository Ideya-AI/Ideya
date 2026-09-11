# What Drives the Housing Affordability Crisis — review packet (2026-07-11)

**Status:** DRAFT loaded as `housing-affordability-crisis`. This was the pipeline's
end-to-end validation run. Stages: research 3 fix rounds, distribute 0 fix rounds (gate
passed first pass after the reorder), icon 1 round, views 1 round.

## Substance gate (stage 1) — 3/4, one residual
- **neutrality** ✓ — all five camps steelmanned at parity; asymmetry carried by prevalence + facts.
- **steelman** ✓ — each position endorsable in its own voice.
- **fact-source** ✗ (residual) — flagged citation-attribution fixes: cost-burdened-renters stat should cite JCHS *State of the Nation's Housing 2025* (not *America's Rental Housing 2024*); zoning-premium city shares are Glaeser, Gyourko & Saks (2005), not the cited 2003 FRBNY paper; "Albert Saks" → "Raven Saks"; "fourth" → "third consecutive record year". **A human should apply these before publishing** — the numbers are right, the source labels/years need correcting.
- **crux** ✓ — genuine narrowing, no house verdict.

## Presentation gate (stage 2) — 3/3
- **compact-self-sufficiency** ✓ · **reading-level-fit** ✓ · **above-fold-selection** ✓
- The distribute stage reordered so each camp's headline stat leads: it pulled the tier-1
  "Social/public housing share" (Tenant-Decommodifier evidence) above the fold and dropped
  the tier-3 homeownership stat below.
- Fold above "Go deeper": basics **7/12**, questions **4/7**, positions **5/5**.

## Icon
Winner: `candidates/housing-affordability-crisis/…-image.1.jpg` — cleanest uniform
monoline, clear duotone, best hierarchy (raised house + climb arrow + person + padlocked
house), legible at 40px. Promoted to `static/img/topics/housing-affordability-crisis.png`
(1035×690). Prompt provenance stored in `Topic.primary_image_prompt`.

## Views
Desktop-1440, mobile-390, mobile-320, OG card, and the print poster all render correctly;
hero art shows on every surface; fold reads as designed. Poster fit: **4px slack** (exit 0).

## Engineering issues (for you — the pipeline does not touch CSS)
These are pre-existing template bugs the view critic surfaced; they affect every topic,
not just this draft:
- **"Connects to" chips overflow at 320px** — related-topic chips don't wrap/scroll below
  ~360px, so long titles clip off the right edge. At 390px they fit. Needs a `white-space`
  wrap or the RESPONSIVE.md horizontal-scroller pattern.
- **Poster collapses a stat unit** — "3.7 M homes" renders as "3.7Mhomes" on the poster
  (the desktop tile is correct). Whitespace handling in the poster stat-unit template.

## Check in 5 minutes
- The four fact-source citation corrections above (source labels/years — quick, cited).
- Confirm the OG card / poster showing 4 of 5 positions (condensed cap) is the intended pick order (Georgist drops).

## To publish
```
load_topic_draft --file research/topics/housing-affordability-crisis.json \
  --slug housing-affordability-crisis --title "What Drives the Housing Affordability Crisis" \
  --category economy --status published --image-brief research/icons/housing-affordability-crisis.md
```
→ set `reviewed_at = now()` → `check_links --topic housing-affordability-crisis` (0/0) →
commit the dossier, topic JSON, icon assets, and this packet.
