# AI Alignment Approaches — review packet (2026-08-27)

**Status:** DRAFT loaded as `ai-alignment`. Stages: research 3 fix rounds + orchestrator
closure (run split across a session-limit interruption; resumed from cache), distribute
1 run + orchestrator closure, icon 1 round (first-batch winner), views 2 rounds
(poster fit saga + one recapture). First topic through the new fully-automated
editorial-fork policy and the first with `prevalence_basis` captured.

## Substance gate (stage 1)

- **fact-source — PASS** (21 checks run).
- **steelman — pass after closure.** One blocking: the Control Engineer description
  misstated Anthropic's RSP v3.0 as requiring a misalignment safety case as a shipping
  gate; the critic's exact prescribed replacement was applied verbatim. Its
  position-by-position endorsement test endorses all camps.
- **neutrality — pass after closure.** One blocking: a genuine missing camp
  (present-harms / sociotechnical alignment). Resolved by the engine per the
  no-mid-run-escalation policy: **Deployment Witness added** (see below).
- **Claim ledger: 60/60 closed.** 54 supported outright; 6 were resolved-by-revision
  (the round-3 fixer had landed the corrections; the ledger's staleness gap is now
  fixed in the engine). The 11 claims of the added camp were verified 11/11 by an
  isolated verifier, every quote confirmed verbatim on source.

## Presentation gate (stage 2)

- **compact-self-sufficiency + selection / reading-level-fit — pass after closure.**
  Four blockings; the fix loop could not land them because two were *label* edits and
  `label` is whitelist-rejected (engine finding, logged). Applied by the orchestrator:
  alignment-faking tile rescoped to what 14% measures + contested clause; scaling-laws
  label names debate as the value's subject; control tile glosses its three protocol
  terms; RLHF/NLP/RLAIF expanded everywhere (zero bare acronyms).
- One prescription deviation: the critic's "about 3% otherwise" figure existed nowhere
  in draft or dossier — not substituted (fact-lock); "almost never otherwise" stays.
- Lint at 0 findings; loader at 0 warnings.

Fold above "Go deeper": basics 5/8, questions 4/7, positions 6/10 (clean tier-1 cut,
weights 80→35 above, 30→20 behind; array order matches prevalence).

## The Deployment Witness decision (flagged for your override)

The neutrality critic verified the present-harms/sociotechnical camp as genuinely
absent (a 2026 position paper partitions alignment into three camps; this is one).
Per your automation policy the engine took the critic's primary prescription:
**Deployment Witness** (weight 35, spectrum 0), authored from the camp's own texts
(Birhane, Gebru, Raji, Bender), 11/11 claims verified, wired into the crux subtitle
and given a DAIR learn-more action. Its `prevalence_basis` is in the dossier plan.
**You may override camp inclusion here before publishing** — the alternative the
critic offered was narrowing scope_covered/scope_excluded instead.

## Poster crux compression (flagged)

The ten-camp crux blew the poster band (233px overflow). Compressed under the
no-silent-drop rule (all ten camps still locate themselves): subtitle 436→192,
empirical 687→355 (regrammared after a critic catch), values 327→274, lead to two
poster lines ("Every camp has an alignment method; none can say what would count as
proof it worked." — lead_highlight updated to match). Poster now fits, **48px slack**.
The dossier keeps the uncompressed crux if you prefer to rebalance differently.

## Icon

Winner: `candidates/ai-alignment/ai-alignment.gemini-3-pro-image.3.jpg`, first batch —
magnifier-over-nodes, target with near-center arrow, nested frames on one ground line;
every mass filled; 40px thumb verified. #2 disqualified (heavy fills), #1 (stray line
artifact), #4 (outline-only lens). All candidates kept for swaps.

## Views

Desktop / mobile-390 / mobile-320, normal + expanded / OG / sq / pt / poster — pass.
Poster fit: 48px slack. The 320px-expanded capture was initially clipped at the old
45,000px window (page runs 53,399px); recaptured after the harness fix and the
previously-unseen region verified clean (Crux band single inversion, all action
cards, clean footer).

## Engineering issues (for you — pipeline does not touch CSS)

1. ~~Position palette exhaustion~~ — **RESOLVED (Jeff-approved, 2026-08-27)**: palette
   extended to 10 hues (berry/indigo/cocoa added, slate demoted to last resort), loud
   loader fallback, migration 0024; all 10 camps verified rendering distinct colors.
2. ~~Poster "SHOWING 4 OF 10" header~~ — **REMOVED (Jeff-approved, 2026-08-27)** per
   the no-further-explanation ruling; poster re-rendered, fits.
3. 2px card-export hairline — register citation confirmed, unchanged.
4. Cosmetic notes: the 2% donut arc reads as empty at a glance (a minimum-arc floor
   would help small percentages); sq/pt cards carry ~200–250px of empty upper panel
   (fixed-aspect artifact); Value Pluralist vs Deployment Witness detail-length gap
   leaves ~580px of empty card in the expanded desktop grid row (trim VP's detail or
   extend DW's if it bothers you).

## Check in 5 minutes

- **Deployment Witness**: keep the 10th camp, or narrow scope instead? (Engine chose
  inclusion per policy; both paths detailed above.)
- **Crux compression**: the poster-driven trims also changed the web page's crux band.
  Read the band once — is the compressed register still the page's anchor?
- **Poster "SHOWING 4 OF 10" header** vs your no-explanation ruling (issue 2).
- The alignment-faking tile's contested clause (a presentation closure): does the
  compact framing read fair to both camps?

## To publish

load_topic_draft --file research/topics/ai-alignment.json --slug ai-alignment
--title 'AI Alignment Approaches' --category ai --status published
--image-brief research/icons/ai-alignment.md
→ set reviewed_at → check_links --topic ai-alignment (0/0) → commit artifacts →
live push per DEPLOY.md §3.
