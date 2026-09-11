# Causes & Cures of Economic Inequality — review packet (2026-09-02)

**DRAFT `economic-inequality`** · 13 stats · 9 questions · 8 positions · 9 actions
Fold above "Go deeper": basics 9/13 · questions 6/9 · positions 6/8

## Look
[page](http://localhost:8641/economic-inequality/) · [expanded](http://localhost:8641/economic-inequality/?expanded=1)
[1440](desktop-1440.png) · [390](mobile-390.png) · [320](mobile-320.png)
[OG](economic-inequality.png) · [square](economic-inequality-sq.png) · [portrait](economic-inequality-pt.png) · [poster](economic-inequality.pdf)
The first two need the dev server up on 8641.

## Run
substance 2/5 on file (shape + ledger PASS; neutrality, steelman, fact-source each FAIL with the fix loop spent — their 9 blocking findings were closed by orchestrator prescription, and 3 of the critics' own replacement facts were refused because they did not verify) · presentation 3/4 (compact-self-sufficiency FAIL, closed; claim-fidelity PASS at the main gate, then a fix_only FAIL that was disproved — text byte-identical to the passing version, ledger d21b)
ledger 73/73 closed on the shipped draft (55 supported · 18 resolved-by-revision · 0 open) · fidelity 55 carried claims checked · lint 0 · links 0 dead / 0 placeholder (5 bot-walled, each verified live by another route) · poster fits (31px)
Rounds: research 3 attempts (2 killed by session limits) · distribute 2 (main + fix_only) · icon 3 refines / 14 candidates · views 1 · PM 1 (0 routed)

## Decided for you
- Kept the WID pre-tax top-1% series as the lead Basics tile; the neutrality critic's "contested series presented as shared fact" was closed by naming the Auten–Splinter dispute in the tile's expanded detail, not by demoting the stat.
- Re-anchored the CBO income-growth stat from the 1979–2021 release to the superseding Jan-2026 1979–2022 series (endpoint caveat now in its detail); its label was then narrowed to "lowest fifth" after the closure had briefly widened it to "US households".
- Removed Autor, Dorn and Hanson from the Trade Shock camp's proponents (they are its evidence; Autor rejects its prescription) — they remain in the position's text as the source of the China-shock finding.
- Replaced the misattributed France Stratégie €3bn / 0.4% sentence with the committee's actual departures-vs-returns finding.
- Kearney's endogeneity rebuttal in Family Structure was inverted and re-stated with the fracking-boom natural experiment; the Abundance banner's Houston/Tokyo claim was softened to "kept building, and kept costs down".
- Above the fold, the two institutional stats (union rate, CBO after-tax growth) were moved up so no single camp's evidence owns the fold; China-shock jobs, top statutory rate, middle-class share and CEO ratio sit below.
- Hero art: the three-figures-on-a-staircase concept was abandoned after the generator kept drawing the lowest figure smaller; shipped as three measured-equal discs on the steps.

## Check in 5 minutes
1. Capital Tax Egalitarian, third paragraph: the rewritten France Stratégie sentence runs "…averaging 260 departures a year against 380 returns … against 950 departures a year against 370 returns …" — grammatical, verified, and hard to read aloud. If you want it tightened, that is a stage-2 fix_only edit.
2. The hero art's discs are equal, but they still sit on ascending steps with a lectern beside them; the engine measured size, not composition. Decide whether a staircase reads as neutral on this topic before it becomes the OG card everyone sees.
3. Basics leans nine-of-thirteen toward the widening story by count; the critics cleared it because the counters sit inside the details. Worth one glance at the compact layer to see if you agree.

## Engineering (the pipeline may not touch CSS)
none new — 3 open entries cited from UI_DEFECTS.md (≤360px ranked two-column override; desktop `.rrow` label geometry, mild here; draft banner on `--pos-amber`, registered this run). No regressions against the Fixed table.

## Publish
manage.py publish_topic --slug economic-inequality --dry-run    # preflight + plan
manage.py publish_topic --slug economic-inequality --confirm    # publish + reviewed_at
→ it prints the commit and DEPLOY.md §3 live-push commands, filled in.
