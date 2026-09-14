#!/bin/bash
# Structural enforcement of two rules that were previously only prose:
#   1. "Automation drafts; a human publishes" — the pipeline's iron rule.
#   2. Port 8642 is the LIVE container; the dev server belongs on 8641.
# A rule stated in a skill is advice the model may or may not be attending to on
# round 14 of a fix loop. A PreToolUse hook is enforcement.
#
# Match the INVOCATION, not the bare string. Version 1 tested for the flag
# anywhere in the command and blocked its own git commit, because the commit
# message quoted the flag it was guarding against. That was patched for commit
# messages; the same bug survived in a second carrier — a heredoc BODY, e.g.
# rewriting the review-packet template in ENGINE.md, which legitimately prints
# the publish command for the human to copy. Documentation that quotes a command
# is not an invocation of it. So: strip heredoc bodies first, then match.
CMD=$(jq -r '.tool_input.command // empty')

# Drop the contents of every heredoc (<<EOF, <<'EOF', <<-"EOF"), keeping the
# line that opens it — that line is a real command and must still be scanned.
SCAN=$(printf '%s\n' "$CMD" | awk '
  !inhd && match($0, /<<-?[[:space:]]*["'"'"']?[A-Za-z_][A-Za-z0-9_]*["'"'"']?/) {
    d = substr($0, RSTART, RLENGTH)
    sub(/^<<-?[[:space:]]*/, "", d); gsub(/["'"'"']/, "", d)
    inhd = 1; delim = d; print; next
  }
  inhd { sub(/^[[:space:]]+/, "", $0); if ($0 == delim) inhd = 0; next }
  { print }
')

# publish_topic is listed by name: it reaches the loader through Python, so it
# never renders a `--status published` string for the rule below to catch.
# Adding a publish path without adding it here would silently retire the guard.
# Anchored to a manage.py/django-admin invocation so that grepping for the word,
# or editing the file that defines it, is not mistaken for running it.
if grep -qE '(manage\.py|django-admin)[[:space:]]+publish_topic\b' <<<"$SCAN"; then
  echo "BLOCKED: publish_topic belongs to the human (PIPELINE.md §2). The pipeline ends at ready." >&2
  exit 2
fi

if grep -q 'load_topic_draft' <<<"$SCAN" && grep -qE -- '--status[= ]+published' <<<"$SCAN"; then
  echo "BLOCKED: publishing is a human step (PIPELINE.md §2). Load without --status published." >&2
  exit 2
fi

if grep -qE 'runserver[^|;&]*8642' <<<"$SCAN"; then
  echo "BLOCKED: 8642 is the LIVE container's port. The dev server runs on 8641." >&2
  exit 2
fi

exit 0
