# Stage 1, run 2: nuclear-energy, 2026-09-16

A fully independent run from an index-only topic, with every correction from
run 1 applied (`2026-09-15-nuclear-energy-run1.md`). Started 02:48 PDT,
verdict at 08:10 PDT after one sleep-through of a five-hour reset. The
working tree holds this run; run 1 is under `research/runs/nuclear-energy/run1/`.

## What ran

Phase A once, Phase B once (with six position reruns for ceilings that were
not beaten and so were discarded), Phase C once to the recheck, a pause at
90%, then on waking a second full Phase C prove over the already-repaired
draft (the recheck's state was not persisted), a block on one lint hit, and a
final pass with no model calls after the lint scoping and resume fixes.

## Cost

Journals are complete for this run.

| | calls | total input | output | $ notional | model min |
|---|---|---|---|---|---|
| A, the map | 13 | 2,485k | 153k | 8.57 | 33 |
| B, the sections | 19 | 881k | 160k | 7.32 | 25 |
| C, before the reset | 91 | 1,366k | | 9.36 | |
| C, re-prove after the reset | 114 | 1,720k | | 12.50 | |
| total | 237 | 6,451k | 947k | 37.75 | 147 |

By model: Sonnet 154 calls, 5.5M tokens, $22.72; Opus 83 calls, 1.0M, $15.04.
Without the post-reset re-prove the run is about 123 calls, 4.7M tokens and
$25. The five-hour window went from fresh to 90% in three and a half hours,
so one stage 1 run is about one window plus the tail after a reset.

## Wins over run 1

- **Six camps, each an answer to the headline question**, ranked with the
  two big ones first, and the hybrid camp ("make firm clean power compete on
  delivery terms") drawn cleanly. No sub-issue camps.
- **Basics from reference and official sources.** All 14 of the
  cartographer's stat candidates passed the class filter without a drop; the
  final tiles cite Wikipedia, GAO, IAEA, IEA, EIA.
- **Questions at the right length**: 81 to 118 characters, details around
  1,100, every one askable aloud, kinds correctly split.
- **Crux under every ceiling on the first try**, with a 170-character lead
  that reads as a lead.
- **Grounding rule worked**: 12 unsourced claims out of 220 extracted, against
  59 of 302 in run 1. Verification passed 188 of 208 model-checked claims on
  the first pass.
- **Bot walls halved**: 16 pages recovered through the archive fallback,
  camp class 9 sources against 5, failed fetches 40 against 71.
- **Proponents and representatives intact**, map-checked by code.
- **No oversized repairs.** Every repair landed inside its bound.
- **The run slept through a reset and resumed on its own** with the cleared
  reading, and the lint block cleared with zero model calls once the state
  was stamped as proven.

## Losses

### Cuts: 50, of which about 6 were legitimate

- **34 were glosses.** The extractor turned framing sentences ("one camp
  holds that…", "the IAEA publishes a low and a high case") into claims with
  no source, and the checks cut them. Fixed: a claim whose own text carries
  no figure, date, quote or attribution is dropped before checking.
- **12 more were sidecar mismatches.** The extractor left a figure unsourced
  although the writer's sidecar had it, because the writer labeled items its
  own way. Fixed: an unsourced extracted claim adopts the source of a sidecar
  claim on the same sentence or figures.
- **Two were HEAD-request artifacts** (a 406 on a page that had fetched
  fine). Fixed: a URL already in the store resolves.
- The rest were inferences a source did not draw, which is the design.

### Basics let four off-topic tiles in

Ghana's peak demand, a French heatwave curtailment, a heat-and-drought loss
share, and an Amazon power purchase. All came from the gap scout, whose fetch
tool stamped every page "reference", so the class filter passed them. Fixed:
the gap scout names each page's class.

### Stat notes drifted after repair

Two notes became commentary ("EDF's accounting is self-reported…") rather than
a statement of the number. A repairer rewriting a note loses the tile's
purpose. Open: the repairer prompt should say a basics note states the value.

### A dead action link was blanked

The repairer "cut" the Sierra Club action's URL field, leaving an action with
no link. Fixed: a failed action URL removes the action.

### Resume inside Phase C re-proved everything

The pause fell during the recheck, and the recheck's ledger was not persisted,
so waking re-ran extraction, verification and repair on a draft that had
already been repaired: $12.50 and an hour. Fixed for the end state (a proven
draft hash skips re-proving); the mid-recheck state is still not persisted.

### Lint scoping

"Proponents argue" in a question's detail is attribution in the page's voice,
and the repairer had been told to attribute. It linted as a hedge and blocked
the topic. Fixed: those phrases lint only inside positions.

### Position details 2 to 16% over the ceiling

The prompt's 1,600-character ceiling was exceeded by every position, and the
bounded rerun did not beat the originals. A 10% tolerance now records small
breaches instead of rerunning.

## State of the draft

Valid stage 1 verdict. 17 stats, 9 questions, 6 positions, crux, 8 actions.
The 50 cuts are in it, so about 44 sentences that should have stayed are
gone, and four basics tiles are off-topic. Re-proving from run 2's Phase B
returns under the fixed code would restore most of that for about $10 and
a third of a window: rebuild the draft with `phase_b.run_phase`, clear
`run/C`, rerun `author`.

## Corrections made after run 2

Code: gloss claims dropped before checking; unsourced extracted claims adopt
a matching sidecar source; the gap scout names each source's class; a failed
action URL removes the action; a fetched URL counts as resolving for actions
and stat sources; lint hedges scoped to positions; a proven draft hash lets
Phase C skip to the verdict; ceiling breaches under 10% are recorded, not
rerun.

Open: persist the recheck state so a mid-Phase-C pause does not re-prove;
basics notes must state the value after repair; Wikipedia still supplies
seven of seventeen tiles.
