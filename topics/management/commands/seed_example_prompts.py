"""Seed the open-participation prompts behind a topic's "Add your view" modal:
a multi-select over the positions ("Align"), a multi-select over the open
questions, and a free-text catch-all. Idempotent — clears the topic's prior
prompts and reseeds, so re-running never accumulates. The loader calls
`seed_topic_prompts` after every load so no authored topic ships without its
participation endcap."""

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from topics.models import Position, Prompt, PromptOption, Question, Topic


def seed_topic_prompts(topic) -> int:
    """(Re)create the standard three Add-your-view prompts on a topic.

    Deletes the topic's prior topic-level prompts first — which cascades any
    reader Responses to them — so on a content reload the prompt options track
    the rebuilt positions/questions instead of dangling.
    """
    topic_ct = ContentType.objects.get_for_model(Topic)
    positions = list(
        Position.objects.filter(
            section__topic=topic, section__kind="positions"
        ).order_by("-prevalence_weight", "order", "id")
    )
    questions = list(
        Question.objects.filter(
            section__topic=topic, section__kind="questions"
        ).order_by("-votes", "order", "id")
    )

    Prompt.objects.filter(content_type=topic_ct, object_id=topic.id).delete()

    # 1 — Align: multi-select across the mapped positions.
    align = Prompt.objects.create(
        content_type=topic_ct,
        object_id=topic.id,
        kind=Prompt.CHOOSE_MANY,
        text="Which of these positions do you align with?",
        help_text="",
        allow_text=True,
        active=True,
        order=1,
    )
    for i, pos in enumerate(positions):
        PromptOption.objects.create(prompt=align, label=pos.name, position=pos, order=i)

    # 2 — Questions: multi-select across the open questions.
    qprompt = Prompt.objects.create(
        content_type=topic_ct,
        object_id=topic.id,
        kind=Prompt.CHOOSE_MANY,
        text="Which of these questions are most important to you?",
        help_text="",
        active=True,
        order=2,
    )
    for i, q in enumerate(questions):
        PromptOption.objects.create(prompt=qprompt, label=q.text, order=i)

    # 3 — Your take: open text.
    Prompt.objects.create(
        content_type=topic_ct,
        object_id=topic.id,
        kind=Prompt.FREE_TEXT,
        text="Anything the positions and questions miss?",
        help_text="",
        active=True,
        order=3,
    )
    return len(positions) + len(questions)


class Command(BaseCommand):
    help = "Seed the Add-your-view prompts on a topic (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--slug",
            default="nuclear-energy",
            help="Topic slug to seed (default: nuclear-energy).",
        )

    def handle(self, *args, **options):
        slug = options["slug"]
        topic = Topic.objects.filter(slug=slug).first()
        if not topic:
            self.stderr.write(
                self.style.ERROR(f"Topic '{slug}' not found — load content first.")
            )
            return
        seed_topic_prompts(topic)
        self.stdout.write(
            self.style.SUCCESS(f"Seeded 3 Add-your-view prompts on {slug}.")
        )
