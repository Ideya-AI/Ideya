# Topic Research Pipeline — initial design thinking (2026-06-16)

Draft thinking for tomorrow. Decision D stands: **AI drafts → human publishes.**
The pipeline turns a *catalog entry* (skeleton from the topic universe) into a
fully-authored, neutral, well-sourced **draft** Topic that meets the design
system's quality bar, ready for review + publish in admin.

## 1. The output contract (what "done" means)
A draft Topic populated across the fixed spine, matching the existing data model:
- **Overview** — summary, scope_covered, scope_excluded, why_now, primary + secondary categories, related topics, icon.
- **Basics** — 6–8 Stats (label, value, viz kind, note, source).
- **Questions** — 3–6 (text, empirical|value, why-contested, optional lean).
- **Positions** — 3–5 (name, colour, one-line steelman, 3–5-sentence description *in the side's own voice*, notable proponents, representative example).
- **Crux** — the synthesis: where the real disagreement actually sits (lead + subtitle + if-empirical / if-values).
- **Actions** — 6–12 (learn / donate / policy / volunteer / local / submit-view), optionally aligned to a position.
- Plus a **research dossier** (sources, key facts, roads-not-taken) attached for the reviewer.

Input = a universe catalog entry (title, summary, why_now, position names, category, related, icon). The pipeline *deepens* the skeleton; it doesn't start cold.

## 2. The quality bar (this is the hard part, and the whole point)
Published content carries the product's promise, so three non-negotiables:
1. **Neutral by intention** — no house position; no section tilts.
2. **Genuine steelman per position** — each side's strongest case, in its own voice, such that a real proponent would endorse it. Not strawmen, not bias-balance theatre.
3. **Accurate + sourced** — facts verified, claims sourced. (Even though citations render *tertiary* in the UI per the 2026-06-13 call, the research must be sound and the reviewer needs sources.)
And the **Crux** must be genuinely insightful — narrowing to where disagreement *actually* sits — not "both sides have a point." This is the differentiator vs. Wikipedia.

## 3. Approaches considered
- **A · Monolithic deep-dive** (one agent writes the whole topic): coherent voice, but uneven section depth, weak structure enforcement, single bias point, hard to fact-check. Not recommended alone.
- **B · Section-decomposed fan-out + adversarial verification** (recommended): mirrors the universe workflow, but per-topic, deeper, with a real verification layer.
- **C · Hybrid, calibrated**: more human checkpoints at first; tune against the hand-built Nuclear Energy gold standard; automate as quality stabilizes.

## 4. Recommended shape (B, orchestrated as a per-topic workflow)
1. **Scope & spine plan** — one agent fixes framing (scope in/out, why_now) and refines the contested space into the final Questions + named Positions. Everyone else builds against this plan.
2. **Parallel section research** (fan-out, web-enabled, schema-valid output): Basics (stats + sources) · Questions (why-contested, empirical/value) · Positions (each: steelman + description + proponents + representative example).
3. **Crux synthesis** — runs after positions/questions; the editorial narrowing.
4. **Adversarial quality gate** (the trust layer — parallel critics): neutrality auditor (any tilt? sides equally charitable/rigorous?) · steelman auditor (would each proponent endorse their section?) · fact/source checker (stats accurate + sourced; flag unsupported claims) · crux critic (insightful + fair, not false balance?). Failures route back for a targeted redo (loop-until-passes, capped).
5. **Assembly** — normalize to the data-model schema (Sections + typed children + reveal levels) → structured JSON → an idempotent management command upserts it as a **draft** Topic (by slug) and stores the dossier.
6. **Human review** in admin — edit, then publish (the existing gate).

## 5. Calibration / eval
**Nuclear Energy is the gold standard** (hand-built to spec). Regenerate it through the pipeline and compare; tune prompts until the pipeline matches the hand-built quality. An objective target before scaling.

## 6. Practical organization
- **On-demand / small batches, not bulk** — human review is the bottleneck; don't pile up ~130 drafts. Author in priority order (Spotlight-worthy / high-importance first).
- **Strict shared schema + voice rules** in every agent prompt (sentence case, steelman, neutral, the design content rules) → drafts load cleanly and read consistently.
- **Idempotent loader** (upsert by slug) so a topic can be re-run / improved.
- **Sources** — Stats already have source fields; either extend Positions/Questions later, or keep a per-topic dossier the reviewer uses (citations stay tertiary in the UI).
- **Cost** — a multi-agent pipeline × ~130 topics is significant; another reason for prioritized, on-demand authoring.

## 7. Open decisions for tomorrow
1. Approach **B** vs. something lighter — how much adversarial verification (cost vs. trust)? *(Lean: the full critic pass; the neutrality promise is the product.)*
2. Authoring **order / batch size** — which topics first.
3. Where **sources** live — dossier vs. model fields vs. both.
4. How deep is **human review** per topic (light approve vs. heavy edit) — sets how polished the draft must be.
5. **Calibrate on Nuclear Energy** first? *(Lean: yes.)*
6. Reuse the **Workflow** tool for orchestration (as with the universe)? *(Lean: yes — same pattern, deeper.)*

## 8. Resolved in design discussion (2026-06-17)
- **Viewpoints — honest non-balance.** Include every genuine position, each steelmanned; never force a 50/50. Where views are asymmetric, the honesty is carried by Basics (shared facts), each position's real prevalence, and the Crux — the page never states a house verdict. No fringe-exclusion-by-omission, no false balance. (Neutrality + steelman critics enforce.)
- **Per-section research requirements** — Overview: framing only. Basics: 6–8 decision-relevant facts that span positions accept, each sourced + dated (most source-heavy). Questions: load-bearing open questions, empirical|value tagged. Positions: steelman in own voice + proponents + representative. Crux: synthesis, no new facts. Actions: real/current/vetted, mapped to positions.
- **Depth = distill down.** Research deep, then summarize upward: condensed = headline + one line (poster/social/mobile-tight); normal = explanatory body (desktop default); deep = caveats, nuance, representative, proponents, sources, go-further. Same 6-section skeleton at every depth; more room adds evidence + nuance, never new sections. Most decision-relevant first; detail sinks deeper.
- **Question ordering** — default by centrality (load-bearing-ness), empirical-before-value tiebreak; importance votes reorder live (already built).
- **Position ordering — DECIDED 2026-06-17:** seed default order by prevalence/influence (mainstream leads; don't open with fringe), then importance votes reorder live, gated at low volume. This makes Positions vote-orderable like Questions — a change from the current "importance reorders Questions but never Positions" rule. Neither prevalence nor votes claims correctness (both descriptive), so neutrality holds. Left↔right spectrum kept as metadata (can drive color/grouping or an optional "view by spectrum" later), NOT the default order — it conflicts with a prevalence list.
- **Freshness — durable by default ("more Buffett than day-trader").** The atlas is a deliberate *lagging* source: it maps enduring debates and long-term change, not the day-to-day. Ideas (positions/questions/crux) are stable and shouldn't chase a news cadence. So:
  1. **Prefer durable facts.** In Basics, favor structural / long-run figures that age well; when a genuinely perishable fact is needed, isolate + date it as the exception — so pages don't rot. Minimize perishable surface area; lean on durable framing.
  2. **Accuracy at authoring still matters.** Run the recency pass when a topic is authored/refreshed to get genuinely-current data (fixes the LLM "good-but-slightly-stale baked in" failure — never trust first-pass recollection); record source publication date + access date.
  3. **Refresh is event-driven, not periodic.** Revisit a topic only when something MATERIALLY changes its shape (a position obsolesced, a key fact moved a lot) — plus an occasional light review for the few truly fast-moving topics (e.g., AI). No refresh treadmill.
  4. **Display:** "as of {date}" on the dated facts + a light "Updated {month}" on the page.
  - Small data-model adds: source publication + access dates on Stats; researched_at / reviewed_at on Topic.
- **Sources** — tiered (primary/official + peer-reviewed > reputable journalism/research > advocacy/opinion); Basics prefers cross-accepted sources; Positions attributed to real proponents/works (the proponent is the idea's source); everything in a reviewer dossier; UI stays tertiary.

## 9. The research session — concrete spec (design locked 2026-06-17)
One session = one topic, end to end. **Input:** a universe catalog entry. **Output:** a structured `TopicDraft` mapping 1:1 to the data model, loaded as a DRAFT topic + a reviewer dossier. Orchestrated as a per-topic Workflow.

**Stage 0 · Scope & spine plan** (1 agent). Lock durable framing (definition, scope in/out, why_now). Finalize the contested space: the load-bearing Questions (empirical|value, ordered by centrality) and the genuine named Positions (refine the catalog's sketch). Assign each Position a **prevalence/influence weight** (default-order seed) and a **spectrum position** (metadata). Everyone builds against this plan.

**Stage 1 · Parallel section research** (fan-out, web-enabled, recency-aware):
- *Basics* — 6–8 stats; **prefer durable facts**, cross-accepted across positions; each with value, viz kind, note, source (title/url/publication-date) + accessed-date; run the recency pass on any time-sensitive figure (latest as of today, never first-pass) and mark it perishable → "as of" display. Layer: headline number → note → source/context.
- *Questions* — per the plan: text, kind, why-contested (normal), optional lean (deep, gated by sample).
- *Positions* — per position (one agent per position or small groups, for depth): one-line steelman (condensed) → 3–5-sentence description in its own voice (normal) → proponents + representative example (deep). Honest non-balance: each steelmanned charitably.
- *Actions* — 6–12 real/current/vetted options across types, mapped to positions where possible, URLs recency-checked.

**Stage 2 · Crux synthesis** (1 agent, after Stage 1). From positions+questions+basics, write the narrowing — where disagreement *actually* sits + the if-empirical/if-values split. No new facts. Honest non-balance lives here: name where evidence points without a house verdict.

**Stage 3 · Adversarial quality gate** (parallel critics → pass/fail + targeted fixes; failures loop back, capped): neutrality auditor (tilt? sides equally charitable/rigorous?) · steelman auditor (would each proponent endorse their section?) · fact/source checker (accurate, sourced, dated, recency-pass done?) · crux critic (insightful + fair, not false balance?).

**Stage 4 · Assemble & load.** Normalize → Sections + typed children (Stat/Question/Position/Crux/Action) with reveal levels (condensed/normal/deep), position color assignment, default ordering (questions by centrality; positions by prevalence weight), related links. Attach the dossier. Idempotent management command upserts a DRAFT Topic by slug + sets researched_at.

**Stage 5 · Human review & publish** in admin (existing gate). **Calibrate against hand-built Nuclear Energy first** — regenerate it, compare to the gold standard, tune prompts before scaling.

## 10. Data-model changes this implies (for implementation)
- **Position:** add `prevalence_weight` (default-order seed) + `spectrum_position` (metadata); **make Positions reorder by importance votes** (seeded by prevalence at low volume) — the detail.html positions section + view ordering change from curated-only to vote-ordered, like Questions.
- **Stat:** add `source_published_date` + `source_accessed_date` (source_url/source_label already exist).
- **Topic:** add `researched_at` / `reviewed_at`; surface a light "Updated {month}".
- **Dossier:** a per-topic store (JSON field or related model) for sources + research notes, visible to the reviewer, not (prominently) to readers.

## 11. Implementation status + model strategy (2026-07-03)
The pipeline is built as a runnable Workflow: `research/workflows/author_topic.js`
(Plan → parallel Research → Crux → Distill → adversarial Gate → capped Fix →
assemble to the `load_topic_draft` shape). First Nuclear Energy calibration
recovered all four gold positions and the gate caught a real sourcing defect;
tuning added the Distill stage + tighter caps to close the "researches deep,
under-distills" gap against the hand-built gold.

**Model strategy — the actual research runs on other / cheaper models; the
premium model is reserved for judgment.** Two supported paths:
- **A · In-workflow.** `author_topic.js` routes each stage to a model via
  `args.models = { research, distill, critique, fix }`. Research defaults to a
  cheaper tier so a run never burns the premium model on web grunt; Crux and the
  critics take the `critique` model so the strong model is spent only where
  editorial judgment matters. Pass `args.today` so `source_accessed` is real.
- **B · External research, same contract.** Because the loader consumes a plain
  `{ draft, verdicts, plan_positions }` JSON file (`reference.md` schema), any
  external model/pipeline can produce a topic draft and load it — the workflow is
  one producer of that contract, not the only one. The adversarial gate and the
  human-publish gate apply regardless of which model did the research.

The invariant across both: **AI drafts → a human publishes.** The gate may fail a
draft and open fixes; it never auto-publishes.
