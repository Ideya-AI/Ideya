# Audit: Universal Healthcare
2026-09-28, verdict: ready

The page tells one story: the United States spends the most and gets middling-to-poor outcomes and incomplete coverage, and the debate is whether the fix is who pays (one public insurer, or a regulated mix), what care costs (price caps), a market reset, or a catastrophic floor. The why-now is the September 2026 Census uninsured report, which belongs to this topic and sets up the subsidy lapse and Medicaid work requirements that the Basics tiles then cover. Basics is balanced: tiles unfavorable to the US (spending, avoidable deaths, the Commonwealth rank) sit beside tiles unfavorable to single-payer and NHS systems (Canadian waits, the NHS England list, NHS satisfaction) and tiles where the US does well (stroke survival, local availability). Sources that lean one way carry a matching caveat on both sides (Fraser, PNHP authors, Commonwealth Fund). The seven questions are fairly worded, each gives both cases at similar length, and the crux follows from Questions 2, 3, 4 and 6. All five camps are named by what they want. Their steelmen and details are within a few words of each other in length (233 to 247 words), each answers its strongest objection, and the page's own voice takes no side. Mechanical checks were clean: 0 text errors, 0 dead or placeholder links, and four links blocked by bots (CBO x2, ACP Journals, Fraser) plus one redirect (HealthCare.gov local help). The renders are newer than topic.json. The live page at localhost:8641 matches them.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- Repetition, none of it misleading: the Canadian wait appears in the Canada stat, question 4 and the single-payer rebuttal. The private-insurer versus Medicare price gap appears in the RAND stat, questions 2 and 3, and the price-cap camp. "Much of the life expectancy gap comes from causes outside medicine" appears in the life-expectancy stat, question 6 and the market camp. Question 2 and the single-payer detail both say prices are set "as Canada's provinces and Medicare (already) do", almost word for word.
- Two Basics tiles report the same fact, US spending the most: share of GDP and spending per person, both from OECD Table 1.6. The per-person tile earns its place through the price and volume split in its detail, but a reader sees the US on top twice.
- Guarantee everyone catastrophic coverage (position 5) cites RAND via Niskanen: a $211 billion cut, "about 8.7 percent" of total national health spending. Against the $5.3 trillion that stat 1's detail gives for 2024, $211 billion is about 4 percent. The RAND base is probably a different year or population. Worth checking against the Niskanen piece, and naming the base if it is narrower.
- Question 3 detail gives physicians per 1,000 people (2.7 US, 3.9 OECD) without naming a source. It is presumably OECD Health at a Glance, which is linked under Actions. Question 6 cites "a randomized IRS outreach experiment" without naming the study. Adding "(OECD)" and the study authors would satisfy the source rule outright.
- Question 5 "case for keeping it" says "150 million people" have employer plans. Stat 2 detail gives 53.5 percent employment-based coverage, about 180 million. Rhetorical rounding inside a case, but the two sit oddly together.
- Stroke tile: the label says "stroke", the note says "ischemic stroke". Harmless, but the label could say ischemic.
- The CBO range tile shows its value as "-0.7–0.3" with a hyphen-minus next to an en dash, which reads awkwardly at glance size. A true minus sign, or "−0.7 to +0.3" if the schema allows, would read more cleanly.
- Actions: the single-payer camp gets two camp-tagged actions (the Medicare for All Act and National Nurses United). Each other camp gets one. Not misleading, but it is the only unevenness on the page.
- Template/CSS: ranked charts mix polarity. Lower is better for avoidable deaths and stroke, higher for life expectancy and satisfaction, and the US bar is green in all of them. The labels make each chart clear, but a reader skimming bars could read long as good. At 1440, the Medicare-X action's camp tag wraps to two lines, right-aligned, beside the Policy label. On mobile, ranked-chart bars are very short (about 45px), so the differences are hard to see.
