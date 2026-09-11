"""Move one topic between the four stops of its life, in the file AND the database.

`research/topics/<slug>.json` is the source of truth, so a lifecycle change has
to land there first — otherwise rebuilding the database from the directory would
undo it. The database is updated in the same breath because that is what the
site reads.

Plain Python on purpose, so `mark_ready` and `publish_topic` share one
implementation and cannot disagree about what a transition means.
"""

import json
from pathlib import Path

from django.conf import settings


def topics_dir():
    """Where the topic files live. Settable so a test never writes into the
    working tree — the first version of this did, and a test fixture published a
    real topic."""
    return Path(getattr(settings, "TOPICS_DIR", "research/topics"))


def path_for(slug):
    """A topic is a directory; `topic.json` in it is the product the loader reads.
    Its evidence, icon brief, packet and run artifacts are its siblings."""
    return topics_dir() / slug / "topic.json"


def set_status(topic, status, **extra_fields):
    """Write `status` to the topic's file, then to its row. Returns the file path.

    `extra_fields` are applied to the row only (reviewed_at and friends are
    database bookkeeping, not content)."""
    path = path_for(topic.slug)
    if not path.exists():
        raise FileNotFoundError(
            f"no topic file at {path} — every topic has one, cradle to grave"
        )
    doc = json.loads(path.read_text(encoding="utf-8"))
    doc["status"] = status
    path.write_text(
        json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )

    topic.status = status
    for k, v in extra_fields.items():
        setattr(topic, k, v)
    topic.save(update_fields=["status", *extra_fields])
    return path
