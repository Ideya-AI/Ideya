# Smartphones, Social Media & Youth Mental Health — review packet (2026-09-04)

**DRAFT `social-media-youth-mental-health`** · 12 stats · 7 questions · 9 positions · 10 actions
Fold above "Go deeper": basics 9/12 · questions 6/7 · positions 6/9

## Look
[page](http://localhost:8641/social-media-youth-mental-health/) · [expanded](http://localhost:8641/social-media-youth-mental-health/?expanded=1)
[1440](desktop-1440.png) · [390](mobile-390.png) · [320](mobile-320.png)
[OG](../../../static/img/social/social-media-youth-mental-health.png) · [square](social-media-youth-mental-health-sq.png) · [portrait](social-media-youth-mental-health-pt.png) · [poster](social-media-youth-mental-health.pdf)
The first two need the dev server up on 8641.

## Run
substance 5/5 recorded (steelman, fact-source, shape PASS; neutrality and claim-ledger recorded FAIL, closed outside the gate — see below) · presentation 4/4 (both critics + editorial-shape + claim-fidelity PASS)
ledger 72/72 closed on the shipped draft (55 supported, 17 resolved-by-revision, 0 open) · fidelity 55 carried-in claim(s) checked · lint 0 · links 0/0 (22: 15 ok, 1 cookie-wall redirect, 6 bot-walled) · poster fits (23px)
Rounds: research 4 launches (2 died on session limits; the 4th completed, 61 agents, 0 errors) · distribute 1 + 1 fix_only · icon 1 (candidate 3 of 4) · views 1 · PM 1 (0 routed)

## Decided for you
- Neutrality FAIL (3) and claim-ledger FAIL (2) were closed by orchestrator prescription, and every replacement fact was checked by a blind claim-verifier before it went in. The critics' own prescribed facts were wrong in all three cases (AADC ruling direction, SB 976 "upheld", Meta "47 states"); the verified versions shipped as ledger entries o1–o6 with source quotes. Rule applied: a verified source outranks a critic's prescription. The two gates were not re-run; the record still reads FAIL.
- Two presentation findings on label register ("ED visits", "variance explained") were closed at stage 1, because `label` is stage-1-owned.
- Poster carries the first three stats by array order (all ranked) and the top four camps by weight, per the poster rule.
- View critic declined the per-topic `wide:true` mitigation for the desktop ranked-label register entry; symptom here is a wrap at spaces, not a mid-word shatter.
- No human figures in the primary art, by rule; phone and sapling measured equal (509px each).

## Check in 5 minutes
1. Selection tilt in the compact layer. Both main camps read the same datasets, so what sits above the fold is what tilts. Above "Go deeper" the Basics carry four rise-direction numbers (girls' sadness 53%, suicide 2.9, ER self-harm 318, loneliness 36/37) against one null (Orben 0.4%); the poster's three stats are the first three, so the skeptic camp has no number on the poster at all. Neutrality passed this deliberately (the PISA detail names the contradicting HBSC series). If you want the null on the poster and in the top row, swap stats 3 and 4 — a stage-2 reorder, nothing else moves.
2. The OG card clamps the summary at "…what should follow, is…" — the word it drops is "contested", the operative one. Square and portrait carry the full sentence. A summary a few words shorter would fit; leave it if you are fine with the ellipsis.
3. "The effect is the size of eating potatoes" is the Weak Evidence steelman on the page, cards and poster. It is the camp's own line and the detail grounds it, but it is the one steelman a cold reader may hear as mockery of the camp rather than by it.

## Engineering (the pipeline may not touch CSS)
none — 4 open entries cited from UI_DEFECTS.md (share-card hairline; desktop ranked label wrap, mild; ≤360px ranked gutter, visible at 320; draft banner `--pos-amber` beside an amber camp). Poster word-unit entry does not fire (all three poster stats are ranked). No regressions.

## Publish
manage.py publish_topic --slug social-media-youth-mental-health --dry-run    # preflight + plan
manage.py publish_topic --slug social-media-youth-mental-health --confirm    # publish + reviewed_at
→ it prints the commit and DEPLOY.md §3 live-push commands, filled in.
