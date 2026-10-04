# Audit: Deepfakes & Shared Truth
2026-10-02 (re-audit), verdict: ready.

Both issues from the first audit are fixed, and the fixes broke nothing around them. The page still tells one story. The overview asks whether AI fakes are wearing down shared facts or riding distrust that was already there. Basics gives the evidence for each reading. The seven questions are distinct and neutrally worded. The four camps are each named by what they want and argued with comparable force. The crux restates the overview's axis, and its empirical and values halves draw on the questions above it. The EU AI Act why-now belongs to this topic. The glance hash matches renders/glance.hash (53c8e65069f8b521), and the renders (03:20) are newer than topic.json (03:17). The dev server at :8641 serves the fixed text. The share cards show the four camps and the full crux. Nothing on the page would mislead or confuse a reader.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- Previous issue 1, fixed. The Schiff liar's-dividend tile is now a single range: "32–34 % opposed" on a scale from 0 to "44 no response". The note says the false claim cut opposition from about 44 to 32–34 percent "across two framings". The end label "44 no response" could briefly read as "44 percent did not respond" rather than "the condition where the politician made no response". The note settles it on the same tile, so this is cosmetic. "44, no reply" or "44 baseline" would be clearer.
- Previous issue 2, fixed. The Q5 detail now reads "…TikTok and major news organizations, and that about 190 companies…", one clean sentence. The two halves are now roughly balanced.
- Previous note, resolved. The Hany Farid caution sentence is gone from the Nightingale & Farid tile. FIRE's quote in position 2 now names its 2026 explainer.
- check_links still reports the Washington Post provenance-test link as dead (timeout). curl also fails at the protocol level, which is consistent with the first audit's finding: the article loads in a real browser and this is bot protection. Public Citizen ×2 and CCDH are blocked (403). Content Credentials Verify and both DOIs redirect. None needs action.
- check_topic_text warns that the "Trust in news and in AI chatbot answers" detail is short (284 characters against a 350 target). It reads complete.
- Carried from the first audit and still open: the Q7 detail says the EPRS reported in January 2026 that Denmark's likeness amendments were "scheduled to take effect that July". It is now October, so a reader can't tell whether they did. The August 2, 2026 Article 50 date in the why-now is stated flatly. Both are worth a check against a current Commission or Danish Ministry of Culture source before publishing.
- Position 1 says "the digital forensics expert Hany Farid argues that platform immunity does not cover output a company's own model creates" with no source a reader can follow. It is a camp's reasoning attributed to a named proponent, not a figure, but it is an "X argues" in prose. Worth a parenthetical source, like the ones the stat details use.
- Unchanged from the first audit, all cosmetic: "1 platforms" is a plural unit on a value of 1. Ring-stat units ("% concerned", "% deceptive", "% of AI ads", "% of adults", "% correct") drop below the value in the narrow 1440 tiles. "HK dollars" drops to its own line at 1440 expanded. Source years show data year rather than publication year for MrDeepFakes (2023) and Schiff (2021). The Diel near-chance finding recurs in stat 1, the Pew detail and Q1. "Trust fell before AI" closes both trust details and is camp 4's core.
- Template: the ring-unit wrap in one-third desktop tiles recurs across topics (views.md). Ranked bars scale to the series maximum, so near-chance accuracy bars look long. The expanded Basics grid leaves the last tile alone on its row.
