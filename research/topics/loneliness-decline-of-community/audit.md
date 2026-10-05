Targeted re-audit of: basics stat `share-of-us-adults-counted-as` (series and detail)

# Audit: Loneliness & Community
2026-10-05, verdict: ready

The fix from run/fixes2.md is in. The chart now has five rows, and every row is US adults overall: Cigna 57, APA weekly 30, Harvard serious 21, Gallup daily 20 (highlighted), APA every day 10. The spread now comes only from differences in the survey instrument, which is the point the chart is there to make. The note's "one in ten to more than half" still fits the rows. In the detail, the 57 is credited to Managed Healthcare Executive's coverage. The Gen Z 67 is credited to the Cigna report, which is the source the earlier audited row used, so the detail claims no more than its sources. The boomers figure is gone from the stat, and no other item on the page cites Cigna, 57 or 67, so nothing contradicts the change. check_topic_text found 0 errors. check_links found 0 dead links and 0 placeholders (1 blocked, 1 redirect). Run against the dev server, render_poster --check-only reports the poster fits with 41px of slack. The edit did not touch the summary, so the og summary is unchanged.

## Issues for editorial
none
## Issues for icons
none
## Needs research (stops the run)
none
## Notes for the human
- The layout re-render script was blocked by the permission classifier, so renders/ still shows the old six-row chart (the glance hash differs). Dropping a row can only shorten the tile, and the poster fit was checked directly.
