# Climate Tipping Points — review packet (2026-08-13)

**Status:** DRAFT loaded as `climate-tipping-points` — NOT published. Stages: research 3 fix rounds (+2 post-run fact fixes), distribute 3 fix rounds (+2 whitelist-refused compact fixes applied by orchestrator), icon 1 round, views 2 rounds.

## Substance gate (stage 1)

- **neutrality / steelman / crux: PASS.** Five camps as planned: Tipping Point Sentinel, Continuum Realist, Framing Critic, Fat-Tail Insurer, Threshold Skeptic.
- **fact-source: FAIL → fixed** per prescriptions: (1) the tipping-cascade stat had **inverted its source** — 39% was the share of simulations that did NOT tip (Wunderling et al. Table 3); corrected to the true ~27% cascade share with the coupling-strength decomposition in the detail; (2) the AMOC slowdown figure (0.46 Sv/decade) was cited to an IPCC landing page that doesn't contain it — re-sourced to Pontes & Menviel, Nature Geoscience (2024) directly.

25 editorial notes in the dossier verdicts.

## Presentation gate (stage 2 — first run on opus critics)

- reading-level-fit / above-fold-selection: PASS (with an unusually thorough reading-level commendation of the compact layer). **compact-self-sufficiency: FAIL → fixed** (both whitelist-refused, applied by hand): the load-bearing "4 elements within 1.5°C" tile now carries its two neutralizing caveats (wide ranges; decades-to-millennia unfolding) in the compact note rather than only behind Go-deeper; the lead question's "Atlantic overturning circulation" got a compact-layer gloss ("the Atlantic current system that carries warm water north"). Fold: basics 5/8, questions 4/7, positions 5/5.

## Post-gate content edits (orchestrator, facts preserved)

Poster interplay: the compact-caveats fix grew the band tile and the 91-char crux lead wrapped to three poster lines — resolved by tighter wording (every fact kept) and a DOM-measured 86-char lead; band rebalanced (coral radial in, Amazon range below). View critique round: garbled crux subtitle rewritten ("what uncertainty licenses…"), stat suffixes shortened (°C, % of runs, Sv/decade), doubled source-label dates removed, ice-sheet chart relabeled to match its three-row content, two prose walls split, two grammar fixes, scope-case fix.

**Site-wide neutrality catch (from this topic's card critique):** OG cards were clamping summaries mid-sentence — on this topic amputating the balancing clause ("…or muddies it"), leaving a one-sided claim on the share card. All nine topics' summaries rewritten to the measured ≤~130-char OG budget (both clauses preserved); plan prompt now carries the cap.

## Icon

Winner: candidate 2 of 4, first batch — ball at the apex of a curve, iceberg at the waterline, snowflake; the only strict two-tone candidate; 40px reads.

## Views

Desktop/mobile/expanded clean after fixes; 5th position card verified spanning its full row (the new odd-grid fill); new palette contrast verified (all dots/rails pass; note: **amber is 3.1:1 — never use it for small text**). Poster fits (19px). Links: 0 dead / 0 placeholder (3 redirects to inline at publish). Social cards clean after the summary trim; pos-green re-shifted to deep pine `#146c4f` (the palette rebuild had left it hue-identical to cat-energy).

## Engineering fixed this round (all topics)

Spanning trailing cards keep a 68ch measure; wrapped stat suffixes keep readable leading; **mobile condensed no longer strips action notes** (condensed-reveal actions show descriptions everywhere); crux eyebrow subtitle restored on desktop; actions grid fills its odd trailing row like positions; sub-360px ranked rows drop the meaningless bar track; action position-labels bumped to readable ink.

## Open/notes for you

1. Second category chip hidden on mobile — deliberate rule, but critics flag it every topic; say the word if you'd rather show both.
2. Scroll-spy "Positions active at top" in captures — verified live-correct before; capture artifact.
3. Amber small-text prohibition worth adding to DESIGN_SYSTEM if you agree.

## Check in 5 minutes

1. The two corrected facts (cascade inversion is the big one — it flipped the number's meaning).
2. The compact-layer caveats on the 1.5°C tile (balance vs alarm framing — your editorial call whether it now under- or over-hedges).
3. The measured crux lead ("If the thresholds can't be placed, is that the strongest case to act — or the weakest?").

## To publish (after your review)

```
.venv/bin/python manage.py load_topic_draft --file research/topics/climate-tipping-points.json \
  --slug climate-tipping-points --title "Climate Tipping Points" \
  --category climate-env --status published --image-brief research/icons/climate-tipping-points.md
```
→ `load_universe` (4 related edges) → reviewed_at → `check_links` → inline the 3 redirects.
