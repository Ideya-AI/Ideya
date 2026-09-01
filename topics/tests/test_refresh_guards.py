"""Guards on the refresh engine specifically.

Separate from `test_workflow_mirrors.py` on purpose. Authoring is under active
development and refresh runs a few times a year; these two move on different
clocks, and the refresh guards should not be sitting in a file that authoring
work edits every week. Run them on their own:

    manage.py test topics.tests.test_refresh_guards

For what refresh has fallen BEHIND on (rather than what it has broken), see
`research/workflows/check_refresh_drift.py` — Runbook B step 0.
"""

from pathlib import Path

from django.test import SimpleTestCase

ROOT = Path(__file__).resolve().parents[2]
WF = ROOT / "research" / "workflows"


def _read(name):
    return (WF / name).read_text()


class RefreshCannotRewriteTests(SimpleTestCase):
    """A refresh corrects what moved; it does not re-author.

    That line was held in prompt language and did not hold. Told to "PRESERVE
    the topic's existing stats" and "never flatten a ranked or range viz to a
    bar", two nuclear-energy refreshes did both: 12 stats to 8 on 2026-07-03,
    then rich viz 5 to 1 on 2026-07-08 *with* the rule in the prompt. The
    richness on the live page exists because a human rebuilt it by hand.

    The line now lives in three independent code locks. These pin all three, so
    a future edit cannot quietly return refresh to whole-section regeneration —
    the shape that caused it.
    """

    def setUp(self):
        self.src = _read("refresh_topic.js")

    def test_shape_and_identity_fields_are_locked(self):
        for field in ("viz", "wide", "tier", "reveal", "prevalence_weight", "name", "text", "label"):
            self.assertRegex(
                self.src,
                rf'LOCKED = new Set\(\[[^\]]*"{field}"',
                f"refresh_topic.js no longer locks '{field}' — the fold and reader "
                "participation both depend on it staying authoring's",
            )
        self.assertIn(
            "if (LOCKED.has(e.field))",
            self.src,
            "refresh_topic.js declares LOCKED but never enforces it on an edit",
        )

    def test_every_edit_must_cite_the_work_order(self):
        self.assertIn(
            "validReasons",
            self.src,
            "refresh_topic.js has no grounding set — an edit that answers nothing "
            "on the work order would reach the draft",
        )
        self.assertIn(
            "!validReasons.has((e.because || \"\").trim())",
            self.src,
            "refresh_topic.js builds a grounding set but does not drop ungrounded edits",
        )

    def test_a_regression_gate_reverts_what_came_back_poorer(self):
        self.assertIn(
            "function regressionCheck(before, after, justified)",
            self.src,
            "refresh_topic.js lost its regression gate",
        )
        for signal in ("dropped with no cited reason", "series rows", "cut from", "removed"):
            self.assertIn(
                signal,
                self.src,
                f"the regression gate no longer detects {signal!r}",
            )
        self.assertIn(
            "applyReverts(draft, regressions)",
            self.src,
            "refresh_topic.js computes regressions but never reverts them",
        )

    def test_re_verify_returns_a_patch_not_a_section(self):
        """The root cause was the output shape: an agent asked to re-emit a
        section emits ITS section, and dropping/flattening/re-prosing is what
        regeneration is. A patch can only say what it names."""
        self.assertIn("const SECTION_PATCH = {", self.src)
        self.assertNotIn(
            "const reverify = (updated) =>",
            self.src,
            "refresh_topic.js is returning whole sections again — this is the "
            "exact shape that deleted and flattened nuclear-energy twice",
        )

    def test_confirmations_stamp_the_verification_date(self):
        """Scoped verification is only honest if a re-confirmation dates itself.
        nuclear-energy carried 5 of 12 undated stats after two refreshes because
        'verified_current' wrote nothing."""
        self.assertIn(
            "live.source_accessed = today",
            self.src,
            "a confirmed item no longer stamps source_accessed — every future "
            "scan will re-flag it and the staleness floor becomes meaningless",
        )
