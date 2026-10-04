# Audit: Birth-Rate Decline
2026-09-29 · verdict: ready (re-audit)

This is a re-audit after an editorial fix. All four issues from the first audit are fixed, and nothing around them broke. The Quebec tile now names the review it reports: Bergsvik, Fauske and Hart, 2021, Population and Development Review. The Italy 2025 figure is credited to ISTAT's March 2026 indicators. The CBO tile no longer carries the OECD clause that contradicted the page's own old-age-ratio tile. The Pew tile now attributes its reading ("those who argue that preferences… lean on this survey more than any other"), which matches how the Gallup tile is framed. The page still tells one story: sub-replacement fertility, then whether policy works, barriers or preferences, legitimacy, economic harm, Korea, immigration, meaning and the right or left package, then a crux that follows from Q1 to Q4. The four camps are distinct and evenly argued. The why-now belongs to the topic. The mechanical checks are clean: 0 errors, and 28 of 29 links OK (CBO is blocked with a 403, which is a note). The glance hash equals renders/glance.hash, so the renders are current. The fix touched only expanded detail text. I confirmed on the dev server that the new text is loaded and that the expanded Quebec and CBO tiles lay out cleanly at 1440.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- Every note from the first audit stands unchanged:
  - The Nordic fall, "cash moves births earlier" and "pressure lands on women" each recur across items.
  - Q8's "why" leans slightly toward the marriage side.
  - Q1's "Every study finds some effect" is a strong universal.
  - Q2's detail gives the barriers side no cited evidence.
  - The "Raise" steelman says "Most people want more children than they have".
  - The US tile gives 1,599.5 per 1,000 as its glance figure.
  - The family spending tile says "spends the least" and uses the marriage tax-advantage jargon.
  - The IHME tile says "UN's projections run higher".
  - The UN Population Division is listed as an Adapt proponent.
  - Some figures are named but unlinked (UNFPA 1950, Al Jazeera 360 trillion won, Poland evaluation, OECD 13 percent).
  - France "-6,000" uses an ASCII hyphen.
  - The expanded 1440 grid leaves an empty third column.
  - views.md miscounts the desktop glance tiles.
- New, minor:
  - Quebec detail: a comma is missing after "North America and Australia" and before "found".
  - Family spending detail: "Poland and Hungary… are below [the OECD average] on fertility" holds for 2024–25. But the page's Hungary tile shows 1.61 in 2021, the spending year, and the chart does not list Hungary. A reader who compares the two tiles may pause.
- The CBO link returns 403 to the checker (bot blocking). The page opens in a browser.
