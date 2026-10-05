Targeted re-audit of: questions[0].detail, questions[2].why

# Audit: Policing Reform
Date: 2026-10-05. Verdict: ready.

Both fixes landed and read cleanly. questions[0].detail now says killings by police "reached a record in 2024", which matches the lead stat (1,383 in 2024, 1,314 in 2025, Mapping Police Violence). No other item on the page makes a current-record claim about killings. questions[2].why now ends with the federal-agent sentence, naming Egbert v. Boule (2022) as its own source. That gives the why-now (a suit against the United States, an immigration agent and officials) a foothold among the accountability items. "All but closed" and "mainly claims against the United States" claim no more than the holding supports, and they agree with the why-now's list of defendants. Cutting "not Congress" and "Congress has repeatedly failed to change it" removes no fact a reader needs. "Returned in September 2025" keeps the reintroduction date. The why still reads neutrally, and the lean labels are unchanged. Mechanical checks: check_topic_text shows 0 errors and 1 warning (questions[2].why at 283 characters, accepted because the fix needs the sentence). check_links shows 0 dead and 0 placeholder (4 redirect, 2 blocked). On the live page at 1440 the lengthened why is not clamped (scrollHeight equals clientHeight).

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- The glance hash changed (36187b2a2732c60c against 88002f3bb3e67dc1 in renders/glance.hash), so the renders under renders/sections/ predate this fix. The post-fix layout script (postfix.sh) was blocked by auto mode and did not run. The poster's crux and the og summary are unchanged; only the 390 Questions tile is unchecked.
