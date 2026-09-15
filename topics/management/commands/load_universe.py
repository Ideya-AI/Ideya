"""Build the whole database from the topic directory.

`research/topics/` IS the set of topics: one file each, cradle to grave, from a
topic that has only a title to a published one with years of participation. This
command reads the taxonomy from `research/categories.json`, then loads every
topic file through `load_topic_draft`. Idempotent, and safe to run at any time.

The database is derived: delete it, migrate, run this, and the atlas is back —
everything except participation, which exists only in the database by nature.

  manage.py load_universe
  manage.py load_universe --slug <slug>     # just one, same rules
"""

import json
from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from topics.management.commands.load_topic_draft import wire_related
from topics.models import Category, Topic

CATEGORIES = Path("research/categories.json")
TOPICS = Path("research/topics")

# Phosphor icon per category (discovery-tier glyph).
CAT_ICON = {
    "global-risk": "radioactive",
    "ai": "brain",
    "digital": "broadcast",
    "climate-energy": "sun-horizon",
    "food-land": "cow",
    "bio-health": "dna",
    "economy": "coins",
    "governance": "gavel",
    "society": "handshake",
    "ethics": "scales",
}


class Command(BaseCommand):
    help = "Build the database from research/topics/ + research/categories.json."

    def add_arguments(self, p):
        p.add_argument("--slug", help="load one topic instead of the directory")

    @transaction.atomic
    def handle(self, *args, **o):
        if not CATEGORIES.exists():
            raise CommandError(f"no taxonomy at {CATEGORIES}")
        for c in json.loads(CATEGORIES.read_text()):
            Category.objects.update_or_create(
                slug=c["slug"],
                defaults={
                    "name": c["name"],
                    "description": c.get("description", ""),
                    "color_key": c["slug"],
                    "icon": CAT_ICON.get(c["slug"], "squares-four"),
                },
            )

        # The file is the taxonomy: a category it no longer lists is gone.
        Category.objects.exclude(
            slug__in=[c["slug"] for c in json.loads(CATEGORIES.read_text())]
        ).delete()

        files = (
            [TOPICS / o["slug"] / "topic.json"]
            if o["slug"]
            else sorted(TOPICS.glob("*/topic.json"))
        )
        if o["slug"] and not files[0].exists():
            raise CommandError(f"no topic file at {files[0]}")

        loaded, failed = 0, []
        for path in files:
            try:
                # Every topic goes through the one loader, so a topic with only a
                # title and a published one take exactly the same path.
                call_command(
                    "load_topic_draft",
                    file=str(path),
                    slug=path.parent.name,  # the directory IS the slug
                    allow_published=True,
                    verbosity=0,
                )
                loaded += 1
            except Exception as exc:  # noqa: BLE001 — report, then keep going
                failed.append((path.parent.name, str(exc).splitlines()[0][:120]))

        # Second pass: a topic's related edges point at slugs that may not have
        # existed when its own file loaded, so wire them once every topic does.
        edges = 0
        for path in files:
            topic = Topic.objects.filter(slug=path.parent.name).first()
            if topic:
                edges += wire_related(topic, json.loads(path.read_text()), self.stderr)

        self.stdout.write(
            f"categories: {Category.objects.count()} · topics loaded: {loaded}"
            f" · related edges wired late: {edges}"
        )
        for slug, why in failed:
            self.stderr.write(self.style.WARNING(f"  {slug}: {why}"))
        if failed:
            raise CommandError(f"{len(failed)} topic file(s) failed to load")
