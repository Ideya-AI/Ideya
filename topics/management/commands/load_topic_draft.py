"""Load a research-pipeline draft (a TopicDraft JSON) into the DB as a topic:
Sections + typed children (Stat/Question/Position/Crux/Action), with reveal levels,
position colours, prevalence/spectrum, source dates, and the dossier. Idempotent —
rebuilds the topic's sections on each run. Use a distinct --slug to keep a gold
standard (e.g. nuclear-energy) intact while comparing.

Reads the workflow result file: { draft: {...}, verdicts: [...], plan_positions: [...] }.
"""

import datetime
import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from topics.models import (
    POS_COLORS,
    Action,
    Category,
    Crux,
    Position,
    Question,
    Section,
    Stat,
    Topic,
)

POS_KEYS = [k for k, _ in POS_COLORS]
ACTION_KINDS = {k for k, _ in Action.KIND_CHOICES}


class Command(BaseCommand):
    help = "Load a research-pipeline TopicDraft JSON into the DB as a topic."

    def add_arguments(self, p):
        p.add_argument("--file", required=True)
        p.add_argument("--slug", required=True)
        p.add_argument("--title", required=True)
        p.add_argument("--category", required=True, help="primary category slug")
        p.add_argument("--status", default="draft", choices=["draft", "published"])

    @transaction.atomic
    def handle(self, *args, **o):
        payload = json.loads(Path(o["file"]).read_text())
        d = payload.get("draft", payload)
        cat = Category.objects.filter(slug=o["category"]).first()
        if not cat:
            raise CommandError(f"category '{o['category']}' not found")

        ov = d.get("overview", {})
        topic, _ = Topic.objects.update_or_create(
            slug=o["slug"],
            defaults={
                "title": o["title"],
                "status": o["status"],
                "primary_category": cat,
                "summary": ov.get("summary", ""),
                "scope_covered": ov.get("scope_covered", ""),
                "scope_excluded": ov.get("scope_excluded", ""),
                "why_now": ov.get("why_now", ""),
                "icon": "atom",
                "researched_at": timezone.now(),
                "research_dossier": {
                    "verdicts": payload.get("verdicts", []),
                    "generated_by": "topic-research pipeline",
                },
            },
        )
        topic.categories.set([cat])
        topic.sections.all().delete()  # clean rebuild

        def sec(kind, **kw):
            return Section.objects.create(topic=topic, kind=kind, **kw)

        sec(Section.OVERVIEW)

        # Basics
        b = d.get("basics", {})
        bs = sec(Section.BASICS, intro=b.get("intro", ""))
        for i, s in enumerate(b.get("stats", [])):
            acc = s.get("source_accessed")
            Stat.objects.create(
                section=bs,
                order=i,
                label=s.get("label", "")[:120],
                value=s.get("value", "")[:24],
                unit=s.get("unit", "")[:12],
                viz=(
                    s.get("viz", "bar")
                    if s.get("viz") in dict(Stat.VIZ_CHOICES)
                    else "bar"
                ),
                fill_pct=s.get("fill_pct"),
                note=s.get("note", "")[:400],
                source_label=s.get("source_label", "")[:120],
                source_url=s.get("source_url", "") or "",
                source_published=s.get("source_published", "")[:40],
                source_accessed=datetime.date.fromisoformat(acc) if acc else None,
                reveal=s.get("reveal", "condensed"),
            )

        # Questions
        qs = sec(Section.QUESTIONS)
        for i, q in enumerate(d.get("questions", [])):
            Question.objects.create(
                section=qs,
                order=i,
                text=q.get("text", "")[:400],
                kind=(
                    q.get("kind", "empirical")
                    if q.get("kind") in ("empirical", "value")
                    else "empirical"
                ),
                why=q.get("why", ""),
                reveal=q.get("reveal", "condensed"),
            )

        # Positions — assign a colour per index; carry prevalence + spectrum.
        ps = sec(Section.POSITIONS)
        for i, p in enumerate(d.get("positions", [])):
            Position.objects.create(
                section=ps,
                order=i,
                name=p.get("name", "")[:120],
                color_key=POS_KEYS[i % len(POS_KEYS)],
                steelman=p.get("steelman", "")[:400],
                description=p.get("description", ""),
                proponents=p.get("proponents", "")[:400],
                representative_name=p.get("representative_name", "")[:120],
                representative_note=p.get("representative_note", "")[:300],
                prevalence_weight=p.get("prevalence_weight") or 0,
                spectrum_position=p.get("spectrum_position"),
            )

        # Crux
        cx = sec(Section.CRUX)
        c = d.get("crux", {})
        if c.get("lead"):
            Crux.objects.create(
                section=cx,
                lead=c.get("lead", "")[:240],
                lead_highlight=c.get("lead_highlight", "")[:80],
                subtitle=c.get("subtitle", ""),
                empirical=c.get("empirical", ""),
                values=c.get("values", ""),
            )

        # Actions — map for_position name -> Position
        acts = sec(Section.ACTIONS)
        pos_by_name = {p.name: p for p in ps.positions.all()}
        for i, a in enumerate(d.get("actions", [])):
            kind = a.get("kind", "learn_more")
            Position_ref = pos_by_name.get(a.get("for_position"))
            Action.objects.create(
                section=acts,
                order=i,
                kind=kind if kind in ACTION_KINDS else "learn_more",
                title=a.get("title", "")[:200],
                description=a.get("description", "")[:400],
                url=a.get("url", "") or "",
                position=Position_ref,
                reveal=a.get("reveal", "condensed"),
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"loaded '{topic.title}' [{o['slug']}] status={o['status']} — "
                f"{bs.stats.count()} stats, {qs.questions.count()} questions, "
                f"{ps.positions.count()} positions, {acts.actions.count()} actions"
            )
        )
