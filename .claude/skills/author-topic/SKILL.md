---
name: author-topic
description: Run the whole Ideya authoring pipeline for one topic, research through audit, in a session dedicated to that topic. Argument: a topic slug or title, optionally followed by --from <stage>.
argument-hint: <slug or title> [--from research|editorial|icons|views|audit]
---

You orchestrate five stages for one topic. Each stage runs as its own subagent with
a fresh context; you do no research, editing or judging yourself. Keep your own
messages short: one line when a stage starts, a few lines when it ends.

Principles the stages carry: intellectual honesty and minimalism. Invariants you
enforce: never publish (the human does), never edit templates or CSS (recommend in
chat), never touch port 8642.

## 1. Resolve and inspect

Parse `$ARGUMENTS`: everything before `--from` is the topic; `--from <stage>` forces
a redo from that stage onward. Resolve the topic to a slug:

```
.venv/bin/python -c "import json,sys,pathlib;a=' '.join(sys.argv[1:]).strip().lower();ds=sorted(p for p in pathlib.Path('research/topics').iterdir() if (p/'topic.json').exists());ex=[p.name for p in ds if p.name==a or json.loads((p/'topic.json').read_text()).get('title','').lower()==a];print(ex[0] if ex else 'AMBIGUOUS '+' '.join(p.name for p in ds if a in p.name or a in json.loads((p/'topic.json').read_text()).get('title','').lower()))" <topic words>
```

If AMBIGUOUS, show the candidates and stop. Let `T=research/topics/<slug>`.

Work out which stages are already done from the files:

| stage | done when |
|---|---|
| research | `T/research.md` contains `## Sources` |
| editorial | `T/topic.json` has `content` with overview, basics, questions, positions, crux, actions, and `authored_at` is set |
| icons | `static/img/topics/<slug>.png` exists and `T/topic.json` has `icon` |
| views | `T/renders/views.md` exists and is newer than `T/topic.json` and the art |
| audit | never skipped, unless status is already `ready` and `T/audit.md` is newer than everything above, in which case say so and stop |

`--from <stage>` marks that stage and all later ones not done, except icons: the art
does not depend on the copy, so icons is redone only by `--from icons` or `--from
research` (a fresh research can change what the topic is about). When forcing
research, move `T/research.md` to `T/run/research.prev.md` first; when forcing
editorial, delete `T/run/edit/*.json` first. Otherwise a stage picks up where it
stopped.

Print one block: the slug, title, and for each stage `skip` or `run`.

## 2. Arm the run

```
mkdir -p T/run && touch T/run/active
```

The usage guard (a PreToolUse hook) only enforces while this marker exists. Remove
it on every exit, including failure, with the final log line in the same command
(an `rm` asks the user for approval; this does not, and the guard lets it through):

```
.venv/bin/python -c "import json,pathlib,datetime;open('T/run/log.jsonl','a').write(json.dumps({'t':datetime.datetime.now().astimezone().isoformat(timespec='seconds'),'stage':'run','event':'exit','result':'<verdict or reason>'})+'\n');pathlib.Path('T/run/active').unlink(missing_ok=True)"
```

The token report defaults to the newest transcript for this project, which is this
session, so call it without `--session`. (The scratchpad path is not the session id
when a session has been resumed.)

## 3. Run the stages

For each stage to run, in order research, editorial, icons, views, audit:

1. Append `{"t": "<ISO now>", "stage": "<stage>", "event": "start"}` to `T/run/log.jsonl`.
   Stage names in the log: `research`, `editorial`, `icons`, `views`, `audit` for
   the first pass; fix cycle n logs `editorial-fix-<n>` / `icons-fix-<n>`, then
   `views-<n>` and `audit-<n+1>`.
2. Spawn with the Agent tool: `subagent_type` and `description` per the table,
   prompt `slug: <slug>`. Wait for it.

| stage | subagent_type | description |
|---|---|---|
| research | `research-topic` | `research-topic <slug>` |
| editorial | `edit-topic` | `edit-topic <slug>` |
| icons | `create-topic-icons` | `create-topic-icons <slug>` |
| views | `create-topic-views` | `create-topic-views <slug>` |
| audit | `audit-topic` | `audit-topic <slug>` |

3. Read its first line. `RESULT: done` continues. `RESULT: blocked` (usage guard or
   anything else) stops the run: log it, remove the marker, print the reason and
   `Resume with: /author-topic <slug>`. `RESULT: failed` stops the run the same way
   with the reason.
4. Append `{"t": ..., "stage": ..., "event": "end", "result": "<first line>"}` to the log,
   run `.venv/bin/python manage.py token_report --slug <slug>`, and
   print one line: stage, minutes, tokens by model from the table.

## 4. Close the audit loop

If the audit says `not ready`:

- If `T/audit.md` lists anything under `Needs research`, stop: remove the marker and
  hand the packet to the user. Research is not re-run inside a loop.
- Otherwise spawn `edit-topic` and/or `create-topic-icons` in FIX MODE, prompt
  `slug: <slug>\nFIX MODE\n<the relevant issue list from audit.md verbatim>`. Then
  re-run views only if a render could have changed: after an icons fix always, and after
  an editorial fix only when
  `.venv/bin/python manage.py check_topic_text --slug <slug> --glance-hash` differs from
  `T/renders/glance.hash` (a detail-only edit leaves it unchanged, and the renders stay
  current). Then re-run audit.
- At most two fix cycles. After the second not-ready audit, stop and hand the packet
  to the user.

Any edit to `T/topic.json` after a `ready` verdict, whether a pass on the audit's
notes or a change the user asks for, is a fix cycle like the others: views when the
glance hash changed, then a re-audit. A topic is ready only on the verdict of an
audit that ran after its last edit.

## 5. Finish

Remove the marker. Print the per-stage table from the last `token_report`, the total
wall time, the verdict, and where things are: `T/audit.md`, the page at
`http://localhost:8641/<slug>/`, the cards in `static/img/social/`. If ready, end
with: the topic is `ready`; publishing is yours. Do not commit.
