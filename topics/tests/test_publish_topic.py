"""Tests for the stage-5 `publish_topic` switch.

These exist because the command CANNOT be smoke-tested by hand from an agent
session: `.claude/hooks/pipeline-guard.sh` blocks `manage.py publish_topic` by
name, which is exactly what it should do. That leaves the test suite as the only
way to verify a command that writes to the DB, so the usual "no new test files"
rule is waived here deliberately.

What matters now is that the switch is only a switch: it reads the readiness
flag, flips `status`, stamps the approval clock on the way public, writes
nothing without --confirm, and touches no content. Readiness itself is earned
upstream; here it is only an input.
"""

import json
import tempfile
from io import StringIO
from pathlib import Path

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings

from topics.models import Topic
from topics.tests.test_core import NuclearFixtureMixin


class PublishTopicTests(NuclearFixtureMixin, TestCase):
    slug = "nuclear-energy"

    def setUp(self):
        super().setUp()
        Topic.objects.filter(slug=self.slug).update(
            status=Topic.READY, reviewed_at=None
        )
        # The switch writes the topic FILE as well as the row, so point it at a
        # throwaway: a test must never publish a real topic in the working tree.
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.topics_dir = Path(self._tmp.name)
        (self.topics_dir / self.slug).mkdir()
        (self.topics_dir / self.slug / "topic.json").write_text(
            json.dumps({"slug": self.slug, "title": "Nuclear Energy",
                        "status": Topic.READY, "categories": ["climate-env"]})
        )
        patch = override_settings(TOPICS_DIR=str(self.topics_dir))
        patch.enable()
        self.addCleanup(patch.disable)

    def _filed_status(self):
        return json.loads(
            (self.topics_dir / self.slug / "topic.json").read_text()
        )["status"]

    def _run(self, **kw):
        out = StringIO()
        call_command("publish_topic", slug=self.slug, stdout=out, stderr=out, **kw)
        return out.getvalue()

    def _topic(self):
        return Topic.objects.get(slug=self.slug)

    def test_refuses_without_confirm_and_writes_nothing(self):
        with self.assertRaises(CommandError):
            self._run()
        self.assertEqual(self._topic().status, Topic.READY)
        self.assertIsNone(self._topic().reviewed_at)

    def test_dry_run_shows_the_change_and_makes_none(self):
        out = self._run(dry_run=True)
        self.assertIn("Would make public", out)
        self.assertEqual(self._topic().status, Topic.READY)
        self.assertIsNone(self._topic().reviewed_at)

    def test_confirm_publishes_and_stamps_reviewed_at(self):
        out = self._run(confirm=True)
        topic = self._topic()
        self.assertEqual(topic.status, Topic.PUBLISHED)
        self.assertEqual(
            self._filed_status(), Topic.PUBLISHED,
            "the switch changed the row but not the file, so a rebuild would undo it",
        )
        self.assertIsNotNone(topic.reviewed_at, "the approval clock was not stamped")
        self.assertIn("docker exec", out, "the live commands were not printed")

    def test_off_takes_it_private_without_touching_the_approval_clock(self):
        self._run(confirm=True)
        stamped = self._topic().reviewed_at
        self._run(off=True, confirm=True)
        topic = self._topic()
        self.assertEqual(topic.status, Topic.READY)
        self.assertEqual(
            topic.reviewed_at, stamped, "taking a topic private re-dated its approval"
        )

    def test_a_no_op_flip_is_refused(self):
        self._run(confirm=True)
        with self.assertRaises(CommandError):
            self._run(confirm=True)

    def test_an_uncertified_topic_cannot_be_made_public(self):
        Topic.objects.filter(slug=self.slug).update(status=Topic.IN_PROGRESS)
        with self.assertRaises(CommandError) as ctx:
            self._run(confirm=True)
        self.assertIn("only a topic", str(ctx.exception))
        self.assertEqual(self._topic().status, Topic.IN_PROGRESS)

    def test_off_returns_it_to_ready_not_to_in_progress(self):
        """Taking a page off the site says nothing about whether its content is
        still verified, so it must stay publishable."""
        self._run(confirm=True)
        self._run(off=True, confirm=True)
        self.assertEqual(self._topic().status, Topic.READY)

    def test_loading_reproduces_the_status_the_file_states(self):
        """The file is the source of truth, so rebuilding the database from the
        directory must not quietly demote a certified topic. Withdrawing
        readiness belongs to whatever CHANGES the content, because that is what
        invalidates the certification."""
        import json
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "t.json"
            call_command("export_topic", slug=self.slug, out=str(path))
            doc = json.loads(path.read_text())
            self.assertEqual(doc["status"], Topic.READY, "the export lost the status")
            Topic.objects.filter(slug=self.slug).update(status=Topic.IN_PROGRESS)
            call_command("load_topic_draft", file=str(path), slug=self.slug)
        self.assertEqual(self._topic().status, Topic.READY)

    def test_unloaded_slug_is_refused(self):
        Topic.objects.filter(slug=self.slug).delete()
        with self.assertRaises(CommandError):
            self._run(confirm=True)

    def test_the_switch_does_not_touch_content(self):
        """A publish must not reload, re-render or otherwise rewrite the topic —
        the thing being made public is exactly the thing that was reviewed."""
        before = {
            "title": self._topic().title,
            "summary": self._topic().summary,
            "stats": self._topic().sections.get(kind="basics").stats.count(),
            "questions": self._topic().sections.get(kind="questions").questions.count(),
        }
        self._run(confirm=True)
        topic = self._topic()
        self.assertEqual(topic.title, before["title"])
        self.assertEqual(topic.summary, before["summary"])
        self.assertEqual(
            topic.sections.get(kind="basics").stats.count(), before["stats"]
        )
        self.assertEqual(
            topic.sections.get(kind="questions").questions.count(),
            before["questions"],
        )
