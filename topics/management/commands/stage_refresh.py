"""Stage a refresh of a published topic as a hidden twin, `<slug>-refresh`.

The database is shared with the live site, so a published topic cannot be
edited in place without readers seeing every intermediate state. The twin is an
ordinary in_progress topic with its own directory: the pipeline stages run on
it unchanged, it ends at `ready`, and `publish_topic --refresh` (run on the
owner's approval) folds it back into the real topic.

  manage.py stage_refresh --slug <slug>

Item ids are unique per section, so the twin carries the real topic's ids and
the votes on every kept item survive the fold. The twin records a hash of the
real topic file; the fold refuses if the real file changed in the meantime.
"""

import hashlib
import json
import shutil

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from topics.item_status import topics_dir
from topics.models import Topic

TWIN = "{}-refresh"


def art_paths(slug):
    d = settings.BASE_DIR / "static" / "img" / "topics"
    return [d / f"{slug}.png", d / f"{slug}.webp"]


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Command(BaseCommand):
    help = "Copy a published topic into a hidden twin for a refresh run."

    def add_arguments(self, p):
        p.add_argument("--slug", required=True)

    def handle(self, *args, **o):
        slug = o["slug"]
        twin = TWIN.format(slug)
        real_dir, twin_dir = topics_dir() / slug, topics_dir() / twin
        if twin_dir.exists():
            raise CommandError(f"{twin_dir} already exists: a refresh is staged.")
        topic = Topic.objects.filter(slug=slug).first()
        if not topic or topic.status != Topic.PUBLISHED:
            raise CommandError(
                f"'{slug}' is not published; refresh is for live topics."
            )

        doc = json.loads((real_dir / "topic.json").read_text(encoding="utf-8"))
        doc["slug"], doc["status"] = twin, Topic.IN_PROGRESS
        (twin_dir / "run").mkdir(parents=True)
        (twin_dir / "topic.json").write_text(
            json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        for name in ("research.md", "icon.md"):
            if (real_dir / name).exists():
                shutil.copy2(real_dir / name, twin_dir / name)
        for src, dst in zip(art_paths(slug), art_paths(twin)):
            if src.exists():
                shutil.copy2(src, dst)
        (twin_dir / "run" / "refresh-base").write_text(
            file_hash(real_dir / "topic.json")
        )

        call_command(
            "load_topic_draft",
            file=str(twin_dir / "topic.json"),
            slug=twin,
            verbosity=0,
        )
        self.stdout.write(f"staged {twin} from {slug}: {twin_dir}")
