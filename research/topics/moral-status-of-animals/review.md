# Moral Status of Animals — review packet (2026-08-28)

**Status:** DRAFT loaded as `moral-status-of-animals`. First ethics topic. The
smoothest run of the batch: stage 1 completed 33/33 with zero errors, every closure
was an exact prescription, no camp fork, and the poster fit on the first render.

## Substance gate (stage 1)

- **claim-ledger — PASS**: 56 claims, 44 supported, 12 resolved-by-revision, 0 open.
- **neutrality / steelman / fact-source — pass after closure.** 8 blockings, all with
  exact source-verified prescriptions, applied verbatim: two question framing lines
  re-attributed symmetrically (each had settled half its own question in house voice
  — once toward welfarists, once toward rights litigants); the Human Exceptionalist
  medical-advances quantifier moved in-voice; the actions rail normalized (the
  animal-research defense had been the only camp action above the fold); the 2005
  Nuffield figure dated; the Breheny dissent softened to the verified habeas
  holding; the Cambridge/NY declaration contrast corrected against both primary
  texts; the Grandin vocalization threshold restated per the audit guidelines.
- **No missing camp** — the plan itself grew past the catalog sketch to six,
  adding Capabilities Entitlement (Nussbaum).

## Presentation gate (stage 2)

Pass after closure: the 3Rs glossed in both reading layers, the research stat label
widened to what the value measures, and (post view-critique) the NY Declaration
label shortened so its row's hero numbers share a baseline, plus one deep-layer
self-duplication removed (Relational Obligation restated its own card summary).
Fold: basics 6/9, questions 4/7, positions 6/6 — every camp above the fold. Lint 0;
loader 0 warnings.

## Camps (6, prevalence order)

Humane Use 85 · Human Exceptionalist 70 · Equal Consideration 62 · Animal Rights
Abolitionist 45 · Relational Obligation 35 · Capabilities Entitlement 28 — six
distinct hues, no palette wrap, amber/rust adjacency verified apart at dot size.

## Icon

Winner: candidate 1, first batch — a level, empty two-pan scale with a paw print
and a human handprint at equal size beneath the pans. The only candidate carrying
the duotone fill on every major element. Best 40px thumb of recent topics (scale,
paw and hand all read), and the composition fills the frame vertically — the
low-baseline dead space flagged on vaccine-mandates is fixed here. All candidates
kept.

## Views

All 9 surfaces pass; poster fit first try (48px-class slack, 69-char lead). The
critic verified: 6/6 camps above the fold at every width, category terracotta only
on badges/chips, single dark inversion, complete honest expanded captures, the
mobile hero art vertically full. Content contract clean (zero straight quotes,
entities, briticisms, double spaces).

## Engineering issues (for you — pipeline does not touch CSS)

1. **NEW, in the register: the poster drops the space between value and word units**
   ("&gt;80billion", "~124billion" here; "~7months" on the published ai-takeoff
   poster). `poster.html` emits units in a bare `<small>` without the web tile's
   `u-word` class — the earlier "unit collapse" fix restored only internal spaces.
   Prescription in `research/reviews/UI_DEFECTS.md`; re-render all posters after
   fixing.
2. 2px card-export hairline — register, unchanged.
3. Critic observation, editorial: the three tier-2 stats behind Go-deeper are all
   bare years (2012, 2022, 2009) — three 4-digit numbers in a row. Defensible,
   visually monotonous; swap one for a count if it bothers you.

## Check in 5 minutes

- The question framing rewrites (Q4 welfare-reforms, Q-legal-form): both now
  attribute symmetrically — read them once.
- The Humane Use camp leads at 85 with Human Exceptionalist at 70: does the
  prevalence order read right to you?
- The poster unit-gap defect (engineering #1) — worth fixing before any topic's
  poster ships to print.

## To publish

load_topic_draft --file research/topics/moral-status-of-animals.json
--slug moral-status-of-animals --status published
--image-brief research/icons/moral-status-of-animals.md --reviewed
→ check_links --topic moral-status-of-animals (0/0) → commit artifacts → live push
per DEPLOY.md §3.
