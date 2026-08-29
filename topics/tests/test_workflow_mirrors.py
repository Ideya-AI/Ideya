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

    def test_stage_two_budget_table_is_machine_readable_and_matches(self):
        """The prompt block tells the AGENTS the budgets; BUDGET_LIMITS is the
        same numbers in a form the deterministic check can read. Stage 2 was
        told the budgets in prose and no code ever compared its output to them,
        which is how "stage 2 authors to the geometry" stayed true of the prompt
        and of nothing else."""
        src = _read("distribute_topic.js")
        m = re.search(r"const BUDGET_LIMITS = \{(.*?)\n\};", src, re.S)
        self.assertTrue(m, "distribute_topic.js lost BUDGET_LIMITS")
        js = dict(
            (f, (int(a), None if h == "null" else int(h)))
            for f, a, h in re.findall(
                r"(\w+): \[(\d+), (\d+|null)\]", m.group(1)
            )
        )
        for field, (_, target, hard, _) in self.budgets.BUDGETS.items():
            self.assertIn(field, js, f"BUDGET_LIMITS is missing {field}")
            self.assertEqual(
                (target, hard),
                js[field],
                f"BUDGET_LIMITS[{field}] has drifted from budgets.py",
            )

    def test_fold_capacity_is_mirrored_everywhere(self):
        """The fold caps live in models.py, are mirrored into budgets.py, and are
        now mirrored again into stage 2 — which needs them as numbers, because
        choosing the fold WITHIN the available space is the editorial decision
        and it was being made without knowing the space."""
        from topics.models import Section

        for name, (mn, mx) in self.budgets.FOLD.items():
            self.assertEqual(
                (
                    getattr(Section, f"{name.upper()}_MIN_SHOWN"),
                    getattr(Section, f"{name.upper()}_MAX_SHOWN"),
                ),
                (mn, mx),
                f"budgets.FOLD[{name}] has drifted from models.py",
            )
        src = _read("distribute_topic.js")
        m = re.search(r"const FOLD = \{(.*?)\};", src, re.S)
        self.assertTrue(m, "distribute_topic.js lost its FOLD table")
        js = {
            k: (int(a), int(b))
            for k, a, b in re.findall(r"(\w+): \[(\d+), (\d+)\]", m.group(1))
        }
        self.assertEqual(
            {k: tuple(v) for k, v in self.budgets.FOLD.items()},
            js,
            "stage 2's FOLD mirror has drifted from budgets.py",
        )


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


class GateSymmetryTests(SimpleTestCase):
    """Stage 2 was a weaker copy of stage 1's architecture. Nearly every guard
    stage 1 earned through a named failure was absent from the stage that
    produces the file that actually ships. These pin the ones that were closed,
    so the asymmetry cannot quietly come back."""

    def test_both_gates_break_ties_on_blocking_count(self):
        """A round that closes 3 of 4 blocking findings but still fails the
        critic scores equal on passes. Without the tie-break it is DISCARDED and
        the unfixed draft ships — the democratic-backsliding failure, which
        stage 1 fixed and stage 2 kept for another two months."""
        for name in ("research_topic.js", "distribute_topic.js"):
            src = _read(name)
            self.assertIn(
                "const blockCount =",
                src,
                f"{name} has no blocking-count tie-break in keep-best",
            )
            self.assertRegex(
                src,
                r"pc === best\.passes && bc < best\.blocks|p === best\.passes && b < best\.blocks",
                f"{name} computes blockCount but does not use it to break ties",
            )

    def test_both_gates_cap_unguided_judgment_rounds(self):
        """Rounds are asymmetric: externally-grounded findings are worth
        iterating on, a critic's round-2 opinion is not (arXiv 2310.01798).
        Stage 2 ran three unanchored rounds on findings that were ALL judgment
        until it had deterministic and fidelity checks to ground them, and
        refresh ran three on the same footing."""
        for name in SCRIPTS:
            src = _read(name)
            self.assertIn(
                "const grounded = failing.some(",
                src,
                f"{name} does not distinguish grounded findings from judgment ones",
            )
            self.assertIn(
                "if (round > 1 && !grounded)",
                src,
                f"{name} lets unguided judgment findings run past one round",
            )

    def test_deterministic_findings_are_gate_input_every_round(self):
        """Computed once and concatenated once, a deterministic verdict drops out
        of the verdict set after the first fix round: its blocking count vanishes
        whether or not the defect was fixed, so keep-best can select a draft that
        still carries it. Both stages must rebuild the verdict from the CURRENT
        draft on every round."""
        for name, fn in (
            ("research_topic.js", "shapeVerdict"),
            ("distribute_topic.js", "presentationVerdict"),
        ):
            src = _read(name)
            self.assertIn(
                f"function {fn}(d)",
                src,
                f"{name}'s deterministic check is not a function of the draft",
            )
            self.assertRegex(
                src,
                r"async function fullGate\(d\)",
                f"{name} has no single gate that scores every source each round",
            )
            self.assertIn(
                f"{fn}(d)",
                src.split("async function fullGate(d)")[1][:400],
                f"{name}'s fullGate does not include {fn}",
            )
            self.assertIn(
                "await fullGate(draft)",
                src,
                f"{name}'s fix loop does not re-gate through fullGate",
            )

    def test_verification_terminates_on_the_shipped_draft(self):
        """The ledger was extracted before the fix loop and never re-run, so
        every sentence the loop rewrote left the run unverified while still
        counting as coverage: of 259 claims across four topics, only 129 were
        still asserted verbatim in stage 1's own final draft. Stage 1 must close
        its ledger on the final draft; stage 2 must check that its rewrites did
        not move a verified claim."""
        self.assertIn(
            "async function closeLedger(",
            _read("research_topic.js"),
            "stage 1 no longer closes its ledger on the final draft",
        )
        src = _read("distribute_topic.js")
        self.assertIn(
            "async function fidelityVerdict(",
            src,
            "stage 2 no longer checks that its rewrites preserved verified claims",
        )
        self.assertIn(
            "dossier.claim_ledger",
            src,
            "stage 2 does not read the ledger it is supposed to protect",
        )

    def test_reveal_belongs_to_stage_two(self):
        """`reveal` is a fold decision. Three stage-1 research agents were each
        assigning a display layer with no knowledge of the display, and stage 2
        reassigned it anyway — schema budget spent on a field whose value was
        discarded, in schemas that have twice hit the classifier's size limit."""
        self.assertNotIn(
            '"condensed", "normal", "deep"',
            _read("research_topic.js"),
            "stage 1 is emitting `reveal` again — it is stage 2's to assign",
        )
        self.assertIn(
            'x.reveal = (x.tier ?? 1) === 1 ? "condensed" : "normal"',
            _read("distribute_topic.js"),
            "stage 2 does not seed `reveal`; unset means the loader defaults "
            "every item to condensed and the whole topic lands in the "
            "always-visible layer",
        )


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
