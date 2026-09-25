# Audit: Smartphones & Childhood
Date: 2026-09-24 (re-audit after a detail-text fix). Verdict: ready.

This re-audit follows a fix to two items that the 2026-09-23 audit listed as notes. Both are now resolved. First, the suicide-rate tile now links to the Inside Higher Ed article that reports the 2024 CDC WONDER figure (9.7). Its source line names both that article and the 2023 NCHS brief, and the detail says which figures come from which source. Second, the phone-ban tile's detail no longer reads "at least 37" against a headline of 38. It now says the tracker "has kept rising, to at least 39 states" as of July 28, which fits a June 2 headline of 38. The fix touched only expanded text and source fields. The glance hash matches renders/glance.hash (44516ba749e7ba91), and every render is newer than topic.json. The dev server serves the new text. The rest of the page is unchanged. It tells one story: the Meta settlement opens it, followed by the distress data, the contested causal evidence, the policy responses, and the independence thread. Eight questions lead into a crux that follows from them. Five distinct camps are written with even weight, and nothing in the page's own voice takes a side. check_topic_text found 0 errors and 0 warnings. check_links found 0 dead and 0 placeholder links, 4 blocked (CDC twice, JAMA, K-12 Legal Insights, all 403) and 3 redirects (National Academies, Nature twice).

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- Share cards: all three still show only four of the five camps. "Keep the internet open to young people without age checks" is missing from every card, which looks like a template cap at four. The og-card clipping of "independence" that the last audit reported is gone.
- Stat "US suicide rate, ages 10 to 24": the link now goes to Inside Higher Ed, so the 2007–2021 and age-band figures are credited to "CDC NCHS Data Brief No. 471 (2023)" by name only, with no link. A reader can still find the brief by its number. The highlighted bar is still the 2021 peak (11.0), not the latest value (9.7), unlike the other time series.
- Stat "US states requiring school districts to ban or restrict student phones": the headline is 38 (June 2) and the detail gives "at least 39" (July 28). The detail explains the rise, but a reader meets two counts from the same tracker.
- Question 1 detail: "about double the risk of depression and anxiety symptoms" sits beside the Riehm tile, which shows 1.78 for internalizing problems alone. This is acceptable in a camp's voice.
- Repetition: the Let Grow co-founding appears in the RCI stat detail, the Question 4 why, and twice in Position 4.
- Question 2 detail: "the cost of waiting … while the cost of delay … is modest" uses "waiting" and "delay" for opposite things in one sentence.
- Questions 7 and 8 build the lifelines and anonymity side's premise into their wording. Each detail contests that premise. This is a judgment call.
- Question 5: lean B "Pandemic recovery" is close to, but not the same as, the question's "phones were never the main cause".
- Position 3 lists the "US National Academies" as a proponent. The Academies are a consensus body, and their report also recommended platform standards.
- Position 2 is named "…instead of banning teens" but lists UNICEF, which the detail says accepts age limits. The detail discloses this.
- Actions: the wider-causes camp has only a reading link.
- Spelling: "wellbeing" in the Florida detail, where the rest of the page uses "well-being".
- Renders: mobile-390/02-basics-2.png is still an empty 141-byte strip. views.md records it as the blank tail.
