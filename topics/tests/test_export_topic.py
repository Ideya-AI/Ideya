"""Round-trip tests for the export_topic command: it must serialise the
nuclear-energy topic into the exact JSON load_topic_draft consumes, so that
re-loading reproduces the topic's sections, typed children, and key fields.
Network-free — exercises only the two management commands against the test DB
(nuclear-energy seeded via NuclearFixtureMixin; the old seed migration was
retired 2026-07-10)."""

import json
import tempfile
from io import StringIO
from pathlib import Path

from django.core.management import call_command
from django.test import TestCase

from topics.models import Action, Crux, Position, Question, Section, Stat, Topic
from topics.tests.test_core import NuclearFixtureMixin


def _counts(topic):
    """Section + typed-child counts for a topic — the round-trip invariant."""
    return {
        "sections": topic.sections.count(),
        "stats": Stat.objects.filter(section__topic=topic).count(),
        "questions": Question.objects.filter(section__topic=topic).count(),
        "positions": Position.objects.filter(section__topic=topic).count(),
        "actions": Action.objects.filter(section__topic=topic).count(),
        "cruxes": Crux.objects.filter(section__topic=topic).count(),
    }


class ExportTopicTests(NuclearFixtureMixin, TestCase):
    slug = "nuclear-energy"

    def _export_payload(self):
        """Export to stdout and parse the JSON envelope."""
        buf = StringIO()
        call_command("export_topic", slug=self.slug, out="-", stdout=buf)
        return json.loads(buf.getvalue())

    def test_envelope_wraps_draft_and_verdicts(self):
        payload = self._export_payload()
        self.assertIn("draft", payload)
        self.assertIn("verdicts", payload)
        d = payload["draft"]
        self.assertEqual(d["slug"], self.slug)
        self.assertTrue(d["overview"]["summary"])

    def test_export_has_expected_anchors(self):
        d = self._export_payload()["draft"]
        # crux lead is non-empty
        self.assertTrue(d["crux"]["lead"])
        # at least one position, carrying a colour
        self.assertTrue(d["positions"])
        self.assertTrue(any(p.get("color_key") for p in d["positions"]))
        # at least one stat and at least one action
        self.assertTrue(d["basics"]["stats"])
        self.assertTrue(d["actions"])

    def test_round_trip_reproduces_topic(self):
        original = Topic.objects.get(slug=self.slug)
        category = original.primary_category.slug  # real category slug from the DB

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ne.json"
            call_command("export_topic", slug=self.slug, out=str(path))
            self.assertTrue(path.exists())
            call_command(
                "load_topic_draft",
                file=str(path),
                slug="nuclear-energy-rt",
                title="RT",
                category=category,
                status="draft",
            )

        rt = Topic.objects.get(slug="nuclear-energy-rt")

        # counts of sections and every typed child match the original
        self.assertEqual(_counts(original), _counts(rt))

        # key field values survive the round-trip
        self.assertEqual(
            original.sections.get(kind=Section.CRUX).crux.lead,
            rt.sections.get(kind=Section.CRUX).crux.lead,
        )
        self.assertEqual(original.summary, rt.summary)

        # the additive color_key passthrough means palettes round-trip exactly
        # (by name, since display order is vote/importance-influenced)
        orig_colors = {
            p.name: p.color_key
            for p in Position.objects.filter(section__topic=original)
        }
        rt_colors = {
            p.name: p.color_key for p in Position.objects.filter(section__topic=rt)
        }
        self.assertEqual(orig_colors, rt_colors)
