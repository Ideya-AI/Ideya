"""Stages and the orchestrator loop (PIPELINE.md §4, §5, §9, §10).

A stage declares three things as assertions about the topic directory:
`requires` (unmet inputs, as a list of reasons), `satisfied` (is this stage
already done, checked separately from its outputs so it never re-runs on
them), and `run`. No stage knows the run order; `author` walks the registry
and runs the first stage that is not satisfied.

Failure semantics: a `CriteriaFailure` blocks the topic at once, naming the
stage it implicates; a `UnitFailed` (transport, retries exhausted) blocks
too; a `Paused` stops dispatching and exits clean, because every unit resumes
from its own file. Re-running `author` on a blocked topic is the decision to
retry: it clears the marker and continues; the marker in `evidence.json`
records what blocked and why until then.

Stage modules register themselves by appending a `Stage` to `STAGES` on
import; `registry()` imports the ones that exist.
"""

import importlib
import sys
import time
from dataclasses import dataclass
from typing import Callable

from .runner import Paused, UnitFailed, reading
from .topic import READY, TopicDir

STAGE_MODULES = [
    "pipeline.stage1",
    "pipeline.stage2",
    "pipeline.stage3",
    "pipeline.stage4",
    "pipeline.stage5",
]


class CriteriaFailure(Exception):
    """The stage ran and its exit check failed: a pipeline bug, not a topic task."""

    def __init__(self, reason: str, implicates: str | None = None):
        super().__init__(reason)
        self.reason = reason
        self.implicates = implicates


@dataclass
class Stage:
    name: str  # "stage1"
    title: str  # "research"
    requires: Callable[[TopicDir], list[str]]
    satisfied: Callable[[TopicDir], bool]
    run: Callable[[TopicDir], None]


STAGES: list[Stage] = []


def registry() -> list[Stage]:
    for mod in STAGE_MODULES:
        try:
            importlib.import_module(mod)
        except ModuleNotFoundError as e:
            if e.name != mod:
                raise
    return sorted(STAGES, key=lambda s: s.name)


def say(msg):
    print(msg, file=sys.stderr, flush=True)


def author(slug: str, only: str | None = None) -> int:
    """Run stages until the topic is `ready`, blocked, or paused. Exit code:
    0 ready or paused, 1 blocked or nothing to run, 2 bad input."""
    topic = TopicDir(slug)
    if not topic.exists():
        say(f"{slug}: no topic directory")
        return 2
    if topic.status == "published":
        say(f"{slug}: published; the pipeline does not touch it")
        return 2
    b = topic.blocked
    if b:
        say(f"{slug}: was blocked at {b['stage']} ({b['at']}): {b['reason']}; retrying")
        topic.unblock()
    stages = registry()
    if not stages:
        say("no stages are built yet")
        return 1
    for stage in stages:
        if only and stage.name != only:
            continue
        if stage.satisfied(topic):
            say(f"{stage.name} {stage.title}: satisfied")
            continue
        unmet = stage.requires(topic)
        if unmet:
            say(f"{stage.name} {stage.title}: cannot run, requires " + "; ".join(unmet))
            return 1
        say(f"{stage.name} {stage.title}: running")
        try:
            while True:
                try:
                    stage.run(topic)
                    break
                except Paused as e:
                    if e.window != "five_hour" or not e.resets_at:
                        say(f"{stage.name}: paused ({e}). Re-run to resume.")
                        return 0
                    wait = max(60, e.resets_at - time.time() + 90)
                    say(f"{stage.name}: paused ({e}); sleeping {wait / 60:.0f} min, then resuming")
                    time.sleep(wait)
                    reading.clear()  # the next dispatch fetches a fresh reading
        except CriteriaFailure as e:
            topic.block(stage.name, e.reason, e.implicates)
            say(
                f"{stage.name}: BLOCKED, {e.reason}"
                + (f" (implicates {e.implicates})" if e.implicates else "")
            )
            return 1
        except UnitFailed as e:
            topic.block(stage.name, f"transport: {e}")
            say(f"{stage.name}: BLOCKED after retries, {e}")
            return 1
        if not stage.satisfied(topic):
            reason = f"{stage.name} ran but is not satisfied by its own outputs"
            topic.block(stage.name, reason)
            say(f"{stage.name}: BLOCKED, {reason}")
            return 1
        say(f"{stage.name} {stage.title}: done")
    if topic.status == READY:
        say(f"{slug}: ready. A human publishes.")
    return 0


def status(slug: str) -> int:
    topic = TopicDir(slug)
    if not topic.exists():
        say(f"{slug}: no topic directory")
        return 2
    print(f"{slug}: {topic.status}")
    b = topic.blocked
    if b:
        print(f"  BLOCKED at {b['stage']} ({b['at']}): {b['reason']}")
    for stage in registry():
        ok, why = topic.verdict_valid(stage.name)
        sat = "satisfied" if stage.satisfied(topic) else "not satisfied"
        unmet = stage.requires(topic)
        print(
            f"  {stage.name} {stage.title}: {sat}; verdict {why}"
            + (f"; requires {'; '.join(unmet)}" if unmet else "")
        )
    returns = (
        sorted(p.relative_to(topic.run_dir) for p in topic.run_dir.glob("*/*.json"))
        if topic.run_dir.exists()
        else []
    )
    if returns:
        print(f"  run files: {len(returns)}")
        for r in returns:
            print(f"    {r}")
    return 0
