"""The reader-facing capture layer: the respond() view (upsert + retract for each
prompt kind, option validation, rating clamp) and that
Prompt.response_stats reflects what was captured."""

from django.test import Client, TestCase
from django.urls import reverse

from topics.models import (
    Position,
    Prompt,
    PromptOption,
    Response,
    Section,
    Topic,
)


def client():
    # SERVER_NAME pinned so tests never touch the network for ALLOWED_HOSTS.
    return Client(SERVER_NAME="127.0.0.1")


class RespondViewTests(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(title="T", slug="t")
        self.sec = Section.objects.create(topic=self.topic, kind=Section.POSITIONS)
        self.pos = Position.objects.create(section=self.sec, name="P", steelman="s")

    def _post(self, prompt, data, c=None):
        c = c or client()
        return c.post(reverse("topics:respond", args=[prompt.id]), data), c

    def test_free_text_upsert_and_retract(self):
        p = Prompt.objects.create(kind=Prompt.FREE_TEXT, text="why?")
        resp, c = self._post(p, {"text": "first"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Response.objects.filter(prompt=p).count(), 1)
        self.assertEqual(Response.objects.get(prompt=p).text, "first")

        # Same participant edits in place — still one row.
        self._post(p, {"text": "second"}, c)
        self.assertEqual(Response.objects.filter(prompt=p).count(), 1)
        self.assertEqual(Response.objects.get(prompt=p).text, "second")

        # Empty text retracts.
        self._post(p, {"text": "   "}, c)
        self.assertEqual(Response.objects.filter(prompt=p).count(), 0)

    def test_choose_one_switch_and_retract(self):
        p = Prompt.objects.create(kind=Prompt.CHOOSE_ONE, text="which?")
        o1 = PromptOption.objects.create(prompt=p, label="A")
        o2 = PromptOption.objects.create(prompt=p, label="B")

        _, c = self._post(p, {"option": o1.id})
        self.assertEqual(Response.objects.get(prompt=p).selected_ids, [o1.id])
        # Switch to the other option (still one row).
        self._post(p, {"option": o2.id}, c)
        self.assertEqual(Response.objects.get(prompt=p).selected_ids, [o2.id])
        # Empty option retracts.
        self._post(p, {"option": ""}, c)
        self.assertEqual(Response.objects.filter(prompt=p).count(), 0)

    def test_choose_one_rejects_foreign_option(self):
        p = Prompt.objects.create(kind=Prompt.CHOOSE_ONE, text="which?")
        PromptOption.objects.create(prompt=p, label="A")
        other = Prompt.objects.create(kind=Prompt.CHOOSE_ONE, text="other")
        foreign = PromptOption.objects.create(prompt=other, label="X")
        # An option that belongs to another prompt is dropped → nothing stored.
        self._post(p, {"option": foreign.id})
        self.assertEqual(Response.objects.filter(prompt=p).count(), 0)

    def test_choose_many_set_and_retract(self):
        p = Prompt.objects.create(kind=Prompt.CHOOSE_MANY, text="which?")
        o1 = PromptOption.objects.create(prompt=p, label="A")
        o2 = PromptOption.objects.create(prompt=p, label="B")

        _, c = self._post(p, {"option": [o1.id, o2.id]})
        self.assertEqual(
            sorted(Response.objects.get(prompt=p).selected_ids), [o1.id, o2.id]
        )
        # Narrow to one.
        self._post(p, {"option": [o1.id]}, c)
        self.assertEqual(Response.objects.get(prompt=p).selected_ids, [o1.id])
        # No options → retract.
        self._post(p, {}, c)
        self.assertEqual(Response.objects.filter(prompt=p).count(), 0)

    def test_rate_clamp_and_retract(self):
        p = Prompt.objects.create(kind=Prompt.RATE, text="rate")
        _, c = self._post(p, {"rating": "9"})  # clamps to 5
        self.assertEqual(Response.objects.get(prompt=p).rating, 5)
        self._post(p, {"rating": "0"}, c)  # clamps to 1
        self.assertEqual(Response.objects.get(prompt=p).rating, 1)
        self._post(p, {"rating": ""}, c)  # retract
        self.assertEqual(Response.objects.filter(prompt=p).count(), 0)

    def test_rank_csv_and_retract(self):
        p = Prompt.objects.create(kind=Prompt.RANK, text="rank")
        o1 = PromptOption.objects.create(prompt=p, label="A")
        o2 = PromptOption.objects.create(prompt=p, label="B")
        _, c = self._post(p, {"ranking": f"{o2.id},{o1.id}"})
        self.assertEqual(Response.objects.get(prompt=p).ranking, [o2.id, o1.id])
        self._post(p, {"ranking": ""}, c)
        self.assertEqual(Response.objects.filter(prompt=p).count(), 0)

    def test_structured_with_optional_text(self):
        p = Prompt.objects.create(kind=Prompt.RATE, text="rate", allow_text=True)
        o = self._post(p, {"rating": "4", "text": "because"})
        self.assertEqual(o[0].status_code, 200)
        r = Response.objects.get(prompt=p)
        self.assertEqual(r.rating, 4)
        self.assertEqual(r.text, "because")

    def test_inactive_prompt_404(self):
        p = Prompt.objects.create(kind=Prompt.FREE_TEXT, text="x", active=False)
        resp, _ = self._post(p, {"text": "hi"})
        self.assertEqual(resp.status_code, 404)


class ResponseStatsViewTests(TestCase):
    def test_stats_reflect_responses_via_view(self):
        p = Prompt.objects.create(kind=Prompt.CHOOSE_ONE, text="which?")
        o1 = PromptOption.objects.create(prompt=p, label="A")
        o2 = PromptOption.objects.create(prompt=p, label="B")
        url = reverse("topics:respond", args=[p.id])

        # Three distinct participants (each its own session) respond.
        for opt in (o1, o1, o2):
            client().post(url, {"option": opt.id})

        stats = p.response_stats
        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["by_option"][o1.id]["count"], 2)
        self.assertEqual(stats["by_option"][o2.id]["count"], 1)
