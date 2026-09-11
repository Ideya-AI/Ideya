# Vaccine Mandates & Public Health Authority — review packet (2026-08-28)

**Status:** DRAFT loaded as `vaccine-mandates`. First bio-health topic. Stages:
research 1 fix round + large orchestrator closure (run split across a session-limit
interruption, resumed from cache), distribute 1 run + 1 closure, icon 1 round
(first-batch winner), views 2 rounds. First topic fully through the improved engine
(structurally blind claim-verifiers, stale-ledger check, per-tier basics).

## Substance gate (stage 1)

- **claim-ledger — PASS**: 73 claims, 55 supported, 18 resolved-by-revision, 0 open.
  The new staleness check worked as designed on its first run.
- **neutrality / steelman / fact-source — pass after closure.** 20 blockings survived
  the single fix round the anti-re-litigation rule allows; 18 carried exact,
  source-verified prescriptions and were applied verbatim by the orchestrator
  (unverifiable quotes and figures cut or attributed in-voice: AAP, THA, IDSA/SHEA/
  PIDS, Army 6.04%, NYC 1,780→1,400+; the 1853 Vaccination Act history corrected;
  Delamater intervals unified; MS/WV statute status corrected; the stale 25-state
  delink updated to KFF's current 27/30; CIDRAP's measles tally attributed).
  1 was already landed by the fixer; 1 was the missing camp (below).

## Decisions the engine made (flagged for your override)

1. **Hassle Factor Architect added** (7th camp, w=43, spectrum −2) — the
   exemption-friction middle (Navin, Largent, McCright, Diekema; the operating
   design in Michigan/Washington/Oregon/Vermont). Verified 11/11 by the blind
   claim-verifier agent. Also wired into Q6's detail as the third reading + a JAMA
   Pediatrics learn_more action.
2. **Lean seeds recalibrated** — the neutrality critic found all seven question bars
   tilted to the mandate-favoring pole (Q1 at 75, above the whole published corpus).
   Q1 75→60, Q7 35→60 (flipped toward the better-evidenced access reading).
3. **Medical Freedom Campaigner weight 40→48** — stage 2's critic found the only
   outright anti-compulsion camp was the one position behind "Go deeper" while an
   academic design-variant camp showed. Revised under stage-1 authority on the
   camp's own recorded basis (15-state legislative footprint); the critic's
   alternative was 60. Fold now: 80/65/55/50/48/45 shown, 43 (Hassle Factor
   Architect) behind Go deeper.
4. **Poster crux compression** — the three-line lead recurred (second topic in a
   row); compressed to "Each camp names a bar compulsion must clear; one sets it
   where nothing clears it." (81 chars, two lines). Poster fits.

## Presentation gate (stage 2)

compact-self-sufficiency + reading-level-fit — pass after closures. Fold: basics
6/10 (7 after the ranked-wide fix re-snap), questions 4/7, positions 6/7. Lint 0;
loader 0 warnings (title/category auto-resolved by the new loader).

## Icon

Winner: `candidates/vaccine-mandates/gemini-3-pro-image.4.jpg`, first batch —
schoolhouse, unsigned exemption form lying flat, syringe at rest on one ground
line; deliberately verdict-free. Honest flag: at 40px the thin syringe fades to an
accent (checked against the runner-up, no better; same class as ai-takeoff's
accepted thumb). All candidates kept.

## Views

All 9 surfaces pass after closures. Poster fit after the lead compression. The
view critic verified: all 7 camps in distinct hues (the extended palette holding,
no slate fallback), category color only on badges/chips, single dark inversion,
complete expanded captures at all widths. Its 3 content findings (stranded
punctuation from a cut clause, the crux subtitle miscounting six camps after the
seventh was added, two ranked stats missing wide:true) were applied and
re-rendered; its harness finding (expanded captures never applied `.is-open`,
producing phantom layout defects) was fixed in the capture style block and the
re-render certified.

## Engineering issues (for you — pipeline does not touch CSS)

1. **NEW, in the register:** ranked-stat rows at ≤360px get a dead right gutter —
   the 360px two-column `.rrow` rule is overridden by the later 640px three-column
   redeclaration. Prescription in `research/reviews/UI_DEFECTS.md`; affects every
   topic with a ranked stat at 320px.
2. 2px card-export hairline — register citation, unchanged.
3. Cosmetic notes from the critic: the icon composition hugs the lower ~60% of its
   frame (dead space above, most visible in the mobile hero card); the exemption-form
   parallelogram is the icon's one ambiguous element.

## Check in 5 minutes

- The four engine decisions above, especially the **Hassle Factor Architect**
  inclusion and the **Medical Freedom Campaigner 40→48** weight call.
- The recalibrated lean bars: Q1 at 60 and Q7 flipped — fair seeds?
- The compressed crux band (two-line lead + seven-accounts subtitle) — still the
  page's anchor?

## To publish

load_topic_draft --file research/topics/vaccine-mandates.json --slug vaccine-mandates
--status published --image-brief research/icons/vaccine-mandates.md --reviewed
→ check_links --topic vaccine-mandates (0/0) → commit artifacts → live push per
DEPLOY.md §3.
