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

ROOT = Path(__file__).resolve().parents[2]
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
