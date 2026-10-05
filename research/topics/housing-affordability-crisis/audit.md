Targeted re-audit of: basics.stats[17] (homelessness)

# Audit: Housing Affordability
2026-10-05, verdict: ready. Both mechanical checks are clean: check_topic_text shows 0 errors and 0 warnings, and check_links shows 29 of 29 ok. The one issue from the last round is fixed. The NLIHC sentence ("first year-on-year decrease since 2016") is gone from the homelessness detail, both in topic.json and on the live dev page. That leaves every claim in the detail sourced to the linked HUD report. The rest of the tile still holds from the earlier fix. The value is 745,652. The 3 percent fall from the record 771,480 matches the note. The 4 percent emergency-shelter fall and the 3 percent unsheltered fall to 266,320 are consistent. No other item on the page states a homelessness figure. The note's claim that individual and chronic homelessness hit new highs agrees with the detail. This round's edit touched only expanded detail text, so the glance, summary and share cards are unchanged by it.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- The layout postfix check (postfix.sh) did not run, because the auto-mode classifier blocked it. Nothing here independently confirms the poster fit or the og summary clamp. The editor reports the poster fits at data-fit=-10, and the summary text has not changed. The section renders predate the earlier homelessness value and note change: the glance hash in renders/ differs from the current one.
