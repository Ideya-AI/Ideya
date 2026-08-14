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

WF = Path(__file__).resolve().parents[2] / "research" / "workflows"
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
