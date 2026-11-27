# Audit: Treating Aging as a Disease
2026-11-26, ready.

Re-audit after the fix. All six issues from the earlier packet are fixed, and nothing around them broke. The inequality question's why now gives each answer a foothold: expensive private products on one side, cheap generic candidate drugs on the other, then the survey expectation. The record-lifespan detail ends on the demographers' disagreement and no longer speaks in one camp's voice. ARPA-H is off the proponents. The first Basics tile is a plain big number (10.5 years) with no axis to misread. The fixed-limit detail now gives each side one study and one quote of about the same length. "Per disease" fits on one line in its pill at 390. The page still tells one story, from the burden of aging, through the evidence and the money, to the two arguments the summary names. The four camps split evenly on those two axes, the crux follows from the questions, and the share cards match the page. check_links again flags afar.org/donate and the Longevity.Technology report as dead, but both return 200 to a browser user agent over HTTP/1.1. I read them as bot-walled, not dead. The glance hash matches renders/glance.hash, and every render is newer than topic.json.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- topics/management/commands/check_links.py `_BOT_WALLED_HOSTS` (line 54): afar.org and longevity.technology close the connection on urllib (and on HTTP/2 curl) but serve 200 over HTTP/1.1 with a browser user agent. Until they are listed, or a closed connection is treated like a timeout, this topic will fail the link gate on every run.
