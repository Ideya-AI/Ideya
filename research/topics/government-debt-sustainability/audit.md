# Audit: Government Debt
2026-10-02 (re-audit), verdict: ready

Re-audit after one editorial fix. The single issue raised, the 175-percent-by-2056 projection on the first Basics tile credited only to CBO's 10-year outlook, is fixed: the glance note now says the figure comes from CBO's 30-year outlook, and the detail names the publication, CBO's The Long-Term Budget Outlook Data: 2026 to 2056 (February 2026). Nothing around the fix broke. The tile still reads cleanly at 390 and 1440, and the projections for 2036 and 2056 still agree with the interest, deficit and gross-debt figures elsewhere on the page. The rest of the page reads as it did before: one coherent account from the US trajectory through Japan, the gilt episode and the "no danger line" evidence, to four camps named by what they want and treated evenly, and a crux (sudden danger or slow cost) that follows from the questions. Both mechanical checks are clean: 0 errors, and no dead or placeholder links (7 blocked, 1 redirect). Renders are current: the glance hash (cdc438d3aa2b57f2) matches renders/glance.hash, and every render is newer than topic.json. The share cards show the four camps and the crux correctly.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- us-federal-debt-held-by-the: the 2056 figure's publication is named in the detail text, but the tile's source line and link still point only to the 10-year outlook (cbo.gov/publication/61882). A reader who wants to check the 2056 number has to look up the long-term outlook by name. Linking that publication as well would need a second source field, which the schema does not provide.
- Question 1 lean labels: "Crisis is possible" and "Crisis is unlikely" are not opposites. The question asks whether a crisis can happen; the second label answers how likely it is. A reader who thinks a crisis is possible but unlikely fits both. "Crisis is a real risk" against "Crisis is unlikely" would make them a pair.
- Question 5 detail, first paragraph: "benefits for future retirees are scheduled to grow faster than wages." Social Security's initial benefits are wage-indexed, so the usual form of this argument is "faster than inflation". Medicare per-person costs do outgrow wages. The SSA Trustees report or CBO's long-term outlook would settle the wording.
- The same point appears four times: euro members borrow in a currency they do not issue (general-government gross debt detail, crisis-thresholds detail, question 1 why, position 4 detail). The 5 percent 10-year yield appears five times (why-now, interest detail, yield tile, average-rate detail, position 1). Paul Krugman's August 2026 writing is cited in the yield detail, question 1 and position 3, each time for a different claim.
- Question 8 says a French candidate proposed to "freeze" the French debt held by the ECB. Position 4 says "the European proposal to cancel debt held by the European Central Bank", as if the reader already knows it. The two verbs differ, and a reader who has not opened question 8 behind Go deeper meets the proposal cold.
- The tile for public debt when crises struck shows "90 % of GDP" as its headline number (Ireland highlighted). At a glance, a reader may take 90 percent as a danger line, the same 90 percent threshold the Reinhart–Rogoff tile later corrects. The note explains, but highlighting the series without a single headline value, or choosing another highlight, would read more cleanly.
- Bar viz on rates that are not shares of a whole: 2.2 percent growth, 3.8 percent of GDP and 9.1 percent inflation each draw a nearly empty bar against a 0–100 scale. This is the template's choice, not a misreading, but the bar says nothing.
- Action "Tell your member of Congress": the description promises to "find your representative and senators", but house.gov's lookup finds only the House member.
- Actions: camp 1 has two camp-tagged actions (Debt Fixer and the Pay.gov gift); each other camp has one. The gift is tenth, behind Go deeper.
- The Pew source label gives the title as "Americans See Health Care Costs, Inflation as Big Problems Facing the Nation". The URL slug includes "deficit", so the label may have dropped a word from the real title. Worth a glance.
- The Moody's detail says the US had been rated Aaa "since 1919". My memory of the May 2025 coverage is 1917. The Moody's rating page cited would settle it; no conclusion changes.
- Template: the Basics grid pairs each wide tile with the next narrow one. At 1440 expanded, the Reinhart–Rogoff, CPI, OBR and Moody's tiles therefore sit beside stats 7 to 10, ahead of their file order. Views also logged lean labels wrapping at 390 ("Mainly cut spending", "Leave markets alone") and long camp tags wrapping on action cards at 390. All cosmetic.
- The live dev page answers at localhost:8641 and its glance text matches the renders.
