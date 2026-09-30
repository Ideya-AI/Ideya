#!/usr/bin/env python3
"""PreToolUse hook: pause an authoring run before the usage meters run out.

Armed only while a topic run is active (research/topics/*/run/active exists and
is under 8 hours old). Reads the current five-hour and seven-day utilization
from the same endpoint the Claude Code binary uses, caches it for 120 s, and
blocks every tool call (exit 2, reason on stderr) at 80% five-hour or 90%
seven-day. Fails open: any error allows the call and logs one warning line to
the active run's log.

    python3 .claude/hooks/usage-guard.py --status    # print what the endpoint returns
"""

import glob
import json
import os
import sys
import time
import urllib.request
from datetime import datetime

FIVE_HOUR_STOP = 0.80
SEVEN_DAY_STOP = 0.90
CACHE = f"/tmp/ideya-usage-guard-{os.getuid()}.json"
CACHE_TTL = 120
MARKER_MAX_AGE = 8 * 3600
ENDPOINT = "https://api.anthropic.com/api/oauth/usage"


def project_dir():
    return os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


def active_markers():
    now = time.time()
    fresh, stale = [], []
    for m in glob.glob(
        os.path.join(project_dir(), "research", "topics", "*", "run", "active")
    ):
        (fresh if now - os.path.getmtime(m) < MARKER_MAX_AGE else stale).append(m)
    return fresh, stale


def token():
    with open(os.path.expanduser("~/.claude/.credentials.json")) as f:
        oauth = json.load(f)["claudeAiOauth"]
    if oauth.get("expiresAt", 0) / 1000 < time.time():
        raise RuntimeError("oauth token expired; open Claude Code once to refresh")
    return oauth["accessToken"]


def fetch():
    if os.path.exists(CACHE) and time.time() - os.path.getmtime(CACHE) < CACHE_TTL:
        with open(CACHE) as f:
            return json.load(f)
    req = urllib.request.Request(
        ENDPOINT,
        headers={
            "Authorization": f"Bearer {token()}",
            "anthropic-beta": "oauth-2025-04-20",
            "Accept": "application/json",
            "User-Agent": "claude-code/usage-guard",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.load(r)
    with open(CACHE, "w") as f:
        json.dump(data, f)
    return data


def windows(data):
    """{name: (utilization 0..1, resets_at)} for the two authoritative meters.

    Read by EXACT key. The response also carries `seven_day_breakdown`, whose rows
    are each model's SHARE of the week's spend, and a row at 100 percent means one
    model did all of it, not that anything is exhausted. A prefix match on
    "seven_day" swallowed that and stopped a run at 2 percent usage (2026-09-21).
    """
    found = {}
    if not isinstance(data, dict):
        return found
    for key in ("five_hour", "seven_day"):
        node = data.get(key)
        if isinstance(node, dict) and isinstance(node.get("utilization"), (int, float)):
            # Always a percent. Treating u <= 1 as a fraction read 1 percent as
            # 100 and stopped runs just after each reset (2026-09-23 to 09-28).
            found[key] = (float(node["utilization"]) / 100, node.get("resets_at"))
    # `limits` is the same numbers in list form; use it only to fill a gap.
    for row in data.get("limits") or []:
        if not isinstance(row, dict) or not isinstance(
            row.get("percent"), (int, float)
        ):
            continue
        key = {"session": "five_hour", "weekly_all": "seven_day"}.get(row.get("kind"))
        if key and key not in found:
            found[key] = (float(row["percent"]) / 100, row.get("resets_at"))
    return found


def _hours_left(resets_at):
    try:
        return (datetime.fromisoformat(resets_at).timestamp() - time.time()) / 3600
    except (TypeError, ValueError):
        return 0


def log(markers, line):
    for m in markers:
        try:
            with open(os.path.join(os.path.dirname(m), "log.jsonl"), "a") as f:
                f.write(
                    json.dumps(
                        {"t": time.strftime("%Y-%m-%dT%H:%M:%S"), "usage_guard": line}
                    )
                    + "\n"
                )
        except OSError:
            pass


def main():
    if "--status" in sys.argv:
        data = fetch()
        print(
            "top-level keys:",
            sorted(data) if isinstance(data, dict) else type(data).__name__,
        )
        for name, (u, reset) in windows(data).items():
            print(f"{name:24} {u:6.1%}  resets_at={reset}")
        fresh, stale = active_markers()
        print("active runs:", fresh or "none", "| stale markers:", stale or "none")
        return 0
    try:
        payload = json.load(sys.stdin) or {}
    except Exception:
        payload = {}
    tool = payload.get("tool_name", "")
    if tool in ("Write", "Edit", "NotebookEdit"):
        return 0  # a stopping agent must be able to save its work
    command = str((payload.get("tool_input") or {}).get("command", ""))
    if (
        tool == "Bash"
        and "run/active" in command
        and ("rm " in command or "log.jsonl" in command)
    ):
        return 0  # the orchestrator must always be able to disarm and log the stop
    fresh, stale = active_markers()
    if stale:
        log(stale, f"stale run/active marker ignored (older than 8h): {stale}")
    if not fresh:
        return 0
    try:
        w = windows(fetch())
    except Exception as e:  # fail open
        log(fresh, f"could not read usage, allowing: {e}")
        return 0
    five = w.get("five_hour")
    week = w.get("seven_day")
    if five and five[0] >= 0.99 and _hours_left(five[1]) > 4.5:
        # Right after a reset the endpoint briefly reports the new window as
        # full, then settles near 0 (seen 2026-09-23 and 09-24; the first stopped
        # a run for two hours). A window cannot be spent in its first half hour,
        # so drop the reading and fetch fresh next call.
        log(
            fresh,
            f"five-hour reads {five[0]:.0%} with the reset {five[1]}; window-start glitch, allowing",
        )
        try:
            os.remove(CACHE)
        except OSError:
            pass
        five = None
    if five is None and week is None:
        log(
            fresh,
            f"no five_hour/seven_day windows in response keys {sorted(w)}; allowing",
        )
        return 0
    for label, val, stop in (
        ("five-hour", five, FIVE_HOUR_STOP),
        ("seven-day", week, SEVEN_DAY_STOP),
    ):
        if val and val[0] >= stop:
            reason = (
                f"USAGE GUARD: {label} window at {val[0]:.0%} (stop at {stop:.0%}), resets {val[1]}. "
                f"Write whatever you have in hand to its file first, then stop and report "
                f"RESULT: blocked. Write and Edit still work; everything else is denied. "
                f"The run resumes with the same command after the reset. "
                f"Meters read: "
                + ", ".join(f"{k} {v[0]:.0%}" for k, v in sorted(w.items()))
            )
            log(fresh, reason)
            print(reason, file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
