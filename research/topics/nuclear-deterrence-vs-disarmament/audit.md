# Audit: Nuclear Weapons
2026-09-30, verdict: ready (re-audit)

This is a re-audit after one editorial fix cycle, and all three issues from the first audit are fixed. The Hiroshima tile now credits the RERF FAQ to 2026, not 1945. The ICAN spending tile's date now agrees with its June 2026 label. The New START detail now names the source it uses: "Arms Control Today's September 2026 issue reported that at an August Defense Department briefing…". The linked March article no longer has to carry the August briefing. The editor also took both optional wraps. The Hiroshima value now reads "90–166 thousand" and fits on one line at 1440 and 390. Q1's lean label is now "Other causes", on one line at both widths. Nothing around the fixes broke. The page still tells one coherent story: New START's lapse as the why-now, Basics running from stockpiles to famine models to treaties, eight questions, and five evenly argued camps. The crux gathers what sits above it. Mechanical checks are clean: 0 text errors, and 0 dead or placeholder links (3 blocked, 2 redirect). The renders are newer than topic.json, and the glance hash matches. The dev server at :8641 serves the fixed text.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- Template: a unit starting with "$" gets no word space, so the page shows "118.8$ billion" and "946$ billion" (`Stat.unit_is_word`, topics/models.py). views.md logged this. It affects every topic that has a "$ billion" unit.
- New START detail: the last sentence credits Arms Control Today's September 2026 issue by name, but the tile's link goes to the March 2026 article. The sentence is now attributed honestly. A reader who wants that sentence's source has to look it up, as with the NBC, Fortune and Air & Space Forces citations elsewhere.
- Doomsday Clock chart: the bars carry no unit, so "1991 … 1,020" reads as a bare number until the note explains seconds. Longer bars mean safer, the reverse of most bars on the page.
- Doomsday note says "the closest since 1947". The clock began in 1947, so "the closest in its history" is what is meant. As written, a reader could take it that 1947 was closer.
- The crux lead, "prevent catastrophic war or only postpone it?" with "kept indefinitely" highlighted, leans slightly toward the compounding-risk frame of the reduce and ban camps. The subtitle balances it. This is a judgment call.
- NATO is the first proponent of "Strengthen nuclear deterrence", while the "Reduce arsenals" detail counts "most NATO members" among its own. That is defensible (an alliance posture against member governments' arms-control stance), but a reader may notice NATO on both sides.
- "Reduce arsenals step by step" has two tagged actions (Arms Control Association, Back from the Brink); every other camp has one.
- The ICRC's "no adequate humanitarian response" point appears in Q2, the ban camp and the prepare camp, which rebuts it. Each use serves a different end.
- Hibakusha, the 16th stat, sits alone on the last Basics row at 1440. That follows from the count.
