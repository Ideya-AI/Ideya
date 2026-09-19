# The authoring pipeline — the brief for the rebuild

Written 2026-09-18, after v1 and v2 both failed. This is not a design. It is
what the next design has to answer for, and what two builds already measured.

## What the pipeline is for

Take a topic from `not_started` to `ready`: fill `content` in
`research/topics/<slug>/topic.json` to the shape in `research/SCHEMA.md`.
Before it is the topic directory. After it is a human who publishes.

The bar is **public understanding, not research**. Wikipedia grade: a reader
can follow a named source, the page is right about as often as a good
encyclopedia is, and errors get fixed when found. Jeff, 2026-09-16: "We aren't
doing research here. Just public understanding."

## What two builds measured

**v1** (deleted 2026-09-14) was prompts plus critic agents plus a claim ledger
plus a fix loop. Verify cost 8–20M tokens a topic and the gate 6–25M more. Two
wrong claims shipped through a 4-of-4 critic gate. Three of three
orchestrator-prescribed replacement facts did not verify. The page still went
out saying 77 reactors under construction where its own cited source said 62,
and a human found it two months later.

**v2** (stage 1 only, three runs on nuclear-energy) harvested 71 pages, then
forbade writers from using anything else. Run 2 cost $37.75 notional over 237
calls, against a design estimate of about 60 calls.

**The ledger caught nothing.** Across runs 1 and 2, 541 checked claims, 98
cuts, **zero factually wrong numbers found**. Both cuts labelled "number not in
quote" were false positives where the claim and the source quote were
identical. Half the cuts were pipeline bugs or unsourced explanatory
sentences; the rest were voice attributions, URL artifacts and precision
nuances.

**A two-minute Opus call matched it.** An off-the-cuff prompt produced a
document whose facts, crux and empirical/value split were as good or better.
Its camps were worse: ten of them, posture-labelled, several of them
sub-groups. Its errors were staleness and mixed accounting bases, not
fabrication.

## What that means

- **Checking transcription finds nothing.** A writer with the page open copies
  correctly. The errors that reach a page come from memory: a stale figure, a
  price year, a superseded revision. The ledger never looked there.
- **The quality gap was organizational, not capability.** v2 split the writing
  across 19 units that could not see each other, forbade the model's own
  knowledge, and gave the stat prose to a weaker model at low effort. The
  result repeated the Vogtle overrun twelve times and padded every detail. One
  mind with full context and full effort wrote better.
- **Prompts cannot police prompts.** Every v1 and v2 check that was a prompt
  either failed or cost a fortune; every check that was code held. A model
  reporting on its own compliance comes from the same process that missed.
  This is the one lesson worth carrying forward, and it is narrow: it argues
  for code where something must be *certified*, not for code everywhere.
- **The human is the certification.** Stage 5 was always the gate. With that
  accepted, most of the machinery has no job.

## What the rebuild must not do again

- No harvest-first. Discovery that forbids the model's own knowledge starves
  the writing and buys nothing measurable.
- No per-claim proof machinery. 541 claims, zero catches.
- No fan-out on synthesis. Retrieval can fan out; writing cannot.
- No models gating models: no critic panels, no fix loops, no PM gate.
- No weaker model on prose.
- No rebuild from principle. Nothing changes unless a measurement says it
  helped.

## What it probably looks like

An author and an editor, both prompts, and a human.

1. **Author.** One call, best model, full effort, full context. Writes the
   whole topic from what it knows into the schema, with the camp rules, the
   style sheet and a staple checklist in the prompt. Searches for anything
   dated, because staleness is the error class that reaches pages. Puts a
   source URL on every stat tile.
2. **Editor.** A fresh session that reads the page as a reader would and
   returns a packet of specific defects. The author fixes what it names. No
   loop. Fresh context is the whole trick.
3. **Jeff** reads and publishes. Readers flag. The file gets fixed.

Code only where it is a tool: the loader, fetch, and a grep for the mechanical
rules (UK spellings, straight quotes, entities, URLs that do not resolve).

## Rules that survive from v2 and are worth keeping as prompt text

- **What a camp is.** Two independent named adherents, at least one
  institutional. Two camps are distinct when there is a proposition one
  affirms and the other denies. Camps are named by what they want, all in the
  same grammatical form. No posture labels (Skeptic, Realist, Pragmatist,
  Advocate). Look for a hybrid and a reject-the-question camp on purpose.
  Three to six. v2's six camps beat the quick doc's ten; this is the rule that
  earned its keep.
- **Order is weight.** Every list is most important first. No tiers, no
  scores.
- **Plain text.** `&`, typographic quotes, no markup, US spelling.
- **Item ids are stable.** Reader votes, leans and prompts attach to them, so
  re-authoring must preserve them or participation detaches.
- Those prompt blocks are in git at `04c827e:pipeline/prompts/shared/`.

## Before building, build the measure

Nothing about v1 or v2 was ever scored, which is why every argument was from
principle and every restart began from scratch. Write the rubric first: the
seven things a page has to be (fair camps, right numbers, full coverage, a
real crux, clean prose, current, valid schema) as gradable questions. Grade
run 2 and the quick doc by hand to calibrate it. Then every model, effort and
structure choice is a number instead of an opinion.

The open measurement: on a *thin* topic, how often is a from-memory claim
wrong? Nuclear is the model's best case. That number decides how much
checking the design needs, and nobody has it.

## Pointers

- `research/SCHEMA.md` — the file shape the pipeline must produce.
- `research/archive/PIPELINE-v2.md` — the v2 design, inert. Stage 1's unit
  table, the §11 machine-level findings and the stage 5 read are the parts
  worth re-reading.
- `research/pipeline/runs/` — the run 1 and run 2 analyses, with costs.
- `research/runs/nuclear-energy/` — both runs archived whole.
- `research/archive/v1/` — v1 pages, converted to the new schema. The best
  existing examples of a finished topic.
