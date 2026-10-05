Targeted re-audit of: basics.stats[2] (CBO single-payer range: value, unit, viz), basics.stats[1].note (uninsured for all of 2025)

# Audit: Universal Healthcare
2026-10-05, verdict: ready

Both fixes landed. Mechanical checks: check_topic_text found 0 errors. Its 10 warnings are 9 older lean-label length warnings and the deliberate "trillion dollars" unit. check_links found 0 placeholders. Its one "dead" result was govtrack.us resetting the connection; the same URL returned 200 on a direct retry, so the host was briefly down and the link is fine. The CBO tile now reads "−0.7 to +0.3 trillion dollars" on the live page and on the poster. The tile shows the true minus sign and an explicit plus, so a reader can no longer take the range as a cut on both ends. With no graphic, the number and the note carry the tile. The value, the note ("a $0.7 trillion cut to a $0.3 trillion rise … in 2030"), the label and the CBO source fields agree, and the value claims nothing the note does not. The uninsured note now reads "uninsured for all of 2025". That matches the tile label, the detail (CPS counts the uninsured only if they lacked coverage for the whole year) and the why-now ("went without health insurance for all of 2025"). The editor flagged the why-now as still reading "at any point", but that phrasing is in research.md only, not on the page. Layout, checked by hand because the post-fix script was blocked: the live poster fits with 57px to spare, and the og card summary is not clamped (4 lines, title 2 lines). The og, square and portrait share cards carry no stats, so the fix does not affect them. The stale poster PDF was re-rendered (fits, 57px slack).

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- Code defect, reported by the editor and consistent with what renders: `Stat.range_band` in `topics/models.py` and the span check in `derive_viz` in `topics/management/commands/load_topic_draft.py` reject "to", a leading "+" and the U+2212 minus. A range that crosses zero therefore cannot keep its band and show its signs, which is why this tile dropped to a text-only `bar`.
