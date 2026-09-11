# AI Takeoff Speed & Loss of Control — review packet (2026-08-12)

**Status:** DRAFT loaded as `ai-takeoff-loss-of-control` — NOT published (stage 5 is yours). Stages: research 3 fix rounds (+2 post-run fact fixes), distribute 1 (+1 whitelist-rejected fix applied by orchestrator), icon 3 rounds, views 2 rounds.

## Substance gate (stage 1)

- **neutrality: PASS** · **steelman: PASS** · **crux: PASS.** All five planned camps delivered: Normal Technology Skeptic, Course-Correction Gradualist, Hard Takeoff Hawk, Gradual Disempowerment Theorist, Effective Accelerationist.
- **fact-source: FAIL → fixed.** 2 blocking defects, both fixed per the critic's prescriptions before persisting: (1) the Epoch compute-concentration stat under-counted Google (TPU row only, missing ~320k NVIDIA H100e) and quoted an unreproducible 4.67M denominator — rebuilt on absolute per-firm figures (Google 1.24M / Microsoft 660k / Meta 400k / Amazon 290k) with the denominator claim dropped; (2) Elon Musk removed as an e/acc proponent (signed the pause letter, endorsed SB 1047 — the position's most prominent counterexample).
- Note: this stage-1 run launched on the pre-improvement engine; the fix-loop tie-break patch (committed `522bb80`) took effect after and applies from the next topic on.

26 editorial notes preserved in the dossier verdicts. Worth a look: the "IEA data via Wikipedia" source on the data-centre stat (figures verified, but a primary IEA citation would be cleaner); AI Impacts survey caveats are carried honestly in-tile.

## Presentation gate (stage 2)

- reading-level-fit: PASS · above-fold-selection: PASS · **compact-self-sufficiency: FAIL → fixed**: the extinction-risk stat's label was narrower than its measured quantity (extinction *or* permanent disempowerment); the patch whitelist correctly refused the label edit, applied by the orchestrator per the critic's wording. Fold: basics 6, questions 4, positions 5 above.

## Post-gate content edits (orchestrator, facts preserved)

View-critique round: promoted 4 actions to `condensed` (**the Actions section rendered completely empty on mobile** — all were `normal`); balanced condensed questions (value question promoted, one empirical demoted); de-"we"'d the value question; shortened two lean labels that broke at 320px; trimmed two 3-line stat labels for row baseline alignment; added the chart's unit to the compute-concentration label; extended why_now with the survey's 13-year shift (already-verified stat); paragraph-broke all five position details; converted all straight quotes to typographic across content.

## Icon

Winner: candidate 3 + one edit round (filled trajectory arrows). Scene: steep-vs-gradual fork from a grounded rocket, human at a control lever — deliberately verdict-free. **Honest flag: the 40px thumb is legible but weaker than other topics'** (linework-heavy scene); consider swapping candidates or re-briefing bolder if it bothers you. All candidates kept.

## Views

Desktop/mobile-390/mobile-320 + expanded: clean after fixes (no truncation, no entities, all previously-fixed items verified holding). Social cards clean in all three formats. Poster **fits with 99px slack** — the new crux length budget landed this without any trimming.

## Engineering issues (from this round's critics)

- **FIXED in this session** (share.html/CSS, commit pending): flex-shrink was pixel-slicing line-clamped summaries mid-glyph on sq/t-mid cards (including DBP's committed sq card — regenerated); summary is now flex:none with clamp-governed truncation, budgets retuned, verified slice-proof across all 9 format×bucket combos. Lean-chip mid-word breaking (my `overflow-wrap:anywhere`) → `break-word + hyphens`. Share-card position dots pinned to first line.
- **OPEN — design decisions for you:**
  1. Mobile hero art eats the fold (355px tall at 390w; summary starts ~890px down). Suggest capping mobile art height ~200px.
  2. Odd-count positions grid leaves a dead column (5th card alone beside ~1,200px of blank in expanded desktop). Options: last odd card spans both columns, or balanced flow.
  3. **Token collision:** `--cat-tech` (ai category) and `--pos-blue` (position palette) are the same hex `#3b7ea1` — on this first ai-category topic, the blue position dot reads as category-colored. One-topic fix: recolor that position; system fix: split the tokens.
  4. Card exports carry a 2px background hairline (pre-existing on every topic, capture-clip artifact).

## Check in 5 minutes

1. The icon's 40px weakness — keep or re-brief.
2. The compute-concentration stat (most-edited fact) and extinction-risk label rewording.
3. Camp diversity of the 4 condensed actions (my pick: Normal-Tech read, MIRI donate, Gradual Disempowerment read, Add your view).
4. Position blue vs ai-category blue on the social card (open decision 3).

## To publish (after your review)

```
.venv/bin/python manage.py load_topic_draft --file research/topics/ai-takeoff-loss-of-control.json \
  --slug ai-takeoff-loss-of-control --title "AI Takeoff Speed & Loss of Control" \
  --category ai --status published --image-brief research/icons/ai-takeoff-loss-of-control.md
```
→ `load_universe` (edges) → reviewed_at → `check_links` → **teaser reconciliation**: retire/redirect the `ai-existential-risk` DB stub and update the teaser list in `topics/views.py` (home bench).
