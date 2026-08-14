#!/bin/bash
# Structural enforcement of two rules that were previously only prose:
#   1. "Automation drafts; a human publishes" — the pipeline's iron rule.
#   2. Port 8642 is the LIVE container; the dev server belongs on 8641.
# A rule stated in a skill is advice the model may or may not be attending to on
# round 14 of a fix loop. A PreToolUse hook is enforcement.
#
# Match the INVOCATION, not the bare string. The first version tested for the
# flag anywhere in the command and promptly blocked its own git commit, because
# the commit message quoted the flag it was guarding against.
CMD=$(jq -r '.tool_input.command // empty')

if grep -q 'load_topic_draft' <<<"$CMD" && grep -qE -- '--status[= ]+published' <<<"$CMD"; then
  echo "BLOCKED: publishing is a human step (author-topic stage 5). Load with --status draft and write the review packet instead." >&2
  exit 2
fi

if grep -qE 'runserver[^|;&]*8642' <<<"$CMD"; then
  echo "BLOCKED: 8642 is the LIVE container's port. The dev server runs on 8641." >&2
  exit 2
fi

exit 0
