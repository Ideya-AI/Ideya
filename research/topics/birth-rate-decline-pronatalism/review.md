# Birth-Rate Decline & Pronatalism — review packet (2026-08-13)

**Status:** DRAFT loaded as `birth-rate-decline-pronatalism`. Stages: research 1 fix
round (cleanest stage 1 of the six runs — a single fact blocker), distribute 1,
icon 1 round (first generation), views 1 round.

Categories: society (primary) · economy · ethics. 10 stats, 7 questions,
5 positions (Family-Policy Reformer, Pronatalist, Reproductive-Autonomy Liberal,
Adaptation Pragmatist, Population Ecologist), 8 actions, 3 prompts.

## Substance gate (stage 1)

- **neutrality — pass.**
- **steelman — pass.**
- **fact-source — FAIL → fixed.** One blocker: the ecological-footprint stat mixed
  per-capita figures from two different National Footprint Accounts editions and
  mislabeled the data year. Fixed per prescription: US ~7.0 gha vs world biocapacity
  ~1.5 gha, sourced to the 2025 edition (data through 2024) with a deep link to
  GFN's how-many-Earths page. Residual notes for you: the South Korea 0.80 TFR is
  arithmetically consistent with the linked MODS release but the English summary
  page doesn't print the headline TFR itself — worth a 30-second confirm.
- **crux — pass.**

## Presentation gate (stage 2)

- **compact-self-sufficiency — FAIL → fixed.** Blocker: the OECD old-age support
  stat presented a 2050 projection in the present tense with the wrong denominator
  ("per 100 workers"). Fixed per prescription: label now
  "Retirees per 100 working-age adults · OECD, 2050", unit dropped.
- **reading-level fit — pass.**
- **above-fold-selection — pass.**

Fold above "Go deeper": basics 5/10, questions 4/7, positions 5/5 (all five camps
are genuine and above the fold; depth carried by expansion, not the fold).

**Declined critic suggestions (close calls for your eye):** the critic's
non-blocking asks to append ", 2050" to the countries-below-replacement label and
to re-scope stat 3's label to "Reproductive-age adults…" were NOT applied — both
stats sit in the poster band, which now fits with only 2px slack, and both already
carry the year/scope in their year-labeled series and note. Overrule if you
disagree; the poster must then be re-gated.

## Icon

Winner: `gemini-3-pro-image.4.jpg`, first generation round — equal-width three-tier
age stack (the brief's neutrality device: neither pyramid nor inverted), occupied
cradle, clean globe, all masses filled; legible at 40px. #3 was disqualified for
tapering into a real pyramid, #1 for a four-tier stack + globe drop shadow.
Candidates in `research/icons/candidates/birth-rate-decline-pronatalism/`.

## Views

Poster initially overflowed by 28px (basics band + questions band each one wrapped
line taller than passing siblings). Fixed with measured trims: three stat notes
tightened (160→147, 164→146, 187→163 chars) and one word ("actually") dropped from
the first empirical question. Poster fit: **2px slack** — tight; any future text
growth in the first three stats or the crux re-triggers the gate.

Two opus view critics ran (screens; cards+poster). Both returned FAIL on first
pass; every blocking finding was content and has been applied and re-rendered:

**Cards+poster critic (2 blocking, fixed):**
- OG summary overran its 3-line clamp mid-word → summary rewritten 127→118 chars
  ("Sub-replacement fertility is now global: …"), verified rendering in full with
  the closing question intact on all three formats.
- Countries-below-replacement series values read as counts of nations → values now
  carry % ("~52%" / "76%" / "97%").
- Non-blocking applied: a values question moved into the poster's top-3 (the sheet
  previously showed three EMPIRICAL tags while the crux is half values); crux
  subtitle reworded ("Five readings of one trend: …") to kill a two-word widow.
- Non-blocking declined per the critic's own recommendation: the fifth position
  (Population Ecologist) is the one cut from the poster/cards while the crux
  subtitle names all five readings; disclosure ("showing 4 of 5", "+1 more") is
  honest, order left alone. Icon and neutrality explicitly verified clean.

**Screens critic (2 blocking, fixed):**
- Hungary stat citation sliced mid-word at the 40-char `source_published` cap →
  shortened to "April 2024; KSH 2025 fertility data", renders whole.
- Same series-values ambiguity plus a bar/label mismatch ("50+" over a bar drawn
  at 52) → "~52%" aligns value and bar; label tightened to "· % of 204".
- Non-blocking applied: 21 British spellings converted to US forms (the US-spelling
  rule is now in the engine RULES — it had never actually been written into the
  prompts); 5 lean chips shortened to hold one line at 320px ("Policy works" /
  "Policy can’t", "Real gap", "For now", "Not worth it"); all 7 question details
  and the Hungary detail split into two paragraphs at the side-pivot seam;
  Family-Policy Reformer detail split into 5 paragraphs; Hungary "4.5-5.5% of GDP"
  corrected to "4.5–5% of GDP" (the range the cited source actually states, per
  the pipeline's own stage-1 residual note, with the en dash); the
  pronatalist-policies note reworded to stop repeating "55" against two
  denominators; Guttmacher action attribution brought to parity ("which this
  position treats as…").
- Non-blocking NOT applied (your call): trimming Family-Policy Reformer's detail
  from ~3,400 toward the ~2,300-char band of the other four positions — that is a
  substantive steelman cut I didn't want to freelance; the paragraph splits fix
  the wall-of-text half of the complaint.

## Engineering issues (for you — pipeline does not touch CSS)

Fixed during this run (template/loader, with session precedent):
- `templates/topics/poster.html` rendered a 0%-filled meter for any bare-number
  stat (null `fill_pct`) — an empty track under "2.3 children per woman" reads as
  "zero of something". Now guarded like the web tile. Affects every topic whose
  poster band has a bare-number tile; older posters get re-gated in the
  normalization sweep.
- `load_topic_draft.py` silently hard-sliced `source_label`/`source_published`
  (the cause of screens blocker 1) — both now go through the same truncation
  warning as `representative_note`.

Logged, not touched:
- Stat tile value/unit run-on for word units ("10.3billion", "2.3children per
  woman" at 390px) — `_stat_tile.html`; needs a margin on non-symbol units.
  Site-wide, all topics.
- At 320px the ranked-stat bar track is hidden but its grid column is still
  allocated — values strand mid-card with an empty right gutter.
- Desktop positions grid: cards in a two-column row stretch to the tallest
  sibling, so expanding an asymmetric pair leaves ~600px of white inside the
  shorter card. `align-items: start` on the row would fix it.
- Card summary clamp is CSS-only and will cut mid-word for any future over-budget
  summary; a word-boundary fallback would make the format robust.
- Dev-server gotcha (now in the skill): Django caches compiled templates even
  under DEBUG; with `--noreload` a template edit is never picked up — restart the
  server before re-rendering after template changes.

## Check in 5 minutes

- South Korea TFR 0.80: confirm against the MODS release (English page omits the
  headline figure; arithmetic checks out).
- The two declined label suggestions above (", 2050" / "Reproductive-age adults").
- Family-Policy Reformer representative note was trimmed to fit the 300-char cap
  (dropped publisher name + compressed the country list) — confirm it still reads
  as her actual claim.
- Poster's 2px slack.
- Whether to trim Family-Policy Reformer's detail toward the other positions'
  length band (screens critic asked; I split paragraphs but declined the cut).

## To publish

load_topic_draft --file research/topics/birth-rate-decline-pronatalism.json
--slug birth-rate-decline-pronatalism --title "Birth-Rate Decline & Pronatalism"
--category society --status published
--image-brief research/icons/birth-rate-decline-pronatalism.md
→ wire related-topic edges (`manage.py load_universe`) → set reviewed_at →
check_links --topic birth-rate-decline-pronatalism (0/0) → commit artifacts →
live-site load per DEPLOY.md §3.
