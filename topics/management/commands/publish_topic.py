"""The publish switch: make one finished topic public, or take it private again.

This does very little on purpose. Everything that decides whether a topic is
*ready* — its renders, its icon, its cards, its links, its gates — happens
earlier and ends at one stop on the topic's core status: `ready`. This command
refuses to make anything public that is not sitting there. It does not re-derive
readiness, and it knows nothing about how it was earned.

So the whole command is: check the status, move it to `published` in the topic's
file and its row, stamp `reviewed_at` (the human-approval clock), move the search
index. It reads no
files, loads no content, and judges no quality. If the topic in the database is
not the one you want public, fix that with `load_topic_draft` — which clears the
readiness flag, because what was verified is then no longer what is loaded — and
have it certified again before publishing.

  manage.py publish_topic --slug <slug> --confirm         # private -> public
  manage.py publish_topic --slug <slug> --off --confirm   # public -> private
  manage.py publish_topic --slug <slug> --dry-run         # say what would happen

Taking a topic private needs no readiness: pulling something off the site is
always allowed.

A human runs this, always: `.claude/hooks/pipeline-guard.sh` blocks it for
automation, and `--confirm` is required before anything is written.
"""

from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from topics.item_status import set_status
from topics.models import Topic


class Command(BaseCommand):
    help = "Make a finished topic public, or take it private again."

    def add_arguments(self, p):
        p.add_argument("--slug", required=True)
        p.add_argument(
            "--off",
            action="store_true",
            help="take a public topic private again (does not touch reviewed_at).",
        )
        p.add_argument(
            "--confirm",
            action="store_true",
            help="required to write anything — this is a deliberate act.",
        )
        p.add_argument(
            "--dry-run",
            action="store_true",
            help="print what would change; change nothing.",
        )

    def handle(self, *args, **o):
        slug = o["slug"]
        topic = Topic.objects.filter(slug=slug).first()
        if not topic:
            raise CommandError(
                f"'{slug}' is not loaded. This command only flips a loaded topic "
                "between public and private; load it first."
            )

        # Off goes back to READY, not IN_PROGRESS: taking a page off the site
        # says nothing about whether its content is still verified.
        target = Topic.READY if o["off"] else Topic.PUBLISHED
        verb = "take private" if o["off"] else "make public"
        if topic.status == target:
            raise CommandError(f"'{slug}' is already {target}. Nothing to do.")

        # The one thing the switch checks, and it checks the status rather than
        # the topic: readiness is earned upstream and recorded by `mark_ready`.
        if not o["off"] and topic.status != Topic.READY:
            raise CommandError(
                f"'{slug}' is {topic.status}, not {Topic.READY} — only a topic "
                "the engine has certified can be made public. Readiness is "
                "earned upstream (every exit check green, nothing left routed) "
                f"and recorded with `manage.py mark_ready --slug {slug}`. A "
                "content load withdraws it, so if this topic was reloaded after "
                "it was verified, verify it again."
            )

        if o["dry_run"] or not o["confirm"]:
            self.stdout.write(
                f"Would {verb} '{topic.title}' [{slug}]: "
                f"status {topic.status} -> {target}"
                + ("" if o["off"] else ", reviewed_at stamped")
            )

            self.stdout.write(self._live_block(slug, o["off"]))
            if not o["dry_run"]:
                raise CommandError("refusing to write without --confirm")
            return

        with transaction.atomic():
            # Status is written to the topic FILE first and then to its row: the
            # file is the source of truth, and a publish that lived only in the
            # database would be undone by the next rebuild from the directory.
            extra = {} if o["off"] else {"reviewed_at": timezone.now()}
            path = set_status(topic, target, **extra)
        # The search index only carries published topics, so the switch has to
        # move it too or a live topic is unfindable (and a hidden one findable).
        call_command("rebuild_search")

        self.stdout.write(
            self.style.SUCCESS(
                f"'{topic.title}' [{slug}] is now {target}"
                + (
                    ""
                    if o["off"]
                    else f" · reviewed_at={timezone.localtime(topic.reviewed_at):%Y-%m-%d %H:%M}"
                )
            )
        )
        self.stdout.write(f"  {path} updated — commit it.")
        self.stdout.write(self._live_block(slug, o["off"]))

    def _live_block(self, slug, off):
        """The live site is a different database on another host, so the switch
        has to be thrown there too. Printing the exact commands beats retyping
        them out of DEPLOY.md."""
        if off:
            return (
                "\nThe live site is a separate database — take it private there too "
                "(DEPLOY.md §3):\n"
                f"  docker exec ideya python manage.py publish_topic --slug {slug} "
                "--off --confirm\n"
            )
        artifacts = [
            f"research/topics/{slug}/topic.json",
            f"research/topics/{slug}/evidence.json",
            f"research/topics/{slug}/icon.md",
            f"research/topics/{slug}/review.md",
            f"static/img/topics/{slug}.png",
            f"static/img/social/{slug}.png",
        ]
        present = " ".join(a for a in artifacts if Path(a).exists())
        return (
            "\nNext — commit, then put it live (DEPLOY.md §3):\n"
            f"  git add {present}\n"
            f"  git commit -m 'Publish {slug}'\n"
            "  # rebuild + redeploy the image first if the JSON changed since the "
            "last build,\n"
            "  # then load the content into the live DB and throw the switch there:\n"
            f"  docker exec ideya python manage.py load_topic_draft "
            f"--file research/topics/{slug}/topic.json --slug {slug}\n"
            f"  docker exec ideya python manage.py publish_topic --slug {slug} --confirm\n"
            "  docker exec ideya python manage.py load_universe\n"
            "  # confirm it actually landed — a just-published topic missing from\n"
            "  # the live site is a known failure mode (ENGINE.md §11):\n"
            f"  curl -s -o /dev/null -w '%{{http_code}}\\n' https://<live-host>/{slug}/\n"
        )
