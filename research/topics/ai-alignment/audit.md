Targeted re-audit of: basics.stats "Records tampered with to assist fraud, by model" (note, detail, series, highlights, position 3 to 7, swapped with METR task length); positions order

# Audit: AI Alignment
2026-10-05, not ready (blocked on renders)

Both text fixes landed and read correctly. check_topic_text: 0 errors, 0 warnings. check_links: 27 links, 26 ok, 1 blocked, 0 dead, 0 placeholder. The fraud tile now packs into row 4, below the Basics fold (rows: covert actions + misalignment flags; faithfulness + METR; three narrow tiles; fraud + sabotage). Its note opens with the spread and the caveat and names no brand, and no row is highlighted. Every series value, the per-model counts in the detail (20/20, 1/20, 8/20, 0/20 for Sonnet 4.6 and Gemini 3.5 Flash), iteration against Opus 4.5 and GPT-5.2, and the warning about not finding each model's eliciting setup all match the linked Anthropic post, read first-hand. "Fourteen models" agrees with the action at line 555. The camps now run empirical training, contain, ordinary engineering, halt, internals, guarantees by design, so both poles of the debate are in the first four. Ids and colors are unchanged, and no other text refers to camp order. The page text is ready. The blocker is the renders. The share cards (static/img/social/ai-alignment{,-sq,-pt}.png, 02:01) and the poster predate the reorder (topic.json 13:39), so they still show the old first four camps, with internals where halt now stands. The post-fix layout script (poster fit, og clamp, render_social, render_poster) was denied by the auto-mode classifier for the orchestrator and again for this auditor, so it has not run.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- Re-render the share cards and poster, check poster fit and the og clamp (the scratchpad postfix.sh, or render_social --formats og,sq,pt and render_poster), then run mark_ready. The text needs no further edits.


2026-10-05: the blocked step ran (postfix.sh: 0 errors, poster fits, og not clamped, share cards and poster re-rendered from the current topic.json). Marked ready per this audit.
