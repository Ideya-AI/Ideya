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
        p.add_argument(
            "--icon",
            default="",
            help="Phosphor icon name; falls back to the draft's overview.icon, else 'atom'.",
        )

    @transaction.atomic
    def handle(self, *args, **o):
        payload = json.loads(Path(o["file"]).read_text())
        d = payload.get("draft", payload)
        cat = Category.objects.filter(slug=o["category"]).first()
        if not cat:
            raise CommandError(f"category '{o['category']}' not found")

        ov = d.get("overview", {})
        # Icon: explicit --icon wins, then the draft's icon (root level, where
        # export_topic writes it, or overview.icon), then the existing topic's
        # icon on a refresh (never clobber it), else 'atom'.
        existing = Topic.objects.filter(slug=o["slug"]).first()
        icon = (
            o["icon"]
            or d.get("icon")
            or ov.get("icon")
            or (existing.icon if existing else "")
            or "atom"
        )
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
                "icon": icon,
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
            # Long units/notes are drafting defects (unit is a display token;
            # a note is one sentence) — slicing silently garbles the rendered
            # tile, so say what was lost.
            for field, cap in (("unit", 12), ("note", 400)):
                if len(s.get(field, "")) > cap:
                    self.stderr.write(
                        self.style.WARNING(
                            f"{field} truncated to {cap} chars on stat "
                            f"'{s.get('label', '')[:60]}'"
                        )
                    )
            # Rich viz needs its data: ranked needs series rows, range needs
            # min/max. Fall back to bar (and say so) rather than render an
            # empty visualization.
            viz = s.get("viz", "bar")
            if viz not in dict(Stat.VIZ_CHOICES):
                viz = "bar"
            series = s.get("series") or []
            if viz == "ranked" and not (
                isinstance(series, list) and series and isinstance(series[0], dict)
            ):
                viz = "bar"
                series = []
            if viz == "range" and not (s.get("range_min") and s.get("range_max")):
                viz = "bar"
            if viz != s.get("viz", "bar"):
                self.stderr.write(
                    self.style.WARNING(
                        f"viz '{s.get('viz')}' missing its data on stat "
                        f"'{s.get('label', '')[:60]}' — fell back to bar"
                    )
                )
            Stat.objects.create(
                section=bs,
                order=i,
                tier=max(1, int(s.get("tier") or 1)),
                label=s.get("label", "")[:120],
                value=s.get("value", "")[:24],
                unit=s.get("unit", "")[:12],
                viz=viz,
                wide=bool(s.get("wide")),
                series=series if viz in ("ranked", "sparkline") else [],
                range_min=str(s.get("range_min") or "")[:40],
                range_max=str(s.get("range_max") or "")[:40],
                range_at=s.get("range_at") if viz == "range" else None,
                fill_pct=s.get("fill_pct"),
                note=s.get("note", "")[:400],
                detail=s.get("detail", ""),
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
                tier=max(1, int(q.get("tier") or 1)),
                text=q.get("text", "")[:400],
                kind=(
                    q.get("kind", "empirical")
                    if q.get("kind") in ("empirical", "value")
                    else "empirical"
                ),
                why=q.get("why", ""),
                detail=q.get("detail", ""),
                lean_label_a=q.get("lean_label_a", "")[:40],
                lean_label_b=q.get("lean_label_b", "")[:40],
                lean_pct_a=q.get("lean_pct_a"),
                reveal=q.get("reveal", "condensed"),
            )

        # Positions — honour an explicit colour when the draft carries one (so an
        # exported topic round-trips its palette); else assign per index as
        # pipeline drafts have always relied on. Carry prevalence + spectrum.
        ps = sec(Section.POSITIONS)
        for i, p in enumerate(d.get("positions", [])):
            ck = p.get("color_key")
            Position.objects.create(
                section=ps,
                order=i,
                tier=max(1, int(p.get("tier") or 1)),
                name=p.get("name", "")[:120],
                color_key=ck if ck in POS_KEYS else POS_KEYS[i % len(POS_KEYS)],
                steelman=p.get("steelman", "")[:400],
                description=p.get("description", ""),
                detail=p.get("detail", ""),
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
                tier=max(1, int(a.get("tier") or 1)),
                kind=kind if kind in ACTION_KINDS else "learn_more",
                title=a.get("title", "")[:200],
                description=a.get("description", "")[:400],
                url=a.get("url", "") or "",
                position=Position_ref,
                reveal=a.get("reveal", "condensed"),
            )

        # Placeholder guard: every external action must arrive with a real URL
        # (submit_view is the internal CTA and has none by design). A "#" here
        # means the draft skipped link authoring — flag it at the boundary so
        # neither the authoring engine nor a refresh can ship it silently.
        unauthored = [
            a
            for a in acts.actions.exclude(kind=Action.SUBMIT_VIEW)
            if not a.url.strip() or a.url.strip().startswith("#")
        ]
        for a in unauthored:
            self.stderr.write(
                self.style.ERROR(f"placeholder action URL: [{a.kind}] {a.title}")
            )
        if unauthored:
            self.stderr.write(
                self.style.ERROR(
                    f"{len(unauthored)} action(s) missing a real URL — fix the draft "
                    f"or run check_links --topic {o['slug']} before publishing."
                )
            )

        # Standard participation prompts — every topic gets the Add-your-view
        # endcap. Re-seeded each load so options track the rebuilt
        # positions/questions (prior reader Responses to them reset with it).
        from .seed_example_prompts import seed_topic_prompts

        seed_topic_prompts(topic)

        self.stdout.write(
            self.style.SUCCESS(
                f"loaded '{topic.title}' [{o['slug']}] status={o['status']} — "
                f"{bs.stats.count()} stats, {qs.questions.count()} questions, "
                f"{ps.positions.count()} positions, {acts.actions.count()} actions, "
                f"3 prompts"
            )
        )
