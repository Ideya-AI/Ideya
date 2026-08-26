#!/bin/bash
# research/ENGINE.md is the engine's single source of truth, kept honest by
# check_engine.py (inventory paths + routing table vs the scripts). Run it after
# any edit that could open drift: the workflow scripts, the skills, the hooks,
# or the manual itself. Non-blocking (the edit already happened) — a failure
# surfaces as feedback telling the session to update the manual in this change.
FILE=$(jq -r '.tool_input.file_path // empty')
case "$FILE" in
  */research/workflows/*|*/research/ENGINE.md|*/.claude/skills/author-topic/*|*/.claude/skills/refresh-topic/*|*/.claude/hooks/*)
    cd "$CLAUDE_PROJECT_DIR" || exit 0
    OUT=$(.venv/bin/python research/workflows/check_engine.py 2>&1) || {
      echo "$OUT" >&2
      exit 2
    }
    ;;
esac
exit 0
