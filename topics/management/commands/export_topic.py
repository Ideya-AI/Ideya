"""Export a DB topic back to the TopicDraft JSON that load_topic_draft consumes —
the inverse of that loader.

**This is a recovery tool, not a step in any routine.** The per-topic JSON is the
source of truth and the database is what the site renders it into, so the normal
direction is file -> load. Reach for this only to rebuild a file that was lost, or
to adopt a direct database edit on purpose. To find out whether the two have
parted company, run `check_topic_drift` rather than exporting over the file and
hoping.

Writes the same ``{ "content": {...} }`` envelope the loader reads, pretty
(indent=1, ascii-escaped) to match the existing research/topics JSON style.

  manage.py export_topic --slug nuclear-energy           # -> research/topics/nuclear-energy/topic.json
  manage.py export_topic --slug nuclear-energy --out -   # -> stdout

`content` mirrors the loader field-for-field. Participation (votes, leans,
prompt responses) is never exported: it lives in the database, keyed by item id.
"""

import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from topics.models import Crux, Section, Topic


def _date(d):
    """A DateField -> ISO string the loader can re-parse, '' when unset."""
    return d.isoformat() if d else ""


def _stat(s):
    return {
        "id": s.item_id,
        "label": s.label,
        "value": s.value,
        "unit": s.unit,
        "viz": s.viz,
        "wide": s.wide,
        "fill_pct": s.fill_pct,
        "series": s.series,
        "range_min": s.range_min,
        "range_max": s.range_max,
        "range_at": s.range_at,
        "note": s.note,
        "detail": s.detail,
        "source_label": s.source_label,
        "source_url": s.source_url,
        "source_published": s.source_published,
        "source_accessed": _date(s.source_accessed),
    }


def _question(q):
    return {
        "id": q.item_id,
        "text": q.text,
        "kind": q.kind,
        "why": q.why,
        "detail": q.detail,
        "lean_label_a": q.lean_label_a,
        "lean_label_b": q.lean_label_b,
    }


def _position(p):
    return {
        "id": p.item_id,
        "name": p.name,
        "color_key": p.color_key,
        "steelman": p.steelman,
        "detail": p.detail,
        "proponents": p.proponents,
    }


def _action(a):
    return {
        "id": a.item_id,
        "kind": a.kind,
        "title": a.title,
        "description": a.description,
        "url": a.url,
        # The loader re-links by position name; null when unaligned.
        "for_position": a.position.name if a.position_id else None,
    }


def _crux(c):
    return {
        "lead": c.lead,
        "lead_highlight": c.lead_highlight,
        "subtitle": c.subtitle,
        "empirical": c.empirical,
        "values": c.values,
    }


class Command(BaseCommand):
    help = "Export a DB topic to the TopicDraft JSON that load_topic_draft consumes."

    def add_arguments(self, p):
        p.add_argument("--slug", required=True)
        p.add_argument(
            "--out",
            default=None,
            help="Output path; '-' for stdout. Default research/topics/<slug>/topic.json.",
        )

    def handle(self, *args, **o):
        topic = Topic.objects.filter(slug=o["slug"]).first()
        if not topic:
            raise CommandError(f"topic '{o['slug']}' not found")

        secs = {s.kind: s for s in topic.sections.all()}

        def children(kind, related, fn):
            sec = secs.get(kind)
            if sec is None:
                return []
            # Authoring order (not the vote/importance display order) so the
            # JSON is stable and the loader re-derives the same `order` field.
            return [fn(x) for x in getattr(sec, related).order_by("order", "id")]

        crux_sec = secs.get(Section.CRUX)
        crux_obj = (
            Crux.objects.filter(section=crux_sec).first()
            if crux_sec is not None
            else None
        )

        draft = {
            # Identity, placement, lifecycle and the art prompt live at the TOP
            # of the file, not in here — `content` is only what the page renders.
            "overview": {
                "summary": topic.summary,
                "scope_covered": topic.scope_covered,
                "scope_excluded": topic.scope_excluded,
                "why_now": topic.why_now,
                "why_now_source_label": topic.why_now_source_label,
                "why_now_source_url": topic.why_now_source_url,
            },
            "basics": {"stats": children(Section.BASICS, "stats", _stat)},
            "questions": children(Section.QUESTIONS, "questions", _question),
            "positions": children(Section.POSITIONS, "positions", _position),
            "crux": _crux(crux_obj) if crux_obj is not None else {},
            "actions": children(Section.ACTIONS, "actions", _action),
        }
        # One file per topic, cradle to grave: the index fields the loader reads
        # sit at the top, `content` is what the page renders, under them.
        cats = [
            c.slug
            for c in topic.categories.order_by("slug")
            if c.pk != topic.primary_category_id
        ]
        payload = {
            "slug": topic.slug,
            "title": topic.title,
            "status": topic.status,
            "authored_at": topic.authored_at.isoformat() if topic.authored_at else None,
            "published_at": (
                topic.published_at.isoformat() if topic.published_at else None
            ),
            "reviewed_at": list(topic.reviewed_at or []),
            "primary_image_prompt": topic.primary_image_prompt,
            "scope": topic.scope,
            "icon": topic.icon,
            "primary_category": topic.primary_category.slug
            if topic.primary_category_id
            else "",
            "categories": cats,
            "related": [
                e.target.slug
                for e in topic.outgoing_edges.select_related("target").order_by("id")
            ],
            "content": draft,
        }

        out = o["out"]
        if out == "-":
            self.stdout.write(json.dumps(payload, indent=1, ensure_ascii=True))
            return
        path = Path(out) if out else Path("research/topics") / topic.slug / "topic.json"

        # Carry forward top-level keys the DB cannot regenerate — anything in the
        # file that the export does not produce is by definition unrecoverable,
        # and writing over it would destroy it silently. Generic rather than a
        # per-key special case, because the next such key is unknowable here.
        preserved = []
        if path.exists():
            try:
                existing = json.loads(path.read_text())
            except (json.JSONDecodeError, OSError):
                existing = {}
            if isinstance(existing, dict):
                for key, value in existing.items():
                    if key not in payload:
                        payload[key] = value
                        preserved.append(key)

        text = json.dumps(payload, indent=1, ensure_ascii=True)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
        self.stdout.write(
            self.style.SUCCESS(
                f"exported '{topic.slug}' -> {path} — "
                f"{len(draft['basics']['stats'])} stats, "
                f"{len(draft['questions'])} questions, "
                f"{len(draft['positions'])} positions, "
                f"{len(draft['actions'])} actions"
                + (f" — preserved: {', '.join(preserved)}" if preserved else "")
            )
        )
