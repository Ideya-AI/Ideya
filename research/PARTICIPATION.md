# Participation — reading what readers did

The operator manual for the participation record. The authoring engine
(`ENGINE.md`) makes topics; the refresh engine (`REFRESH.md`) keeps them
current; this one turns what readers do on the pages into something an editor
can read. It is deliberately small: one durable table, one command, and the
existing editor-gated text digest. How the data is *used* is still an open
decision (Jeff, 2026-09-01: "we'll decide how to utilize them later") — this
manual only makes it legible.

## 1. What is recorded

Every reader action on a topic page writes one row to
**`ParticipationEvent`** — append-only, never updated, nothing cascades:

| Action on the page | `kind` | `action` | `payload` |
|---|---|---|---|
| Upvote a question / position (and undo) | `vote` | `cast` / `retract` | — |
| Pick a pole on a question (change / undo) | `lean` | `cast` / `switch` / `retract` | `{value, label}` |
| Answer any prompt (edit / clear) | `response` | `save` / `clear` | `{selected: [labels], notes: {label: text}, text, rating, ranking}` |

Each row also carries **where** (`topic_slug`, `target_kind` = topic / section /
stat / question / position, `target_text`, `prompt_text`, `trigger`) and **who**
(`session_key`, `user` — null until accounts exist — `ip`, `user_agent`,
`created_at`). Item and prompt *text* is copied in, not referenced, so the
record survives reloads that rebuild sections and reseed prompts.

`trigger` says which entry point the prompt came from: `vote` (follow-up after
an upvote), `lean_a` / `lean_b` (after picking that pole), `respond` (the
Respond button under an expanded fact / question / position), `missing`
(Something missing? beside a section's Show less), blank (the Add-your-view
modal). Prompts themselves are templated in
`topics/management/commands/seed_example_prompts.py` and reseeded on every load.

The **current-state** tables (`Vote`, `QuestionLean`, `Response`) drive what the
page shows — counts, lean bars, a reader's saved answers. They are a cache of
the event log's latest state, with two caveats: a topic reload re-attaches
votes and leans by item text but drops `Response` rows, and reveal gates
(numbers at 5, bars at 10, reorder at 25) hide small samples on the page.
When the two disagree, the event log is the truth.

## 2. The digest

```
manage.py participation_report                          # every topic, all time → stdout
manage.py participation_report --topic <slug>
manage.py participation_report --since YYYY-MM-DD --out research/participation/<date>.md
```

Reads only the event log. Resolves each participant's **last** action per item
and prompt (a retract / clear drops it, a switch / re-save replaces it), then
prints, per topic and per item:

- upvote count and lean split;
- for every prompt that was answered: option tallies, rating average, rank
  order, and every note and free-text answer verbatim with its session stub
  and date.

Items are keyed by their text, so a digest reads the same before and after a
republish. `research/participation/` is gitignored: digests quote reader text
and must not ride into the public repo.

Free text at volume: `manage.py summarize_input [--prompt <id>] [--min-new N]`
drafts a Claude "what readers think" digest per prompt into `InputSummary`;
it shows on the page only after an editor approves it in admin. Occasional
background job, never in the request path.

Row-level browsing: admin → **Participation events** (read-only; filter by
kind / action / topic / trigger, search text / IP / session).

## 3. When to run it

- **Before a stage-5 review or a refresh of a topic**: `--topic <slug>`. What
  readers flagged (Disagree, Reword + note, Remove, Something missing) is
  reviewer input alongside the PM packet — it does not edit anything by
  itself. A refresh work order may cite it; the three refresh locks still
  apply.
- **Periodically (with the weekly `check_links` sweep once the site is up)**:
  `--since <last run> --out research/participation/<date>.md` for a
  site-wide read.
- **Ad hoc**: any time a number on a page looks off — the log has the history
  the page's cache does not.

## 4. What it is not (yet)

- No automation acts on responses: no reordering, no rewording, no removal.
  Every content change still goes through the human at stage 5 or the refresh
  proposal.
- No retention or anonymization policy: IPs and user agents are stored
  indefinitely. Decide before the public flip and record it here.
- No reader-facing view beyond the existing gated aggregates on the page.

## 5. Runbook — participation review (`/participation-review <slug>`)

The skill at `.claude/skills/participation-review/SKILL.md` launches this.
Usually run as part of a refresh (REFRESH.md step 1 points here) and before a
stage-5 review; runnable on its own. It produces one saved report per topic.
**It recommends; a human decides every line; the refresh engine makes any
edit.** The skill never touches topic JSON or the DB. Runs inline in the
invoking session — no subagents, no workflow.

### 1 · Digest
```
.venv/bin/python manage.py participation_report --topic <slug> \
  --out research/participation/<slug>.<today>.md
```
(`mkdir -p research/participation` if needed; it is gitignored.) If the digest
says **No participation recorded**, write the report's empty variant (template
below, parts 1–3 collapsed to one line each) and stop. Not a failed run.

### 2 · Read
- the digest;
- `research/topics/<slug>.json` — what the items readers touched actually say;
- `research/dossiers/<slug>*` — the sources behind them;
- any `research/refresh/<slug>.*` from earlier runs, so the proposal does not
  re-raise what a refresh already handled.

### 3 · What readers did (report part 1)
Narrate, do not dump: volume and window; where attention clustered; lean
splits against the editorial lean; what was flagged (Disagree / Reword /
Remove / Something missing) and the reasons behind it. Say `n` everywhere —
three readers is three readers, not "readers think". Paraphrase; cite as
`(session abc123, 2026-09-14)`. No verbatim reader text in this file — it is
committed and the repo is public; the verbatim digest is the gitignored file.

### 4 · Research and thoughts (report part 2)
Light — the fact-checking an ordinary question gets, more or less as the claim
needs. Only claims that, if true, would change the topic: a disputed figure, a
"missing" fact / question / position, a reword that asserts something. Check
each against the dossier and the cited source first; WebFetch a primary source
only when the claim turns on one. Verdict per claim: **holds / does not hold /
cannot tell**, with the evidence in one or two lines. Leans, agree/disagree
verdicts and importance votes are signal, not claims — weigh them, do not
research them. Then the noise: single-session pile-ons, off-topic, samples
under the reveal gates, duplicates of earlier refresh findings.

### 5 · Proposal (report part 3)
Per item touched: **incorporate / decline / defer**, each with a reason.
Incorporate lines are written in the editor-findings shape that
`refresh_topic.js` takes as `args.findings` (see
`research/refresh/nuclear-energy.findings.2026-09-01.md`): what the topic says,
what readers said, what the evidence says, source. The refresh's locks still
apply — a reader "Reword" is only proposed when a claim or lint reason backs
it, never as re-authoring. Reorder asks: positions render by
`prevalence_weight` (reader votes cannot move them — say so if asked);
questions / stats order is array order and a refresh may reorder with a
reason. "Nothing to change" is a valid proposal.

### 6 · Save and stop
`research/refresh/<slug>.PARTICIPATION.<today>.md`, from the template. Print
the path. The human ticks the decisions; the refresh reads the proposal. Do
not edit the topic; do not open a refresh.

### Report template
```
# <slug> — participation review <today>

Window: <first> → <last> · <n> events · <k> participants · digest: research/participation/<slug>.<today>.md
Previous participation review: <path or none> · last refresh: <date or none>

## 1 · What readers did
<narrative, paraphrased, n everywhere, cited by session stub + date>

## 2 · Research and thoughts
### <claim 1> — holds | does not hold | cannot tell
Topic says: … · Readers said (n=…): … · Evidence: … (source)
### Noise
…

## 3 · Proposal for the next refresh
(Feed this section to refresh_topic.js as args.findings.)
### P1 · <section> · <item> — incorporate | decline | defer
Topic says: … · Readers: … · Evidence: … · Recommendation: … · Source: …
### P2 · …
Nothing to change: <yes/no + one line>

## Decisions (human)
- [ ] P1 — accept / reject / edit: …
```
