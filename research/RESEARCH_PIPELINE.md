# The Ideya authoring engine — design rationale

**This doc is the "why": Part I is the current design and its reasoning; [Part II](#part-ii--decision-history-archive)
is the dated decision history. For the "how" — operating the engine (runbooks,
routing, contracts, failure modes) — `research/ENGINE.md` is the single source of
truth.** Last revised 2026-08-26.

The engine turns a catalog entry into a publish-ready **draft** topic plus a review
packet. It does not publish. Every guard below exists because something failed; the
failure is named next to the guard, because a rule whose reason has been forgotten is
the first one someone deletes.

---

## 1. What the engine is for

One topic in, one draft out, with human input approaching zero. The target is **one
human item per ten topics** — and a legitimate human item is a judgment call only the
editor can make (does this camp deserve its own card, is this framing right). *"Please
verify this fact"* is not a human item; it is the pipeline failing to close its own loop.

**Iron rule: automation drafts, a human publishes.** Enforced by a `PreToolUse` hook
(`.claude/hooks/pipeline-guard.sh`), not by prose — a rule stated in a skill is advice
the model may or may not be attending to on round 14 of a fix loop.

## 2. Artifacts and contracts

| Artifact | Written by | Contract |
|---|---|---|
| `research/catalog/topic-universe.json` | human / stage 0 | skeleton: title, slug, summary, why_now, categories, position names, `related_slugs` |
| `research/dossiers/<slug>.json` | stage 1 | substance record: draft, plan, verdicts, `claim_ledger`, shape notes |
| `research/topics/<slug>.json` | stage 2 | **the loader contract and a topic's source of truth** |
| `static/img/topics/<slug>.png` + `research/icons/<slug>.md` | stage 3 | hero art + the brief it was generated from |
| `research/reviews/<slug>/` | stage 4 | screenshots, cards, poster, `REVIEW.md` |

Each stage is independently re-runnable from the previous stage's artifact. Workflow
scripts have **no filesystem access** — the script coordinates agents, agents read and
write. That is why stage 2 bakes its 60KB dossier into a run script (`reference.md`).

## 3. Stage flow

```
0 catalog ─▶ 1 research ─▶ 2 distribute ─▶ 3 icon ─▶ 4 views ─▶ 5 HUMAN publishes
             plan                distill        brief      render
             parallel research   tier/reveal    generate   critique
             crux                fold           pick       fix
             CLAIM LEDGER        gate (2)       postproc
             gate (3)            fix loop
             fix loop
```

**Stage 1 · research (substance).** A plan agent locks scope, questions, positions and
the Phosphor glyph. Section agents research basics/questions/positions/actions in
parallel. A crux agent writes the editorial narrowing. Then verification, then the gate,
then a capped fix loop. Facts are settled here and nowhere else.

**Stage 2 · distribute (presentation).** Distils the compact layer, assigns tier (the
Go-deeper fold) and reveal (compact vs expanded), and reorders so the most
decision-relevant items lead. **Display order = array order**; `tier` only marks the
drop-off *within* that order, so moving an item across the fold means reordering.
Positions are the exception — they render by `prevalence_weight`. Facts are locked: the
patch whitelist rejects edits to value/unit/source_*/url/name/text.

**Stages 3–4 · icon and views.** A brief agent writes the art brief from
`ICONOGRAPHY.md`; candidates are generated, scored against the brief, post-processed,
and checked at 40px. Views render at 1440/390/320 (normal and expanded), three social
formats, and the poster — whose fit check is a **hard exit-code gate**.

**Stage 5 · human.** The only step the engine does not do.

## 4. The claim ledger — how facts are actually verified

Between crux and gate, an extraction agent enumerates every load-bearing claim as a
verbatim `quote` plus an atomic restatement. Verifiers then check them in parallel.

Four properties carry the weight:

1. **Verifiers are blind to the draft.** They see one claim and its cited URL, nothing
   else. Handing a judge the surrounding document primes it to rationalise what is
   already written; isolating the claim turns a re-read into a check.
2. **`kind: fact | inference`.** A fact is checked against a source. An **inference** —
   a causal, comparative or predictive conclusion — is checked against *who draws it*.
   Welding two sourced figures into a third claim neither source makes is the failure
   mode where every component verifies and the sentence joining them does not. Its
   remedy leads with **attribution to a named proponent**, which preserves the steelman
   while removing our invention.
3. **No source quote ⇒ `unverifiable`, in code.** Not at the model's discretion.
4. **Findings ride the existing fix loop.** Stage 1's `applyPatch` has no field
   whitelist, so `value`/`label`/`source_*` are repairable there. Failing claims are
   **re-verified every round**, so a fix that changed nothing cannot drop out of the
   verdict set and score clean.

*Why it exists:* only stats carry `source_*` fields — position and question prose carries
none, so it is unsourced by construction. Two wrong claims shipped through a 4/4 gate in
exactly that prose. On its first calibration the ledger flagged six claims nobody had
planted, most of them real errors in a topic that had passed the gate and a human review.

## 5. The verdict contract

Every critic returns `{critic, pass, blocking[], notes[], checks_run[]}`.

- **`pass` is derived, never self-reported**: no blocking findings *and* every named
  check ran. A critic that files blocking items cannot report a pass.
- **`checks_run` is machine-read.** A check with `ran: false` fails that critic and
  **re-runs it once**, WebFetch-first. *Why:* a critic once passed while noting in prose
  that it never performed its central check — and a caveat inside a verdict the human
  reads as 4/4 looks like coverage that never happened. The first fix was prompt text
  and was inert, because `pass` didn't read the field.
- **Every blocking finding carries a verbatim `quote`.** A defect a critic cannot quote
  is one it cannot show, and the quote gives the fixer an exact identifier instead of a
  paraphrase to guess at.
- **`notes` may never carry a factual matter.** An unverifiable load-bearing claim is
  *blocking*, with a remedy that works without the missing verification: cut, soften to
  what the source supports, or attribute in-voice.

**Critics are chosen on measured yield.** Across the corpus `fact-source` blocked 71% of
the time while the crux critic produced 0 blocking findings in 21 verdicts and
above-fold-selection 0 in 9; both were folded into the neighbouring critic that reads the
same material. Neutrality and steelman are kept despite low block rates — their downside
is asymmetric, since they guard the product's core promise.

## 6. The fix loop

Keep-best across rounds, tie-broken on blocking count, so a regressed round never ships
and never seeds the next one. Two refinements:

- **Rounds are asymmetric.** Externally-grounded findings (ledger, deterministic shape)
  keep three rounds; judgment findings get one. Unguided self-correction degrades output
  rather than improving it ([arXiv 2310.01798](https://arxiv.org/abs/2310.01798)), and a
  critic's round-2 opinion has no external anchor.
- **Dropped edits are fed forward.** `missed` (and stage 2's `rejected`) reach the next
  round's prompt. Previously they were logged and discarded, so an edit whose identifier
  matched nothing was indistinguishable from one that applied — the fixer could keep
  "fixing" while the draft never changed.

## 7. The deterministic layer

Anything decidable must never cost critic attention or reach the human.

| Check | Where | Catches |
|---|---|---|
| `lint_draft.py` | before the gate; `--fix` for safe rewrites | typography, entities, over-cap fields, wrapped lean chips, one-paragraph details, poster-band units, Words-to-Watch classes |
| `shapeCheck` | inside stage 1, **as gate input** | minimum counts, tiering, missing detail, near-cap prose |
| poster `?fit=1` | stage 4 | pixel overflow of a fixed 18×24in sheet |
| `pipeline-guard.sh` | `PreToolUse` | publishing; the live container's port |

Words to Watch is **scoped by voice**: editorialising adverbs and loaded attribution
verbs are exempt in a camp's own voice (a steelman is meant to sound committed), while
weasel phrasing is flagged everywhere — "studies show" instead of naming the study is a
weak steelman *and* a sourcing failure. The relative-time class is the "durable by
default" rule expressed mechanically, and it is the cheapest durability check available.

## 8. Editorial rules that shape the output

Mirrored by hand across the three workflow scripts (scripts cannot import), and guarded
by `topics/tests/test_workflow_mirrors.py` — that duplication has already drifted with
consequences.

- **Neutral by intention**; no house verdict, no section tilts.
- **Genuine steelman** per position, in its own voice, at its real prevalence.
- **Source quality is judged per claim, not globally.** Basics take official statistics
  and peer-reviewed *secondary* literature. Positions take **the camp's own texts and
  named proponents as the preferred source** — an advocacy org is a reliable primary
  source for its own position. *Why:* a global ladder that ranked advocacy last pushed
  position research toward opponents' characterisations, manufacturing the strawmen the
  steelman critic then had to catch.
- **Plain text, typographic quotes, US spelling** (except inside proper nouns).
- **Vary the form.** A corpus scan found 11 of 11 crux leads ending in "?" and position
  names collapsing into five suffixes, because one worked example was copied
  structurally. Within a topic that reads as rigor; across the atlas it reads as a form
  letter, and no per-topic gate can see it.

## 9. Model routing

Judgment on **opus**; web research on **sonnet**; never below sonnet. No Fable anywhere —
its weekly limit ran out mid-run and killed three gate critics, and an `args.models`
override was **not** enough to prevent it because the default won. Defaults are removed
from all three scripts and a test guards against reintroduction.

Web search is a **shared pool** (`CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`, default 200,
counted across every subagent; raised to 1500 here). WebFetch draws on a different pool
and keeps working when search is spent — which is why verification is WebFetch-first.

## 10. How the engine is measured

- **`research/engine-scorecard.local.md`** — per-run, five axes, and the distinction that
  matters: **caught** (engine fixed it — good), **escaped** (a later stage found it — a
  gate underperformed), **human** (reached the editor — the number to drive to zero).
- **`seed_defects.py`** — injects defects of known class into a lint-clean topic and
  scores a gate run. This is the only way to tell a *sensitive* judge from an *agreeable*
  one; "the bar is PARITY, not perfection" is editorially right but is also an unmeasured
  leniency lever. Blatant classes score near 100% and discriminate poorly; the subtle
  classes (`synthesis`, `over-hedge`, `due-weight`, `source-misattributed`) are the
  informative ones.
- **`tally_tokens.py`** → `research/token-ledger.local.md` — output tokens by model.
- **`lint_draft.py --all`** — corpus-wide mechanical quality; the count collapsed from
  8–33 per topic to 0 once the rules were encoded.

## 11. Known gaps

- **Repeated agent roles are still inline prompts.** Custom `agentType` did not resolve
  from a workflow script when probed; unresolved between "unsupported" and a
  directory-watcher caveat, and only a session restart distinguishes them. Consequence:
  the verifier's blindness is honour-system — the agent inherits `Read` and could open
  the dossier. A `tools: WebFetch` definition would make it structural.
- **`prevalence_weight` has no stated basis and no critic judges it**, while the rules
  push only toward inclusion (omitting a camp is a failure) with no counter-pressure —
  so the engine ratchets toward over-inclusion, and equal-sized cards assert a parity the
  weight only weakly corrects. Wikipedia's DUE is the prior art; a `prevalence_basis`
  routed through the ledger would make it checkable.
- **The refresh changelog is generated and discarded at load**, so corrections never
  reach the reader. `last_touched` exists on the model and no template renders it.
- **Corpus-level quality is unmeasured by the engine** — the mode-collapse scan was
  manual. Every gate reads one topic.
- **CSS defects** remain the standing list in each review packet; the pipeline is
  forbidden from touching templates.

---
# Part II · Decision history (archive)

> Kept because the *reasons* behind locked decisions are the expensive part to
> reconstruct. Sections are dated and some supersede others; where this half and
> Part I disagree, **Part I is authoritative**. Read this for why a decision was
> made, not for how the engine currently works.

## Original design thinking (2026-06-16)

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

## 12. Staged pipeline (2026-07) — supersedes the single-workflow shape of §9/§11

The pipeline is now split into independently re-runnable stages, each an automated
create-and-refine step with its own gate, orchestrated by the `author-topic` skill
(`.claude/skills/author-topic/`). §9's single `author_topic.js` is retired; §9/§11 stay
as the design record. The five stages:

1. **Research (substance)** — `research/workflows/research_topic.js`: plan (now also emits
   the Phosphor `icon`) → parallel section research → crux → the four-critic **substance
   gate** (neutrality / steelman / fact-source / crux) → keep-best fix loop. Judges
   substance on the full, un-compressed draft. Artifact: `research/dossiers/<slug>.json`.
2. **Distribute (presentation)** — `research/workflows/distribute_topic.js`: distill the
   compact layer → assign tier (the "Go deeper" fold), reveal (compact vs expanded), and
   item **order** → the three-critic **presentation gate** (compact-self-sufficiency,
   reading-level-fit, above-fold-selection) → presentation-only fix loop. Never changes a
   fact (the patch whitelist rejects value/source/url/name/text edits; a JS port of
   `Section._tier_lead_count` gives agents the real fold). Artifact: the loader contract
   `research/topics/<slug>.json`, with verdicts stage-tagged `substance`/`presentation`.
3. **Iconography** — skill-driven: brief → `generate_icons.py` (Nano Banana, per-slug
   candidates, `--edit` refine mode) → Claude picks → `postprocess_icon.py` normalizes to
   `static/img/topics/<slug>.png` (1035×690). Prompt provenance wired into
   `Topic.primary_image_prompt` via `load_topic_draft --image-brief`.
4. **Views** — `render_screens.py` (full-height desktop/mobile) + `render_social` +
   `render_poster` → `opus` critics read the images → content findings loop back through
   `distribute_topic.js --fix_only`; CSS defects are logged for the human, not auto-fixed.
   Artifacts under `research/reviews/<slug>/` incl. `REVIEW.md`.
5. **Human review & publish** — unchanged: preview the draft, publish, set `reviewed_at`,
   `check_links`, commit.

Gate placement is the point of the split: the **substance gate ends stage 1**, the
**presentation gate ends stage 2**, so presentation tuning (the common iteration) re-runs
without re-spending web research. The invariant holds throughout: **AI drafts → a human
publishes.**

**Content-policy limit:** dual-use topics (engineered pathogens / bioweapons-adjacent)
are blocked by the safety classifier — stage-1 research agents error out. Those topics are
not automatable through Claude agents; use path B (external research → the same
`research/topics/<slug>.json` contract) and resume at stage 3.

## 13. Review layer retired (2026-08-03)

A standing `review-topic` skill + `PIPELINE_TUNING_LOG.md` tuning loop ran 2026-08-01
→ 2026-08-03 (housing deep review, wildfires, UBI published-topic cycle, and a
post-fix pass). It found and closed real defects, and its 14 generalized lessons were
applied directly to the workflow files, the loader, and the render commands — where
they now live as code and prompts. With the pipelines hardened, the standing loop was
deliberately retired (decision 2026-08-03): topic pages are close enough that the
human prompts specific changes directly, and each run's own adversarial gates carry
the quality bar. Kept from that era: the `--expanded` render mode (stage 4), required
`--base-url` on render commands, and `refresh_topic.js`'s `args.findings` seed for
human-flagged items.
