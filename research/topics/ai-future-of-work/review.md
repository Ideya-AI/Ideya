# AI & the Future of Work — review packet (2026-08-12)

**Status:** DRAFT loaded as `ai-future-of-work` — NOT published (stage 5 is yours). Stages: research 3 fix rounds (+2 post-run fact fixes), distribute 1 fix round → 3/3, icon 1 round, views 2 rounds.

## Substance gate (stage 1)

- **neutrality: PASS** (thorough note: camp coverage complete; suggested naming a labor-movement voice on Institution Shaper — done, see below). **steelman: PASS · crux: PASS.** Six camps: Transition Realist, Augmentation Optimist, Institution Shaper, Displacement Hawk, Scale Skeptic, Post-Labor Futurist.
- **fact-source: FAIL → fixed** per the critic's prescriptions before persisting: (1) a fabricated "~4%" employment figure attached to a mischaracterized mechanism in Acemoglu/Manera/Restrepo — replaced with the paper's actual 1.35%/5.85% and its real lever (reducing excess automation, not capital taxes); (2) the Census AI-adoption tile headlined a stale, narrower 3.8% (late 2023) contradicted twice elsewhere on the page — now headlines the May 2026 19.8% figure with the question-change caveat in the detail.
- Note: neutrality critic's missing-camp check ran from model knowledge — the run's web-search budget (200 calls) was exhausted before its searches. Engine note logged.

21 editorial notes in the dossier verdicts.

## Presentation gate (stage 2)

3/3 pass (compact-self-sufficiency converged in 1 fix round — first topic on the tie-break-patched fix loop, and the first needing zero orchestrator gate fixes). Fold: basics 5/7, questions 4/7, positions 6/6.

## Post-gate content edits (orchestrator, facts preserved)

- Loader-truncation repair: two representative_notes over the 300-char cap re-written to fit gracefully (they had been hard-cut mid-sentence).
- View-critique round: proponent lists deduplicated to one camp per person (Autor/Brynjolfsson/Acemoglu each anchored 2–3 camps; cross-camp mentions stay in prose; AFL-CIO Technology Institute added to Institution Shaper per the stage-1 neutrality suggestion); ranked risk-estimate rows relabeled by study ("Frey & Osborne 2013" etc. — bare years read as a backwards time series); two over-budget stat labels trimmed; crux lead's ASCII apostrophe fixed; two lean-chip pairs re-ordered to match their question's clause order; Anthropic Economic Index blurb de-editorialized ("survey speculation" → "self-report"); Q4's "the other positions" now names its opposing camps; quote-style consistency.
- Poster fits (40px slack) after: crux lead tightened 120→82 chars, crux subtitle and hero summary trimmed, poster band rebalanced (bar + radial + radial).
- Position palette: explicit color keys, no amber on this economy-category topic (category-amber collision — same token issue class as AI Takeoff's blue, still an open system decision).

## Icon

Winner: candidate 4 of 4, first batch, no refine rounds — the new filled-masses rule produced a clean 40px thumb immediately. Scene: human and machine arm at equal weight over one shared worktable, unclaimed sheet between them, briefcase intact.

## Views

Desktop/mobile/expanded: clean after fixes (positions grid balanced at 6, all sections alive on mobile, no truncation/entities). Social cards: **all three formats verified clean** — first topic through with zero card defects; the share.html rebuild holds on the base bucket. Scroll-spy anomaly in captures confirmed to be a capture artifact (live browser correct). Links: 0 dead, 0 placeholder (3 "blocked" are bot-refusals; 2 redirects worth inlining at publish).

## Engineering fixed this round (all topics benefit)

Ranked-tile label hyphenation (was mid-word breaking), ranked value column one-line up to 12ch (was hard 52px wrapping "~20 years"), expanded sections size cards to content (was ~250px dead white in short row-mates), action meta row stacks under 360px, external-link arrows glued to the last word, template-chrome apostrophes typographic. All six posters re-gated after the CSS changes: every one fits.

## Check in 5 minutes

1. The two most-edited facts: the Acemoglu tax-code figures and the Census 19.8% adoption tile.
2. Proponent dedup calls — especially Acemoglu anchored to Scale Skeptic (his "Power and Progress" institution-shaping work stays in that camp's prose).
3. Actions lean read-heavy (4 of 8 are Learn more) — the critic suggested swapping one for a doing-action (retraining program / open comment docket). Needs fresh sourcing, so left to your call.
4. Q7 poses three actors but offers two lean chips — reword to binary or accept.

## To publish (after your review)

```
.venv/bin/python manage.py load_topic_draft --file research/topics/ai-future-of-work.json \
  --slug ai-future-of-work --title "AI & the Future of Work" \
  --category economy --status published --image-brief research/icons/ai-future-of-work.md
```
→ `load_universe` (5 related edges) → reviewed_at → `check_links` → inline the 2 redirect URLs.
