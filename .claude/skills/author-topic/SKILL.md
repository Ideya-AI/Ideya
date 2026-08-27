---
name: author-topic
description: Author ONE new Ideya topic end to end through the staged pipeline — research (substance) → distribute (presentation) → iconography → views → a review packet for the human. Use when turning a catalog entry into a publish-ready draft. AI drafts → a human publishes.
disable-model-invocation: true
argument-hint: "[slug]"
---

# author-topic

> **Iron rule — automation drafts; a human publishes.** Stages 1–4 run unattended and
> produce a DRAFT topic + a review packet. Publishing (stage 5) is a human hard stop.

This skill is a launcher. The procedure lives in **`research/ENGINE.md`** — the
engine's single source of truth. Read it and follow **§5 Runbook A — author a topic**
for `<slug>` ($ARGUMENTS), start to finish: stage 0 (catalog entry, only if
uncataloged) → 1 research → 2 distribute → 3 iconography → 4 views → **4.5 the
`topic-pm` gate**, which verifies the finished topic, routes findings back to the
stage that owns them, and writes the one-page packet → stop at the stage-5 human
gate. You do not write the packet yourself; the PM returns it and you persist it.

Everything you need is there: the stage procedures and gates, model/effort routing
(§9 — Fable only for the PM gate, opus fallback), artifact contracts and the
`__ARGS` recipe (§10), recovery and resume (§7), and the failure-modes table (§11).
