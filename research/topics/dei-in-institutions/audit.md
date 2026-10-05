Targeted re-audit of: basics.stats[0].note, basics.stats[1] series order, positions[3]/positions[4] order

# Audit: DEI in Institutions
2026-10-05, verdict: ready

All three fixes are in place and read correctly. basics.stats[0].note now says "run from 1989 to 2015 … with no decline over the period". That matches the tile's source_published (1989–2015) and its detail, which says the studies "stop at 2015". The sentence no longer reads as a claim about today. In basics.stats[1] the series now runs Black all workers 12.7, Black managers 8.8 (highlighted), Women all workers 47.1, then Women chief executives 33.0. The first four rows, which the poster takes, now include both workforce baselines. Values and the highlight are unchanged. "Target help by economic disadvantage, not race or sex" is now positions[3], so it is fourth and makes the cards. "Protect free inquiry from both DEI mandates and DEI bans" is fifth. Their color keys were swapped to keep the color order, and the proponents and text did not change. Both actions with a for_position still match their camp names exactly. The new order fits what q5.why says about institutions moving to income and adversity criteria. No other item depends on the old order. check_topic_text shows 0 errors and 1 warning. The warning is a dated sentence in action[5], which this fix did not touch. check_links shows 0 placeholders and 1 dead link, the Conference Board URL, which this fix did not touch. That link failed on a timeout, and curl with a browser user agent returns 200 for it again, so it is a false positive.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- The post-fix render step did not run because the auto-mode classifier blocked postfix.sh. The share cards in static/img/social/dei-in-institutions*.png (02:02) and the poster are older than topic.json (13:39), and the glance hash has changed. They still show the free-inquiry camp as fourth and the old stats[1] row order. Run render_social (og,sq,pt) and render_poster for this slug before publishing. The editor reports poster fit at -20 px, so nothing overflows. The summary did not change, so the og clamp is unchanged.
