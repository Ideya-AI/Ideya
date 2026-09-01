# nuclear-energy — editor findings for the next refresh run

Feed these to `refresh_topic.js` as `args.findings` (they land in every flagged
section's work order and become citable `because` ids). Found 2026-09-01 while
repairing dead source links; NOT acted on, because changing a published figure
and its note is a content change that belongs in a gated run with a human diff,
not a hand-edit.

## 1 · "Operating reactors worldwide" — country count is wrong

Stat says: "About 417 power reactors run across **30 countries**".
IAEA Reference Data Series No. 2, 45th edition (data as of 31 Dec 2024) says:
"377 GW(e), provided by **417 reactors across 31 Member States**."

The reactor count matches exactly; the country count is off by one. Also worth
re-checking whether 417 still holds — the World Nuclear Industry Status Report
has since run "Number of Operating Reactors Drops — Taiwan Completes Nuclear
Phaseout", so the 2026 figure may be lower than the end-2024 one.

Source: https://www-pub.iaea.org/MTCD/publications/PDF/RDS-2-45_web.pdf

## 2 · "Reactors under construction" — figure looks ~3 high

Stat says: "About **77** reactors are under construction today … China alone
accounts for nearly half" (the 2026-07-08 refresh recorded "37 of 77, ~48%").

Current reporting puts it at **74** in 13 countries, China 37 — which makes
China's share exactly half, not "nearly" half. IAEA RDS-2-45 gives 62 as of
31 Dec 2024, a different vintage rather than a contradiction.

Both the value and the note's China clause need re-checking together.

## Note on the sources

Both stats cited `pris.iaea.org/pris/worldstatistics/…aspx` deep links. The IAEA
retired that entire statistics site; every path now 302s to the JS dashboard at
`https://pris-stats.iaea.org/`, which has no stable deep links and cannot be
fetch-verified. The URLs were repaired to that dashboard on 2026-09-01 — same
source, current home — deliberately NOT to RDS-2-45, because that PDF's numbers
(62 under construction) contradict the stats as written, and swapping in a
source that does not support its claim is worse than a redirect.

If the refresh moves these figures, RDS-2-45 is the better citation: stable,
dated, fetchable, and durable-by-default. It just has to be adopted together
with its numbers, not instead of the live count.
