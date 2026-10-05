Targeted re-audit of: positions order (positions[3] and positions[4] swapped)

# Audit: AI Existential Risk
Date: 2026-10-05. Verdict: not ready (blocked on renders).

The fix landed and is correct. "Accelerate AI development to capture its benefits" (rust) is now fourth and "Put AI’s present harms ahead of extinction scenarios" (purple) is fifth. Both items are unchanged apart from their position and keep their ids, and the color keys run green, blue, amber, rust, purple. Actions point to camps by name, so they are unaffected, and their order already listed accelerate before present harms. Nothing in the crux, the questions or the actions refers to camps by position. The dev page at localhost:8641 shows the new order. check_topic_text has 0 errors; its 8 lean-label-length warnings were there before the fix. check_links found 27 links: 23 ok, 4 redirect, 0 dead, 0 placeholder. The page itself is ready. The shipped share cards are not. The views and layout step (postfix.sh) was blocked by the permission classifier and never ran. All three cards in static/img/social/ (ai-existential-risk.png, -sq.png, -pt.png, timestamped 2026-10-05 01:59) predate the topic.json edit (13:38). The landscape card still shows "Put AI’s present harms ahead of extinction scenarios" as the fourth camp and leaves out accelerate. That is exactly the misreading the fix was meant to remove, so anyone who shares the page would spread it. The poster fit and the og-summary clamp were also not measured by this run, though the editor reports the poster fits with 85 px to spare.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- The share cards and poster must be regenerated from the current topic.json, and the post-fix layout check (postfix.sh) must be run, before this topic can be marked ready. The run was stopped because auto mode blocked the script, not because of any content defect. After a clean re-render, if the cards show accelerate as the fourth camp and the poster and og summary fit, run mark_ready with no further editorial pass.


2026-10-05: the blocked step ran (postfix.sh: 0 errors, poster fits, og not clamped, share cards and poster re-rendered from the current topic.json). Marked ready per this audit.
