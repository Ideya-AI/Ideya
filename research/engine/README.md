# The Ideya authoring engine (v3) — operator's guide

One command turns a topic file into a loaded draft topic, its renders, cards,
poster, icon, and a one-page review packet. A human publishes; nothing else does.

```
.venv/bin/python research/engine/engine.py author <slug>          # run (or resume) the whole thing
.venv/bin/python research/engine/engine.py status <slug>          # the 17-step table
.venv/bin/python research/engine/engine.py step   <slug> <step>   # run exactly one step now
.venv/bin/python research/engine/engine.py reset  <slug> <step>   # forget a step and everything after it
```

For what each step does and why, in run order, read `FLOW.md` first.

Always `.venv/bin/python`, always from the repo root. The topic must have a file
at `research/topics/<slug>.json` carrying six fields: slug, title, status, a
one-line `scope`, its categories and its related topics. Nothing else is required
up front — the topic name is the whole input, and the driver starts the dev server
itself if 8641 is not answering.

---

## 1. The three files

| File | What it is |
|---|---|
| `engine.py` | The driver. A 17-step state machine; each step is a method that reads what the previous steps persisted, does one thing, and records itself in `research/runs/<slug>/state.json`. |
| `harness.py` | How agents run. Serves every `agent()` call by launching headless Claude Code through the Claude Agent SDK on the user's subscription. Journals each call, sleeps through usage limits, enforces the tool policy, limits concurrency. |
| `bridge.mjs` | A 50-line Node shim. Runs the two stage scripts (`research/workflows/research_topic.js`, `distribute_topic.js`) **unchanged**, giving them the `agent / parallel / pipeline / phase / log / args` API they were written against, over a JSON-lines pipe to the harness. |

The stage scripts, the lint, the loader, the render commands, `fit_check.py`, the
agent definitions in `.claude/agents/`, the design docs and the defect register are
all reused as they are. The engine is the joints between them.

## 2. Where everything lives

```
research/runs/<slug>/
  state.json              step statuses, notes, loader warnings, link summary, icon winner
  engine.log              every log line, timestamped (the thing to read when something fails)
  <step>/                 one directory per step that ran agents
    args.json             the exact args the stage script received
    journal/<hash>.json   one file per agent call: label, opts, result, usage, seconds
    usage.json            totals for that script run (only for bridge-run steps)
  fit0.json …             fit_check findings, when the poster overflowed
  pm.json                 the PM's routing + packet, verbatim
  devserver.log           if the driver started the server

research/runs/<slug>/record.json   the engine's own record: plan, stage-1 draft, verdicts, claim ledger,
                                  prescriptions. Process, never product — nothing here is loaded or shipped.
research/topics/<slug>.json        stage 2's output (presentation) — what the loader loads
research/reviews/<slug>/           renders, sections/, cards, poster, views.json, REVIEW.md, tokens.md
research/icons/<slug>.md           the icon brief (+ ## Selection)
research/icons/candidates/<slug>/  the generated candidates
static/img/topics/<slug>.png       the icon (1035×690) · static/img/social/<slug>.png the served OG card
```

## 3. The seventeen steps

Each step is idempotent: run it twice and the second run does nothing (or replays
agent calls from the journal for free). "Skips if" is the artifact guard.

| Step | Does | Reads | Writes | Skips if |
|---|---|---|---|---|
| `s1.plan` | stage 1 phase 1: scope, questions, positions, icon | topic file (slug, title, scope, categories) | record `plan` | — |
| `s1.research` | phase 2: parallel section research + crux | record `plan` | record `draft` | — |
| `s1.verify` | phase 3: claim ledger extraction + blind per-claim verification | `plan`, `draft` | record `claim_ledger` | — |
| `s1.gate` | phase 4: three critics + shape + ledger, scoped fix loop, prescriptions, closing ledger (re-extracted after its repair) | `plan`, `draft`, `claim_ledger` | record `verdicts`, fixed `draft`, `gate_status` | — |
| `s2.distribute` | distill → order/tier/reveal → editorial critics + deterministic checks + fidelity, scoped fix loop | record | `research/topics/<slug>.json` (content only) | — |
| `s2.lint` | `lint_draft.py --fix`; remaining judgment findings go through `fix_only` (≤2 passes) | topic JSON | topic JSON | lint already 0 |
| `s2.load` | `manage.py load_topic_draft … --status draft`; records loader warnings | topic JSON | the DB | — (cheap, always runs) |
| `s2.fit` | `fit_check.py`: measures the poster; if over, `fix_only` with sized trims, re-lint, re-load (≤2 loops) | loaded topic | topic JSON, DB | poster already fits |
| `s3.brief` | icon-briefer agent returns the brief; driver writes it | ICONOGRAPHY.md, categories.md, exemplar briefs | `research/icons/<slug>.md` | brief with `## Generation prompt` exists |
| `s3.generate` | `generate_icons.py --n 4` (Gemini; needs `GEMINI_API_KEY` in `.env`) | brief | `candidates/<slug>/*.jpg` | ≥4 candidates exist |
| `s3.select` | vision agent reads candidates + neighbor winners, picks one; driver appends `## Selection` | candidates, neighbors | brief | `## Selection` exists |
| `s3.postprocess` | `postprocess_icon.py` → 1035×690 + 40px thumb | winner | `static/img/topics/<slug>.png` | icon exists |
| `s4.render` | screens (3 widths, normal + expanded) **with per-section captures**, og card to `static/img/social/`, sq/pt + poster to the review dir | DB | `research/reviews/<slug>/…` | — (always re-renders) |
| `s4.links` | `manage.py check_links --topic`; fails the run on a dead link | DB | `state.links` | — |
| `s4.views` | three design-conformance critics (desktop, mobile, cards+icon) read the **section images**, not full pages | `sections/`, cards | `views.json` | — |
| `s5.pm` | the driver runs the seven deterministic CHECKS itself, hands them plus the run facts to the `topic-pm` agent (Fable), which reads the sections and returns routing + the packet; routes are closed by rule (§5) and the PM reads once more | everything above | `REVIEW.md`, `pm.json` | — |
| `s5.packet` | token record from the journals | `*/journal/*.json` | `tokens.md` | — |

Then it prints the publish command. **Stage 5 — reading the packet and running
`publish_topic` — is yours.**

## 4. Resume, limits, failures

- **Resume** is `author <slug>` again. Done steps are skipped; a `running` or `failed`
  step re-runs; inside it, every agent call whose prompt is unchanged replays from
  the journal at zero cost. So a run that died in the middle of stage 1's gate
  re-runs only the agents that had not returned.
- **Usage limits.** When a call fails with "session limit · resets 7pm", the harness
  parses the time, sleeps until it plus 90 seconds, and retries the same call. The
  wait does not count against the six attempts. Expect one per run; a run may pause
  for hours and needs nothing from you. The log line is
  `[label] usage limit — sleeping N min until the reset`.
- **Other agent failures** (CLI died, malformed output) retry up to six times with
  backoff, then the call returns `null` — the same contract the stage scripts were
  written against — and the script's own guards take it from there.
- **A step fails** when it raises: dead link, poster still over after two measured
  trims, lint still failing after two passes, an agent that returned nothing six
  times. `status` shows `failed` with the cause; `engine.log` has the detail. Fix the
  cause, then `author` again (it re-runs the failed step) or `step <slug> <step>`.
- **Redo a step deliberately** (you changed a prompt, a template, a rule):
  `reset <slug> <step>` forgets it and everything after, then `author`. Journals are
  kept, so anything whose inputs did not change is still free.
- **Concurrency** is `ENGINE_CONCURRENCY` (default 4). The subscription's rate limits
  set the real ceiling; raising this mostly moves the limit earlier.

## 5. Rules the engine decides by (so you don't have to)

- Facts are locked after stage 1; stage 2 changes presentation only (its patch
  applier rejects fact fields).
- A critic on round 2+ sees only its own open findings and the fields the fixer
  changed; a new finding on unchanged text is demoted to a note, in code.
- Judgment findings still open when a loop ends go to the packet as residuals, not
  back to a stage. Prescriptions that quote both target and replacement are applied
  verbatim (unless elided or sentence-mismatched).
- PM routes: stage 1 (a fact with no ledger result) → blind claim-verifier, verdict
  appended to the ledger; if not supported, one `fix_only` softens it. `register` →
  a row appended to `research/reviews/UI_DEFECTS.md`. Stage 2 → one `fix_only`.
  Stages 3/4 → left for you, named in the log. Then the PM reads once more, and
  whatever it routes the second time is yours.
- The pipeline never edits templates or CSS; every code defect it sees becomes a
  register row and a packet line.

## 6. Tool policy (who may do what)

| agentType (from the scripts) | Tools | System prompt |
|---|---|---|
| none (critics, fixers, distill, planner's helpers) | none | engine default |
| `general-purpose` (stage-1 researchers, fixers with web) | WebSearch, WebFetch | engine default |
| `claim-verifier` | WebSearch, WebFetch | `.claude/agents/claim-verifier.md` — cannot see the draft, by construction |
| `camp-scout` | WebSearch, WebFetch | `.claude/agents/camp-scout.md` |
| `topic-critic` (neutrality, steelman) | none | `.claude/agents/topic-critic.md` |
| `icon-briefer`, `view-critic`, `topic-pm` | Read | their definitions |

Agent definitions are passed as **system prompts**, not resolved by name: in print
mode `--agent <name>` silently drops the JSON schema. MCP servers are off. Models:
whatever the script passes (`sonnet` web work, `opus` judgment and fixes, `fable`
for the PM with an `opus` fallback); efforts likewise.

## 7. Walking through a topic by hand

The same run, one step at a time, so you can look at each artifact as it lands:

```
E=".venv/bin/python research/engine/engine.py"
$E step antimicrobial-resistance s1.plan        # ~1 min   → look at record.plan (positions, questions, icon hint)
$E step antimicrobial-resistance s1.research    # ~10 min  → record.draft (every section, in voice)
$E step antimicrobial-resistance s1.verify      # ~15 min  → record.claim_ledger (claims + blind verdicts)
$E step antimicrobial-resistance s1.gate        # ~60 min  → record.verdicts, gate_status; watch "Re-gate rN: scoped to K changed field(s)"
$E step antimicrobial-resistance s2.distribute  # ~15 min  → research/topics/<slug>.json, fold in the log
$E step antimicrobial-resistance s2.lint
$E step antimicrobial-resistance s2.load        # then open http://127.0.0.1:8641/<slug>/
$E step antimicrobial-resistance s2.fit         # prints the per-element poster table
$E step antimicrobial-resistance s3.brief       # read research/icons/<slug>.md
$E step antimicrobial-resistance s3.generate    # look at candidates/<slug>/
$E step antimicrobial-resistance s3.select      # ## Selection appended
$E step antimicrobial-resistance s3.postprocess # static/img/topics/<slug>.png
$E step antimicrobial-resistance s4.render      # research/reviews/<slug>/ + sections/
$E step antimicrobial-resistance s4.links
$E step antimicrobial-resistance s4.views       # views.json
$E step antimicrobial-resistance s5.pm          # REVIEW.md; watch for "routed" lines
$E step antimicrobial-resistance s5.packet      # tokens.md
```

`status <slug>` between steps shows what is done. To run a stage script outside the
driver (for example against a scratch record), the harness is a CLI too:

```
.venv/bin/python research/engine/harness.py research/workflows/distribute_topic.js <args.json> <run_dir>
```

with `args.json` shaped as `engine.py`'s `s2_args()` builds it (or
`research/workflows/bake.py`'s builders — the same shapes).

## 8. Reading a failure

1. `status <slug>` — which step, and the one-line cause.
2. `research/runs/<slug>/engine.log` — the harness lines above it: attempts,
   limit waits, `node:` stderr from the bridge, script `log()` lines.
3. The step's `journal/` — each agent's result; a `null` result means six attempts
   failed and the reason is in the log just above.
4. `research/ENGINE.md` §11 — the failure-modes table for the stage scripts
   themselves (schemas too large, content-policy refusals, capture caps, and so on).

Print-mode facts that will save you an hour: `--bare` drops the login; a 200KB
prompt hangs on CLI stdin but is fine through the SDK; an image `Read` needs the
SDK's message buffer raised (the harness sets 64MB); a usage limit can arrive as a
`ResultError` exception rather than an error result (the harness handles both).

## 9. What "done" means

`DONE:` in the log, `REVIEW.md` and `tokens.md` in the review folder, the topic
loaded as `draft`, and `status` all green. Then:

```
manage.py publish_topic --slug <slug> --dry-run          # say what would change
manage.py publish_topic --slug <slug> --confirm          # private -> public
manage.py publish_topic --slug <slug> --off --confirm    # public -> private
```

The engine never runs those. A hook blocks it from trying.
