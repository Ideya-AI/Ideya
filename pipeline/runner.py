"""One unit is one SDK call (PIPELINE.md §3, §5, §6, §11).

A `Unit` names its model, effort, prompts, tool surface and return shape. The
runner spawns a fresh headless Claude Code process for it, constrains the
output to the shape's JSON schema, validates the return, and journals it to
`run/<phase>/<unit>.json` together with usage and both windows' utilization.

    done      the journal exists and its output validates; the unit is skipped
    transport rate limit, killed process, malformed or invalid output:
              retried, then UnitFailed
    paused    utilization over the guard, or a rejected rate-limit status:
              Paused, and the orchestrator stops dispatching

Agents never write the product files: no unit may hold Write, Edit, Bash or
Agent, and the runner refuses a spec that asks for them.
"""

import asyncio
import datetime
import time
from dataclasses import dataclass, field

from claude_agent_sdk import (
    ClaudeAgentOptions,
    ClaudeSDKError,
    RateLimitEvent,
    ResultMessage,
    query,
)
from pydantic import BaseModel, ValidationError

from .paths import ROOT
from .topic import TopicDir, now

WEEKLY_PAUSE = 0.80
FIVE_HOUR_PAUSE = 0.90
ATTEMPTS = 3
BACKOFF = (5, 20, 60)
FORBIDDEN_TOOLS = {
    "Agent",
    "Task",
    "Write",
    "Edit",
    "MultiEdit",
    "NotebookEdit",
    "Bash",
}


class Paused(Exception):
    """Stop dispatching; resume later from the files. `resets_at` is the epoch
    second the window resets; `window` is five_hour or seven_day."""

    def __init__(self, msg, window="", resets_at=None):
        super().__init__(msg)
        self.window = window
        self.resets_at = resets_at


class UnitFailed(Exception):
    """A transport failure that outlasted its retries."""


@dataclass
class Unit:
    name: str
    phase: str
    model: str  # "opus" | "sonnet" | "haiku" | a full model id
    effort: str  # "low" | "medium" | "high" | "xhigh" | "max"
    prompt: str
    system: str = ""
    output: type[BaseModel] | None = None
    tools: list[str] = field(default_factory=list)  # built-in and mcp tool names
    mcp: dict = field(default_factory=dict)  # name -> server config
    max_turns: int = 60
    env: dict = field(default_factory=dict)
    max_buffer: int | None = None


@dataclass
class Reading:
    five_hour: float | None = None
    seven_day: float | None = None
    status: str = ""
    resets_at: int | None = None
    five_hour_resets_at: int | None = None
    at: str = ""

    def update(self, ev: RateLimitEvent):
        raw = ev.rate_limit_info.raw or {}
        win = raw.get("unifiedWindows") or {}
        self.five_hour = (win.get("five_hour") or {}).get("utilization", self.five_hour)
        self.seven_day = (win.get("seven_day") or {}).get("utilization", self.seven_day)
        self.five_hour_resets_at = (win.get("five_hour") or {}).get("resetsAt", self.five_hour_resets_at)
        self.status = ev.rate_limit_info.status
        self.resets_at = ev.rate_limit_info.resets_at
        self.at = now()

    def clear(self):
        """Forget the last reading, after sleeping through a window reset;
        the guard is then blind until the next call reports."""
        self.five_hour = self.seven_day = None
        self.status = ""

    def guard(self):
        if self.status == "rejected":
            raise Paused(f"rate limit rejected; resets at {self._reset()}", "five_hour", self.resets_at)
        if (self.seven_day or 0) >= WEEKLY_PAUSE:
            raise Paused(
                f"weekly window at {self.seven_day:.0%}; resets at {self._reset()}", "seven_day", self.resets_at
            )
        if (self.five_hour or 0) >= FIVE_HOUR_PAUSE:
            raise Paused(
                f"five-hour window at {self.five_hour:.0%}; resets at {self._reset(self.five_hour_resets_at)}",
                "five_hour",
                self.five_hour_resets_at or self.resets_at,
            )

    def _reset(self, at=None):
        at = at or self.resets_at
        if not at:
            return "unknown"
        return datetime.datetime.fromtimestamp(at).strftime("%Y-%m-%d %H:%M")

    def as_dict(self):
        return {
            "five_hour": self.five_hour,
            "seven_day": self.seven_day,
            "status": self.status,
            "resets_at": self._reset(),
        }


reading = Reading()  # process-wide; one unit stale by construction (§6)


def done(topic: TopicDir, unit: Unit) -> bool:
    doc = topic.read_return(unit.phase, unit.name)
    if not doc or "output" not in doc:
        return False
    if unit.output is None:
        return True
    try:
        unit.output.model_validate(doc["output"])
        return True
    except ValidationError:
        return False


def result(topic: TopicDir, unit: Unit):
    """The validated output of a finished unit."""
    doc = topic.read_return(unit.phase, unit.name)
    out = doc["output"]
    return unit.output.model_validate(out) if unit.output else out


def _options(unit: Unit) -> ClaudeAgentOptions:
    bad = FORBIDDEN_TOOLS & set(unit.tools)
    if bad:
        raise ValueError(f"unit {unit.name} may not hold {sorted(bad)}")
    return ClaudeAgentOptions(
        model=unit.model,
        effort=unit.effort,
        system_prompt=unit.system or None,
        tools=list(unit.tools),
        allowed_tools=list(unit.tools),
        mcp_servers=unit.mcp,
        permission_mode="bypassPermissions",
        setting_sources=[],
        output_format=unit.output.output_format() if unit.output else None,
        max_turns=unit.max_turns,
        env=unit.env,
        max_buffer_size=unit.max_buffer,
        cwd=str(ROOT),
    )


async def _call(unit: Unit) -> tuple[ResultMessage, list[str]]:
    final, notes = None, []
    async for m in query(prompt=unit.prompt, options=_options(unit)):
        if isinstance(m, RateLimitEvent):
            reading.update(m)
        elif isinstance(m, ResultMessage):
            final = m
    if final is None:
        raise UnitFailed(f"{unit.name}: no result message")
    return final, notes


async def run_unit(topic: TopicDir, unit: Unit, force: bool = False):
    """Run a unit unless its return file already validates. Returns the
    validated output (a shape instance, or the raw dict for shapeless units)."""
    if not force and done(topic, unit):
        return result(topic, unit)
    reading.guard()
    started, errors = now(), []
    for attempt in range(1, ATTEMPTS + 1):
        t0 = time.monotonic()
        try:
            res, _ = await _call(unit)
        except ClaudeSDKError as e:
            errors.append(f"attempt {attempt}: {type(e).__name__}: {e}")
            res = None
        if res is not None:
            err = _transport_error(res, unit)
            if err is None:
                out = (
                    res.structured_output
                    if unit.output
                    else (res.structured_output or res.result)
                )
                topic.write_return(
                    unit.phase,
                    unit.name,
                    {
                        "unit": unit.name,
                        "phase": unit.phase,
                        "model": unit.model,
                        "effort": unit.effort,
                        "started": started,
                        "finished": now(),
                        "seconds": round(time.monotonic() - t0, 1),
                        "attempts": attempt,
                        "session_id": res.session_id,
                        "num_turns": res.num_turns,
                        "usage": res.usage,
                        "models": sorted(res.model_usage or {}),
                        "cost_usd": res.total_cost_usd,
                        "utilization": reading.as_dict(),
                        "errors": errors,
                        "output": out,
                    },
                )
                reading.guard()
                return result(topic, unit)
            errors.append(f"attempt {attempt}: {err}")
        reading.guard()
        if attempt < ATTEMPTS:
            await asyncio.sleep(BACKOFF[attempt - 1])
    raise UnitFailed(f"{unit.phase}/{unit.name}: " + "; ".join(errors))


def _transport_error(res: ResultMessage, unit: Unit) -> str | None:
    if res.api_error_status:
        return f"api error {res.api_error_status}"
    if res.is_error or res.subtype != "success":
        return f"{res.subtype}: {'; '.join(res.errors or []) or res.result or 'error'}"
    if unit.output is not None:
        if res.structured_output is None:
            return "no structured output"
        try:
            unit.output.model_validate(res.structured_output)
        except ValidationError as e:
            return f"output failed validation: {e.error_count()} errors: {str(e)[:500]}"
    return None


async def run_units(topic: TopicDir, units: list[Unit], parallel: int = 1, force=False):
    """Run several units, at most `parallel` at once. A Paused raised by any
    one stops the rest at their next dispatch."""
    sem = asyncio.Semaphore(parallel)

    async def one(u):
        async with sem:
            return await run_unit(topic, u, force=force)

    return await asyncio.gather(*(one(u) for u in units))


def run(coro):
    return asyncio.run(coro)
