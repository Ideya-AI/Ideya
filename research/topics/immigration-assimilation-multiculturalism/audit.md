Targeted re-audit of: questions[do-integration-gaps-come-mainly-from].detail

# Audit: Immigration & Assimilation
2026-10-05 (targeted re-audit), verdict: not ready (blocked on the link check, not on the page)

The fix landed and holds. The newcomer-choices side now names Koopmans 2016 in the Journal of Ethnic and Migration Studies (Eurislam survey of Turkish, Moroccan, Pakistani and former Yugoslav Muslims). The host-barriers side names Adida, Laitin and Valfort. Each side has one named study and runs about the same length, so the two read evenly. The new sentence says the employment gaps "shrank sharply, often below statistical significance" once language skills, ties to natives and gender-role views were taken into account. That stays within the abstract's "strongly reduced and in many cases become statistically insignificant", and the sentence names no countries. check_topic_text: 0 errors, 0 warnings. check_links reports 1 dead, which stops the run under the usual rule. The dead link is the action "Read the AfD’s own definition of “remigration”" (https://www.afd.de/afd-positionspapier-zur-remigration-raeumt-mit-deportationsluege-auf/), and it returns HTTP 503. The cause is a site-wide outage: the afd.de homepage returns the same 503 with the body "Wartungen sind gerade in Gange" (maintenance in progress). The URL is not broken, and this fix pass did not touch it. Re-run check_links once afd.de is back. If the link comes back ok, the page is ready as it stands.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- afd.de is down for maintenance (HTTP 503 site-wide as of 2026-10-05). Re-run `check_links --topic immigration-assimilation-multiculturalism` later; if it comes back clean, run `mark_ready`.


2026-10-05: afd.de back up; check_links re-run clean (28 links, 0 dead). Marked ready per this audit's next step.
