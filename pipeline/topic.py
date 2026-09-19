"""The topic directory as the pipeline sees it (PIPELINE.md §5, §7).

A topic is `research/topics/<slug>/`. `topic.json` is the product, `evidence.json`
is what the pipeline knows, `run/` is process. The artifact is the state: a
stage looks here to see whether its inputs are present and its outputs are not.

This module is the only writer of the product files. Every write is atomic, a
content write to a `ready` topic withdraws that certification, and a published
topic is never written at all.

Gate verdicts and the blocked marker live in `evidence.json`:

    "verdicts": { "stage1": { "passed": true, "at": "…", "fields": [...], "hash": "…" } }
    "blocked":  { "stage": "stage1", "reason": "…", "implicates": "stage1", "at": "…" }

A verdict names the fields it certified as `topic:<dotted.path>` or
`evidence:<dotted.path>` and stores a hash of their values, so "stage N valid"
is a file assertion rather than a memory of run order.
"""

import datetime
import hashlib
import json
import os
from pathlib import Path

from topics.item_ids import ensure_ids

from .paths import TOPICS

NOT_STARTED, IN_PROGRESS, READY, PUBLISHED = (
    "not_started",
    "in_progress",
    "ready",
    "published",
)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def write_json(path: Path, doc):
    """Atomic: a killed process leaves the old file, never half a new one."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    os.replace(tmp, path)


def read_json(path: Path, default=None):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def dig(doc, dotted):
    """`draft.positions` -> doc['draft']['positions'], None if any step is missing."""
    cur = doc
    for key in dotted.split("."):
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur


class TopicDir:
    def __init__(self, slug: str, topics_dir: Path | None = None):
        self.slug = slug
        self.path = (topics_dir or TOPICS) / slug
        self.topic_json = self.path / "topic.json"
        self.evidence_json = self.path / "evidence.json"
        self.run_dir = self.path / "run"

    def __repr__(self):
        return f"TopicDir({self.slug!r})"

    def exists(self):
        return self.topic_json.exists()

    # -- product files -----------------------------------------------------

    def load_topic(self) -> dict:
        doc = read_json(self.topic_json)
        if doc is None:
            raise FileNotFoundError(f"no topic at {self.topic_json}")
        return doc

    def save_topic(self, doc: dict):
        """Write the product file. Refuses a published topic; a content write
        moves `not_started` to `in_progress` and withdraws `ready`."""
        if doc.get("status") == PUBLISHED:
            raise PermissionError(
                f"{self.slug} is published; the pipeline never writes a published topic"
            )
        if doc.get("draft"):
            ensure_ids(doc["draft"])
            if doc.get("status") in (NOT_STARTED, READY):
                doc["status"] = IN_PROGRESS
        write_json(self.topic_json, doc)

    def load_evidence(self) -> dict:
        return read_json(self.evidence_json, {}) or {}

    def save_evidence(self, ev: dict):
        write_json(self.evidence_json, ev)

    @property
    def status(self):
        return self.load_topic().get("status", NOT_STARTED)

    # -- run files ---------------------------------------------------------

    def return_path(self, phase: str, unit: str) -> Path:
        return self.run_dir / phase / f"{unit}.json"

    def read_return(self, phase: str, unit: str):
        return read_json(self.return_path(phase, unit))

    def write_return(self, phase: str, unit: str, doc: dict):
        write_json(self.return_path(phase, unit), doc)

    # -- blocked -----------------------------------------------------------

    @property
    def blocked(self) -> dict | None:
        return self.load_evidence().get("blocked")

    def block(self, stage: str, reason: str, implicates: str | None = None):
        ev = self.load_evidence()
        ev["blocked"] = {
            "stage": stage,
            "reason": reason,
            "implicates": implicates or stage,
            "at": now(),
        }
        self.save_evidence(ev)

    def unblock(self):
        ev = self.load_evidence()
        ev.pop("blocked", None)
        self.save_evidence(ev)

    # -- gate verdicts -----------------------------------------------------

    def _field_hash(self, fields: list[str]) -> str:
        topic = self.load_topic()
        ev = self.load_evidence()
        values = []
        for f in fields:
            scope, _, dotted = f.partition(":")
            doc = {"topic": topic, "evidence": ev}[scope]
            values.append(dig(doc, dotted))
        blob = json.dumps(values, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()

    def certify(self, stage: str, fields: list[str], note: str = ""):
        """Record a passing verdict for `stage` over `fields`, each written as
        `topic:<dotted>` or `evidence:<dotted>`."""
        ev = self.load_evidence()
        ev.setdefault("verdicts", {})[stage] = {
            "passed": True,
            "at": now(),
            "fields": fields,
            "hash": self._field_hash(fields),
            "note": note,
        }
        self.save_evidence(ev)

    def verdict(self, stage: str) -> dict | None:
        return self.load_evidence().get("verdicts", {}).get(stage)

    def verdict_valid(self, stage: str) -> tuple[bool, str]:
        v = self.verdict(stage)
        if not v:
            return False, f"{stage}: no verdict"
        if not v.get("passed"):
            return False, f"{stage}: verdict did not pass"
        if self._field_hash(v["fields"]) != v["hash"]:
            return False, f"{stage}: certified fields have changed since the verdict"
        return True, f"{stage}: valid"
