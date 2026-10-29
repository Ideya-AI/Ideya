---
name: refresh-topic
description: Refresh one published Ideya topic, staged as a hidden twin until the owner approves it. Passed dates, outdated pieces, missing developments, weakened order. Argument: a topic slug or title.
argument-hint: <slug or title>
---

You orchestrate a refresh of one published topic. The work runs on a twin,
`<slug>-refresh`, an ordinary in-progress topic readers never see; the live page
is untouched until the owner approves. Each stage is the authoring pipeline's own
subagent with a fresh context; you do no research, editing or judging yourself.
Keep your messages short. Never publish or fold in a refresh without the owner's
explicit go-ahead, never edit templates or CSS, never touch port 8642.

## 1. Resolve and stage

Resolve `$ARGUMENTS` to a slug with the one-liner in
`.claude/skills/author-topic/SKILL.md` §1. Let `S=<slug>-refresh` and
`T=research/topics/S`. If `T` does not exist, stage it:

```
.venv/bin/python manage.py stage_refresh --slug <slug>
```

If `T` exists, this is a resumed run: a stage whose `end` event in
`T/run/log.jsonl` starts `RESULT: done` is skipped.

## 2. Run

Arm, log and close exactly as `/author-topic` §2–§4 do, with `T` and `S` in place of
the topic, and these stages in order:

| stage | subagent_type | prompt |
|---|---|---|
| research | `research-topic` | `slug: S`, `REFRESH MODE`, then the output of `.venv/bin/python manage.py check_topic_text --slug S --passed` |
| editorial | `edit-topic` | `slug: S`, `FIX MODE`, then the `### Changes` list under the last `## Refresh` heading of `T/research.md`, verbatim |
| views | `create-topic-views` | `slug: S` |
| audit | `audit-topic` | `slug: S` |

After research: if its result is `done: re-author`, stop and recommend
`/author-topic <slug> --from research` (discard the twin with the owner's go-ahead).
If its Changes list is empty, stop: nothing passed the bar; offer to discard the twin.

## 3. Finish

Disarm, then print the token table, wall time, the verdict, the Changes list, and
where things are: `T/audit.md`, the twin at `http://localhost:8641/S/`, the live
page at `http://localhost:8641/<slug>/`. If ready, end with: the refresh is staged
and `ready`; say go and I fold it in with
`.venv/bin/python manage.py publish_topic --slug <slug> --refresh --confirm`
(or `--discard --confirm` to throw it away). Do not commit.
