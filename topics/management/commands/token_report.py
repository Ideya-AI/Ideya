"""Tokens by stage and by model for one authoring session.

    manage.py token_report --slug <slug> --session <session-id>
    manage.py token_report --slug <slug>            # newest transcript in this project

Reads the Claude Code transcripts under
~/.claude/projects/<project>/: the main <session>.jsonl (reported as
"orchestrator") and <session>/subagents/agent-*.jsonl, each attributed to the
stage named by its .meta.json agentType and kept only when its description
mentions the slug. Sums message.usage over assistant records by model. Prints a
table and writes research/topics/<slug>/run/tokens.json. Close, not perfect:
a subagent's own subagents roll into it, and iterations[] is not double-counted.
"""

import json
import os
from collections import defaultdict
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

FIELDS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")
SHORT = {"claude-opus-5": "opus", "claude-sonnet-5": "sonnet", "claude-haiku-4-5-20251001": "haiku",
         "claude-fable-5-1": "fable"}


def project_dir():
    enc = str(Path(settings.BASE_DIR).resolve()).replace("/", "-")
    return Path.home() / ".claude" / "projects" / enc


def usage_of(path):
    """{model: {field: n}} over one transcript file."""
    out = defaultdict(lambda: defaultdict(int))
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            if rec.get("type") != "assistant":
                continue
            msg = rec.get("message") or {}
            u = msg.get("usage") or {}
            model = msg.get("model") or "?"
            if not u or model == "<synthetic>":
                continue
            for k in FIELDS:
                out[model][k] += int(u.get(k) or 0)
    return out


def report(slug, session=None):
    pdir = project_dir()
    if not pdir.exists():
        raise CommandError(f"no transcripts at {pdir}")
    if not session:
        files = sorted(pdir.glob("*.jsonl"), key=os.path.getmtime)
        if not files:
            raise CommandError("no session transcripts")
        session = files[-1].stem
    main = pdir / f"{session}.jsonl"
    if not main.exists():
        raise CommandError(f"no transcript {main}")
    rows = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))  # stage -> model -> field
    for model, u in usage_of(main).items():
        for k, v in u.items():
            rows["orchestrator"][model][k] += v
    subs = pdir / session / "subagents"
    for meta_path in sorted(subs.glob("agent-*.meta.json")) if subs.exists() else []:
        try:
            meta = json.loads(meta_path.read_text())
        except ValueError:
            continue
        desc = (meta.get("description") or "") + " " + (meta.get("name") or "")
        if slug not in desc:
            continue
        stage = meta.get("agentType") or meta.get("name") or "subagent"
        transcript = meta_path.with_name(meta_path.name.replace(".meta.json", ".jsonl"))
        if not transcript.exists():
            continue
        for model, u in usage_of(transcript).items():
            for k, v in u.items():
                rows[stage][model][k] += v
    return session, rows


class Command(BaseCommand):
    help = "Tokens by stage and model for one authoring session."

    def add_arguments(self, p):
        p.add_argument("--slug", required=True)
        p.add_argument("--session", default=None)
        p.add_argument("--no-write", action="store_true")

    def handle(self, *a, **o):
        session, rows = report(o["slug"], o["session"])
        self.stdout.write(f"session {session}")
        self.stdout.write(f"{'stage':22} {'model':8} {'input':>9} {'cache_w':>10} {'cache_r':>11} {'output':>9} {'total':>11}")
        grand = defaultdict(int)
        for stage in sorted(rows, key=lambda s: (s == "orchestrator", s)):
            for model, u in sorted(rows[stage].items()):
                total = sum(u[k] for k in FIELDS)
                grand[model] += total
                self.stdout.write(
                    f"{stage:22} {SHORT.get(model, model)[:8]:8} {u['input_tokens']:>9,} "
                    f"{u['cache_creation_input_tokens']:>10,} {u['cache_read_input_tokens']:>11,} "
                    f"{u['output_tokens']:>9,} {total:>11,}"
                )
        for model, t in sorted(grand.items()):
            self.stdout.write(f"{'all stages':22} {SHORT.get(model, model)[:8]:8} {'':9} {'':10} {'':11} {'':9} {t:>11,}")
        if not o["no_write"]:
            run = Path("research/topics") / o["slug"] / "run"
            run.mkdir(parents=True, exist_ok=True)
            (run / "tokens.json").write_text(json.dumps(
                {"session": session, "stages": {s: {m: dict(u) for m, u in ms.items()} for s, ms in rows.items()}},
                indent=1) + "\n")
            self.stdout.write(f"wrote {run / 'tokens.json'}")
