# Audit: Electoral Rules
2026-11-21, verdict: ready. This is a re-audit after a fix. The twin (refresh of electoral-system-design) tells the same story as the live page: two debates, how votes become seats and how to weigh access against checks, which meet in a crux about what makes an election legitimate. Questions, positions, crux and nine of ten actions are unchanged from the live page. The refresh made five changes. The why-now now leads with the November 3, 2026 ballot results and keeps the Burnham commission with a named source. Stats 7 and 12 record those results. The confidence tile moved from Gallup 2024 to Pew's 2026 midterm reading, and the 2024 Gallup figures are kept in its detail. The dead ACE guide link was replaced by IDEA's Electoral System Design handbook. The SAVE America Act vote that left the why-now is still in stat 1, and the Labour pledge is still in the crux subtitle. The one issue from the last audit is fixed. The confidence tile's closing sentence now gives the verification side a reading drawn from the tile's own mail-ballot gap, as specific as the access side's reading, so the two sides are even again. The dev server serves the fixed wording. Comparing the twin item by item with the live page: no regression against the live page. check_topic_text shows 0 errors and 2 warnings on "November 2026" in stats 12 and 14; both refer to past events or cite a source, so neither will go stale. check_links: the CDCE PDF and makevotesmatter.org.uk show as dead, but both were already verified as false positives (a TLS chain error, and a 200 when fetched with a browser user agent); one link is blocked (403) and one redirects. These are notes, not failures. The Chrome extension did not connect, so the live-browser pass was not done. I read the page from the 390 and 1440 renders, whose glance hash matches topic.json, and read the expanded detail the fix touched from topic.json. I also checked the three share cards.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
none
