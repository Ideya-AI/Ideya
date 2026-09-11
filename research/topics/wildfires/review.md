# Living With Wildfire — review packet (2026-08-01)

**Status:** DRAFT loaded as `wildfires`. Stages: research 1 fix round, distribute 0 fix
rounds (3/3 first pass) + 1 view-feedback `fix_only` round, icon 1 round, views 1 round.
New catalog entry (115th) authored from scratch — Wildfires was not in the universe;
skeleton added to `topic-universe.json` with related links to climate-tipping-points,
net-zero-pace, and housing-affordability-crisis (TopicEdges created).

## Substance gate (stage 1) — 4/4
- **neutrality** ✓ — all six camps steelmanned at parity; the two most contestable stats
  carry explicit both-readings detail text; asymmetry flows through prevalence (85→22).
- **steelman** ✓ — each position endorsable in its own voice; Jack Cohen correctly
  claimed by two camps.
- **fact-source** ✓ after 1 fix round — the critic caught 5 real defects the fixer
  applied: LA firestorm death toll 29→31, dead Moody's URL replaced, Zone 0 described
  as finalized → still draft regulation, the 4–12M pre-1800 burn range corrected to the
  cited task-force PDF's ~4.5M, and the 98.9% initial-attack figure rescoped from
  national to Pacific-Northwest (national = 98%).
- **crux** ✓ — "Do we still get a vote on the fire itself — or only on what it finds
  when it arrives?" judged a genuine narrowing against the nuclear gold standard.
- The planner **added a sixth camp** the skeleton lacked: Thinning Skeptic (Hanson/
  Ingalsbee wing), prevalence 22 — honest non-balance carried through weights.

## Presentation gate (stage 2) — 3/3 first pass
Distill 7 edits · distribute 25 edits (reorder so each camp's headline stat leads).
Fold above "Go deeper": basics **8/12**, questions **4/7**, positions **6/6**.
22 substance + 19 presentation editorial notes ride in the JSON for your review.

## Icon
Winner: `candidates/wildfires/wildfires.gemini-3-pro-image.1.jpg` — cleanest uniform
monoline; flame-at-treeline → drip torch in the firebreak → four-dot ember arc landing
on the hardened house; legible at 40px. Promoted to `static/img/topics/wildfires.png`
(1035×690); prompt provenance in `Topic.primary_image_prompt`. Note: the composition is
a wide horizontal strip, so it under-fills the portrait share card's art tile (~45%
height) — swap candidates or run an `--edit` round if that bothers you.

## Views
Desktop-1440, mobile-390, mobile-320, OG/square/portrait cards, print poster — all
render; **poster fits with 13px slack** (exit 0). 7 critics + adversarial verification:
12 confirmed findings (0 refuted), 32 notes. The one content-fixable defect (the
beneficial-fire ranked tile wrapping its row labels into a 6-line sliver) was routed
back through `distribute_topic.js --fix_only`, which set the tile `wide` and re-packed
the grid — re-rendered and verified clean.

## Engineering issues (for you — the pipeline does not touch CSS)
- **Range-viz ghost dot**: `_stat_tile.html:32` hard-codes `<span class="ghost"
  style="left:95%">` on every range stat (a Nuclear-era artifact) — on the embers tile
  it reads as a phantom data point at 95. Make it data-driven or drop it.
- **Range viz shows a midpoint pin, not a band**: "60–90%" renders as one pin at 75
  (plus the ghost) — nothing marks 60 or 90; a skimmer can read the range as ~75–95.
- **`.rrow` fixed 64px label column at all viewports** (`ideya.css:281`) — root cause
  of ranked-label wrapping; label column should widen in wide tiles / narrow viewports.
- **Poster multi-word unit collapse REPRODUCED**: "13–19 M ha missing" renders
  "13–19Mhamissing" on the poster (the known housing bug, still open; web surfaces are
  fine).
- **Poster/cards truncate 6 camps to 4 with no "+2 more" indicator** (template slice
  `:4`); the two dropped camps are the lowest-prevalence two — order is right, but a
  reader can't tell the list is partial.
- **Mobile position cards have no visible tap affordance** to reach detail; Positions
  is the one section without a Go-deeper control.
- New-topic gap: related-topic edges are seeded only by `load_universe` — the pipeline
  doesn't create them (I created wildfires' three edges manually this run).
- Fixed this run (pipeline tooling): the poster `?fit=1` stamp never fired under
  current headless Chrome (rAF removed; stamps synchronously now), and `render_social`/
  `render_poster` silently default to dead `localhost:8000` — always pass `--base-url`.

## Post-critique update (2026-08-01, after the view renders above)
Per your participation changes: question ANSWER OPTIONS (lean poles) were added to 6 of
7 wildfires questions (the three-way attribution question has no binary axis, so it
correctly has none), the position agree/disagree bar was removed site-wide, and votes
are upvote-only. The desktop/mobile screenshots were re-rendered after these changes;
the social cards and poster carry no vote UI and did not change.

## Check in 5 minutes
- The fact-source fixes were re-verified by the re-gate, but eyeball the LA-firestorm
  stat (31 deaths, $25–30B insured) and the initial-attack detail (98% national /
  98.9% PNW) — the two most-cited numbers.
- Title casing: "Living With Wildfire" — decide "With" vs "with".
- The poster's three questions are all empirical (the values question sits just below
  the `:3` slice) — fine if intended, easy re-tier if not.
- OG/square/portrait cards show the top-4 camps by prevalence (Cultural Fire Steward
  and Thinning Skeptic drop) — confirm that's the pick you want.

## To publish
```
.venv/bin/python manage.py load_topic_draft --file research/topics/wildfires.json \
  --slug wildfires --title "Living With Wildfire" --category climate-env \
  --status published --image-brief research/icons/wildfires.md
```
→ set `reviewed_at = now()` → `check_links --topic wildfires` (0/0) → commit
`research/runs/wildfires/record.json`, `research/topics/wildfires.json`, the icon assets,
the catalog entry, and this packet.
