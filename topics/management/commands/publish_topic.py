"""Publish one reviewed topic: the whole local half of ENGINE.md Runbook A
stage 5, in one human-invoked command, plus the exact container commands for the
live push.

Stage 5 was nine hand-typed steps — three near-identical loader invocations with
hand-typed --title/--category and two raw `shell -c` one-liners. None of that
friction is what the "a human publishes" rule protects: the rule is that a human
DECIDES and INITIATES. This command is still initiated by a human, still refuses
to run without an explicit confirmation, and is still blocked for automation by
.claude/hooks/pipeline-guard.sh — which covers this command by name, precisely
because calling the loader through Python would otherwise route around the guard
that watches the shell.

Order matters here and is not the order the runbook used to specify: links are
checked BEFORE the publish, not after. Checking afterwards means a dead link is
discovered on a topic that is already live.

  manage.py publish_topic --slug <slug> --confirm
  manage.py publish_topic --slug <slug> --dry-run     # show the plan, touch nothing
"""

from io import StringIO
from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from topics.models import Topic


class Command(BaseCommand):
    help = "Publish a reviewed topic locally, then print the live-push commands."

    def add_arguments(self, p):
        p.add_argument("--slug", required=True)
        p.add_argument(
            "--confirm",
            action="store_true",
            help="required to write anything — publishing is a deliberate act.",
        )
        p.add_argument(
            "--dry-run",
            action="store_true",
            help="print the plan and the preflight results; change nothing.",
        )
        p.add_argument(
            "--file",
            default="",
            help="defaults to research/topics/<slug>.json.",
        )
        p.add_argument(
            "--skip-links",
            action="store_true",
            help="skip the pre-publish link check (it is the stage-4.5 gate's "
            "check re-run for elapsed time; skip only when it just ran).",
        )

    def handle(self, *args, **o):
        slug = o["slug"]
        path = Path(o["file"] or f"research/topics/{slug}.json")
        if not path.exists():
            raise CommandError(f"no topic JSON at {path}")

        topic = Topic.objects.filter(slug=slug).first()
        if not topic:
            raise CommandError(
                f"'{slug}' is not loaded. Stage 5 publishes a topic that stage 2 "
                "already loaded as a draft; load it first."
            )

        brief = Path(f"research/icons/{slug}.md")
        art = Path(f"static/img/topics/{slug}.png")
        card = Path(f"static/img/social/{slug}.png")

        # --- Preflight. Everything decidable, before anything is written. ---
        problems = []
        if not brief.exists():
            problems.append(f"no icon brief at {brief} (--image-brief needs it)")
        if not art.exists():
            problems.append(f"no primary art at {art} — the page falls back to a glyph")
        if not card.exists():
            problems.append(
                f"no OG card at {card} — link previews will serve the generic site "
                "image. Render it with `render_social --slug <slug> --formats og` "
                "and NO --out."
            )

        if not o["skip_links"]:
            buf = StringIO()
            call_command("check_links", topic=slug, stdout=buf, stderr=buf)
            report = buf.getvalue()
            summary = report.strip().splitlines()[-1] if report.strip() else ""
            self.stdout.write(f"links: {summary}")
            for bad in ("dead", "placeholder"):
                # The summary line reads "... · 0 dead · 0 placeholder".
                if f" 0 {bad}" not in summary:
                    problems.append(f"link check reports {bad} links — {summary}")

        if problems:
            self.stderr.write(self.style.ERROR("preflight FAILED:"))
            for p in problems:
                self.stderr.write(f"  - {p}")
            raise CommandError(
                "not publishing. These are stage-4/4.5 defects; close them there."
            )
        self.stdout.write(self.style.SUCCESS("preflight OK"))

        plan = [
            f"load_topic_draft --file {path} --slug {slug} "
            f"--status published --image-brief {brief} --reviewed",
        ]
        if o["dry_run"] or not o["confirm"]:
            self.stdout.write("\nWould run:")
            for step in plan:
                self.stdout.write(f"  manage.py {step}")
            self.stdout.write(self._live_block(slug, path, topic))
            if not o["dry_run"]:
                raise CommandError("refusing to publish without --confirm")
            return

        # --- The publish itself. One loader call; --reviewed puts the human
        # approval stamp in the same transaction. ---
        call_command(
            "load_topic_draft",
            file=str(path),
            slug=slug,
            status="published",
            image_brief=str(brief),
            reviewed=True,
        )
        call_command("rebuild_search")
        topic.refresh_from_db()
        self.stdout.write(
            self.style.SUCCESS(
                f"published '{topic.title}' [{slug}] · reviewed_at="
                f"{timezone.localtime(topic.reviewed_at):%Y-%m-%d %H:%M}"
            )
        )
        self.stdout.write(self._live_block(slug, path, topic))

    def _live_block(self, slug, path, topic):
        """The live push stays manual: it targets a different database on another
        host, and DEPLOY.md §3 requires the image to carry the JSON. Printing the
        exact commands beats retyping them from another document."""
        return (
            "\nNext — commit, then push to live (DEPLOY.md §3):\n"
            f"  git add research/dossiers/{slug}.json research/topics/{slug}.json \\\n"
            f"      research/icons/{slug}.md research/reviews/{slug}/ \\\n"
            f"      static/img/topics/{slug}.png static/img/social/{slug}.png\n"
            f"  git commit -m 'Publish {slug}'\n"
            "  # rebuild + redeploy the image first if the JSON changed since the last build\n"
            f"  docker exec ideya python manage.py load_topic_draft \\\n"
            f"      --file {path} --slug {slug} --status published \\\n"
            f"      --image-brief {path.parent.parent}/icons/{slug}.md --reviewed\n"
            "  docker exec ideya python manage.py load_universe\n"
            "  docker exec ideya python manage.py rebuild_search\n"
            f"  # confirm it actually landed — a just-published topic missing from\n"
            f"  # the live site is a known failure mode (ENGINE.md §11):\n"
            f"  curl -s -o /dev/null -w '%{{http_code}}\\n' https://<live-host>/{slug}/\n"
        )
