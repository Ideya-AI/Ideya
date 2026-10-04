# Audit: Loneliness & Community
2026-10-03 (re-audit), verdict: ready.

This is a re-audit after the editorial fix. All three issues from the first audit are fixed, and nothing around them broke. The deaths-a-year detail no longer sets the WHO estimate against tobacco's total deaths. It now stops at the attributable-burden caveat and the WHO's "100 deaths every hour" framing. The why-it's-contested for the "epidemic" question now credits supporters and critics in parallel, with neither ruled on in the page's voice. The England detail now says the Community Life Survey has asked the question since 2013/14 and that the 2018 strategy made it a national measure, so it matches the note, and the unsourced "longest series" claim is gone. The fix also cleared some of the earlier notes:
- The Q1 detail now names its Japanese meta-analysis (Homma and Takase, Frontiers in Psychology).
- The deaths tile's unit is now "deaths", so "871,000 deaths" sets on one line.
- The "20 of 26" and "36 of 37" values no longer drop a unit onto its own line.

Read top to bottom, the page still tells one story: how much loneliness there is, then whether it is rising, whether it harms health, what drives it, and who should act. The crux follows from those questions. The four camps are distinct, each is named by what it wants, and they are argued with comparable weight. The renders, share cards and poster are current: the glance hash matches and the renders postdate topic.json. The dev server serves the fixed text.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- Repeated example: the smoking comparison now appears in three places, the position 1 steelman, the extra-risk detail and the Q2 detail. Each use is different (the claim, its provenance, the critics' reading of it), so a reader is not misled.
- Other repeated points:
  - Hawkley et al. on older Americans appears in both the young-adults stat detail and the Q1 detail.
  - The "half of Americans are lonely" multi-item point appears in the survey-question detail, the Q1 detail and the position 3 detail.
- The "Time Americans spend with friends" and "Time Americans spend alone" tiles both highlight the 2020 lockdown year. The friends detail itself calls the pre-pandemic trend "the cleaner reading". The notes do name 2020 as the pandemic year, so this is a judgment call.
- The "Share of US adults counted as lonely, by survey question" tile mixes subgroup rows (Cigna Gen Z 67, boomers 44) with whole-population rows. Cigna's overall 57 percent appears only in the detail. The rows are labeled, so nobody is misled.
- The time-alone detail quotes the WHO's 16.5 percent rise for 2003 to 2020. The tile's own figures (285 to 333) give about 17 percent. The gap is small and changes no reading.
- Q5 (AI companions): the worried side cites a named study (MIT and OpenAI, 981 people), while the hopeful side cites only "early controlled experiments". The position 4 detail does name the 2025 Journal of Consumer Research study.
- Actions: positions 1 and 2 have two actions each, and positions 3 and 4 have one each.
- Layout: at 390, the Q6 lean labels fit on one line now. Nothing is clipped at either width.
- Template:
  - Poster: the income-gradient tile keeps only four rows, so it drops the High income row (10.6), which the tile's note compares against.
  - Ranked Basics tiles show bare values with no unit.
- Links:
  - eldercare.acl.gov redirects to /home.
  - The New York State Office for the Aging ElliQ page and the Survey Center on American Life page return 403 to the checker (bot blocking).
