"""Assert the database still matches the topic files it was built from.

`research/topics/` is the source of truth: one file per topic, cradle to grave.
The database is what the site renders those files into. That only holds if
nothing edits the database directly, so this turns the assumption into a check —
export each topic back out, compare it to its file, and fail loud on any
difference.

Reader state is not content and is ignored: vote counts and importance live only
in the database by design.

    manage.py check_topic_drift --slug nuclear-energy
    manage.py check_topic_drift --all
"""

import json
import re
import tempfile
from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from topics.models import Topic

TOPICS = Path("research/topics")  # a topic is a directory; topic.json is the product

# Written by readers, never by the file.
IGNORE = {"votes", "importance"}

# Engine-produced attributes with model defaults: the file may omit them and the
# database will still hold something sensible.
DERIVED = (".icon", ".primary_image_prompt")

# Carried for the engine's own use; the topic tables have no column for it, so
# a round-trip legitimately drops it.
FILE_ONLY = (".lean_basis",)


def _flat(node, prefix=""):
    out = {}
    if isinstance(node, dict):
        for k, v in node.items():
            if k in IGNORE:
                continue
            out.update(_flat(v, f"{prefix}.{k}"))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            out.update(_flat(v, f"{prefix}[{i}]"))
    else:
        out[prefix] = node
    return out


def _same(x, y):
    # "" and null both mean unset; the loader normalizes one to the other.
    return x == y or (x in ("", None) and y in ("", None))


def _derived(path, disk, db):
    """True when the difference is the loader deriving a value the file leaves
    open, rather than the database having drifted from it. Each rule is a loader
    behaviour, and each is why a strict diff would cry wolf for ever."""
    generic = re.sub(r"\[\d+\]", "[]", path)
    # a cap: the model stores a prefix and the loader warns as it slices
    if (
        isinstance(disk, str)
        and isinstance(db, str)
        and db
        and disk.startswith(db)
        and len(disk) > len(db)
    ):
        return True
    # the palette is assigned at load time when the file names no colour
    if path.endswith(".color_key") and disk in ("", None, "<absent>"):
        return True
    # range_at is only kept for a range viz; elsewhere the loader drops it
    if path.endswith(".range_at") and disk in (0, "", None) and db is None:
        return True
    if disk == "<absent>" and generic.endswith(DERIVED):
        return True
    if db == "<absent>" and generic.endswith(FILE_ONLY):
        return True
    return False


def _normalize(doc):
    """The file is input; the database holds what the loader made of it. Fold the
    one structural difference so the rest compares like for like: stage 1 writes
    the Phosphor glyph inside the content's `overview`, but the icon is an index
    field — an unauthored topic has no content and still needs one — so it settles
    at the top of the file."""
    draft = doc.get("content")
    if isinstance(draft, dict):
        ov = draft.get("overview") or {}
        found = draft.pop("icon", None) or ov.pop("icon", None)
        if found and not doc.get("icon"):
            doc["icon"] = found
    return doc


def drift(slug):
    """Field paths where the database and the file disagree, as (path, file, db)."""
    path = TOPICS / slug / "topic.json"
    if not path.exists():
        return [("<file>", "missing", str(path))]
    disk = json.loads(path.read_text())

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "export.json"
        call_command("export_topic", slug=slug, out=str(out), stdout=open(out.parent / "log", "w"))
        db = json.loads(out.read_text())

    # A topic with no content is not "empty content" — the export builds a
    # hollow content skeleton for it, and comparing that to nothing is noise.
    if not disk.get("content"):
        disk.pop("content", None)
        db.pop("content", None)

    # `categories` (the secondaries) and `related` are unordered in the
    # database: secondaries are a plain many-to-many and edges carry no rank. So
    # compare them as sets, and `primary_category` — its own column — exactly.
    # Any order the file keeps is for the reader of the file; the loader cannot
    # promise to give it back.
    unordered = []
    for doc in (disk, db):
        primary = doc.pop("primary_category", "") or ""
        cats = doc.pop("categories", None) or []
        rel = doc.pop("related", None) or []
        unordered.append((primary, sorted(cats), sorted(rel)))
    rows = []
    if unordered[0] != unordered[1]:
        for i, label in enumerate(("primary category", "secondary categories", "related")):
            if unordered[0][i] != unordered[1][i]:
                rows.append((f".{label}", unordered[0][i], unordered[1][i]))

    a, b = _flat(_normalize(disk)), _flat(_normalize(db))
    for k in sorted(set(a) | set(b)):
        x, y = a.get(k, "<absent>"), b.get(k, "<absent>")
        if _same(x, y) or _derived(k, x, y):
            continue
        rows.append((k, x, y))
    return rows


class Command(BaseCommand):
    help = "Fail if a loaded topic has drifted from its file."

    def add_arguments(self, p):
        p.add_argument("--slug")
        p.add_argument("--all", action="store_true", help="every topic that has a file")

    def handle(self, *a, **o):
        if o["all"]:
            slugs = sorted(
                p.parent.name for p in TOPICS.glob("*/topic.json")
                if Topic.objects.filter(slug=p.parent.name).exists()
            )
        elif o["slug"]:
            slugs = [o["slug"]]
        else:
            raise CommandError("pass --slug or --all")

        drifted = 0
        for slug in slugs:
            rows = drift(slug)
            if not rows:
                if not o["all"]:
                    self.stdout.write(f"{slug}: in sync")
                continue
            drifted += 1
            self.stderr.write(self.style.WARNING(f"{slug}: DRIFTED — {len(rows)} field(s)"))
            for path, disk, db in rows[:12]:
                self.stderr.write(
                    f"    {path}\n      file: {str(disk)[:90]}\n      db:   {str(db)[:90]}"
                )
            if len(rows) > 12:
                self.stderr.write(f"    ... and {len(rows) - 12} more")
        if drifted:
            raise CommandError(
                f"{drifted} of {len(slugs)} topic(s) drifted from their file. The file "
                "is the source of truth: reload it with `load_universe --slug <slug>`, "
                "or export the database over it deliberately if the database holds the "
                "version you meant to keep."
            )
        self.stdout.write(self.style.SUCCESS(f"{len(slugs)} topic(s) in sync"))
