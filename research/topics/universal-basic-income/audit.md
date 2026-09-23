# Audit: Universal Basic Income

Date: 2026-09-22
Verdict: ready

The page tells one story and holds it from top to bottom: a recurring unconditional
payment, what it would cost, what the trials say it does to work, and the two rival
answers (better-targeted transfers, a guaranteed job) that the cost arithmetic keeps
pushing back into view. Basics opens with the number everyone argues about and the
trial that cuts against the advocates, which is the right order for a topic whose
believers are the ones most often accused of dodging cost. The six positions are
distinct camps, named by what each wants rather than by posture, and they come in
within twenty words of each other in length; the two behind Go deeper (category
allowances, full replacement) are genuinely the two a reader is least likely to have
met, so order carries weight correctly. The crux lands where the questions and the
positions actually converge, and its two panels split the work question cleanly into
the evidence nobody has and the value judgment no evidence would settle. Both mechanical
checks pass: 0 errors and 0 warnings from check_topic_text, and 25 of 26 links OK with
one IMF PDF returning 403 to an automated request. Nothing on the page would mislead or
confuse a reader.

## Issues for editorial
- none

## Issues for icons
- none

## Needs research (stops the run)
- none

## Notes for the human
- The OECD budget-neutral simulation is the most-travelled item on the page. A reader
  who opens everything meets it seven times: two Basics tiles, two question details,
  two position details and one action card. Two of those are near-verbatim restatements
  of the Basics tile a reader has already opened. "Who moves into poverty" detail says
  the UK's "aggregate poverty gap narrows even as the headcount rises, because a flat
  payment reaches the very poorest, who are often the people missing from the claiming
  system"; question two closes with "a flat payment narrows the UK poverty gap while
  raising the headcount, because it reaches the very poorest, who are often missing from
  the claiming system." Question five's "For a floor" paragraph likewise repeats the
  same tile's sentence about unemployment insurance and disability payments exceeding
  any flat rate. The position details restating it are defensible, since a camp arguing
  in its own voice should reach for its best evidence; the two question details are the
  avoidable ones and could cite the finding without re-deriving it.
- Crux subtitle: "the money comes from taxes on the same society that receives it. How
  much of it comes back decides what the policy costs." On first pass "it" reads as
  though it could be the society rather than the money, and the chain from the lead
  (do people do more or less) through earnings to tax receipts is left for the reader to
  supply. The sentence resolves on a second read; a few words would save the first.
- Question seven ends "The two models that tried to project a national program from this
  evidence, Penn Wharton's and the Roosevelt Institute's, came out 16 points of GDP
  apart." In a paragraph otherwise about cost, "16 points of GDP apart" reads as a cost
  disagreement; the two models are in fact projecting the program's effect on GDP. The
  Penn Wharton Budget Model's 2018 UBI analysis and the Roosevelt Institute's 2018
  macroeconomic report would settle which quantity is meant and confirm the gap.
- Why it matters now carries three dated claims in the page's own voice (Cook County,
  20 November 2025; Texas, 1 January 2026; the Supreme Court tariff ruling, 20 February
  2026) and the schema gives why_now no source field, so none of them names a source a
  reader can follow. The tariff dividend is also the one event on the page that appears
  nowhere else, so a reader meets "President Donald Trump's promised $2,000-a-person
  dividend" without learning when it was promised or what it was.
- Scope excludes "cash transfers judged as development policy," and the page then draws
  on Kenya, Iran and the IMF's emerging-economy figures, and question two argues about
  countries with no benefit registry. The distinction intended (using those cases as
  evidence about unconditional cash, not judging them as aid) is coherent, but the
  exclusion line is narrower than it sounds against what follows.
- "Gross cost of $1,000 a month for every US adult" puts a 2019 cost bar in the same
  ranked chart as 2025 budget aggregates. Both the note and the detail disclose the
  six-year gap, so the tile is honest; it is worth knowing that the glance layer invites
  an apples-to-apples comparison the tile itself then withdraws.
- "Employment effect across randomized US pilots" has no headline value, so the tile
  opens straight into its two bars, and the longer bar (3.2) is the fall while the
  shorter (0.8) is the rise. It works only because the direction is written into each
  series label. Worth watching if that pattern is reused elsewhere.
- No template or CSS defects observed. Renders (15:32-15:36) are newer than topic.json
  (03:13) and match the live page at localhost:8641. The IMF link's 403 is a blocked
  automated request, not a dead URL.
