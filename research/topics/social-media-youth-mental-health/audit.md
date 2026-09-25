# Audit: Smartphones & Childhood
Date: 2026-09-23 (re-audit after fix). Verdict: ready.

This is a re-audit, and both issues from the first audit are fixed. The experiments chart now shows two bars that point the same way: a week or longer at 0.156, and all 27 pooled at 0.088, which is highlighted. Its note gives both figures, and the detail still explains the withdrawal effect of very short cuts, so the chart can no longer be read backwards. In the depression tile, the detail now says the rise came during the spread of smartphones and social media, which matches the chart (flat at 8 to 9 percent through 2011, then rising) and Question 1's dating of the turn to about 2012. Neither fix disturbed the text around it. The page still tells one story. The Meta settlement opens it, followed by distress data, contested evidence, policy, and independence. Eight questions lead into a crux that follows from them. Five distinct camps are written with even weight, and nothing in the page's own voice takes a side.

Mechanical checks: check_topic_text found 0 errors and 6 warnings. The warnings are all UK-spelling false positives on "unsupervised" and "analyses". check_links found 0 dead and 0 placeholder links, 5 blocked (CDC, JAMA, K-12 Legal Insights, all returning 403) and 3 redirects. The glance hash matches renders/glance.hash, and the renders are newer than topic.json. The live dev page serves the fixed text: "A week or longer" is present and "Under a week" is gone.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- Share cards: all three show only four of the five camps, so "Keep the internet open to young people without age checks" is missing from every card. This looks like a template cap at four. The og card (1200x630) also clips "Give children back independence" at the right edge ("independenc"), as views.md reports. Both are template/CSS defects.
- Stat "US suicide rate, ages 10 to 24": the highlighted bar is the 2021 peak (11.0), not the latest value (9.7, 2024 provisional). The other time series highlight their latest year.
- Stat "US states requiring school districts to ban or restrict student phones": the note says 38 states, but the detail quotes the same tracker as "at least 37 states".
- The 2024 suicide figure (9.7) is attributed to "CDC WONDER via Inside Higher Ed", but the only link is the 2023 NCHS brief, which cannot contain 2024 data. A reader cannot follow the source for that number.
- Question 1 detail: "about double the risk of depression and anxiety symptoms" (the Surgeon General's framing) sits beside the Riehm tile, which shows 1.78 for depression and anxiety alone and explains that the doubling applies to combined problems. This is acceptable in a camp's voice.
- Repetition: the Let Grow co-founding appears in the RCI stat detail, the Question 4 why, and twice in Position 4.
- Question 2 detail: "the cost of waiting … while the cost of delay … is modest" uses "waiting" and "delay" for opposite things in one sentence.
- Questions 7 and 8 build the lifelines and anonymity side's premise into their wording. Each detail contests that premise. This is a judgment call.
- Question 5: lean B "Pandemic recovery" is close to, but not the same as, the question's "phones were never the main cause".
- Position 3 lists the "US National Academies" as a proponent. The Academies are a consensus body, and their report also recommended platform standards.
- Position 2 is named "…instead of banning teens" but lists UNICEF, which the detail says accepts age limits. The detail discloses this.
- Actions: the wider-causes camp has only a reading link.
- Spelling: "wellbeing" in the Florida detail, where the rest of the page uses "well-being". The checker's six UK-spelling warnings are false positives and worth fixing in the checker.
- Renders: mobile-390/02-basics-2.png is an empty 141-byte strip. views.md is otherwise consistent.
