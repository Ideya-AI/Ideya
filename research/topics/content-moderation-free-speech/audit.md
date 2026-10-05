Targeted re-audit of: actions[choose-or-run-your-own-moderation].url, plus the four earlier fixes (basics.stats[x-s-trust-and-safety-staff].detail, basics.stats[us-adults-who-say-harassment-targets].detail, crux.values, actions[become-a-community-notes-contributor-on].for_position)

# Audit: Content Moderation
2026-10-05, targeted re-audit after a fix pass, verdict: ready.

The one open issue is fixed. The Bluesky action now links to https://atproto.com/guides/moderation, which returns 200 with no redirect and is titled "Moderation - AT Protocol". It covers labels, subscribing to moderation labelers, creating a labeler and running Ozone, so it fits both halves of the action's title and description. check_links: 27 links, 24 ok, 0 dead, 0 placeholder; one redirect (EFF donate) and two blocked (counterhate 403, Internet Association 429) are notes only. check_topic_text: 0 errors; the 7 warnings are lean-label length plus a false-positive "humor". The four earlier fixes still hold: the X staffing detail ends "The figures are as reported by the Associated Press."; the Pew harassment-lawsuit detail has no pipeline voice; the crux values read "a diffuse loss of lawful speech"; the Community Notes action is tagged "Give users control of moderation", which matches the fifth position. Layout checks were run separately and are clean.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
none
