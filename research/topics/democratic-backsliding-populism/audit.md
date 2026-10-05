Targeted re-audit of: actions order (swap of actions[4] and actions[5]); positions order (earlier fix); share cards

# Audit: Democratic Backsliding
Date: 2026-10-05. Verdict: not ready.

The actions fix landed. "Read the case that the decline is overstated" (skeptic camp) is now fifth and "Volunteer with Our Revolution" (oligarchy camp) is sixth. The camp-linked actions in the first six now follow the Positions order: defend checks, return power to voters, answer grievances, reserve the label, mobilize against oligarchy. Ids and text are unchanged. The earlier positions swap still holds. check_topic_text: 0 errors. The 3 warnings are the proper noun "Insoumise" twice and a November 2026 date that is still 56 days away. check_links: 28 links, 26 ok, 2 blocked, 0 dead, 0 placeholder. The text is now consistent. One problem is left. The shipped share cards (static/img/social/democratic-backsliding-populism.png, -sq.png, -pt.png, all dated 2026-10-05 02:03, before the 13:50 topic.json edit) still list "Mobilize the many against economic oligarchy" as the fourth camp and leave out "Reserve the backsliding label for real regime change". Someone who sees the card ranks the camps differently from the page, and that ranking is the reason for the positions fix. The card regeneration and the poster/og fit checks (postfix.sh) were blocked by the auto-mode classifier and have not run.

## Issues for editorial
- share cards (static/img/social/democratic-backsliding-populism.png, -sq.png, -pt.png): the cards still show the old fourth camp (oligarchy) where the page now ranks "Reserve the backsliding label for real regime change" fourth. A reader of the card is told a different camp ranking from the page's. Fix: regenerate the three cards and the poster from the current topic.json (postfix.sh democratic-backsliding-populism), check the poster fit and the og summary, then re-audit the cards only. No text change is needed.

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- postfix.sh (card regeneration plus the poster and og fit checks) is blocked by the auto-mode classifier as "Code from External". The run cannot clear the card issue above without it. Run it yourself from the repo root, or add a Bash permission rule for it, then rerun the audit.


2026-10-05: cards and poster regenerated from the current topic.json (postfix.sh: 0 errors, poster fits, og not clamped); the landscape card now lists "Reserve the backsliding label for real regime change" fourth, matching the page. Marked ready per this audit.
