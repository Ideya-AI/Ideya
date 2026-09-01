---
name: refresh-topic
description: Re-check ONE topic as it goes stale — scan what is broken or undated, scout what has moved in the world, re-verify only that, and propose a cited diff for human approval. Never rewrites the topic and never publishes. Use when refresh_scan / topics_due flags a topic, or when something material changed a topic's shape.
disable-model-invocation: true
argument-hint: "[slug]"
---

# refresh-topic

> **Iron rule — automation may OPEN a proposal; a human approves every content
> change. Never auto-publish.**
>
> **Second iron rule — a refresh corrects what moved; it does not re-author.**
> Enforced in code (whitelist / grounding / regression gate), not asked for in a
> prompt: prompt language was tried and Nuclear Energy lost work twice anyway.

This skill is a launcher. The procedure lives in **`research/REFRESH.md`** — the
refresh engine's own manual, kept separate from the authoring engine because the
two run on different clocks. Read it and follow the runbook for `<slug>`
($ARGUMENTS), **starting at step 0**:

```
.venv/bin/python research/workflows/check_refresh_drift.py
```

Refresh sits idle for months while authoring is developed weekly. Step 0 reports
what refresh has fallen behind on; catch that up before the run.

The runbook is shaped around the three questions a refresh answers:

1. **Is there new information to incorporate?** — the scout
2. **What needs updating, refining, or deprecating?** — `refresh_scan`'s work
   order, then a targeted re-verify of only what it flags
3. **Is the topic still accurate, fair, and intellectually honest?** — the
   deterministic floor, one diff-scoped critic, then `topic-pm` reading it whole

Start with `manage.py refresh_scan --slug <slug>`. It is free, and a clean scan
plus a quiet scout is a complete refresh: stamp `reviewed_at` and stop.
"Nothing changed" is the expected outcome, not a failed run.

Contracts, the `__ARGS` recipe, and failure modes: `research/ENGINE.md` §10–§11
(shared with authoring). The three locks, cadence, and automation boundaries:
`research/REFRESH.md`.
