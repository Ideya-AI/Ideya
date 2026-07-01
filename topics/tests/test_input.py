"""Open-participation layer: Prompt (any-scale attach), Response (upsert +
aggregation), InputSummary (editorial gate)."""

from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, transaction
from django.test import TestCase

from topics.models import (
    InputSummary,
    Position,
    Prompt,
    PromptOption,
    Response,
    Section,
    Topic,
)


class PromptModelTests(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(title="T", slug="t")
        self.sec = Section.objects.create(topic=self.topic, kind=Section.POSITIONS)
        self.pos = Position.objects.create(section=self.sec, name="P1", steelman="s")

    def test_attach_to_any_scale(self):
        ct_topic = ContentType.objects.get_for_model(Topic)
        p = Prompt.objects.create(
            kind=Prompt.FREE_TEXT,
            text="thoughts?",
            content_type=ct_topic,
            object_id=self.topic.id,
        )
        self.assertEqual(p.target, self.topic)
        ct_pos = ContentType.objects.get_for_model(Position)
        p2 = Prompt.objects.create(
            kind=Prompt.RATE,
            text="how important?",
            content_type=ct_pos,
            object_id=self.pos.id,
        )
        self.assertEqual(p2.target, self.pos)
        self.assertIn("Position", p2.target_label)

    def test_kind_helpers(self):
        ft = Prompt.objects.create(kind=Prompt.FREE_TEXT, text="why?")
        self.assertTrue(ft.collects_text)
        self.assertFalse(ft.is_structured)
        ch = Prompt.objects.create(
            kind=Prompt.CHOOSE_ONE, text="which?", allow_text=True
        )
        self.assertTrue(ch.is_structured)
        self.assertTrue(ch.collects_text)  # allow_text
        self.assertFalse(
            Prompt.objects.create(kind=Prompt.RATE, text="r").collects_text
        )

    def test_response_unique_per_session(self):
        p = Prompt.objects.create(kind=Prompt.FREE_TEXT, text="why?")
        Response.objects.create(prompt=p, session_key="s1", text="first")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Response.objects.create(prompt=p, session_key="s1", text="dup")

    def test_choose_stats(self):
        p = Prompt.objects.create(kind=Prompt.CHOOSE_ONE, text="which?")
        o1 = PromptOption.objects.create(prompt=p, label="A", order=0)
        o2 = PromptOption.objects.create(prompt=p, label="B", order=1)
        for sk, opt in [("s1", o1), ("s2", o1), ("s3", o2)]:
            Response.objects.create(prompt=p, session_key=sk, selected_ids=[opt.id])
        stats = p.response_stats
        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["by_option"][o1.id]["count"], 2)
        self.assertEqual(stats["by_option"][o2.id]["count"], 1)

    def test_rate_stats(self):
        p = Prompt.objects.create(kind=Prompt.RATE, text="rate")
        Response.objects.create(prompt=p, session_key="s1", rating=4)
        Response.objects.create(prompt=p, session_key="s2", rating=2)
        self.assertEqual(p.response_stats["mean"], 3.0)
        self.assertEqual(p.response_stats["n"], 2)

    def test_rank_stats(self):
        p = Prompt.objects.create(kind=Prompt.RANK, text="rank")
        o1 = PromptOption.objects.create(prompt=p, label="A")
        o2 = PromptOption.objects.create(prompt=p, label="B")
        Response.objects.create(prompt=p, session_key="s1", ranking=[o1.id, o2.id])
        stats = p.response_stats
        self.assertEqual(stats["by_option"][o1.id]["points"], 2)
        self.assertEqual(stats["by_option"][o2.id]["points"], 1)

    def test_text_count(self):
        p = Prompt.objects.create(kind=Prompt.FREE_TEXT, text="why?")
        Response.objects.create(prompt=p, session_key="s1", text="because")
        Response.objects.create(prompt=p, session_key="s2", text="   ")  # blank
        self.assertEqual(p.response_stats["text_count"], 1)


class InputSummaryTests(TestCase):
    def test_default_draft_then_approve(self):
        p = Prompt.objects.create(kind=Prompt.FREE_TEXT, text="why?")
        s = InputSummary.objects.create(
            prompt=p, body="readers say…", n_responses=5, model="claude-x"
        )
        self.assertEqual(s.status, InputSummary.DRAFT)
        s.status = InputSummary.APPROVED
        s.save(update_fields=["status"])
        self.assertEqual(
            InputSummary.objects.filter(status=InputSummary.APPROVED).count(), 1
        )
