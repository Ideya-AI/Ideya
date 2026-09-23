---
name: research-topic
description: Stage 1: research one Ideya topic into research/topics/<slug>/research.md. Runs alone, outside a full author-topic run. Argument: a topic slug or title.
disable-model-invocation: true
argument-hint: <slug or title>
---

Run stage "research-topic" of the Ideya authoring pipeline for one topic, in a fresh subagent.

1. Resolve the argument `$ARGUMENTS` to a slug:
   ```
   .venv/bin/python -c "import json,sys,pathlib;a=' '.join(sys.argv[1:]).strip().lower();ds=sorted(p for p in pathlib.Path('research/topics').iterdir() if (p/'topic.json').exists());ex=[p.name for p in ds if p.name==a or json.loads((p/'topic.json').read_text()).get('title','').lower()==a];print(ex[0] if ex else 'AMBIGUOUS '+' '.join(p.name for p in ds if a in p.name or a in json.loads((p/'topic.json').read_text()).get('title','').lower()))" 
   ```
   If it prints AMBIGUOUS, show the candidates and stop.
2. Spawn the `research-topic` agent with the Agent tool: `subagent_type: "research-topic"`,
   `description: "research-topic <slug>"`, prompt: `slug: <slug>`. Wait for it.
3. Relay its report to the user, starting with its RESULT line. Then run
   `.venv/bin/python manage.py token_report --slug <slug> --session <id>` where
   `<id>` is the directory name just above `scratchpad` in your scratchpad path,
   and show the table.

Never publish a topic and never edit templates or CSS.
