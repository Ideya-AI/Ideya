# Audit: Content Moderation
2026-09-28, re-audit after one editorial fix, verdict: ready.

The page still tells one coherent story. The why-now is the House bill to sunset Section 230, and the first question takes it up. Basics opens on the fact that 99.8 percent of EU moderation decisions cite a platform's own rules rather than the law. The eight questions lead to a crux that follows from them: does policing lawful speech prevent more harm than it silences, and who should hold that power. The five camps are named by what they want and argued with even energy.

The one issue from the first audit is fixed. The Community Notes chart and its note now carry only the X figures from the Digital Democracy Institute of the Americas, which is the source they link. The Meta 6 percent figure appears only in the detail, where the Oversight Board is named as its source. The fix broke nothing around it: the series still runs largest first, the highlighted bar (X English, 2021 to 2025, 7.1) matches the note, and the tile sits cleanly in the Go deeper grid on the live page at 1440.

Mechanical checks:
- check_topic_text: 0 errors, 1 warning. The warning flags "humor", which is a false positive.
- check_links: 27 links, 23 ok, 3 redirect and 1 blocked (CCDH answers 403). None dead, none placeholder.

The renders are current. The glance hash f8932daae0d00b98 matches renders/glance.hash, and every render and share card postdates topic.json. The live page at :8641 serves the fixed text.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- Carried from the first audit, unchanged and still notes:
  - Research-process voice appears in the X staff detail ("could not be loaded") and in the harassment-lawsuit detail ("found", "turned up in research").
  - The Meta tile's May 2025 figures are not on the linked January 2025 post.
  - The EU 6 percent fine is named but not linked.
  - Several source_published years give the data year rather than the publication year: Meta, AP/X and Kaushal.
  - Meta's 2025 rollback recurs across six items, each from a different angle.
  - Two Pew 2020 tiles repeat the same sample line.
  - The summary and the crux subtitle share the phrase "companies, governments, courts or users".
  - Two page-voice judgment calls: "best public data" in the Meta tile and "thin loss" in the crux values.
  - The Community Notes action is tagged to the viewpoints camp, so that camp has two actions.
  - The Bluesky action renders a "Local" label.
  - The harassment-lawsuit chart mixes two questions in one bar set.
  - The OG card truncates the summary before "users", and the share cards show four camps by design.
  - Template: radial units wrap at 1440, action camp tags wrap at 390, ranked tracks are short at 390, and ranked bars scale to the series maximum.
  - Links: counterhate is blocked; the Internet Association, Bluesky and EFF links redirect.
- New and minor: the Community Notes detail ends "Supporters answer that notes are meant to be few and trusted." It now follows the Meta sentence, so the objection it answers (most notes never appear) sits three sentences back. It is not misleading.
