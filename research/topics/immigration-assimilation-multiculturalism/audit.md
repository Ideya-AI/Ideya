# Audit: Immigration & Assimilation
2026-10-03 (re-audit), verdict: ready

This re-audit follows the fix to the one issue the first audit raised. The first Basics tile now says the sons' gap "narrowed to 3 points" and the daughters' gap "closed", which matches its bars (5, 3, 0). The page's lead point about the second generation no longer overstates convergence, and the crux's empirical half ("how fast and how fully") now builds on a tile that agrees with itself. The fix touched only that note. Nothing around it shifted: the detail, the multicultural camp's out-earning claim and the crux still read consistently with it. check_topic_text is clean. check_links finds no dead or placeholder links (3 blocked: the Canada act page, which times out, and the Jo Cox Foundation and Copenhagen Post pages, which return 403). The renders postdate topic.json and the glance hash matches (8f344514c418ece0). The dev server at :8641 serves the corrected sentence. The rest of the page still holds as the first audit described it: one story, four distinct camps steelmanned at similar length, a neutral why-now and art, and a crux that follows from the questions.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- Carried from the first audit, unchanged:
  - Canada Multiculturalism Act link: check_links reports it blocked (timeout). The page is live; it hangs only for the checker's scripted User-Agent (Akamai). Adding www.canada.ca to `_BOT_WALLED_HOSTS` in topics/management/commands/check_links.py would stop the false alarm. The Jo Cox Foundation and Copenhagen Post links are 403 `blocked`.
  - Why-now date: the page dates the USCIS "neighborhood investigations" Policy Manual change to August 25, 2026. The previous auditor recalled a similar policy from August 2025. The linked USCIS Policy Manual updates page would settle it.
  - Australians' views stat: "Immigrants add new ideas" shows 78 in the chart, and the detail has a different item falling from 78 to 67. Worth checking against the Scanlon 2025 report.
  - Fundamentalist-views detail: the phrase "first item" is ambiguous against the chart order.
  - Return camp: its detail does use "we" and "our", so the earlier remark about third-person voice applies mainly to its steelman. It ends on Trump's harshest lines, which accurately show how far the broad wing goes.
  - Evidence weight: in the Q2, Q5 and Q6 details, named studies fall mostly on the barriers, early-citizenship and support side.
  - The Dutch retreat from multiculturalism appears three times: the MPI detail, the Q3 why and the multicultural camp's detail.
  - About twelve of the seventeen stat details close on "camp A reads X; camp B reads Y."
  - Several detail figures name a source without a link: IamExpat, EU Law Live, The World/Mandag Morgen, Canadian Press, The Local Denmark.
  - At 390 px, the "Newcomer choices" lean label wraps, and so do the long camp tags on four action cards.
  - Template: the og card sets "&" alone on its own title line.
