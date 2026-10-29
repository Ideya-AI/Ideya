"""The publish switch: make one finished topic public, or take it private again.

This does very little on purpose. Everything that decides whether a topic is
*ready* — its renders, its icon, its cards, its links, its gates — happens
earlier and ends at one stop on the topic's core status: `ready`. This command
refuses to make anything public that is not sitting there. It does not re-derive
readiness, and it knows nothing about how it was earned.

So the whole command is: check the status, move it to `published` in the topic's
file and its row, stamp `published_at`, move the search
index. It reads no
files, loads no content, and judges no quality. If the topic in the database is
not the one you want public, fix that with `load_topic_draft` — which clears the
readiness flag, because what was verified is then no longer what is loaded — and
have it certified again before publishing.

  manage.py publish_topic --slug <slug> --confirm         # private -> public
  manage.py publish_topic --slug <slug> --off --confirm   # public -> private
  manage.py publish_topic --slug <slug> --dry-run         # say what would happen
  manage.py publish_topic --slug <slug> --refresh --confirm  # fold a ready refresh in
  manage.py publish_topic --slug <slug> --discard --confirm  # throw a staged refresh away

A refresh is staged by `stage_refresh` as a hidden twin, `<slug>-refresh`, and
certified there like any new topic. `--refresh` copies its content into the live
topic (status stays published, reviewed_at gets a stamp), moves its packet,
renders and cards across, and deletes the twin.

Taking a topic private needs no readiness: pulling something off the site is
always allowed.

Only on the owner's explicit approval, and `--confirm` is required before
anything is written.
"""

import json
import shutil

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from topics.item_status import set_status, topics_dir
from topics.management.commands.stage_refresh import TWIN, art_paths, file_hash
from topics.models import Topic


class Command(BaseCommand):
    help = "Make a finished topic public, or take it private again."

    def add_arguments(self, p):
        p.add_argument("--slug", required=True)
        p.add_argument(
            "--off",
            action="store_true",
            help="take a public topic private again (does not touch published_at).",
        )
        p.add_argument(
            "--refresh",
            action="store_true",
            help="fold the ready twin <slug>-refresh into this published topic.",
        )
        p.add_argument(
            "--discard",
            action="store_true",
            help="delete the staged twin <slug>-refresh without applying it.",
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
        if o["refresh"] or o["discard"]:
            return self._refresh(slug, o)
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
                + ("" if o["off"] else ", published_at stamped")
            )

            self.stdout.write(self._live_block(slug, o["off"]))
            if not o["dry_run"]:
                raise CommandError("refusing to write without --confirm")
            return

        with transaction.atomic():
            # Status is written to the topic FILE first and then to its row: the
            # file is the source of truth, and a publish that lived only in the
            # database would be undone by the next rebuild from the directory.
            extra = {} if o["off"] else {"published_at": timezone.now()}
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
                    else f" · published_at={timezone.localtime(topic.published_at):%Y-%m-%d %H:%M}"
                )
            )
        )
        self.stdout.write(f"  {path} updated — commit it.")
        self.stdout.write(self._live_block(slug, o["off"]))

    def _refresh(self, slug, o):
        twin = TWIN.format(slug)
        real_dir, twin_dir = topics_dir() / slug, topics_dir() / twin
        twin_row = Topic.objects.filter(slug=twin).first()
        if not twin_dir.exists():
            raise CommandError(f"no staged refresh at {twin_dir}.")
        social = settings.BASE_DIR / "static" / "img" / "social"
        posters = settings.BASE_DIR / "static" / "posters"
        if o["refresh"]:
            if not twin_row or twin_row.status != Topic.READY:
                raise CommandError(f"'{twin}' is not {Topic.READY}; the audit has not passed it.")
            if file_hash(real_dir / "topic.json") != (twin_dir / "run" / "refresh-base").read_text():
                raise CommandError(
                    f"{real_dir}/topic.json changed after the refresh was staged; "
                    "folding the twin in would overwrite that change."
                )
        if o["dry_run"] or not o["confirm"]:
            self.stdout.write(
                f"Would {'fold ' + twin + ' into' if o['refresh'] else 'discard ' + twin + ' for'} {slug}"
            )
            if not o["dry_run"]:
                raise CommandError("refusing to write without --confirm")
            return

        if o["refresh"]:
            path = real_dir / "topic.json"
            doc = json.loads(path.read_text(encoding="utf-8"))
            new = json.loads((twin_dir / "topic.json").read_text(encoding="utf-8"))
            doc["content"], doc["icon"] = new["content"], new.get("icon", doc.get("icon"))
            doc["reviewed_at"] = list(doc.get("reviewed_at") or []) + [
                timezone.now().isoformat(timespec="seconds")
            ]
            path.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
            for name in ("research.md", "audit.md"):
                if (twin_dir / name).exists():
                    shutil.copy2(twin_dir / name, real_dir / name)
            if (twin_dir / "renders").exists():
                shutil.rmtree(real_dir / "renders", ignore_errors=True)
                shutil.move(twin_dir / "renders", real_dir / "renders")
            for card in (twin_dir / "share").glob(f"{twin}-*.png"):
                (real_dir / "share").mkdir(exist_ok=True)
                shutil.move(card, real_dir / "share" / card.name.replace(twin, slug, 1))
            for d, ext in ((social, "png"), (posters, "pdf")):
                if (d / f"{twin}.{ext}").exists():
                    shutil.move(d / f"{twin}.{ext}", d / f"{slug}.{ext}")
            call_command(
                "load_topic_draft", file=str(path), slug=slug, allow_published=True, verbosity=0
            )
        for d, ext in ((social, "png"), (posters, "pdf")):
            (d / f"{twin}.{ext}").unlink(missing_ok=True)
        for p in art_paths(twin):
            p.unlink(missing_ok=True)
        if twin_row:
            twin_row.delete()
        shutil.rmtree(twin_dir)
        if o["refresh"]:
            call_command("rebuild_search")
            self.stdout.write(self.style.SUCCESS(f"'{slug}' refreshed from {twin}; {path} updated — commit it."))
            self.stdout.write(self._live_block(slug, False))
        else:
            self.stdout.write(self.style.SUCCESS(f"{twin} discarded; '{slug}' unchanged."))

    def _live_block(self, slug, off):
        """One database serves this session and the live site, so the switch is
        already live; what is left is committing the file (docs/ARCHITECTURE.md, Operations §3)."""
        if off:
            return "Private on the live site too (one shared database).\n"
        return (
            "Live now (one shared database) once the site is up. Check:\n"
            f"  curl -s -o /dev/null -w '%{{http_code}}\\n' https://ideya1.org/{slug}/\n"
            "New hero art or a new share card also needs an image rebuild and restart.\n"
        )
