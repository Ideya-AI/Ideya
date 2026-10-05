Targeted re-audit of: durable-dates pass

# Audit: Taxing Extreme Wealth
2026-10-05, verdict: ready

The only change since the ready audit is that time-sensitive wording is now tied to explicit dates. check_topic_text reports 0 errors. Its seven warnings are expected: six are date-anchored sentences, and the "next year" in question[2].detail means the year after a gain, not a calendar year. check_links finds 0 dead links and 0 placeholders. One link redirects (Warren score) and four are blocked by scripted-host refusals; neither counts as a failure. I checked each reworded sentence against the diff. All figures, dates, names and attributions are unchanged, and no new claim was added. "Unpublished working paper" became "2025 working paper, not a peer-reviewed publication", which says the same thing and matches the source label. "Has already seen billionaires leave" became a past-tense statement tied to the January 1, 2026 cutoff, with the same fact. Every changed sentence reads naturally and will still read true after November 3, 2026. That includes the why-now ("Proposition 40, on California’s November 3, 2026 ballot, is …") and the retitled voter-guide action. I searched the file for remaining now-anchored wording (this year, next year, currently, pending, so far, not yet, upcoming, will, today) and found none that goes false when a date passes. The remaining present-tense uses are either general ("today’s system", "current taxes") or explicitly dated ("in 2026 the exemption is $15 million"). The editor has already flagged the one remaining dependency: once the vote happens, the Proposition 40 result belongs in the why-now, the poll tile and the two campaign actions. Glance text changed, so the card and poster renders are re-run by the orchestrator.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- After November 3, 2026, add the Proposition 40 result to overview.why_now, stat[8] and the two campaign actions (action[2], action[3]).
