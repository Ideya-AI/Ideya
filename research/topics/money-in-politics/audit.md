# Audit: Money in Politics
2026-10-03, verdict: ready

This is a re-audit after one editorial fix. The single issue raised before is fixed. The crux's values panel now reads "justifies limits on political spending" instead of "restricting political speech", so the page no longer settles question 2 in its own voice one clause before calling it open. The editor also acted on the Q2 note. The question now ends at "a form of protected speech?" and its lean labels are "Is speech" / "Isn't speech", which answer it cleanly. The glance hash moved (a60a64c2bb7f2520), and every render, share card and the poster were regenerated after topic.json, so they are current. The dev server at :8641 serves the new crux and Q2 text. Neither change broke anything around it. At 390 the Q1, Q2 and Q8 lean labels now sit on one line, and the crux lead and share cards are unchanged. The rest of the page reads as before: one story built on NRSC v. FEC, Basics ordered from cost to context, eight questions that are real fault lines, four camps of even energy each named by what it wants, and a crux that follows from them. Mechanical checks are clean. check_topic_text has 0 errors (the three "fundraising" warnings are false positives). check_links finds 23 ok, 1 redirect, 3 blocked and 0 dead.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- Template (from views.md): currency units that are not dollars render after the number, so the UK tile reads "94.5£ million". Ranked charts never show their unit (rows read "5.6", "304", "93.9"), and only the note carries it.
- Repetition: the claim that money just finds a new route when rules tighten appears in the outside-spending detail, in Q3's why and detail, and in the details of positions 2, 3 and 4. A reader meets it about six times.
- Basics pattern: 11 of the 16 stat details close with a "Reformers read this as X; defenders answer Y" pair. Each pair is balanced, but the pattern moves argument into Basics and the closing sentence becomes predictable.
- Crux lead: "limits on what people spend to be heard" leans slightly toward speech-camp wording, balanced by "distort democracy" in the same sentence. Changing it means regenerating the share cards.
- Position 1: "which Republican Representative Tom Barrett introduced in near-identical form in June 2026" does not say what the amendment is near-identical to.
- Position 3 lists two proponents (ACLU, Michael Malbin), where the other camps list six or seven. Position 4 has one action, where the others have two.
- Super PAC cash chart: every bar is a Republican, crypto or AI fund. The one Democratic figure, House Majority PAC, is given as money raised, not cash on hand. Worth checking against the NBC list.
- FEC detail: "By March 2026 the Senate had not acted" is seven months old. The tile's count of two commissioners is sourced to the FEC page as accessed today, so the facts agree.
- Equal Citizens action: it says the group "is defending" Maine's super PAC cap in federal court. The case's current stage is worth confirming on the group's page or the First Circuit docket.
- Q3 detail quotes Samuel Issacharoff ("wrote in 2026") without naming where.
- Links: the UK Electoral Commission and OpenSecrets outside-spending pages return 403, and the web.archive.org snapshot returns 429. That is bot blocking, but each link is worth a manual click. ifs.org/donate redirects to the site's donation page.
