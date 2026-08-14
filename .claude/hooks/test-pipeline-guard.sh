#!/bin/bash
# Regression tests for pipeline-guard.sh. The cases live in this file rather than
# on a command line because the guard would (correctly) block a command line that
# contained a real publish invocation.
cd "$(dirname "$0")" || exit 1
pass=0; fail=0
check() { # <expected-exit> <label> <command-string>
  local want="$1" label="$2" cmd="$3" got
  printf '{"tool_input":{"command":%s}}' "$(python3 -c 'import json,sys;print(json.dumps(sys.argv[1]))' "$cmd")" \
    | ./pipeline-guard.sh >/dev/null 2>&1
  got=$?
  if [ "$got" = "$want" ]; then pass=$((pass+1)); printf '  ok    %-34s exit=%s\n' "$label" "$got"
  else fail=$((fail+1)); printf '  FAIL  %-34s exit=%s want=%s\n' "$label" "$got" "$want"; fi
}

P='--status published'
check 2 "real publish"            ".venv/bin/python manage.py load_topic_draft --slug x $P"
check 2 "real publish (equals)"   ".venv/bin/python manage.py load_topic_draft --slug x --status=published"
check 0 "draft load"              ".venv/bin/python manage.py load_topic_draft --slug x --status draft"
check 0 "commit quoting the flag" "git commit -m 'never pass $P from the pipeline'"
check 0 "grep for the flag"       "grep -rn '$P' research/"
check 2 "live container port"     "DJANGO_DEBUG=true .venv/bin/python manage.py runserver 8642"
check 0 "dev port"                "DJANGO_DEBUG=true .venv/bin/python manage.py runserver 8641"
check 0 "unrelated"               "git status --short"

echo "  ${pass} passed, ${fail} failed"
[ "$fail" = 0 ]
