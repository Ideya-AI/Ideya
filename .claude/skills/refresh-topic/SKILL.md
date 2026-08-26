---
name: refresh-topic
description: Re-research, adversarially verify, and update ONE topic's content as it goes stale — propose a cited diff for human approval, then load it as a draft and publish. Use when topics_due / check_links flags a topic, or when something material changed a topic's shape.
disable-model-invocation: true
argument-hint: "[slug]"
---

# refresh-topic

> **Iron rule — automation may OPEN a proposal; a human approves every content
> change. Never auto-publish.**

This skill is a launcher. The procedure lives in **`research/ENGINE.md`** — the
engine's single source of truth. Read it and follow **§6 Runbook B — refresh a
topic** for `<slug>` ($ARGUMENTS): detect → research & verify (`refresh_topic.js`)
→ propose a cited diff (the human gate) → staged load → review & publish → push to
live. The light path for barely-stale topics is in the same runbook.

Contracts, editorial rules, the `__ARGS` recipe, and failure modes: ENGINE.md
§10–§11. Cadence and automation boundaries: end of §6.
