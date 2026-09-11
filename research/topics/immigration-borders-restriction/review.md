# Immigration: Open Borders vs. Restriction — review packet (2026-09-06)

**DRAFT `immigration-borders-restriction`** · 10 stats · 9 questions · 12 positions · 15 actions
Fold above "Go deeper": basics 10/10 · questions 6/9 · positions 6/12

## Look
[page](http://localhost:8641/immigration-borders-restriction/) · [expanded](http://localhost:8641/immigration-borders-restriction/?expanded=1)
[1440](desktop-1440.png) · [390](mobile-390.png) · [320](mobile-320.png) · per-section tiles under `sections/`
[OG](../../../static/img/social/immigration-borders-restriction.png) · [square](immigration-borders-restriction-sq.png) · [portrait](immigration-borders-restriction-pt.png) · [poster](immigration-borders-restriction.pdf)
The first two need the dev server up on 8641.

## Run
substance 5/5 ran, 3/5 pass on file (fact-source, shape, claim-ledger) · presentation 4/4 (compact-self-sufficiency, reading-level-fit, editorial-shape, claim-fidelity)
Neutrality and steelman are stored as FAIL: one blocking finding each, closed after the loop by the critic's own prescription applied verbatim (`prescribed_fixes`, by orchestrator-closure). Both closures are in the shipped text; the steelman closure's two new facts were blind-verified (ledger x-closure-1/2). The array keeps one record per critic, so the pre-closure FAIL is what a cold reader sees — a known record-shape limit, not an open defect.
ledger 59 supported + 7 resolved-by-revision of 66 · 0 contradicted · 0 unverifiable · 66/66 with a verdict · closed on the shipped draft (includes the PM-routed r1) · fidelity 58 verified claims carried in and checked · lint 0 · links 24 checked: 0 dead, 0 placeholder (3 bot-walled hosts left as cited) · poster fits (fit_check/render_poster passed upstream; slack not reported to me)
Rounds: research 1 gate run on file (wf_521248de-554) · distribute 1 + 10 fix_only passes (pass 5 died on a usage limit, closed by the orchestrator; pass 10 scoped re-gate 4/4) · icon and views not reported to me · PM: this read routed 0; the prior read's routes (ledger r1, two register rows) are closed.

## Decided for you
- Crux subtitle had no Family Unity claimant (neutrality's one blocker) → the critic's clause "the spouse or child waiting out a queue on the other side" added verbatim. Rule: a prescription quoting target and replacement is applied once the loop is spent.
- Hathaway was named as backing the Global Compact he called a "cop-out" (steelman's one blocker) → Compact-backing reattributed to UNHCR and the IRC, Hathaway given his own wing; both new facts blind-verified before entry.
- Camp scout's three candidates (Faith-Based Hospitality Reformer, Population/Environmental Restrictionist, Refugee Burden-Sharing) rejected under the four-part bar; twelve camps stand. The critic named the faith-based camp as the one to add if you ever want a thirteenth.
- Poster fit: the GDP-gain note cut to ≤170 chars and both crux axis paragraphs to 252/253 by the orchestrator after fix_only fell short; verified by render_poster, not a critic.
- Two stat labels reworded on locked fields, no fact changed: "…on the average native-born worker" (names the scope) and "International Labour Organization" spelled out · social-trust stat fill_pct 0 → null (empty-meter workaround) · five redirecting source URLs repointed to their final URLs.
- Fold: Basics shows all 10 with no Go deeper — the row-snap rule found no full-row cut that keeps every tier-1 tile (9 tier-1, 1 tier-2, one wide), so it shows everything · Questions 6/9 at the tier drop · Positions 6/12 by prevalence (locked) · Actions: one tier-1 action per camp; the two second actions and Add-your-view sit in the normal layer (base on desktop, behind Go deeper on mobile).

## Check in 5 minutes
1. **Crux subtitle names seven claimants for twelve camps.** "Each camp names a different claimant: …" now omits Skills Selector (weight 40), Cohesion Communitarian (26), Origin-Country, Migrant Labor Rights and Mobility Partnership. Per-camp locatability was the neutrality gate's only blocking finding; its closure (the family clause) survived, but the later cut to the poster band's budget dropped five others. It reads fine cold; if you want the promise honest, soften it ("The camps name different claimants…") or send a ~200-char version through stage 2 `fix_only` that keeps the two heavy camps.
2. **The open-borders pole is last and below the fold** on a page titled for it: Open Borders Universalist is weight 7 of 12, the twelfth card, and absent from all three share cards (top four + "8 more"). Prevalence is locked and its basis is on record ("almost no legislative footprint; standing rests on a well-cited literature"). The rule working — override only if you disagree with the weight.
3. **Question 6 gives one side the last word inside the other's paragraph**: the "gains erode" paragraph closes with the expansionists' no-threshold rebuttal — the only asymmetric question of nine (neutrality note, non-blocking, shipped as is). Drop the rebuttal or give the skeptic a matching reply.

## Engineering (the pipeline may not touch CSS)
None new. Eleven OPEN register entries show on this topic, cited not re-reported: draft banner in `--pos-amber` (all widths; this page also carries the amber category chip and an amber camp) · desktop non-wide ranked tile ("Potential world GDP gain"): 64px label column, four-line labels, stub bars, and its wide row-neighbor stretched to ~340px of blank card in the collapsed grid · ≤360px ranked rows lose their bars and strand the value (mobile-320 Basics, both ranked tiles) · **position palette wraps at 12**: Mobility Partnership Pragmatist = Border Sovereigntist green, Open Borders Universalist = Skills Selector blue, on card rails and on touching Actions rows; the loader warned twice — the design call (extend `--pos-*` past 10 or cap camps) is yours · mobile question/position cards show no expand affordance (deliberate, REOPENED) · vote pills 45×27 under the 44px floor · nav search does not collapse under 640 · "Go deeper" chip ~34px tall · share-card art border in a category color-mix · card 2px capture hairline · poster value/unit spacing ("304million" in the PDF text layer). The fill_pct-0 guard is closed on the content side here (null); code half still open.
No regressions against the FIXED list: web value/unit spacing, 320 lean chips, connects-to chips, the mobile hero cap and the expanded mobile grids all hold. OG summary drops its last word ("…who the border…") by the designed 3-line clamp for long titles (`share.html` ~73); square and portrait carry it whole. Housekeeping: the two rows appended to the register today (nav search, Go deeper chip) carry the routing sentence in their Where/Fix cells — tidy when burning down.

## Publish
manage.py publish_topic --slug immigration-borders-restriction --dry-run    # preflight + plan
manage.py publish_topic --slug immigration-borders-restriction --confirm    # publish + reviewed_at
→ it prints the commit and DEPLOY.md §3 live-push commands, filled in.
