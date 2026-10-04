# Audit: Antimicrobial Resistance
Date: 2026-10-01 (re-audit after the notes pass). Verdict: ready.

The page still tells one story. Resistance is rising, and the fight is over which lever does the most work: restraint on farms and in clinics, guaranteed payments for new drugs, or wider access. Two counter-camps answer them: veterinarians against the farm-cut camp, and public or nonprofit R&D against payments. The crux follows from the questions and positions above it, and the why-now event (the World Health Assembly's 2026–2036 action plan) belongs to this topic. The previous audit found no issues. This pass checked that the editor's later changes to its notes held and broke nothing around them:
- The 2050 projection tile now highlights the GBD attributable figure (1.91) instead of the O'Neill 10 million scenario, so the glance no longer stresses the figure its own detail calls a scenario.
- The England stat is now labeled "England's top yearly payment per subscription antibiotic" and reads cleanly.
- Question one's "manageable" side now says the 2019-to-2021 fall was partly because fewer people died of other infections, which matches the first stat tile.
- At 1440 expanded, the 2050 tile's Respond link renders in full.

Mechanical checks pass. Text check: 0 errors and 4 "Organisation" warnings, all inside the proper noun. Link check: 27 ok, 2 CDC links blocked (403), none dead. The glance hash matches renders/glance.hash (9c5911d974db388b), and every render postdates topic.json (15:06:46 and later, against 15:06:05). The live page at localhost:8641 carries the fixed text.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- Stat "Projected yearly deaths from drug resistance in 2050" (carried over): the source label names both the GBD paper and the O'Neill review, but the only link is the GBD PubMed abstract, so a reader cannot follow the O'Neill 10 million through it. The highlight now sits on the GBD figure, which narrows the gap. A link to the O'Neill final report would close it if the schema allowed a second URL.
- Stat "US sales of medically important antibiotics for food animals" (carried over) still glances as "16% rise", and position four argues against that one-year rise. The note balances it with "27% below their 2015 peak." Which figure leads is a judgment call.
- Repetition (carried over, none verbatim): China's colistin ban appears in its stat tile, question five, position four's rebuttal and action two. Prevention recurs across several stats, questions one, four and eight, and positions three and four. Both are central to the debate.
- Position five ("Fund public and nonprofit antibiotic R&D") sits behind Go deeper and is off the share cards by design. It does not outweigh any of the first four.
