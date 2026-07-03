"""GenAI input-summarizer command (`summarize_input`).

Network-free: the single Gemini seam (`_generate`) is monkeypatched so no API
call is made. These tests pin the command's load-bearing guarantees — it creates
exactly one InputSummary per qualifying prompt, ALWAYS as a DRAFT (never
auto-approved), records the right n_responses/model, and the --min-new gate
skips under-threshold prompts (counting only responses since the last summary).
"""

from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.test import TestCase

from topics.management.commands import summarize_input
from topics.models import InputSummary, Prompt, Response


def _stub(calls):
    """A deterministic stand-in for _generate that records every call."""

    def fake(prompt_obj, texts, stats, model):
        calls.append(
            {
                "prompt": prompt_obj,
                "texts": list(texts),
                "stats": stats,
                "model": model,
            }
        )
        return {
            "body": "Readers broadly agree, with a vocal minority dissenting.",
            "themes": [
                {"title": "Cost", "summary": "Many cite cost.", "support": "broad"}
            ],
        }

    return fake


def _run(calls, **kwargs):
    """Run summarize_input with the Gemini seam patched; return captured stdout."""
    out = StringIO()
    with mock.patch.object(summarize_input, "_generate", _stub(calls)):
        call_command("summarize_input", stdout=out, **kwargs)
    return out.getvalue()


class SummarizeInputTests(TestCase):
    def setUp(self):
        self.prompt = Prompt.objects.create(
            kind=Prompt.FREE_TEXT, text="What do you think?"
        )
        for i in range(6):  # 6 >= default min-new of 5
            Response.objects.create(
                prompt=self.prompt, session_key=f"s{i}", text=f"opinion {i}"
            )

    def test_creates_single_draft_with_correct_bookkeeping(self):
        calls = []
        _run(calls, prompt=self.prompt.id)

        summaries = InputSummary.objects.filter(prompt=self.prompt)
        self.assertEqual(summaries.count(), 1)
        s = summaries.get()
        self.assertEqual(s.status, InputSummary.DRAFT)
        self.assertEqual(s.n_responses, 6)
        self.assertEqual(s.model, summarize_input.DEFAULT_MODEL)
        self.assertTrue(s.body)
        self.assertEqual(s.themes[0]["title"], "Cost")

        # The seam was called once, with all six texts and the model.
        self.assertEqual(len(calls), 1)
        self.assertEqual(len(calls[0]["texts"]), 6)
        self.assertEqual(calls[0]["model"], summarize_input.DEFAULT_MODEL)

    def test_never_auto_approves(self):
        _run([], prompt=self.prompt.id)
        self.assertEqual(
            InputSummary.objects.exclude(status=InputSummary.DRAFT).count(), 0
        )

    def test_custom_model_is_recorded_and_passed(self):
        calls = []
        _run(calls, prompt=self.prompt.id, model="gemini-2.5-pro")
        self.assertEqual(calls[0]["model"], "gemini-2.5-pro")
        self.assertEqual(
            InputSummary.objects.get(prompt=self.prompt).model, "gemini-2.5-pro"
        )

    def test_min_new_gating_skips_under_threshold(self):
        thin = Prompt.objects.create(kind=Prompt.FREE_TEXT, text="thin?")
        for i in range(3):  # 3 < default min-new of 5
            Response.objects.create(prompt=thin, session_key=f"t{i}", text=f"meh {i}")
        calls = []
        _run(calls, prompt=thin.id)

        self.assertEqual(InputSummary.objects.filter(prompt=thin).count(), 0)
        self.assertEqual(calls, [])  # the seam was never called

    def test_blank_text_responses_do_not_count(self):
        # A structured prompt that also collects an optional 'why'; only 4 of the
        # rows carry real text, so the default min-new of 5 is not met.
        p = Prompt.objects.create(
            kind=Prompt.CHOOSE_ONE, text="which?", allow_text=True
        )
        for i in range(4):
            Response.objects.create(prompt=p, session_key=f"a{i}", text=f"because {i}")
        for i in range(3):
            Response.objects.create(prompt=p, session_key=f"b{i}", text="   ")
        calls = []
        _run(calls, prompt=p.id)
        self.assertEqual(InputSummary.objects.filter(prompt=p).count(), 0)
        self.assertEqual(calls, [])

    def test_dry_run_generates_but_saves_nothing(self):
        calls = []
        out = _run(calls, prompt=self.prompt.id, dry_run=True)
        # Generated (seam called) and printed, but nothing persisted.
        self.assertEqual(len(calls), 1)
        self.assertEqual(InputSummary.objects.filter(prompt=self.prompt).count(), 0)
        self.assertIn("Readers broadly agree", out)

    def test_min_new_counts_only_responses_since_last_summary(self):
        # An existing summary postdates the six setUp responses, so none are
        # "new" — a re-run must skip.
        InputSummary.objects.create(
            prompt=self.prompt, body="prior", n_responses=6, model="x"
        )
        calls = []
        _run(calls, prompt=self.prompt.id)
        self.assertEqual(calls, [])  # 0 new since the prior summary
        self.assertEqual(InputSummary.objects.filter(prompt=self.prompt).count(), 1)

        # Add five fresh responses → back over the threshold; a new draft is made
        # and it summarizes ALL current text responses (the full snapshot, n=11).
        for i in range(5):
            Response.objects.create(
                prompt=self.prompt, session_key=f"n{i}", text=f"new {i}"
            )
        _run(calls, prompt=self.prompt.id)
        self.assertEqual(len(calls), 1)
        self.assertEqual(InputSummary.objects.filter(prompt=self.prompt).count(), 2)
        latest = InputSummary.objects.filter(prompt=self.prompt).order_by(
            "-generated_at"
        )[0]
        self.assertEqual(latest.status, InputSummary.DRAFT)
        self.assertEqual(latest.n_responses, 11)

    def test_scan_all_active_text_prompts(self):
        # No --prompt: scans active text-collecting prompts. self.prompt qualifies;
        # an inactive prompt and a non-text prompt are both ignored.
        inactive = Prompt.objects.create(
            kind=Prompt.FREE_TEXT, text="inactive?", active=False
        )
        for i in range(6):
            Response.objects.create(prompt=inactive, session_key=f"i{i}", text=f"x {i}")
        rate = Prompt.objects.create(kind=Prompt.RATE, text="rate?")
        for i in range(6):
            Response.objects.create(prompt=rate, session_key=f"r{i}", rating=4)

        calls = []
        _run(calls)
        self.assertEqual(len(calls), 1)  # only self.prompt
        self.assertEqual(calls[0]["prompt"].id, self.prompt.id)
        self.assertEqual(InputSummary.objects.count(), 1)

    def test_non_text_prompt_is_a_clean_error(self):
        rate = Prompt.objects.create(kind=Prompt.RATE, text="rate?")
        from django.core.management.base import CommandError

        with self.assertRaises(CommandError):
            _run([], prompt=rate.id)
