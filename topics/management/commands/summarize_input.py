"""Draft a GenAI "what readers think" digest of a Prompt's free-text Responses.

Amazon-review-style synthesis of reader opinions for the open-participation
layer: themes, where readers agree/disagree, and representative *paraphrased*
views (never verbatim, never any email/PII). The result is written as an
``InputSummary`` with ``status=DRAFT`` only — an editor approves it in the admin
before it ever surfaces publicly (decision D: AI drafts, a human publishes).
This command therefore NEVER creates an approved summary.

This runs OUT-OF-BAND, not in the request path. Structured participation
(votes, stances, question leans) is captured and shown live in the app; the
free-text input is aggregated here on an occasional cadence — an editor runs
this by hand or on a schedule, the same "AI drafts → human publishes" shape as
the authoring engine. Nothing on the reader-facing pages waits on it.

  manage.py summarize_input                       # every active text-collecting prompt
  manage.py summarize_input --prompt 12           # just one prompt
  manage.py summarize_input --min-new 10          # require 10 new responses
  manage.py summarize_input --model claude-opus-4-8
  manage.py summarize_input --dry-run             # print the digest, save nothing

For each prompt that collects text and has at least ``--min-new`` text responses
*since its most recent summary*, the free-text responses plus the structured
distribution (``Prompt.response_stats``) are sent to Claude, which returns a
concise digest. The actual API call lives behind ``_generate`` (the SDK is
imported there, lazily) so it can be monkeypatched in tests; a missing key or
SDK exits gracefully with an actionable message rather than a traceback.
"""

import json
import os

from django.core.management.base import BaseCommand, CommandError

from topics.models import InputSummary, Prompt

# Claude is the provider for this background editorial job (claude-api skill's
# default: the latest, most capable Opus-tier model).
DEFAULT_MODEL = "claude-opus-4-8"
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

# Structured-output schema (output_config.format): a digest body plus optional
# typed themes. Kept to plain types + required + additionalProperties:false so it
# is accepted as-is (no unsupported numeric/length constraints).
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
                "additionalProperties": False,
            },
        },
    },
    "required": ["body", "themes"],
    "additionalProperties": False,
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
    """The single seam to the Anthropic API — tests monkeypatch this.

    Returns ``{"body": str, "themes": list}``. The SDK is imported here, lazily,
    so a missing dependency or missing API key raises ``SummarizerError`` (the
    command turns it into a clean CommandError) instead of failing at import.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SummarizerError(
            "ANTHROPIC_API_KEY is not set — export it before running "
            "summarize_input (generating the digest needs the Claude API)."
        )
    try:
        import anthropic
    except ImportError as exc:  # pragma: no cover - environment-dependent
        raise SummarizerError(
            "The 'anthropic' SDK is not installed — run `pip install anthropic`."
        ) from exc

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model,
        max_tokens=16000,
        # Adaptive thinking for the synthesis; medium effort balances cost/quality.
        thinking={"type": "adaptive"},
        output_config={
            "effort": "medium",
            "format": {"type": "json_schema", "schema": _SCHEMA},
        },
        system=_SYSTEM,
        messages=[
            {"role": "user", "content": _build_user_content(prompt_obj, texts, stats)}
        ],
    )
    # output_config.format guarantees the final text block is valid JSON.
    raw = next((b.text for b in response.content if b.type == "text"), "")
    data = json.loads(raw)
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
            help=f"Claude model id (default {DEFAULT_MODEL}).",
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
