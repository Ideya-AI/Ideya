# Audit: Democratic Backsliding
Date: 2026-09-29 (re-audit after an editorial fix). Verdict: ready.

This is a re-audit. Both issues from the first audit are fixed, and the fixes read cleanly in context. The US tile's detail now names the source of the 0.79 and 0.75 values: V-Dem data charted by the Pew Research Center, with the article's title and date. The same Pew article is linked from the Actions section, so a reader can follow it. The detail's "24 percent in one year" agrees with 0.75 to 0.57. The OSF tile no longer reads Hungary's election in the page's own voice. The inference about young Tisza voters is now attributed to "those who read Hungary’s 2026 election as a democratic recovery," which matches how the Hungary tile presents the result as having two readings. Neither fix touched glance text: the glance hash matches renders/glance.hash, and the live dev page serves both new sentences. The mechanical checks pass (0 errors; 26 links ok, 2 archive redirects). On a full reread the page still tells one story. The five camps are distinct and evenly argued, the crux follows from questions 3, 4 and 7, and nothing new meets the bar for an issue.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- United States tile: the glance note and chart show 0.75 to 0.57, but the tile's source link is the V-Dem report, which prints only 0.57 and the 24 percent fall. The earlier values are credited to Pew in the detail, not in the source field. That meets the sourcing rule, but a reader who opens only the V-Dem PDF will not find 0.75 there.
- Actions at 1440: the lean tag "Reserve the backsliding label for real regime change" wraps to two lines on the "Read the case that the decline is overstated" card, and its color dot sits apart from the wrapped text. A shorter camp name would fix it. On mobile, several lean tags wrap the same way, which looks like template behavior.
- Question 7's why says that leaders in Venezuela, Turkey, Russia and Nicaragua "moved beyond electoral reach." Turkey is the arguable member of that list, and V-Dem's or Freedom House's current Turkey classification would settle it.
- Question 2's why ("answers split almost perfectly along party lines") is an unsourced characterization in the page's own voice.
- Lean labels: "Populists renew it" (question 1) is stronger than the plain "no" answer, so a reader who holds the middle view has no label to pick. "It is hardball" (question 2) uses "hardball" with no explanation.
- The crux lead's "take over" leans slightly toward the first camp's vocabulary; the subtitle balances it.
- V-Dem, Freedom House and International IDEA are listed as proponents of "Defend the checks on elected power," and they also supply most of Basics. Worth a look at whether the monitors should be named as proponents.
- Repetition: Hungary's 2026 election appears in about seven items, Venezuela in five, and Kyle & Mounk and Funke et al. each feed two stats. Each use serves a different camp.
- Kyle & Mounk figures: 46 populist leaders or parties over 1990–2018 (backsliding tile) against 47 times a populist took office over 1990–2014 (exits tile). The unit differs, but a careful reader may pause at this.
- The International IDEA tile (viz "bar", "22 of 28") draws no bar at either width. This looks like template behavior for non-percent units.
- The share cards show four of the five camps (the measurement skeptics are dropped), because the card design caps at four.
- check_topic_text warns on "Insoumise". It is part of the proper noun La France Insoumise, not a spelling error.
