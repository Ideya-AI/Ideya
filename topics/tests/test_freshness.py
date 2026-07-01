"""Topic content-freshness cadence: volatility intervals, review-due logic, and
the `topics_due` report command."""

import datetime
from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from topics.models import Topic


class FreshnessCadenceTests(TestCase):
    def _topic(self, slug, **kw):
        return Topic.objects.create(title=slug.title(), slug=slug, **kw)

    def test_interval_by_volatility(self):
        self.assertEqual(
            self._topic("f", volatility=Topic.FAST).review_interval_days, 90
        )
        self.assertEqual(
            self._topic("m", volatility=Topic.MEDIUM).review_interval_days, 180
        )
        self.assertEqual(
            self._topic("s", volatility=Topic.SLOW).review_interval_days, 365
        )

    def test_never_touched_is_always_due(self):
        t = self._topic("never")
        self.assertIsNone(t.last_touched)
        self.assertIsNone(t.review_due_at)
        self.assertTrue(t.is_review_due)
        self.assertGreater(t.days_overdue, 100_000)

    def test_recent_review_not_due(self):
        t = self._topic("fresh", volatility=Topic.MEDIUM, reviewed_at=timezone.now())
        self.assertFalse(t.is_review_due)
        self.assertLess(t.days_overdue, 0)

    def test_old_review_is_due(self):
        old = timezone.now() - datetime.timedelta(days=200)
        t = self._topic("stale", volatility=Topic.MEDIUM, reviewed_at=old)
        self.assertTrue(t.is_review_due)  # 200 > 180-day medium interval
        self.assertGreater(t.days_overdue, 0)

    def test_reviewed_at_overrides_researched_at(self):
        now = timezone.now()
        t = self._topic(
            "both",
            volatility=Topic.FAST,
            researched_at=now - datetime.timedelta(days=200),
            reviewed_at=now,
        )
        # The clock runs from the most recent human review, not old research.
        self.assertEqual(t.last_touched, t.reviewed_at)
        self.assertFalse(t.is_review_due)

    def test_falls_back_to_researched_at(self):
        old = timezone.now() - datetime.timedelta(days=400)
        t = self._topic("researched-only", volatility=Topic.SLOW, researched_at=old)
        self.assertEqual(t.last_touched, t.researched_at)
        self.assertTrue(t.is_review_due)  # 400 > 365-day slow interval


class TopicsDueCommandTests(TestCase):
    def _topic(self, slug, **kw):
        return Topic.objects.create(title=slug.title(), slug=slug, **kw)

    def test_lists_due_topic(self):
        self._topic("due-one")  # never reviewed → due
        out = StringIO()
        call_command("topics_due", stdout=out)
        self.assertIn("due-one", out.getvalue())

    def test_hides_fresh_topic_by_default(self):
        self._topic("fresh-one", volatility=Topic.SLOW, reviewed_at=timezone.now())
        out = StringIO()
        call_command("topics_due", stdout=out)
        self.assertNotIn("fresh-one", out.getvalue())

    def test_all_flag_shows_fresh_topic(self):
        self._topic("fresh-two", volatility=Topic.SLOW, reviewed_at=timezone.now())
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
