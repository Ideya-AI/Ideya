"""Export a DB topic back to the canonical TopicDraft JSON that load_topic_draft
consumes — the inverse of that loader. A topic round-trips: export then load
reproduces its sections, typed children, and key fields, so the per-topic JSON
can become the single source of truth (edit the JSON, reload it).

Writes the same ``{ "draft": {...}, "verdicts": [...] }`` envelope the loader
reads (``payload.get("draft", payload)`` + ``payload.get("verdicts")``), pretty
(indent=1, ascii-escaped) to match the existing research/topics JSON style.

  manage.py export_topic --slug nuclear-energy           # -> research/topics/nuclear-energy.json
  manage.py export_topic --slug nuclear-energy --out -   # -> stdout

The draft mirrors the loader field-for-field, and is a superset: fields the
loader does not (yet) read — e.g. stat series/range, question votes/lean,
position importance/detail — are exported too, so the JSON captures the whole
topic. The loader ignores keys it doesn't know, so the round-trip stays safe.
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
        "reveal": s.reveal,
    }


def _question(q):
    return {
        "text": q.text,
        "kind": q.kind,
        "why": q.why,
        "detail": q.detail,
        "votes": q.votes,
        "lean_label_a": q.lean_label_a,
        "lean_label_b": q.lean_label_b,
        "lean_pct_a": q.lean_pct_a,
        "reveal": q.reveal,
    }


def _position(p):
    return {
        "name": p.name,
        "color_key": p.color_key,
        "steelman": p.steelman,
        "description": p.description,
        "detail": p.detail,
        "representative_name": p.representative_name,
        "representative_note": p.representative_note,
        "proponents": p.proponents,
        "importance": p.importance,
        "prevalence_weight": p.prevalence_weight,
        "spectrum_position": p.spectrum_position,
    }


def _action(a):
    return {
        "kind": a.kind,
        "title": a.title,
        "description": a.description,
        "url": a.url,
        # The loader re-links by position name; null when unaligned.
        "for_position": a.position.name if a.position_id else None,
        "reveal": a.reveal,
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
            help="Output path; '-' for stdout. Default research/topics/<slug>.json.",
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

        basics = secs.get(Section.BASICS)
        crux_sec = secs.get(Section.CRUX)
        crux_obj = (
            Crux.objects.filter(section=crux_sec).first()
            if crux_sec is not None
            else None
        )

        draft = {
            # Topic-level meta. The loader takes title/slug/status/category from
            # CLI args and ignores these, but they make the export self-describing
            # (and a future loader could read them).
            "slug": topic.slug,
            "title": topic.title,
            "status": topic.status,
            "volatility": topic.volatility,
            "icon": topic.icon,
            "primary_category": (
                topic.primary_category.slug if topic.primary_category_id else None
            ),
            "categories": [c.slug for c in topic.categories.order_by("slug")],
            "overview": {
                "summary": topic.summary,
                "scope_covered": topic.scope_covered,
                "scope_excluded": topic.scope_excluded,
                "why_now": topic.why_now,
            },
            "basics": {
                "intro": basics.intro if basics is not None else "",
                "stats": children(Section.BASICS, "stats", _stat),
            },
            "questions": children(Section.QUESTIONS, "questions", _question),
            "positions": children(Section.POSITIONS, "positions", _position),
            "crux": _crux(crux_obj) if crux_obj is not None else {},
            "actions": children(Section.ACTIONS, "actions", _action),
        }
        payload = {
            "draft": draft,
            "verdicts": (topic.research_dossier or {}).get("verdicts", []),
        }
        text = json.dumps(payload, indent=1, ensure_ascii=True)

        out = o["out"]
        if out == "-":
            self.stdout.write(text)
            return
        path = Path(out) if out else Path("research/topics") / f"{topic.slug}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
        self.stdout.write(
            self.style.SUCCESS(
                f"exported '{topic.slug}' -> {path} — "
                f"{len(draft['basics']['stats'])} stats, "
                f"{len(draft['questions'])} questions, "
                f"{len(draft['positions'])} positions, "
                f"{len(draft['actions'])} actions"
            )
        )
