"""Certify a topic ready to publish, or withdraw that certification.

Readiness and publication are two different things. Readiness is a statement
about the topic — every exit check green, nothing left routed, a human's review
packet written — and it is the engine's job. Publication is a decision about the
site, and it is the human's. Keeping them apart is what lets `publish_topic` be
nothing but a switch: it can refuse to make anything public that was never
certified, without itself knowing how to judge a topic.

Readiness is deliberately fragile: writing new content withdraws it, because the
moment the content changes, what was verified is no longer what the file says.
The engine does that when it persists a draft, so it certifies LAST.

The status is written to the topic FILE and then to its row — the file is the
source of truth, and a change that lived only in the database would be undone by
the next rebuild.

  manage.py mark_ready --slug <slug>
  manage.py mark_ready --slug <slug> --clear
"""

from django.core.management.base import BaseCommand, CommandError

from topics.item_status import set_status
from topics.models import Topic


class Command(BaseCommand):
    help = "Mark a topic ready to publish (or clear that mark)."

    def add_arguments(self, p):
        p.add_argument("--slug", required=True)
        p.add_argument(
            "--clear",
            action="store_true",
            help="withdraw readiness — the topic can no longer be made public.",
        )

    def handle(self, *args, **o):
        topic = Topic.objects.filter(slug=o["slug"]).first()
        if not topic:
            raise CommandError(f"'{o['slug']}' is not loaded.")
        if topic.status == Topic.PUBLISHED:
            raise CommandError(
                f"'{o['slug']}' is already published. Take it off the site first "
                "if you mean to re-certify it."
            )
        target = Topic.IN_PROGRESS if o["clear"] else Topic.READY
        path = set_status(topic, target)
        if o["clear"]:
            self.stdout.write(f"'{o['slug']}' is back to {target} — not publishable.")
        else:
            self.stdout.write(self.style.SUCCESS(f"'{o['slug']}' is ready to publish."))
        self.stdout.write(f"  {path} updated — commit it.")
