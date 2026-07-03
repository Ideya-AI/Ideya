"""Draft a GenAI "what readers think" digest of a Prompt's free-text Responses.

Amazon-review-style synthesis of reader opinions for the open-participation
layer: themes, where readers agree/disagree, and representative *paraphrased*
views (never verbatim, never any email/PII). The result is written as an
``InputSummary`` with ``status=DRAFT`` only — an editor approves it in the admin
before it ever surfaces publicly (decision D: AI drafts, a human publishes).
This command therefore NEVER creates an approved summary.

  manage.py summarize_input                       # every active text-collecting prompt
  manage.py summarize_input --prompt 12           # just one prompt
  manage.py summarize_input --min-new 10          # require 10 new responses
  manage.py summarize_input --model gemini-2.5-pro
  manage.py summarize_input --dry-run             # print the digest, save nothing

For each prompt that collects text and has at least ``--min-new`` text responses
*since its most recent summary*, the free-text responses plus the structured
distribution (``Prompt.response_stats``) are sent to Gemini, which returns a
concise digest. The actual API call lives behind ``_generate`` (the SDK is
imported there, lazily) so it can be monkeypatched in tests; a missing key or
SDK exits gracefully with an actionable message rather than a traceback.
"""

import json
import os

from django.core.management.base import BaseCommand, CommandError

from topics.models import InputSummary, Prompt

# Gemini is the app's AI provider. Flash balances cost and quality for this
# reader-opinion synthesis; pass --model gemini-2.5-pro for the higher tier.
DEFAULT_MODEL = "gemini-2.5-flash"
DEFAULT_MIN_NEW = 5

_SYSTEM = (
    'You write an Amazon-review-style "what readers think" digest summarizing '
    "the free-text opinions readers submitted in response to a single prompt on "
    "a curated atlas of hard topics.\n\n"
    "Rules:\n"
    "- Be fair and neutral. Represent each side in its own strongest terms "
    "(steelman); do not editorialize or fact-check the readers.\n"
    "- Identify the main themes, and call out clearly where readers AGREE and "
    "where they DISAGREE.\n"
    "- Any representative opinions must be PARAPHRASED in your own words. NEVER "
    "quote a reader verbatim.\n"
    "- NEVER reproduce any email address, name, handle, URL, or other personal "
    "or identifying detail that appears in a response.\n"
    "- Be concise — a few short paragraphs at most. This is a reader-opinion "
    "digest, clearly distinct from the topic's editorial content.\n"
    "- If the structured distribution is provided, weave it in (e.g. how the "
    "vote/rating split relates to what people wrote)."
)

# Structured-output schema (Gemini response_schema): a digest body plus typed
# themes. Kept to the OpenAPI subset Gemini accepts — plain types + required,
# no `additionalProperties` and no numeric/length constraints.
_SCHEMA = {
    "type": "object",
    "properties": {
        "body": {
            "type": "string",
            "description": "The reader-opinion digest, a few short paragraphs.",
        },
        "themes": {
            "type": "array",
            "description": "Distinct themes surfaced across the responses.",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "summary": {"type": "string"},
                    "support": {
                        "type": "string",
                        "description": "How widely held, e.g. 'broad agreement', "
                        "'contested', 'minority view'.",
                    },
                },
                "required": ["title", "summary", "support"],
                "property_ordering": ["title", "summary", "support"],
            },
        },
    },
    "required": ["body", "themes"],
    "property_ordering": ["body", "themes"],
}


class SummarizerError(Exception):
    """Configuration problem (missing key / SDK) — surfaced as a clean message."""


def _build_user_content(prompt_obj, texts, stats):
    """Assemble the user turn: the prompt, the structured distribution, then the
    paraphrase-only reader responses."""
    parts = [f"Prompt shown to readers: {prompt_obj.text}"]
    if prompt_obj.help_text:
        parts.append(f"Prompt help text: {prompt_obj.help_text}")
    parts.append(
        "\nStructured response distribution (counts/means as available): "
        + json.dumps(stats, default=str)
    )
    parts.append(
        f"\n{len(texts)} free-text reader response(s) follow. Paraphrase only — "
        "never quote verbatim, and never reproduce any email or personal "
        "identifier from them.\n"
    )
    for i, text in enumerate(texts, 1):
        parts.append(f"[{i}] {text[:2000]}")
    return "\n".join(parts)


def _generate(prompt_obj, texts, stats, model):
    """The single seam to the Gemini API — tests monkeypatch this.

    Returns ``{"body": str, "themes": list}``. The SDK is imported here, lazily,
    so a missing dependency or missing API key raises ``SummarizerError`` (the
    command turns it into a clean CommandError) instead of failing at import.
    """
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise SummarizerError(
            "GEMINI_API_KEY is not set — export it before running "
            "summarize_input (generating the digest needs the Gemini API)."
        )
    try:
        from google import genai
        from google.genai import types
    except ImportError as exc:  # pragma: no cover - environment-dependent
        raise SummarizerError(
            "The 'google-genai' SDK is not installed — run `pip install google-genai`."
        ) from exc

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=_build_user_content(prompt_obj, texts, stats),
        config=types.GenerateContentConfig(
            system_instruction=_SYSTEM,
            # Constrain the output to the digest schema so response.text is JSON.
            response_mime_type="application/json",
            response_schema=_SCHEMA,
        ),
    )
    data = json.loads(response.text)
    return {"body": data["body"], "themes": data.get("themes", [])}


class Command(BaseCommand):
    help = (
        "Draft an editor-gated GenAI digest of readers' free-text responses to a "
        "prompt. Creates InputSummary(status=DRAFT) only — never auto-approves."
    )

    def add_arguments(self, p):
        p.add_argument(
            "--prompt",
            type=int,
            default=None,
            help="Prompt id to summarize. Omit to scan every active text-collecting prompt.",
        )
        p.add_argument(
            "--min-new",
            type=int,
            default=DEFAULT_MIN_NEW,
            help=f"Minimum new text responses since the last summary (default {DEFAULT_MIN_NEW}).",
        )
        p.add_argument(
            "--model",
            default=DEFAULT_MODEL,
            help=f"Gemini model id (default {DEFAULT_MODEL}).",
        )
        p.add_argument(
            "--dry-run",
            action="store_true",
            help="Generate and print the digest without saving an InputSummary.",
        )

    def handle(self, *args, **o):
        prompt_id = o["prompt"]
        min_new = o["min_new"]
        model = o["model"]
        dry_run = o["dry_run"]

        prompts = self._select_prompts(prompt_id)

        created = 0
        for prompt in prompts:
            if self._summarize_one(prompt, min_new, model, dry_run):
                created += 1

        if not dry_run:
            self.stdout.write(
                self.style.SUCCESS(f"done — {created} draft summary(ies) created")
            )

    def _select_prompts(self, prompt_id):
        """One explicit prompt (validated), else every active text-collecting one."""
        if prompt_id is not None:
            prompt = Prompt.objects.filter(pk=prompt_id).first()
            if prompt is None:
                raise CommandError(f"prompt {prompt_id} not found")
            if not prompt.collects_text:
                raise CommandError(
                    f"prompt {prompt_id} ({prompt.get_kind_display()}) does not "
                    "collect free text — nothing to summarize."
                )
            return [prompt]
        # collects_text is a property, so filter active in the DB and text in Python.
        return [p for p in Prompt.objects.filter(active=True) if p.collects_text]

    def _summarize_one(self, prompt, min_new, model, dry_run):
        """Generate one draft for ``prompt`` if it clears the --min-new gate.
        Returns True iff an InputSummary was saved."""
        responses = list(prompt.responses.order_by("created_at", "id"))
        texts = [(r.text or "").strip() for r in responses]
        # Keep responses (and texts) aligned so the "new since" cutoff is accurate.
        text_pairs = [(r, t) for r, t in zip(responses, texts) if t]
        if not text_pairs:
            self.stdout.write(f"prompt {prompt.id}: no text responses — skipped")
            return False

        last = prompt.summaries.order_by("-generated_at").first()
        cutoff = last.generated_at if last else None
        new_count = sum(
            1 for r, _ in text_pairs if cutoff is None or r.created_at > cutoff
        )
        if new_count < min_new:
            self.stdout.write(
                f"prompt {prompt.id}: {new_count} new text response(s) "
                f"< min-new {min_new} — skipped"
            )
            return False

        digest_texts = [t for _, t in text_pairs]
        try:
            result = _generate(prompt, digest_texts, prompt.response_stats, model)
        except SummarizerError as exc:
            raise CommandError(str(exc))

        body = result["body"]
        themes = result.get("themes", [])
        n = len(digest_texts)

        if dry_run:
            self.stdout.write(
                f"\n--- prompt {prompt.id}: {prompt.text} "
                f"(n={n}, {new_count} new) ---\n{body}\n"
                f"themes: {json.dumps(themes, indent=2)}\n"
            )
            return False

        InputSummary.objects.create(
            prompt=prompt,
            body=body,
            themes=themes,
            n_responses=n,
            model=model,
            status=InputSummary.DRAFT,
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"prompt {prompt.id}: draft summary created (n={n}, {new_count} new)"
            )
        )
        return True
