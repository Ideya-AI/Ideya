# Audit: AI & Copyright
2026-11-23, verdict: ready

Re-audit after a layout fix. All three issues from the first audit are fixed, and the renders are current (glance hash 0ba8a8a221357df3 matches, renders newer than topic.json). The statutory damages tile is now wide, so "$750–30,000 per work" reads as one figure at 1440 and at 390. The Llama tile is relabeled "Llama 3 training data" and sits on one line. The entrenchment question's lean label is now "Favors incumbents" and fits its button at 390. Making the damages tile wide reflowed the Basics grid. The new rows pair cleanly, collapsed and expanded, with no orphaned or broken tiles. On a full reread the page still tells one story. The why-now (the Third Circuit's Westlaw ruling) leads into the litigation, scale and licensing figures, then eight questions that build to a crux that maps onto the four camps. The camps are even in length, evidence and energy, and each is named by what it wants. Lean labels are fair opposites, highlights mark the row each note is about, and the three share cards are clean. Nothing would mislead or confuse a reader.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- check_links reports the Llama 3 source (https://ai.meta.com/blog/meta-llama-3/) as DEAD (HTTP 400). Re-checked 2026-11-23: a HEAD request returns 200 and a GET with a browser user agent returns 400, so the 400 is Meta blocking scripted clients, not a missing page. It is blocked, not dead. The checker could treat a GET 400 that follows a HEAD 200 as blocked.
