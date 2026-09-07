"""Runs a workflow script through bridge.mjs and serves its agent() calls with
headless Claude Code on the user's subscription (Claude Agent SDK).

    from research.engine.harness import run_script
    result = asyncio.run(run_script(script, args, run_dir))

What this adds over the Workflow tool, and why the engine moved here:
- JOURNAL: every agent call is keyed by a hash of (prompt, opts) and written to
  <run_dir>/journal/<key>.json with its result and usage. A rerun replays hits
  without spending anything, so a crash, a kill, or a usage limit costs at most
  the calls in flight — the checkpoint is per call, not per stage.
- USAGE LIMITS: a "session limit … resets 7pm" answer is parsed, the harness
  sleeps until the reset (+90s), and the call is retried in place. The script
  never sees it. Expect one per run.
- TOOL POLICY: agentType decides the tool set and system prompt (the agent
  definitions in .claude/agents are read as system prompts, not resolved by
  name — print mode drops the JSON schema when an --agent is named). Anything
  without an agentType is tool-less. general-purpose means web only: the
  Bash-and-filesystem churn the old runs paid for was never needed.
- CONCURRENCY: a semaphore (ENGINE_CONCURRENCY, default 4) — the plan's rate
  limits set the ceiling, not the fan-out in the script.
"""

import asyncio
import datetime as dt
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path
from zoneinfo import ZoneInfo

from claude_agent_sdk import ClaudeAgentOptions, query

REPO = Path(__file__).resolve().parents[2]
BRIDGE = Path(__file__).with_name("bridge.mjs")
AGENT_DEFS = REPO / ".claude" / "agents"
WEB = ["WebSearch", "WebFetch"]
# agentType -> (tools, agent-definition file whose body becomes the system prompt)
POLICY = {
    None: ([], None),
    "general-purpose": (WEB, None),
    "claim-verifier": (WEB, "claim-verifier.md"),
    "camp-scout": (WEB, "camp-scout.md"),
    "topic-critic": ([], "topic-critic.md"),
    "icon-briefer": ([], "icon-briefer.md"),
    "view-critic": (["Read"], "view-critic.md"),
    "topic-pm": (["Read"], "topic-pm.md"),
}
LIMIT_RX = re.compile(r"limit.*?resets?\s+(\d{1,2})(?::(\d{2}))?\s*([ap]m)\s*\(([^)]+)\)", re.I | re.S)


def _agent_body(name):
    if not name:
        return None
    text = (AGENT_DEFS / name).read_text(encoding="utf-8")
    m = re.match(r"^---\n.*?\n---\n", text, re.S)
    return text[m.end():].strip() if m else text.strip()


def _reset_delay(text):
    """Seconds until the reset named in a usage-limit message, or None."""
    m = LIMIT_RX.search(text or "")
    if not m:
        return None
    hour, minute, ampm, tz = int(m.group(1)), int(m.group(2) or 0), m.group(3).lower(), m.group(4)
    hour = hour % 12 + (12 if ampm == "pm" else 0)
    try:
        zone = ZoneInfo(tz.strip())
    except Exception:
        zone = ZoneInfo("America/Los_Angeles")
    now = dt.datetime.now(zone)
    at = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if at <= now:
        at += dt.timedelta(days=1)
    return (at - now).total_seconds() + 90


class Harness:
    def __init__(self, run_dir, concurrency=None, log=print):
        self.run_dir = Path(run_dir)
        self.journal = self.run_dir / "journal"
        self.journal.mkdir(parents=True, exist_ok=True)
        self.sem = asyncio.Semaphore(int(concurrency or os.environ.get("ENGINE_CONCURRENCY", "4")))
        self.log = log
        self.usage = {"calls": 0, "cached": 0, "input": 0, "output": 0, "cache_read": 0, "cache_write": 0}

    def _key(self, prompt, opts):
        return hashlib.sha256(json.dumps({"p": prompt, "o": opts}, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:24]

    async def agent(self, prompt, opts):
        key = self._key(prompt, opts)
        hit = self.journal / f"{key}.json"
        if hit.exists():
            self.usage["cached"] += 1
            return json.loads(hit.read_text(encoding="utf-8"))["result"]
        label = opts.get("label") or "agent"
        tools, defn = POLICY.get(opts.get("agentType"), ([], None))
        system = _agent_body(defn) or "You are one worker in the Ideya authoring engine. Do exactly the task in the prompt and return only the structured output requested."
        model = opts.get("model")  # 'sonnet' | 'opus' | 'fable' | None
        schema = opts.get("schema")
        options = ClaudeAgentOptions(
            model=model,
            fallback_model="opus" if model == "fable" else None,
            effort=opts.get("effort"),
            tools=tools,
            strict_mcp_config=True,
            mcp_servers={},
            system_prompt=system,
            output_format={"type": "json_schema", "schema": schema} if schema else None,
            max_turns=60,
            # An agent that Reads a 1440px section image gets a tool result over
            # the SDK's default 1MB message cap and dies with CLIJSONDecodeError
            # (immigration s5.pm, 2026-09-06). Images are the point of stages 3-5.
            max_buffer_size=64 * 1024 * 1024,
            cwd=str(REPO),
            permission_mode="dontAsk",
        )
        async with self.sem:
            for attempt in range(6):
                t0 = time.time()
                result = None
                res_msg = None
                try:
                    async for msg in query(prompt=prompt, options=options):
                        if type(msg).__name__ == "ResultMessage":
                            res_msg = msg
                except Exception as e:  # CLI died, JSON decode, connection
                    self.log(f"  [{label}] attempt {attempt + 1}: {type(e).__name__}: {str(e)[:160]}")
                    await asyncio.sleep(20 * (attempt + 1))
                    continue
                text = (res_msg.result if res_msg else "") or ""
                errs = " ".join(str(e) for e in (getattr(res_msg, "errors", None) or []))
                if res_msg is None or res_msg.is_error:
                    delay = _reset_delay(text + " " + errs)
                    if delay:
                        self.log(f"  [{label}] usage limit — sleeping {delay / 60:.0f} min until the reset")
                        await asyncio.sleep(delay)
                        continue
                    self.log(f"  [{label}] attempt {attempt + 1} failed: {(text or errs)[:200]}")
                    await asyncio.sleep(30 * (attempt + 1))
                    continue
                if schema:
                    result = res_msg.structured_output
                    if result is None:
                        # the model answered in prose; try once more with a nudge
                        self.log(f"  [{label}] no structured output on attempt {attempt + 1}; retrying")
                        prompt = prompt + "\n\nReturn ONLY the structured output; no prose."
                        continue
                else:
                    result = text
                u = res_msg.usage or {}
                self.usage["calls"] += 1
                for k, src in (("input", "input_tokens"), ("output", "output_tokens"), ("cache_read", "cache_read_input_tokens"), ("cache_write", "cache_creation_input_tokens")):
                    self.usage[k] += int(u.get(src) or 0)
                hit.write_text(json.dumps({"label": label, "opts": {k: v for k, v in opts.items() if k != "schema"}, "result": result, "usage": u, "model_usage": getattr(res_msg, "model_usage", None) and {m: dict(v.__dict__) if hasattr(v, "__dict__") else v for m, v in res_msg.model_usage.items()}, "secs": round(time.time() - t0), "ts": dt.datetime.now().isoformat(timespec="seconds")}, ensure_ascii=False, default=str), encoding="utf-8")
                self.log(f"  [{label}] done in {time.time() - t0:.0f}s")
                return result
        self.log(f"  [{label}] gave up after 6 attempts — returning null")
        return None

    async def run(self, script, args):
        args_path = self.run_dir / "args.json"
        args_path.write_text(json.dumps(args, ensure_ascii=False), encoding="utf-8")
        proc = await asyncio.create_subprocess_exec(
            "node", str(BRIDGE), str(script), str(args_path),
            stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
            limit=64 * 1024 * 1024,
        )
        tasks = set()
        result = {"result": None, "error": None}

        async def serve(msg):
            out = await self.agent(msg["prompt"], msg.get("opts") or {})
            proc.stdin.write((json.dumps({"id": msg["id"], "result": out}, ensure_ascii=False) + "\n").encode())
            await proc.stdin.drain()

        async def pump_stderr():
            async for line in proc.stderr:
                self.log("  node: " + line.decode(errors="replace").rstrip())

        stderr_task = asyncio.create_task(pump_stderr())
        async for raw in proc.stdout:
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError as e:
                raise RuntimeError(f"bridge sent an unparseable line ({len(raw)} bytes): {e}; head={raw[:120]!r}")
            t = msg.get("type")
            if t == "agent":
                tasks.add(asyncio.create_task(serve(msg)))
            elif t == "log":
                self.log(msg["message"])
            elif t == "phase":
                self.log(f"— {msg['title']} —")
            elif t == "result":
                result["result"] = msg["result"]
            elif t == "error":
                result["error"] = msg["error"]
        await proc.wait()
        stderr_task.cancel()
        (self.run_dir / "usage.json").write_text(json.dumps(self.usage, indent=1), encoding="utf-8")
        if result["error"]:
            raise RuntimeError(result["error"])
        return result["result"]


async def run_script(script, args, run_dir, concurrency=None, log=print):
    return await Harness(run_dir, concurrency, log).run(Path(script), args)


if __name__ == "__main__":
    script, args_file, run_dir = sys.argv[1:4]
    out = asyncio.run(run_script(script, json.loads(Path(args_file).read_text()), run_dir))
    Path(run_dir, "result.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("result ->", Path(run_dir, "result.json"))
