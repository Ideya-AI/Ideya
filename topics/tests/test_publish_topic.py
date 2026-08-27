"""Tests for the stage-5 `publish_topic` command.

These exist because the command CANNOT be smoke-tested by hand from an agent
session: `.claude/hooks/pipeline-guard.sh` blocks `manage.py publish_topic` by
name, which is exactly what it should do. That leaves the test suite as the only
way to verify a command that writes to the DB, so the usual "no new test files"
rule is waived here deliberately.

What matters is the preflight: it must refuse to publish when a stage-4/4.5
artifact is missing, and it must never write anything without --confirm.
"""

import json
import tempfile
from io import StringIO
from pathlib import Path
from unittest import mock

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from topics.models import Topic
from topics.tests.test_core import NuclearFixtureMixin


class PublishTopicTests(NuclearFixtureMixin, TestCase):
    slug = "nuclear-energy"

    def setUp(self):
        super().setUp()
        Topic.objects.filter(slug=self.slug).update(
            status=Topic.DRAFT, reviewed_at=None
        )

    def _export(self, tmp):
        path = Path(tmp) / f"{self.slug}.json"
        call_command("export_topic", slug=self.slug, out=str(path))
        return path

    def _run(self, path, exists=True, links_clean=True, **kw):
        """Run publish_topic with artifact existence and the link check stubbed:
        the real ones touch the working tree and the network."""
        link_line = (
            "Summary: 3 links  ·  3 ok  ·  0 placeholder  ·  0 dead"
            if links_clean
            else "Summary: 3 links  ·  2 ok  ·  0 placeholder  ·  1 dead"
        )

        def fake_check_links(*a, **k):
            k["stdout"].write(link_line)

        real = call_command
        real_exists = Path.exists

        def artifact_exists(self):
            # The topic JSON must always resolve — `exists` here controls only
            # the stage-3/4 artifacts (icon brief, primary art, OG card).
            if self.suffix == ".json":
                return real_exists(self)
            return exists

        with mock.patch.object(Path, "exists", artifact_exists), mock.patch(
            "topics.management.commands.publish_topic.call_command"
        ) as cc:
            cc.side_effect = lambda name, *a, **k: (
                fake_check_links(*a, **k)
                if name == "check_links"
                else real(name, *a, **k)
            )
            out = StringIO()
            call_command(
                "publish_topic", slug=self.slug, file=str(path), stdout=out, **kw
            )
            return out.getvalue(), cc

    def test_refuses_without_confirm_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._export(tmp)
            with self.assertRaises(CommandError):
                self._run(path)
        self.assertEqual(Topic.objects.get(slug=self.slug).status, Topic.DRAFT)
        self.assertIsNone(Topic.objects.get(slug=self.slug).reviewed_at)

    def test_dry_run_shows_the_plan_and_changes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._export(tmp)
            out, _ = self._run(path, dry_run=True)
        self.assertIn("Would run:", out)
        self.assertIn("--reviewed", out)
        self.assertEqual(Topic.objects.get(slug=self.slug).status, Topic.DRAFT)

    def test_missing_artifact_blocks_the_publish(self):
        """A missing OG card or icon is a stage-4 defect; it must stop the
        publish rather than ship a topic whose link previews are the generic
        site image."""
        with tempfile.TemporaryDirectory() as tmp:
            path = self._export(tmp)
            with self.assertRaises(CommandError) as ctx:
                self._run(path, exists=False, confirm=True)
        self.assertIn("not publishing", str(ctx.exception).lower())
        self.assertEqual(Topic.objects.get(slug=self.slug).status, Topic.DRAFT)

    def test_dead_link_blocks_the_publish(self):
        """Links are checked BEFORE the publish. Checking afterwards means
        finding a dead link on a topic that is already live."""
        with tempfile.TemporaryDirectory() as tmp:
            path = self._export(tmp)
            with self.assertRaises(CommandError):
                self._run(path, links_clean=False, confirm=True)
        self.assertEqual(Topic.objects.get(slug=self.slug).status, Topic.DRAFT)

    def test_confirm_publishes_and_stamps_reviewed_at(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._export(tmp)
            out, _ = self._run(path, confirm=True)
        topic = Topic.objects.get(slug=self.slug)
        self.assertEqual(topic.status, Topic.PUBLISHED)
        self.assertIsNotNone(
            topic.reviewed_at, "reviewed_at not stamped — topics_due will re-queue it"
        )
        self.assertIn("docker exec", out, "the live-push commands were not printed")

    def test_unloaded_slug_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._export(tmp)
            Topic.objects.filter(slug=self.slug).delete()
            with self.assertRaises(CommandError):
                self._run(path, confirm=True)
