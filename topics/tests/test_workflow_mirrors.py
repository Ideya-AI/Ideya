"""The three Workflow scripts deliberately duplicate their editorial rules and
verdict contract, because workflow scripts cannot import anything.

That duplication has already drifted once with consequences: `refresh_topic.js`
carried the "an unperformed check is not a pass" rule in its prompt while having
no `checks_run` field to enforce it, and trusted the critic's self-reported
`pass` outright. The rule read as enforced and was inert.

These tests are the cheap standing guard on that. They do not check the content
of the rules — only that the copies have not diverged.
"""

import re
from pathlib import Path

from django.test import SimpleTestCase

import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / ".claude" / "hooks" / "pipeline-guard.sh"
WF = ROOT / "research" / "workflows"
AGENTS = ROOT / ".claude" / "agents"
# Fable is barred from the engine (weekly limit exhausted mid-run, 2026-08-13,
# killing three gate critics). The ban is about VOLUME, not fitness: Fable was
# running plan/crux/distribute and the stage-1 gate — the highest-call-count work
# in the engine. Jeff reopened it 2026-08-27 for high-level, low-call-count roles
# only. Every agent allowed to name Fable is listed here, so the exception stays
# a decision instead of an oversight.
FABLE_ALLOWED_AGENTS = {"topic-pm"}
SCRIPTS = ["research_topic.js", "distribute_topic.js", "refresh_topic.js"]
GATED = [
    "research_topic.js",
    "refresh_topic.js",
]  # distribute has its own shorter rules


def _read(name):
    return (WF / name).read_text()


# Rules that must exist verbatim in every script that authors or edits content.
# Not the whole RULES block — the scripts legitimately differ in emphasis
# (refresh leads with DISTILL HARD). These are the invariants; drift here means
# one script was updated and its mirror was not, which has already happened.
ALL_SCRIPTS_RULES = [
    "US spelling throughout",
    "Neutral by intention",
    "PLAIN TEXT ONLY",
    "Typographic punctuation",
    "Honest non-balance",
]
# Substance scripts only — distribute never touches facts or sources.
SUBSTANCE_RULES = [
    "SOURCE QUALITY IS JUDGED PER CLAIM",
    "Genuine steelman per position",
]


class WorkflowMirrorTests(SimpleTestCase):
    def test_scripts_exist(self):
        for name in SCRIPTS:
            self.assertTrue((WF / name).exists(), f"{name} is missing")

    def test_no_fable_defaults(self):
        """Fable's weekly limit ran out mid-run and killed three gate critics; an
        args override was NOT enough to prevent it, because the default won."""
        for name in SCRIPTS:
            self.assertNotIn(
                '?? "fable"',
                _read(name),
                f"{name} reintroduced a fable default — an args override does not reliably reach the script",
            )

    def test_fable_is_confined_to_the_allowlisted_agents(self):
        """The scripts-only check above had a hole: an agent definition naming
        `model: fable` never touches a .js file, so per-run Fable spend could
        reappear through .claude/agents/ without tripping anything. The allowlist
        is the exception made explicit."""
        for path in sorted(AGENTS.glob("*.md")):
            if "fable" not in path.read_text().lower():
                continue
            self.assertIn(
                path.stem,
                FABLE_ALLOWED_AGENTS,
                f"{path.name} names Fable but is not in FABLE_ALLOWED_AGENTS. "
                "Fable is permitted only for high-level, low-call-count roles — "
                "the 2026-08-13 limit exhaustion came from putting it on "
                "high-volume work. Add it deliberately or use opus.",
            )

    def test_allowlisted_fable_agents_exist(self):
        """An allowlist entry for a deleted agent silently widens the exception
        for whatever later takes that name."""
        for stem in FABLE_ALLOWED_AGENTS:
            self.assertTrue(
                (AGENTS / f"{stem}.md").exists(),
                f"FABLE_ALLOWED_AGENTS names {stem}, which has no definition",
            )

    def test_shared_editorial_rules_are_mirrored(self):
        for frag in ALL_SCRIPTS_RULES:
            for name in SCRIPTS:
                self.assertIn(
                    frag,
                    _read(name),
                    f"{name} is missing the mirrored rule {frag!r} — updated one script, not its mirrors",
                )

    def test_substance_rules_are_mirrored(self):
        for frag in SUBSTANCE_RULES:
            for name in GATED:
                self.assertIn(
                    frag,
                    _read(name),
                    f"{name} is missing the mirrored substance rule {frag!r}",
                )

    def test_every_gate_enforces_checks_run(self):
        """A named check that did not run must fail the verdict. The prompt rule is
        inert unless `pass` actually reads the field."""
        for name in SCRIPTS:
            src = _read(name)
            self.assertIn("checks_run", src, f"{name} lost the checks_run field")
            self.assertRegex(
                src,
                r"checks_run \|\| \[\]\)\.every\(\(c\) => c\.ran !== false\)",
                f"{name} declares checks_run but never enforces it in `pass`",
            )

    def test_pass_is_derived_not_self_reported(self):
        """`pass` must follow from evidence, never from the critic's own claim."""
        for name in SCRIPTS:
            self.assertIn(
                "!(v.blocking || []).length",
                _read(name),
                f"{name} does not derive `pass` from blocking findings",
            )

    def test_blocking_findings_require_a_quote(self):
        for name in SCRIPTS:
            self.assertIn(
                '"issue", "fix", "quote"',
                _read(name),
                f"{name} allows a blocking finding with no verbatim quote",
            )


class PipelineGuardTests(SimpleTestCase):
    """The publish guard is the enforcement behind "automation drafts, a human
    publishes". It has twice been too greedy — blocking its own commit message,
    then a heredoc that quoted the command it guards — and each loosening risks
    the opposite failure. These cases pin both edges."""

    def _verdict(self, command):
        result = subprocess.run(
            ["bash", str(HOOK)],
            input=json.dumps({"tool_input": {"command": command}}),
            capture_output=True,
            text=True,
        )
        return "BLOCK" if result.returncode == 2 else "ALLOW"

    def test_blocks_every_real_publish_invocation(self):
        for command in [
            "manage.py load_topic_draft --file x.json --slug s --status published",
            ".venv/bin/python manage.py load_topic_draft --slug s --status=published",
            "docker exec ideya python manage.py load_topic_draft --slug s --status published",
            "cd /repo && manage.py load_topic_draft --slug s --status published",
            # publish_topic reaches the loader through Python, so it never renders
            # a `--status published` string — it must be blocked by name.
            "manage.py publish_topic --slug s --confirm",
            ".venv/bin/python manage.py publish_topic --slug s --dry-run",
            "docker exec ideya python manage.py publish_topic --slug s",
            "DJANGO_DEBUG=true python manage.py runserver 8642 --noreload",
            # a heredoc whose OPENING line is a real publish still blocks
            "manage.py load_topic_draft --status published <<'EOF'\nnotes\nEOF",
        ]:
            self.assertEqual(
                "BLOCK", self._verdict(command), f"guard let this through: {command!r}"
            )

    def test_allows_documentation_that_quotes_the_command(self):
        """The review packet prints the publish command for the human to copy.
        Quoting a command is not invoking it."""
        for command in [
            "cat > doc.md <<'EOF'\nmanage.py load_topic_draft --slug s --status published\nEOF",
            "cat > doc.md <<'EOF'\nRun publish_topic --slug s --confirm when ready\nEOF",
            "git commit -F - <<'EOF'\nfix: --status published in prose\nEOF",
            "python3 - <<'PY'\nprint('load_topic_draft --status published')\nPY",
            'cat > x.sh <<-"END"\n  manage.py publish_topic --slug s\n  END',
            "manage.py load_topic_draft --file x.json --slug s --status draft",
            "grep -rn publish_topic topics/",
            "cat topics/management/commands/publish_topic.py",
            "DJANGO_DEBUG=true python manage.py runserver 8641 --noreload",
        ]:
            self.assertEqual(
                "ALLOW", self._verdict(command), f"guard falsely blocked: {command!r}"
            )


class RenderBudgetMirrorTests(SimpleTestCase):
    """budgets.py is the single source of truth for how long content may be, and
    distribute_topic.js mirrors it in a prompt because workflow scripts cannot
    import. Same hand-mirroring the verdict contract has, same guard.

    The asymmetry this closes: stage 2 decides how short everything gets and
    carried three budget numbers, while stage 1 — told by its own rules to ignore
    length and research for substance — carried fourteen. Stage 4 then
    rediscovered the overflow one topic at a time."""

    def setUp(self):
        import sys

        wf = str(WF)
        if wf not in sys.path:
            sys.path.insert(0, wf)
        import budgets

        self.budgets = budgets

    def test_db_caps_still_match_the_model(self):
        """A migration that narrows a column must not leave the table behind —
        the loader would slice content the lint calls valid."""
        self.assertEqual(
            [], self.budgets.check_db_caps(), "budgets.py has drifted from models.py"
        )

    def test_targets_never_exceed_hard_limits(self):
        for field, (_, target, hard, _) in self.budgets.BUDGETS.items():
            if hard is not None:
                self.assertLessEqual(
                    target, hard, f"{field}: target {target} above hard limit {hard}"
                )

    def test_stage_two_carries_the_budget_numbers(self):
        """Every target must actually reach the stage that writes to it."""
        src = _read("distribute_topic.js")
        self.assertIn("RENDER_BUDGETS", src, "stage 2 lost its budget block")
        for field, (_, target, _, _) in self.budgets.BUDGETS.items():
            self.assertIn(
                f"{field}: aim <= {target} chars",
                src,
                f"distribute_topic.js is missing the {field} budget — regenerate "
                "the RENDER_BUDGETS block from budgets.prompt_block()",
            )
        self.assertIn(f"<= {self.budgets.LEAN_LABEL_CAP} chars", src)
        self.assertIn(f"<= {self.budgets.UNIT_CAP} chars", src)

    def test_patch_applier_enforces_the_hard_limits(self):
        """The whitelist checks WHICH field may change; HARD_LIMITS checks that
        the new value still fits. Without it a stage-4 fix_only pass — which runs
        to fix a rendering complaint — can hand the loader a value it slices."""
        import re

        src = _read("distribute_topic.js")
        self.assertIn("HARD_LIMITS", src, "the patch applier lost its length check")
        # Only fields the whitelist lets stage 2 edit can ever reach the length
        # check; the rest are rejected on the field name first.
        pres = {
            p.strip().strip('"')
            for p in re.search(
                r"const PRES_FIELDS = new Set\(\[(.*?)\]\)", src, re.S
            )
            .group(1)
            .split(",")
            if p.strip()
        }
        block = re.search(r"const HARD_LIMITS = \{(.*?)\};", src, re.S).group(1)
        for field, (_, _, hard, _) in self.budgets.BUDGETS.items():
            if hard is None or field not in pres:
                continue
            self.assertRegex(
                block,
                rf"\b{field}: {hard}\b",
                f"HARD_LIMITS has drifted on {field} (expected {hard} from budgets.py)",
            )

    def test_distill_does_not_contradict_the_anti_template_rule(self):
        """RULES forbids copying one crux form; the distill prompt used to
        REQUIRE a rhetorical question, and 11 of 11 published leads ended in "?"."""
        src = _read("distribute_topic.js")
        self.assertNotIn("sharp rhetorical question", src)


class TallySignatureMirrorTests(SimpleTestCase):
    """tally_tokens.py classifies workflow subagents into phases by matching a
    verbatim fragment of each prompt. Reword a prompt and the fragment stops
    matching — the agent silently files under "other" and the phase breakdown
    quietly rots. Same hand-mirror problem as the verdict contract, same guard."""

    def test_every_signature_appears_in_a_workflow_script(self):
        import sys

        wf = str(WF)
        if wf not in sys.path:
            sys.path.insert(0, wf)
        import tally_tokens

        sources = "".join(_read(n) for n in SCRIPTS)
        for needle, phase in tally_tokens.SIGNATURES:
            self.assertIn(
                needle,
                sources,
                f"tally signature {needle!r} (phase {phase}) matches no workflow "
                "script — a prompt was reworded; update SIGNATURES with it",
            )

    def test_every_agent_definition_is_classifiable(self):
        """AGENT_TYPES keys are substrings matched against meta.json fields (a
        named spawn records its NAME as agentType, so exact keys miss them). The
        guard that matters is the reverse direction: every real agent definition
        must be covered by some key, or its spend files under "other"."""
        import sys

        wf = str(WF)
        if wf not in sys.path:
            sys.path.insert(0, wf)
        import tally_tokens

        for path in AGENTS.glob("*.md"):
            self.assertTrue(
                any(key in path.stem for key in tally_tokens.AGENT_TYPES),
                f"{path.name}: no AGENT_TYPES substring matches it — its token "
                "spend would be unclassifiable in the per-phase tally",
            )
