# Audit: Assisted Dying
2026-09-30 (re-audit after an editorial fix), verdict: ready.

Both issues from the first audit are fixed, and the fixes break nothing around them. First, the "Assisted deaths as a share of all deaths" detail now names each row's own report (RTE, Health Canada, Belgium's federal commission, Swiss FSO, Go Gentle Australia, Oregon Health Authority, Spain's Ministry of Health), and its source label says so. Second, the "US public support" chart now shows three figures from one year and one source: the linked May 2024 Gallup poll (71, 66, 53). The 2025 and 2026 morality figures and the British polls move into the detail with their pollsters named. The rest of the page reads as it did before. It is one account of the debate: where the eligibility line belongs and whether the request stays the person's own. There are seven well-ordered questions and five camps named by what they want, argued with similar energy. The crux follows from Q2, Q5 and the disability camp. Proponents now use semicolons, which follows the schema change, and they render as dot-separated lists. Checks: check_topic_text shows 0 errors and 1 warning (the palliative care stat note is 208 characters). check_links shows 0 dead and 0 placeholder, with 2 redirects and 1 blocked. The glance hash matches, so the renders are current. The dev server at :8641 serves the fixed text. Nothing on the page would mislead a reader.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- New, US public support tile: the chart now gives 53 percent "morally acceptable" for 2024, and the detail says the figure was also 53 in 2025 before 49 in 2026. A reader meets 53 as both the 2024 and the 2025 value. That can be right, but it is worth checking that the linked 2024 Gallup article carries 53 for its own year, since the earlier draft attached 53 only to 2025. The article itself settles it; I did not open it.
- New, sources named but not linked: six of the seven rows in the share-of-deaths chart, Gallup's 2025 and 2026 morality figures, BSA 2025 and YouGov 2025 are now named in their details but have no URL. A reader can find each one, though not in one click. The glance note's Spain figure ("one in 750") still sits directly above the Dutch-only link.
- New, cosmetic: the US tile's source line reads "Gallup, Values and Beliefs poll, May 2024 · 2024", so the year appears twice.
- Layout, from views.md (content-caused, minor): at 1440 the ring-stat units ("% of deaths", "% of cases", "% worldwide") drop to their own line under the value. At 390 the lean label "Consent must be now" wraps, as do the long position names used as action lean tags. Nothing is clipped.
- Carried from the first audit (judgment calls, unchanged):
  - No sanctity-of-life or religious camp. The prohibition camp argues on secular grounds.
  - The why-now's France date (18 August 2026) has no source of its own. The first auditor remembered a Commons bill history that differs from the page; the Pharmaceutical Journal article settles it.
  - "DIGNITAS is the only provider that accepts non-residents" may be wrong; Pegasos is a possible second.
  - The extend camp's "a fraction of one percent … to a few percent" sits beside Basics' 6.0 and 7.9.
  - The Oregon chart highlights "Losing autonomy" although it ties at 89.
  - The CPS tile's "6 of 209 cases" reads as six prosecutions; the note says eight.
  - The Oregon prescriptions detail says "read that unused third differently" without saying how.
  - The "both sides cite / invoke / reach for" tic runs across six details.
  - The terminal-legalization camp has two actions.
  - Courts and a UN body appear as proponents.
  - Dated facts in question details carry no source field.
  - Template: the crux toggle still reads "See how it resolves" when expanded.
  - Links: Compassion & Choices and DIGNITAS redirect, and Dying With Dignity Canada returns 403 to the checker.
