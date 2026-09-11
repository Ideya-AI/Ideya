---
name: participation-review
description: Review what readers did on ONE topic — digest the participation log, narrate it, lightly fact-check what readers claimed, and save a report proposing what an editor might change. Recommends only; a human decides every line. Use before a stage-5 review of a topic, or when a topic's participation looks worth reading.
disable-model-invocation: true
argument-hint: "[slug]"
---

# participation-review

> **Iron rule — the report recommends; a human decides every line and makes any
> edit.** This skill never touches a topic's JSON or the database, and never
> publishes.

This skill is a launcher. The procedure lives in **`research/PARTICIPATION.md`
§5 — Runbook: participation review**. Read it and follow it for `<slug>`
($ARGUMENTS), starting at step 1:

```
.venv/bin/python manage.py participation_report --topic <slug> \
  --out research/participation/<slug>.<today>.md
```

The report has three parts — **what readers did**, **research and thoughts**
(light: the fact-checking an ordinary question would get), and a **proposal** of
what an editor might change. Nothing consumes the proposal automatically.
"Nothing to change" is a valid proposal, and an empty digest is a short report,
not a failed run.

Save to `research/reviews/<slug>/PARTICIPATION.<today>.md` (committed —
paraphrase readers there; verbatim text stays in the gitignored digest), print
the path, stop.
