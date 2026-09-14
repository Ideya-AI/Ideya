# Standing UI-defect register

Site-wide code and CSS defects found while reviewing rendered topics. Per-topic
content findings never go here. The pipeline never fixes these (it may not touch
templates or CSS); the human burns the list down.

How it is used: a reviewer that finds a defect matching an Open row cites the row
instead of re-reporting it. A match on a Fixed row is a regression and is reported
loudly. A genuinely new site-wide defect goes in the topic's review packet and is
appended here.

## Open

| Defect | Where | First seen | Prescribed fix |
|---|---|---|---|
| Card exports carry a 2px background hairline (capture-clip artifact) | share-card capture path | ai-takeoff, 2026-08 | cosmetic; revisit with a card design pass |
| Poster drops the space between a value and a word unit ("&gt;80billion"): the unit is a bare `<small>` with no `u-word` class and Chrome's print path eats the leading space | `templates/topics/poster.html` ~145, ~55 | moral-status-of-animals, 2026-08-28 | mirror the web tile: `u-word` class on space-led units plus `.tv small.u-word { margin-left: .18em }` in poster styles; re-render posters |
| Ranked tiles at desktop shatter single-word labels mid-word ("Instagra/m"): `.rrow`'s `minmax(64px, 28%)` label column hits its 64px floor in a 274px 3-col tile; the ≤640px rule raises the floor, desktop never got it | `static/css/ideya.css` ~295 | encryption-vs-lawful-access, 2026-08-28 | `.rrow { grid-template-columns: minmax(88px, 28%) minmax(36px, 1fr) minmax(52px, 10ch); }`; meanwhile `wide: true` on the stat |
| Ranked rows at ≤360px get a dead right gutter: the 360px two-column `.rrow` rule is overridden by the later 640px three-column rule at equal specificity | `static/css/ideya.css` ~479 vs ~855 | vaccine-mandates, 2026-08-28 | move the 360px rule after the 640px block so it wins |
| Share-card art tile border is category-colored (`color-mix(... var(--cat) 22%)`) where hairlines are 1px `ink-100` everywhere else; the poster does it right | `templates/topics/share.html` ~38 | immigration-borders-restriction, 2026-09-05 | `1px solid var(--ink-100)` |
| Position palette exhausted at 12 camps: the loader wraps modulo (`ck = POS_KEYS[i % len(POS_KEYS)]`), so camps 11 and 12 reuse camps 1 and 2's hues on the card rail, head dot and Actions dots. The 2026-08-27 fix (10 hues plus a loud warning) held on the warning half only | `load_topic_draft.py` ~424; `topics/models.py` ~23-34; `tokens.css` ~79-92 | immigration-borders-restriction, 2026-09-05, 12 camps | design call: extend `--pos-*` past 10, or a camp cap the engine enforces |
| Mobile position and question cards have no expand affordance: `.xtoggle` is hidden at ≤640px to avoid the vote pill, body tap drives expand, but nothing hints at it and `_position.html` still documents the caret as visible on all viewports. Reopens a Fixed row | `static/css/ideya.css` ~857, ~871 | immigration-borders-restriction, 2026-09-05 | human decides: restore an affordance (hint glyph beside the pill, or caret below it) or move to By design |
| Vote controls under the 44px touch floor at ≤640px: `.qvote` / `.pvote` / `.pimp` pills measure 45×27 and `.vbtn` 15×15 | `static/css/ideya.css` ~866, ~875 | immigration-borders-restriction, 2026-09-05, measured via CDP | give `.vbtn` a 44px hit area via padding or a pseudo-element without growing the pill |
| "Go deeper" ghost chip is ~34px tall on mobile, under the 44px touch floor. Separate CSS location from the vote-pill row | ghost chip rule, `static/css/ideya.css` | immigration-borders-restriction, 2026-09-06 | 44px min hit area via padding or a pseudo-element |
| Nav search does not collapse to an icon under 640px: the full field renders at 390 and 320 (only the `/` hint drops). `docs/DESIGN.md` Responsive > Nav | nav block, `templates/base.html` | immigration-borders-restriction, 2026-09-06 | collapse to an icon that opens the full-width search overlay under 640px |
| A bar-viz stat with `fill_pct: 0` renders an empty track: the guard is `is not None` only. The poster's null guard has the same hole | `_stat_tile.html` ~41; `poster.html` | immigration-borders-restriction, 2026-09-05 | treat 0 like null in both guards, or have stage 1's shape check reject `fill_pct: 0` on a bar |
| Draft banner uses a position token (`--pos-amber`) for its border and icon, mixing color systems; on an amber-category topic with an amber camp three unrelated ambers share a viewport. Draft-only, no reader sees it | `static/css/ideya.css` ~255-256 | economic-inequality, 2026-09-02 | needs a chrome notice token; `tokens.css` has none, so picking one is a design call |

## By design (do not report)

| Behavior | Decision |
|---|---|
| Poster shows only the top 4 positions with no "+N more" | Jeff, 2026-08-26 |

## Fixed (report a match as a regression)

| Defect | Fixed by |
|---|---|
| Stat value/unit run-on ("28countries") | `u-word` class on space-led units plus `.tv small.u-word` margin |
| Poster multi-word unit collapse ("3.7Mhomes") | poster stat unit gets normal tracking (`poster.html` ~53) |
| Range-viz ghost dot hard-coded at 95%; midpoint pin for a true range | real band (`rband`) with pin fallback, `_stat_tile.html` |
| Ranked-row hard 64px label column at mobile | label column is a share of the tile (`ideya.css` ~294) |
| Lean-chip overflow at 320px | `white-space:normal; overflow-wrap:break-word; hyphens:auto` |
| Caret exponents rendered literally ("10^26") | `sup_exp` templatetag |
| "Connects to" chips clipped under 360px | `.rchip { max-width:100% }` |
| Scope card "Not" missing its colon | `detail.html` ~145 |
| Mobile position cards lacked a tap affordance | caret `xtoggle` on all viewports (since reopened, see Open) |
| Expanded captures clipped at a fixed height, and forced-visible layers missing `.is-open` layout rules | per-breakpoint override in `detail.html`; capture cap raised to 60,000px and the near-cap check made a hard `CommandError` in `render_screens.py`; `.is-open` rules added to the capture style block |
| Square/OG share cards clipped summary and CTA | `flex:none` plus clamp-governed truncation |
| Poster rendered a 0% meter for bare-number stats | null `fill_pct` guard in `poster.html` |
| Loader silently hard-sliced `source_label` / `source_published` | truncation warnings in `load_topic_draft.py` |
| Token collisions (cat-tech = pos-blue, cat-econ = pos-amber, focus ring) | palette de-collision, `d22c081` |
| Position palette exhausted at 7 | extended to 10 hues, slate last, loud loader fallback (2026-08-27) |
| Mobile hero art ate the fold (355px at 390w) | 300px art cap, `d22c081` |
| Odd-count position grid left a dead column | trailing odd card spans the row, `d22c081` |
