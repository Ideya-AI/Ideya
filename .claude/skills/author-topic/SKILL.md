---
name: author-topic
description: Author ONE new Ideya topic end to end — research (substance) → editorial (presentation) → iconography → integration → the PM gate and a one-page packet — as a single automated, checkpointed run on the user's subscription. Use when turning a catalog entry into a publish-ready draft. AI drafts → a human publishes.
disable-model-invocation: true
argument-hint: "[slug]"
---

# author-topic

> **Iron rule — automation drafts; a human publishes.** The engine runs stages 1–5
> unattended and stops at a loaded DRAFT plus a review packet. Publishing is the
> human's hard stop, always.

Run the engine and let it finish:

```
.venv/bin/python research/engine/engine.py author <slug>
```

That is the whole procedure. `<slug>` is `$ARGUMENTS`. The driver
(`research/engine/engine.py`) walks seventeen checkpointed steps — stage 1 in four
phases, stage 2 with lint, load and poster fit, stage 3 brief → candidates →
selection → icon, stage 4 renders + per-section captures + links + design critics,
stage 5 the `topic-pm` read with routes closed by rule and one re-read — and writes
`research/reviews/<slug>/REVIEW.md` and `tokens.md`. State lives in
`research/runs/<slug>/state.json`; every agent call is journaled, so if the process
dies or a usage limit hits, run the same command again and it resumes at the last
call. A usage limit inside a run is handled by the harness (it sleeps until the
reset); expect one per run and do not intervene.

Watch it, don't drive it: `engine.py status <slug>` shows the step table; the log is
`research/runs/<slug>/engine.log`. Intervene only when a step reports FAILED with a
cause the engine cannot fix itself (a missing API key for the icon generator, a dev
server that will not start, a content-policy refusal in stage 1). The stage
procedures the driver executes, the model routing, the contracts and the
failure-modes table are in **`research/ENGINE.md`**; read it when something fails,
not to run the topic by hand.
