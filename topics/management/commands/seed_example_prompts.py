"""Seed a topic's open-participation prompts: the three behind the "Add your
view" modal (a multi-select over the positions ("Align"), a multi-select over
the open questions, and a free-text catch-all) plus the per-item follow-ups
that open in a modal when a reader upvotes a question or a position, leans
to one of a question's poles, taps the respond button under an expanded
fact / question / position, or a section's Something-missing button (one to
three each, always with an open-ended one). Idempotent — clears the topic's prior prompts
and reseeds, so re-running never accumulates. The loader calls
`seed_topic_prompts` after every load so no authored topic ships without its
participation endcap."""

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from topics.models import Position, Prompt, PromptOption, Question, Section, Stat, Topic

# Follow-ups, templated per item type and trigger. The modal names the item
# the reader just acted on; these ask what the click alone can't carry. Lean
# prompts take {a} / {b} — the question's own pole labels.
QUESTION_VOTE_FOLLOW_UPS = [
    dict(
        kind=Prompt.CHOOSE_ONE,
        text="Why does this question matter to you?",
        options=[
            "It decides where I land",
            "It’s where the sides talk past each other",
            "It’s under-discussed",
        ],
    ),
    dict(
        kind=Prompt.FREE_TEXT,
        text="What would it take to settle it for you?",
    ),
]
QUESTION_LEAN_FOLLOW_UPS = [
    dict(
        kind=Prompt.CHOOSE_ONE,
        text="How firmly do you lean “{a}”?",
        options=["Firmly", "On balance", "Could go either way"],
    ),
    dict(
        kind=Prompt.FREE_TEXT,
        text="What makes you lean “{a}” rather than “{b}”?",
    ),
]
# Respond button at the foot of every expanded fact / question / position: a
# verdict, what should happen to it (multi-select, each with a note), and an
# open channel. {verdict} is the per-type first prompt.
RESPOND_VERDICTS = {
    "stat": "Does this fact hold up?",
    "question": "Is this the right question?",
    "position": "Is this position fairly stated?",
}
RESPOND_FOLLOW_UPS = [
    dict(
        kind=Prompt.CHOOSE_ONE,
        text="{verdict}",
        options=["Agree", "Disagree", "Unsure"],
    ),
    dict(
        kind=Prompt.CHOOSE_MANY,
        text="What should happen to it?",
        help_text="Pick any that apply — a note on each helps the editor.",
        options=["Keep as is", "Promote", "Demote", "Reword", "Remove"],
    ),
    dict(
        kind=Prompt.FREE_TEXT,
        text="Suggest a rewording, or say why.",
    ),
]
# "Something missing?" beside a section's Show less: the add-in-place channel.
MISSING_FOLLOW_UPS = {
    "basics": [
        dict(
            kind=Prompt.FREE_TEXT,
            text="What number is missing from the basics?",
            help_text="Say where it comes from, if you can.",
        ),
    ],
    "questions": [
        dict(
            kind=Prompt.FREE_TEXT,
            text="What question is missing?",
            help_text="The best ones are questions the sides answer differently.",
        ),
    ],
    "positions": [
        dict(
            kind=Prompt.FREE_TEXT,
            text="What position is missing?",
            help_text="Who holds it, and what’s its strongest case?",
        ),
    ],
}
POSITION_FOLLOW_UPS = [
    dict(
        kind=Prompt.CHOOSE_ONE,
        text="How close is this to your own view?",
        options=["It’s my view", "Close, with reservations", "Not mine, but it matters"],
    ),
    dict(
        kind=Prompt.FREE_TEXT,
        text="Where does it get things right — or wrong?",
    ),
]


def _upsert_prompt(kept, ct, object_id, order, **fields):
    """One prompt, identified by where it hangs and its slot — never recreated.
    A reader Response points at the Prompt row, so replacing the row destroys
    the answer. Options carry no reader data and are rewritten freely."""
    options = fields.pop("options", [])
    prompt, _ = Prompt.objects.update_or_create(
        content_type=ct, object_id=object_id, order=order,
        trigger=fields.pop("trigger", ""),
        defaults={"active": True, **fields},
    )
    kept.add(prompt.pk)
    prompt.options.all().delete()
    for j, label in enumerate(options):
        PromptOption.objects.create(prompt=prompt, label=label, order=j)
    return prompt


def _seed_item_prompts(kept, ct, objs, trigger, specs, labels=lambda obj: {}):
    n = 0
    for obj in objs:
        fmt = labels(obj)
        for i, spec in enumerate(specs):
            _upsert_prompt(
                kept, ct, obj.id, i + 1,
                kind=spec["kind"],
                trigger=trigger,
                text=spec["text"].format(**fmt),
                help_text=spec.get("help_text", ""),
                options=spec.get("options", []),
            )
            n += 1
    return n


def seed_topic_prompts(topic) -> int:
    """(Re)create the standard three Add-your-view prompts on a topic plus the
    vote follow-ups on each of its questions and positions. Returns the number
    of prompts created.

    Idempotent, and deliberately so: prompts are upserted in place and only the
    ones this run did not produce are removed. Deleting and recreating them
    instead would cascade every reader Response, on every content reload. Item
    prompts whose question/position is gone are still swept, because a
    GenericForeignKey does not cascade.
    """
    ct = ContentType.objects.get_for_model
    topic_ct, question_ct, position_ct, stat_ct, section_ct = (
        ct(Topic), ct(Question), ct(Position), ct(Stat), ct(Section),
    )
    sections = list(
        Section.objects.filter(topic=topic, kind__in=MISSING_FOLLOW_UPS).order_by("id")
    )
    stats = list(
        Stat.objects.filter(section__topic=topic, section__kind="basics").order_by(
            "order", "id"
        )
    )
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

    # Orphan sweep: a GenericForeignKey does not cascade, so prompts whose
    # target row is gone would linger for ever.
    for target_ct, model in (
        (topic_ct, Topic), (question_ct, Question), (position_ct, Position),
        (stat_ct, Stat), (section_ct, Section),
    ):
        Prompt.objects.filter(content_type=target_ct).exclude(
            object_id__in=model.objects.values("id")
        ).delete()

    kept = set()

    # 1 — Align: multi-select across the mapped positions.
    align = _upsert_prompt(
        kept, topic_ct, topic.id, 1,
        kind=Prompt.CHOOSE_MANY,
        text="Which of these positions do you align with?",
        help_text="",
        allow_text=True,
    )
    for i, pos in enumerate(positions):
        PromptOption.objects.create(prompt=align, label=pos.name, position=pos, order=i)

    # 2 — Questions: multi-select across the open questions.
    qprompt = _upsert_prompt(
        kept, topic_ct, topic.id, 2,
        kind=Prompt.CHOOSE_MANY,
        text="Which of these questions are most important to you?",
        help_text="",
    )
    for i, q in enumerate(questions):
        PromptOption.objects.create(prompt=qprompt, label=q.text, order=i)

    # 3 — Your take: open text.
    _upsert_prompt(
        kept, topic_ct, topic.id, 3,
        kind=Prompt.FREE_TEXT,
        text="Anything the positions and questions miss?",
        help_text="",
    )

    # 4 — Follow-ups: upvote on every question and position; each lean pole on
    # the questions that have poles.
    n = 3
    n += _seed_item_prompts(
        kept, question_ct, questions, Prompt.TRIGGER_VOTE, QUESTION_VOTE_FOLLOW_UPS
    )
    poled = [q for q in questions if q.lean_label_a and q.lean_label_b]
    n += _seed_item_prompts(
        kept, question_ct, poled, Prompt.TRIGGER_LEAN_A, QUESTION_LEAN_FOLLOW_UPS,
        lambda q: {"a": q.lean_label_a, "b": q.lean_label_b},
    )
    n += _seed_item_prompts(
        kept, question_ct, poled, Prompt.TRIGGER_LEAN_B, QUESTION_LEAN_FOLLOW_UPS,
        lambda q: {"a": q.lean_label_b, "b": q.lean_label_a},
    )
    n += _seed_item_prompts(
        kept, position_ct, positions, Prompt.TRIGGER_VOTE, POSITION_FOLLOW_UPS
    )

    # 5 — Respond button on every expandable fact, question and position.
    for target_ct, objs, key in (
        (stat_ct, stats, "stat"),
        (question_ct, questions, "question"),
        (position_ct, positions, "position"),
    ):
        n += _seed_item_prompts(
            kept, target_ct, objs, Prompt.TRIGGER_RESPOND, RESPOND_FOLLOW_UPS,
            lambda obj, key=key: {"verdict": RESPOND_VERDICTS[key]},
        )

    # 6 — Something missing? on each Basics / Questions / Positions section.
    for sec in sections:
        n += _seed_item_prompts(
            kept, section_ct, [sec], Prompt.TRIGGER_MISSING, MISSING_FOLLOW_UPS[sec.kind]
        )

    # Anything this run did not produce no longer belongs to the topic (a lean
    # pole dropped, a follow-up retired). Scoped to this topic's own targets.
    stale = Prompt.objects.filter(content_type=topic_ct, object_id=topic.id)
    for target_ct, objs in (
        (question_ct, questions), (position_ct, positions),
        (stat_ct, stats), (section_ct, sections),
    ):
        stale = stale | Prompt.objects.filter(
            content_type=target_ct, object_id__in=[o.id for o in objs]
        )
    stale.exclude(pk__in=kept).delete()
    return n


class Command(BaseCommand):
    help = "Seed the Add-your-view + vote follow-up prompts on a topic (idempotent)."

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
        n = seed_topic_prompts(topic)
        self.stdout.write(self.style.SUCCESS(f"Seeded {n} prompts on {slug}."))
