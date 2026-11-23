# Audit: AI & the Future of Work
Date: 2026-11-21. Verdict: ready.

The refresh updates only time-bound facts and leaves the debate itself as it was: the four camps, seven questions, crux and lean labels are word for word the live page's. The why-now, the job-cuts tile, the unemployment tile, the Gallup worker-use tile and the Census firm-use tile now run through October and November 2026. Two actions were brought up to date (the Kelly bill is named, the Per Scholas link is fixed), and the AFL-CIO quote is now quoted in full. I compared every changed field with the live page by id and found no regression against the live page. Nothing was cut except what events overtook: AI is no longer the leading stated reason for layoffs, and the Yale tracker quote is replaced by its October finding, which makes the same point. The glance figures and the facts moved into details still follow their sources. The new figures agree with each other and with the rest of the page: 120,136 plus October's 1,265 makes the 121,401 shown, and 25 percent of firms against 53 percent of workers keeps the "firm adoption lags" point. The Census detail notes that the survey question was reworded to "Super Intelligence," and adds that the estimate did not jump across the change, so a reader does not take the rise from 17.7 to 25 percent as a wording artifact. check_topic_text reports 0 errors and the 2 known lean-length warnings. check_links reports 0 dead and 0 placeholder links. I did not open the live page in a browser because the Chrome extension was not connected; I read the page from the renders, which are current (the glance hash matches), at 390 and 1440, collapsed and expanded, along with the three share cards. Views logged two wraps at 390. "Leave them to markets" breaks cleanly onto two lines inside its chip, and the position 1 name breaks onto two lines on the action cards. Both are legible and complete, neither changes meaning, and renaming either would change what existing leans and votes mean. Neither is an issue.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- Template/CSS: at both widths the crux lead shows a visible gap before the comma inside the highlighted span ("people use , or"), though the text has no space. The likely cause is the heavy 800-weight lead font at `.clead` (static/css/ideya.css:392), rendered from templates/topics/detail.html:277 through the `lead_hl` filter. It would affect any crux lead whose highlight contains a comma. The share cards do not show it.
