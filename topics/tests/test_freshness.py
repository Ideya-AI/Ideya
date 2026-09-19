"""Topic content-freshness cadence: the shared review interval, review-due
logic, and the `topics_due` report command."""

import datetime
from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from topics.models import Topic


class FreshnessCadenceTests(TestCase):
    def _topic(self, slug, **kw):
        return Topic.objects.create(title=slug.title(), slug=slug, **kw)

    def test_shared_interval(self):
        self.assertEqual(self._topic("f").review_interval_days, 180)

    def test_never_touched_is_always_due(self):
        t = self._topic("never")
        self.assertIsNone(t.last_touched)
        self.assertIsNone(t.review_due_at)
        self.assertTrue(t.is_review_due)
        self.assertGreater(t.days_overdue, 100_000)

    def test_recent_review_not_due(self):
        t = self._topic("fresh", reviewed_at=[timezone.now().isoformat()])
        self.assertFalse(t.is_review_due)
        self.assertLess(t.days_overdue, 0)

    def test_old_review_is_due(self):
        old = timezone.now() - datetime.timedelta(days=200)
        t = self._topic("stale", reviewed_at=[old.isoformat()])
        self.assertTrue(t.is_review_due)  # 200 > the 180-day interval
        self.assertGreater(t.days_overdue, 0)

    def test_latest_review_overrides_authored_at(self):
        now = timezone.now()
        older = now - datetime.timedelta(days=300)
        t = self._topic(
            "both",
            authored_at=now - datetime.timedelta(days=200),
            reviewed_at=[older.isoformat(), now.isoformat()],
        )
        # The clock runs from the most recent review, not the oldest or the
        # authoring date.
        self.assertEqual(t.last_touched, t.last_reviewed_at)
        self.assertFalse(t.is_review_due)

    def test_falls_back_to_authored_at(self):
        old = timezone.now() - datetime.timedelta(days=400)
        t = self._topic("authored-only", authored_at=old)
        self.assertEqual(t.last_touched, t.authored_at)
        self.assertTrue(t.is_review_due)  # 400 > the 180-day interval


class TopicsDueCommandTests(TestCase):
    def _topic(self, slug, **kw):
        # The queue defaults to published topics (2026-08-03: the catalog's
        # ~130 unauthored draft stubs are "always due" and drowned it).
        kw.setdefault("status", Topic.PUBLISHED)
        return Topic.objects.create(title=slug.title(), slug=slug, **kw)

    def test_lists_due_topic(self):
        self._topic("due-one")  # never reviewed → due
        out = StringIO()
        call_command("topics_due", stdout=out)
        self.assertIn("due-one", out.getvalue())

    def test_hides_fresh_topic_by_default(self):
        self._topic("fresh-one", reviewed_at=[timezone.now().isoformat()])
        out = StringIO()
        call_command("topics_due", stdout=out)
        self.assertNotIn("fresh-one", out.getvalue())

    def test_all_flag_shows_fresh_topic(self):
        self._topic("fresh-two", reviewed_at=[timezone.now().isoformat()])
        out = StringIO()
        call_command("topics_due", "--all", stdout=out)
        self.assertIn("fresh-two", out.getvalue())

    def test_json_output_is_valid(self):
        import json

        self._topic("due-json")
        out = StringIO()
        call_command("topics_due", "--json", stdout=out)
        data = json.loads(out.getvalue())
        self.assertTrue(any(r["slug"] == "due-json" for r in data))
