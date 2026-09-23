# Audit: Living With Wildfire

2026-09-21 — **ready**

The page tells one story and holds it from the first line to the last. The overview
poses the loss and asks which lever shrinks it and who is obliged to pull it; Basics
supplies the loss (structures, dollars, deaths), the exposure (interface growth), the
hazard (warming, fuel deficit, ignition sources) and the price of each lever; the eight
questions are the branch points between those levers; the six camps are the levers
themselves; and the crux — decided by the fire or by the town — is the question the
first question already asked, now stated as the thing everything above was arguing
about. Steelmanning is even to an unusual degree: every camp runs 240 to 280 words,
every camp is named by what it wants rather than by a posture, every camp answers its
hardest objection, and the four that argue about the land disagree with each other as
sharply as they do with the two that argue about the house. The numbers hold together
across items (14 million added interface homes matches the 30.1 → 44.1 series; three
quarters of a trillion matches $768 billion; a decade of suppression against a single
Los Angeles January matches $2.52 billion a year against $65 billion). Nothing is said
twice: where a figure reappears — the fall in global burned area, the doubling of
western forest area — it reappears in a different voice doing different work. Mechanical
checks are clean: 0 errors, and 28 links with 0 dead and 0 placeholder.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- Basics, `ember-resistant-zone-effect-on-ignition`: the one place the page's own voice
  answers an objection instead of leaving it standing. The detail raises the two real
  objections to California's Zone 0 rule (tearing out a mature yard, inspecting millions
  of parcels) and then replies to the second — "Enforcement is also what the measure's
  own logic asks for… That is why California wrote the requirement as a rule for
  everyone in a hazard zone rather than as advice." Every other contested tile stays
  level in the same spot: the prescribed-burn tile says "the standing argument on both
  sides," the treatment-efficacy tile says "it cuts both ways." Since Zone 0 is also
  half the why-now, the effect is that Basics defends the news the page chose. Cutting
  the last two sentences would cost nothing the reader needs.
- Order of Basics: the first tile is acres burned, and its own detail then calls acreage
  "the oldest wildfire number and the weakest," while the second tile says structure loss
  "tracks the social cost of fire far better than acreage does." Order is the site's only
  weight mechanism, so leading with the metric the page discounts is a deliberate-looking
  choice. Defensible — it is the live 2026 number the why-now rests on, and the debunk is
  part of the point — but worth a second look. Smoke deaths sitting eleventh is the same
  kind of call in reverse: the page calls it "the exposure almost everyone shares."
- The crux says four camps would change the fire and two would change the town. That is
  an accurate count of the page as written, and it means the camp roster is 4–2 on the
  axis the page names as the whole debate. The positions are genuinely distinct and
  evenly written, so this does not read as favoritism, but it is the one structural
  asymmetry on the page.
- `insured-losses-january-2025-los-angeles` is sourced to Wikipedia — the only Wikipedia
  citation on a page that otherwise cites NIFC, PNAS, IBHS, the Forest Service and the
  FAIR Plan, and it carries one of the page's largest figures ($40B insured, $65B total,
  31 deaths). An insurance-industry or state source would sit better under that number.
- `forest-service-acres-treated-for-hazardous`: a reader who divides the plotted series
  (4.1 → 2.6) gets a 37 percent fall against the stated 35 percent. Rounding explains it,
  but the two numbers sit in the same tile.
- "Beneficial fire" is used twice in the fourth question's detail (400,000 acres of goal,
  188,881 delivered) without a foothold; every other term of art on the page is glossed
  in place, including Zone 0 and the interface.
- Template/CSS, not content: at 390 the ranked-bar track is roughly 45px wide whatever
  the labels are, so 10.12 / 8.92 / 8.54 in the first tile and 44.0 / 11.5 in the Camp
  Fire tile are visually near-identical. The numbers are adjacent, so nothing is lost,
  but the viz is doing no work on mobile.
- Template/CSS, not content: at 1440, expanding a short wide tile beside a very tall
  narrow tile (Forest Service acres beside Prescribed burns, FAIR Plan beside Smoke
  deaths) leaves a column of dead space several hundred pixels tall. Visible in
  `renders/sections/desktop-1440-expanded/02-basics-3.png`.
- `topic.json` has no `primary_image_prompt`, which SCHEMA.md lists as a stage-3 field.
  nuclear-energy and universal-basic-income are missing it too, so it is a pipeline gap,
  not a defect in this topic.
- `check_links` notes, neither a failure: five 403s from publishers that block automated
  requests (Science, PNAS, ScienceDirect, congress.gov, westernpriorities.org) and two
  redirects (Yale ISPS to its resource page, Springer to a cookie-consent URL).
- `check_topic_text` warns on "Firewise" in the eighth action; it is NFPA's program name.
