# Audit: Labor Power
2026-10-02 (re-audit), verdict: ready

The single issue from the first audit is fixed. The labor-share tile is now titled “Workers’ share of US gross domestic income”, which matches its note, detail and FRED/BEA series. The fix shows in the 1440 expanded render and on the dev server page. Values and source are unchanged, and nothing around the tile was disturbed. The editor also acted on one note: position 1 now says unions’ “near-record popularity”, so it no longer contradicts the Gallup tile. On a full reread the page still tells one story. Pay against productivity, unions, the minimum wage and app work each get stats, a question and a camp. The crux follows from them, and the why-now (California certifying a statewide Uber and Lyft drivers’ union on September 9, 2026) belongs to the topic. The four camps are even in length and energy, each named for what it wants. Mechanical checks pass: 0 text errors, 0 dead or placeholder links. Renders postdate topic.json and the glance hash matches. The three share cards show the four camps and the crux cleanly.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- The stat’s internal id is still `workers-share-of-us-national-income`. Readers never see it, but anything keyed on it (anchors, participation rows) keeps the old wording.
- Labor-share detail: the BLS nonfarm labor share index (93.4 in Q2 2026, lowest since 1947) is credited to BLS by name, but the only link is the FRED/BEA series, so a reader cannot click through to that figure.
- The federal minimum’s real values ($15.67, $11.28) are computed from CPI-U, as the detail explains. The linked DOL chart carries only the nominal rates. The method is stated and reproducible, but the link alone does not show the numbers.
- Repetition: the 2021 to 2023 surge in low-wage pay comes up in Q1 detail, in Q7’s why and detail, and in positions 2 and 3. The Faster Labor Contracts Act appears in the first-contract stat, position 3 and an action. Q2 detail and position 2 detail share a near-verbatim line (“fewer hours, slower hiring … firms that never open rather than as layoffs”). None of this misleads.
- Judgment call: the glance Basics pairs the EPI productivity–pay gap with Neumark and Shirley’s 79.2 percent radial, a large single number from one camp’s tally. The rival Cengiz result is only in the note. The CBO chart highlights “Jobs lost, average” rather than the raises. Both choices are defensible.
- Judgment call: position 4 (middle status for app workers) covers one strand of the topic, while the other three are economy-wide. On the share cards it sits beside them as if equal in reach.
- Q3 lean labels pair a policy (“Easier organizing”) with a value (“Individual choice”), and the second sounds more appealing on its face. A symmetric pair would be cleaner.
- At 390, lean labels wrap to two lines on Q1 (“Power held pay down”), Q4 (“Keep as contractors”) and Q8 (“Independent unions”), and long camp tags wrap on action cards. This is cosmetic, and shorter text would fix it.
- Links: 11 BLS, DOL, CBO, EPI and FRED links return 403 or time out to the checker (bot blocking, not dead). Worth one manual click before publishing.
