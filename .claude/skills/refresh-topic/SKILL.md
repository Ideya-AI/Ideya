---
name: refresh-topic
description: Re-research, adversarially verify, and update ONE topic's content as it goes stale — propose a cited diff for human approval, then load it as a draft and publish. Use when topics_due / check_links flags a topic, or when something material changed a topic's shape.
---

# refresh-topic

Keep a published Topic accurate as the world moves. One run = one topic, end to end:
**detect → re-research & verify → propose a cited diff (the human gate) → load the
approved content as a draft → review against live → publish.** This is the upkeep
mirror of the authoring pipeline in `research/RESEARCH_PIPELINE.md`.

> **Iron rule — automation may OPEN a proposal; a human approves every content change.
> Never auto-publish.** (Decision D: AI drafts → human publishes.) Stages 1–2 can run
> unattended; stage 3 is a hard stop.

Run from the repo root in the project venv. `<slug>` is the topic slug; `<cat-slug>`
is a top-level category slug: `global-risk · ai · digital · climate-env · bio-health
· economy · governance · society · ethics`. The durable, diffable record for each
topic lives at `research/topics/<slug>.json`; the DB holds the live copy. Longer
detail (JSON shape, verdict shape, exact publish commands, snippets) is in
[`reference.md`](reference.md).

---

## 1 · Detect — assess what's stale
- **Queue / cadence.** `python manage.py topics_due` lists topics past their review
  cadence, most-overdue first. Cadence = `Topic.volatility` (fast 90 / medium 180 /
  slow 365 days) measured from `reviewed_at`, else `researched_at`; never-touched
  topics are always due. Useful flags: `--all` (every topic), `--status published`,
  `--json`. Confirm `<slug>` is actually due before spending a research run.
- **Links.** `python manage.py check_links --topic <slug>` flags dead / placeholder /
  redirected external links (Stat sources + Action URLs). Cheap; run it first.
- **Current content + provenance.** `python manage.py export_topic --slug <slug>
  --out research/topics/<slug>.json` re-syncs the file from the live DB (in case admin
  edits drifted from it). Read its `research_dossier` (sources, notes, prior
  `verdicts`) — that's the provenance you're re-verifying against.

## 2 · Research & verify — the heart of it
Use the **`deep-research`** skill to re-verify the topic element by element. The
research itself is grunt work — run it on other / cheaper models (the same
strategy as the authoring engine, `research/RESEARCH_PIPELINE.md` §11); reserve the strong
model for the adversarial verdicts and the crux. Honor the project's locked
editorial rules (full checklist in `reference.md`):
- **Every Stat** — find a current, authoritative source; record value, `source_url`,
  `source_published`, and today's `source_accessed`. Never trust first-pass
  recollection — run the recency pass on any time-sensitive figure. **Prefer durable
  facts;** isolate + date the genuinely perishable ones.
- **Questions / Positions / Crux** — are the load-bearing open questions still the live
  ones? Has a position obsolesced or a new one emerged? Keep each position a genuine
  **steelman in its own voice** (honest non-balance, never forced 50/50). Does the
  **Crux** still narrow to where disagreement *actually* sits?
- **Every Action** — link live, current, vetted, still mapped to the right position.
- **Source tiers** — primary/official + peer-reviewed > reputable journalism > advocacy.
- **Adversarially verify**, as the pipeline does: produce `verdicts`
  (`{pass, issues, fixes}`) per element. Note what **CHANGED vs the current JSON**:
  updated numbers, moved/dead links, new positions, questions now arguably resolved,
  a shifted crux.

## 3 · Propose — a cited diff (the gate, never a silent overwrite)
Produce a **changelog the reviewer can act on** — do not edit the DB yet. For each
change: **old → new**, with **source URL + date + a confidence note**, plus the
verdict that drove it. Group by section (Basics / Questions / Positions / Crux /
Actions / Overview). Call out anything you could not verify or that needs an editorial
call. **A human reads this and approves before anything is written.**

## 4 · Apply — load the approved content as a draft
On approval, write the merged content into `research/topics/<slug>.json` in the
loader's `{ draft, verdicts, plan_positions }` shape (schema in `reference.md`;
`nuclear-energy.gold.json` is the *content* bar but is in export shape — copy its
quality, not its structure; `nuclear-energy-pipeline.json` is a loadable-shape example).

Load it as a **staging draft** — a distinct slug so the **live topic stays published
and online** and the two can be compared side by side (the loader upserts by slug and
rebuilds sections, so loading onto the live slug would flip it to draft and take it
offline — don't):

```
python manage.py load_topic_draft \
  --file research/topics/<slug>.json \
  --slug <slug>-draft --title '<Title>' --category <cat-slug> --status draft
```

(Drafts render only for staff.) For a brand-new / unpublished topic, load straight
onto `<slug>` instead — there's no live version to protect.

## 5 · Review & publish — the human gate
1. **Compare** the staging draft against the live topic (preview both as staff).
2. **Publish** the approved content onto the canonical slug — re-run the loader with
   `--slug <slug> --status published` (atomic, upserts in place), then delete the
   `<slug>-draft` staging topic. Or, for light changes, edit + publish in the Django
   admin (`TopicAdmin` → status, or the **Publish selected topics** action).
3. **Set `Topic.reviewed_at = now()`** — the loader sets `researched_at` but not
   `reviewed_at`; setting it records human approval and resets the cadence clock.
   (Internal only — there is deliberately no reader-facing "last reviewed" badge.)
   Edit the field in admin (Research provenance fieldset) or via shell (snippet in
   `reference.md`).
4. **Verify links landed** — `python manage.py check_links --topic <slug>` must
   report **0 placeholder / 0 dead**. Non-optional, and it especially matters
   after a piecemeal admin apply: that is exactly how the 2026-07-03 nuclear
   refresh shipped fixed action URLs in the proposal but left `#` placeholders
   live. (The loader also errors on placeholder action URLs now.)
5. **Commit** `research/topics/<slug>.json` to git — the diff *is* the content history.

---

## Cadence & automation
- **Links — continuous.** Cheap, so check often: `check_links` in CI on every change,
  plus a weekly scheduled sweep across all topics (via the **`schedule`** skill / cron).
  A broken link opens a proposal; it does not auto-fix.
- **Full re-research — per topic, on the volatility interval**, surfaced by
  `topics_due` as a backstop so nothing rots silently. But the project is **durable by
  default** (`research/RESEARCH_PIPELINE.md` §8): the strongest trigger is **event-driven** — a
  position obsolesced, a key fact moved a lot — with the cadence as the safety net and
  the occasional light review for genuinely fast-moving topics (e.g. AI).
- **The gate never moves.** A scheduled run may detect staleness and OPEN a cited
  proposal (stages 1–3). It must stop there. **A human approves every content change.**
- **Presentation/display is out of this skill's scope** — `topics_due` measures
  content/link freshness only. Display concerns are handled directly by the human
  (prompted specific changes). Content findings the human wants verified seed a run
  via `args.findings` and route through this skill's stages 2–5 unchanged.
