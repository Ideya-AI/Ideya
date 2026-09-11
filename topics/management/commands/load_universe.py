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

from topics.models import Category

CATEGORIES = Path("research/categories.json")
TOPICS = Path("research/topics")

# Category slug -> --cat-* colour key (see tokens.css / CAT_COLORS).
COLOR = {
    "global-risk": "risk",
    "ai": "tech",
    "digital": "digital",
    "climate-env": "energy",
    "bio-health": "bio",
    "economy": "econ",
    "governance": "gov",
    "society": "society",
    "ethics": "ethics",
}
# Phosphor icon per category (discovery-tier glyph).
CAT_ICON = {
    "global-risk": "warning-octagon",
    "ai": "cpu",
    "digital": "globe-hemisphere-west",
    "climate-env": "leaf",
    "bio-health": "heartbeat",
    "economy": "chart-line-up",
    "governance": "bank",
    "society": "users-three",
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
                    "color_key": COLOR.get(c["slug"], "gov"),
                    "icon": CAT_ICON.get(c["slug"], "squares-four"),
                },
            )

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

        self.stdout.write(
            f"categories: {Category.objects.count()} · topics loaded: {loaded}"
        )
        for slug, why in failed:
            self.stderr.write(self.style.WARNING(f"  {slug}: {why}"))
        if failed:
            raise CommandError(f"{len(failed)} topic file(s) failed to load")
