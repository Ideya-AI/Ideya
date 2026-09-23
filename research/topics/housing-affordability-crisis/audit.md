# Audit: Housing Affordability
2026-09-23 (re-audit after fix), verdict: ready.

The page tells one clear story. It opens on price against income and cost burden, lays out the disputed shortage and the money-side evidence (rates, the Bank of England paper), moves through eight questions that each give both cases at even length, and presents six camps, each named by what it wants and written at close to the same weight. The crux ("is building enough on its own?") follows from the questions and from the fact that nearly every camp concedes some supply. The why-now event is on topic. It now says why the law went unsigned (a protest over an elections bill), which also settles the earlier puzzle about the investor limit and camp 2. The Basics tiles note which way their sources lean (Demographia, NAHB). San Francisco, Vienna and Minneapolis each carry both readings. The one issue from the first audit is fixed. Each bar of the large-investor ownership chart now names its source and year ("350+, John Burns 2026", "1,000+, Urban/GAO 2022", "100+, Census 2024"), and the detail explains why the three national bars do not nest. The fix reads cleanly at 390 and 1440, collapsed and expanded, and on the live dev page. check_topic_text is clean, all 29 links resolve, and the glance hash matches the renders.

## Issues for editorial
none

## Issues for icons
none

## Needs research (stops the run)
none

## Notes for the human
- Camp 3 steelman (glance, every viewport): it opens with a quoted phrase inside the template's quote marks, so it renders as a doubled opening quote ("“Pitting “just build”…"). Single inner quotes, or a reworded opening, would remove it.
- The Harvard Joint Center is quoted in camp 3 ("market forces alone are unlikely to meet the need for deeply affordable homes") and in camp 5 ("private markets are incapable of producing enough deeply affordable units"). Both are presented as what the Center "concludes", in different words, so a reader meets the same point twice from the same source. Check that both are verbatim. If only one is, keep it in one camp.
- Camp 6 is the only camp whose detail fact-checks its own proponent (PolitiFact on Vance's 30 million). No other camp's quoted proponent gets the same treatment. Judgment call: keep it, or lead with the Canadian case and drop the contested figure.
- Camp 1's quote "would jeopardize the financial viability…" is attributed only to "our coalition". Every other camp quote names its speaker.
- Mamdani is placed in "Build more homes and protect tenants" rather than "Build social housing and cap rents". That is defensible given the rezoning plank, but worth a second look.
- The credit-and-rates view (Q1's "too much money" side, the Bank of England stat, the crux's "cheap credit") has no position of its own. It is folded into camp 2 through Ryan-Collins. This is adequate as written.
- Two figures for the same thing: the US price-to-income multiple is 4.7 in the lead stat (JCHS) and 4.5 in the Demographia detail. Atlanta is "about a quarter" (25 on the chart), while the same tile's GAO six-metro range tops out at 22 percent. Both gaps come from different sources and change no conclusion.
- share-of-us-single-family-home (investor purchases): the ranked chart is not in rank order (20+, 19, 30), so Cotality's broader count, the longest bar, sits last.
- Actions: camp 1 has two (YIMBY Action, National Zoning Atlas) and each other camp has one. Camps 2 and 6 get reading material rather than something to do.
- Share cards list the first four camps only, so social housing and population growth are absent from every card. This is presumably the template's fixed count.
- Template or CSS: in the expanded 1440 Basics, the last row holds two narrow tiles (Vienna, homelessness) and leaves the right third of the row empty. At 390 the ranked-chart bars are very short (about 40px), so small differences, such as 350+ at 5 against 1,000+ at 3, are hard to see.
