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
from django.utils.text import slugify

from topics.models import (
    POS_COLORS,
    Action,
    Category,
    Crux,
    Position,
    Question,
    QuestionLean,
    Section,
    Stat,
    Topic,
    TopicEdge,
    Vote,
)

POS_KEYS = [k for k, _ in POS_COLORS]
ACTION_KINDS = {k for k, _ in Action.KIND_CHOICES}


def _pct(v):
    """A valid 0-100 integer or None — the workflow schemas use -1 as their
    'unset' sentinel (structured output can't emit null), which must never
    reach the PositiveSmallIntegerField."""
    return v if isinstance(v, int) and 0 <= v <= 100 else None


def image_prompt_from_brief(path: Path) -> str:
    """The '## Generation prompt' blockquote from an icon brief (same rule the
    generator reads), for provenance in Topic.primary_image_prompt."""
    lines = path.read_text().splitlines()
    try:
        start = next(
            i
            for i, l in enumerate(lines)
            if l.lower().startswith("## generation prompt")
        )
    except StopIteration:
        return ""
    block, in_block = [], False
    for line in lines[start + 1 :]:
        if line.startswith(">"):
            in_block = True
            block.append(line.lstrip("> ").rstrip())
        elif in_block and line.strip() == "":
            block.append("")
        elif in_block:
            break
    return "\n".join(block).strip()


class Command(BaseCommand):
    help = "Load a research-pipeline TopicDraft JSON into the DB as a topic."

    def add_arguments(self, p):
        p.add_argument("--file", required=True)
        p.add_argument("--slug", required=True)
        # Title and category were required and hand-typed on every invocation —
        # three near-identical ones per publish (local, container, and the
        # DEPLOY seed). Both are recoverable from the artifacts, so they are now
        # optional and resolved in _resolve_title / _resolve_category, which
        # error loudly rather than guess when nothing supplies them.
        p.add_argument(
            "--title",
            default="",
            help="defaults to the draft's own title, else the catalog entry for --slug.",
        )
        p.add_argument(
            "--category",
            default="",
            help="primary category slug; defaults to draft.primary_category, "
            "then draft.categories[0] (stage 2 writes the primary first), "
            "then the catalog's primary_category_slug.",
        )
        p.add_argument("--status", default="draft", choices=["draft", "published"])
        p.add_argument(
            "--reviewed",
            action="store_true",
            help="also stamp reviewed_at=now() in the same transaction. This is "
            "the human-approval clock topics_due schedules from; setting it by "
            "hand afterwards was a separate `shell -c` that is easy to forget, "
            "and forgetting it is SILENT — the topic just quietly comes due early.",
        )
        p.add_argument(
            "--icon",
            default="",
            help="Phosphor icon name; falls back to the draft's overview.icon, else 'atom'.",
        )
        p.add_argument(
            "--image-brief",
            default="",
            help="path to research/icons/<slug>.md; its '## Generation prompt' "
            "blockquote is stored as Topic.primary_image_prompt for provenance.",
        )

    @staticmethod
    def _catalog_entry(slug):
        """The stage-0 catalog entry for a slug, or {}. The catalog is the
        authoritative source for a topic's title; pipeline-emitted drafts do not
        carry one."""
        path = Path("research/catalog/topic-universe.json")
        if not path.exists():
            return {}
        try:
            entries = json.loads(path.read_text()).get("catalog", [])
        except (json.JSONDecodeError, OSError):
            return {}
        return next(
            (e for e in entries if (e.get("slug") or slugify(e["title"])) == slug), {}
        )

    def _resolve_title(self, o, d, entry):
        title = o["title"] or d.get("title") or entry.get("title") or ""
        if not title:
            raise CommandError(
                f"no title for '{o['slug']}': not in --title, the draft, or the "
                "catalog. Pass --title explicitly."
            )
        return title

    def _resolve_category(self, o, d, entry):
        # draft.categories is written primary-first by stage 2 (ENGINE.md §5).
        cats = d.get("categories") or []
        slug = (
            o["category"]
            or d.get("primary_category")
            or (cats[0] if cats else "")
            or entry.get("primary_category_slug")
            or ""
        )
        if not slug:
            raise CommandError(
                f"no category for '{o['slug']}': not in --category, the draft, or "
                "the catalog. Pass --category explicitly."
            )
        cat = Category.objects.filter(slug=slug).first()
        if not cat:
            raise CommandError(f"category '{slug}' not found")
        return cat

    def _cap(self, value, cap, field, ident):
        """Slice to the model's max_length, but never silently: mid-sentence
        truncation ships broken prose to readers (found live on UBI's
        Targeted-Transfer representative_note, cut at exactly 300 chars)."""
        value = value or ""
        if len(value) > cap:
            self.stderr.write(
                self.style.WARNING(
                    f"{field} truncated to {cap} chars on '{ident[:60]}'"
                )
            )
        return value[:cap]

    @transaction.atomic
    def handle(self, *args, **o):
        # Atomic is load-bearing: the rebuild starts with a destructive
        # sections.delete(); any later error must roll the whole load back.
        payload = json.loads(Path(o["file"]).read_text())
        d = payload.get("draft", payload)
        entry = self._catalog_entry(o["slug"])
        title = self._resolve_title(o, d, entry)
        cat = self._resolve_category(o, d, entry)
        # Say what was inferred: a wrong title loaded silently is worse than one
        # the operator was asked for.
        if not o["title"] or not o["category"]:
            self.stdout.write(f"resolved: title={title!r} category={cat.slug!r}")

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
        # Primary-art generation prompt: from --image-brief if given, else keep
        # what the topic already had (never blow away provenance on a refresh),
        # else what the draft carries.
        image_prompt = d.get("primary_image_prompt", "")
        if o["image_brief"]:
            brief_path = Path(o["image_brief"])
            if not brief_path.exists():
                raise CommandError(f"--image-brief not found: {brief_path}")
            image_prompt = image_prompt_from_brief(brief_path) or image_prompt
        if not image_prompt and existing:
            image_prompt = existing.primary_image_prompt
        defaults = {
            "title": title,
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
        }
        if image_prompt:
            defaults["primary_image_prompt"] = image_prompt
        # Volatility drives the review cadence; the export carries it — a
        # round-trip must not silently reset it to the model default.
        if d.get("volatility") in dict(Topic.VOLATILITY_CHOICES):
            defaults["volatility"] = d["volatility"]
        # reviewed_at is the HUMAN-approval clock (researched_at above is the
        # machine's). Stamping it here puts it in the same atomic transaction as
        # the load, so a publish cannot half-succeed into a state where the topic
        # is live but its review cadence still reads "never reviewed".
        if o["reviewed"]:
            defaults["reviewed_at"] = timezone.now()
        topic, _ = Topic.objects.update_or_create(
            slug=o["slug"],
            defaults=defaults,
        )
        if d.get("categories") is None and existing:
            # A refresh draft carries no categories key — never clobber the
            # topic's existing secondaries (same rule as icon/volatility).
            extra_cats = [c for c in topic.categories.all() if c.pk != cat.pk]
        else:
            # The catalog is the source of truth for a topic's categories, and
            # it is right here. The workflows do not emit `draft.categories`, so
            # the runbook asked the orchestrator to hand-copy the catalog's
            # secondary_category_slugs onto the draft before loading — a manual
            # step whose only failure mode is silent. Four published topics
            # (housing-affordability-crisis, universal-basic-income, wildfires,
            # nuclear-energy-pipeline) carry no categories key at all, which is
            # what forgetting it looks like. Falling back to the catalog makes
            # the hand-step unnecessary rather than merely recommended.
            cslugs = d.get("categories")
            source = "draft"
            if not cslugs:
                cslugs = entry.get("secondary_category_slugs") or []
                source = "catalog"
            extra_cats = [
                c
                for cslug in cslugs
                if (c := Category.objects.filter(slug=cslug).first()) and c.pk != cat.pk
            ]
            if extra_cats:
                self.stdout.write(
                    f"  secondary categories ({source}): "
                    + ", ".join(c.slug for c in extra_cats)
                )
        topic.categories.set([cat] + extra_cats)

        # Participation survives a reload: the rebuild cascades Vote/QuestionLean
        # rows, so snapshot them keyed by question text / position name and
        # re-attach to the matching rebuilt rows. Rows whose text/name changed
        # in the new draft genuinely refer to something else — those votes drop
        # (reported below), which is the honest outcome.
        part_key = ("user_id", "session_key", "value")
        saved_qv = [
            (v.question.text, tuple(getattr(v, k) for k in part_key))
            for v in Vote.objects.filter(question__section__topic=topic).select_related(
                "question"
            )
        ]
        saved_pv = [
            (v.position.name, tuple(getattr(v, k) for k in part_key))
            for v in Vote.objects.filter(position__section__topic=topic).select_related(
                "position"
            )
        ]
        saved_leans = [
            (l.question.text, tuple(getattr(l, k) for k in part_key))
            for l in QuestionLean.objects.filter(
                question__section__topic=topic
            ).select_related("question")
        ]

        topic.sections.all().delete()  # clean rebuild

        def sec(kind, **kw):
            return Section.objects.create(topic=topic, kind=kind, **kw)

        sec(Section.OVERVIEW)

        # Basics
        b = d.get("basics", {})
        bs = sec(Section.BASICS, intro=b.get("intro", ""))
        for i, s in enumerate(b.get("stats", [])):
            acc = s.get("source_accessed")
            # A non-ISO date would abort the whole atomic load — degrade and
            # warn like the other malformed-field guards instead.
            try:
                acc_date = datetime.date.fromisoformat(acc) if acc else None
            except ValueError:
                self.stderr.write(
                    self.style.WARNING(
                        f"source_accessed '{acc}' is not YYYY-MM-DD on stat "
                        f"'{s.get('label', '')[:60]}' — stored as unset"
                    )
                )
                acc_date = None
            # Long units/notes are drafting defects (unit is a display token;
            # a note is one sentence) — slicing silently garbles the rendered
            # tile, so say what was lost.
            for field, cap in (("unit", 24), ("note", 400)):
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
            if viz in ("ranked", "sparkline") and not (
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
                unit=s.get("unit", "")[:24],
                viz=viz,
                wide=bool(s.get("wide")),
                series=series if viz in ("ranked", "sparkline") else [],
                range_min=str(s.get("range_min") or "")[:40],
                range_max=str(s.get("range_max") or "")[:40],
                range_at=s.get("range_at") if viz == "range" else None,
                fill_pct=s.get("fill_pct"),
                note=self._cap(s.get("note", ""), 400, "note", s.get("label", "")),
                detail=s.get("detail", ""),
                source_label=self._cap(
                    s.get("source_label", ""), 120, "source_label", s.get("label", "")
                ),
                source_url=s.get("source_url", "") or "",
                source_published=self._cap(
                    s.get("source_published", ""),
                    40,
                    "source_published",
                    s.get("label", ""),
                ),
                source_accessed=acc_date,
                reveal=s.get("reveal", "condensed"),
            )

        # Questions
        qs = sec(Section.QUESTIONS)
        for i, q in enumerate(d.get("questions", [])):
            Question.objects.create(
                section=qs,
                order=i,
                tier=max(1, int(q.get("tier") or 1)),
                text=self._cap(
                    q.get("text", ""), 400, "question text", q.get("text", "")
                ),
                kind=(
                    q.get("kind", "empirical")
                    if q.get("kind") in ("empirical", "value")
                    else "empirical"
                ),
                why=q.get("why", ""),
                detail=q.get("detail", ""),
                lean_label_a=q.get("lean_label_a", "")[:40],
                lean_label_b=q.get("lean_label_b", "")[:40],
                lean_pct_a=_pct(q.get("lean_pct_a")),
                reveal=q.get("reveal", "condensed"),
            )

        # Positions — honour an explicit colour when the draft carries one (so an
        # exported topic round-trips its palette); else assign per index as
        # pipeline drafts have always relied on. Carry prevalence + spectrum.
        ps = sec(Section.POSITIONS)
        assigned_keys = [
            p.get("color_key")
            for p in d.get("positions", [])
            if p.get("color_key") in POS_KEYS
        ]
        for i, p in enumerate(d.get("positions", [])):
            ck = p.get("color_key")
            if ck not in POS_KEYS:
                # First unused colour, not index-modulo: a refresh that swaps
                # one position out must not hand the newcomer a colour an
                # existing card already wears.
                ck = next((k for k in POS_KEYS if k not in assigned_keys), None)
                if ck is None:
                    # Palette exhausted — wrap, but LOUDLY: duplicate same-page
                    # position colors reached a render unnoticed once (a 10-camp
                    # topic vs the old 7-color palette, 2026-08-27).
                    ck = POS_KEYS[i % len(POS_KEYS)]
                    self.stderr.write(
                        self.style.WARNING(
                            f"position palette EXHAUSTED: '{p.get('name')}' wraps to "
                            f"duplicate color '{ck}' — extend POS_COLORS/--pos-* tokens"
                        )
                    )
                assigned_keys.append(ck)
            Position.objects.create(
                section=ps,
                order=i,
                tier=max(1, int(p.get("tier") or 1)),
                name=p.get("name", "")[:120],
                color_key=ck,
                steelman=self._cap(
                    p.get("steelman", ""), 400, "steelman", p.get("name", "")
                ),
                description=p.get("description", ""),
                detail=p.get("detail", ""),
                proponents=self._cap(
                    p.get("proponents", ""), 400, "proponents", p.get("name", "")
                ),
                representative_name=p.get("representative_name", "")[:120],
                representative_note=self._cap(
                    p.get("representative_note", ""),
                    300,
                    "representative_note",
                    p.get("name", ""),
                ),
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
            # A typo'd/renamed for_position silently unaligns the action —
            # surface it at the boundary like the placeholder-URL guard.
            if a.get("for_position") and Position_ref is None:
                self.stderr.write(
                    self.style.WARNING(
                        f"for_position '{a.get('for_position', '')[:60]}' matches no "
                        f"position on action '{a.get('title', '')[:60]}' — left unaligned"
                    )
                )
            Action.objects.create(
                section=acts,
                order=i,
                tier=max(1, int(a.get("tier") or 1)),
                kind=kind if kind in ACTION_KINDS else "learn_more",
                title=a.get("title", "")[:200],
                description=self._cap(
                    a.get("description", ""), 400, "description", a.get("title", "")
                ),
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

        # Re-attach the snapshotted participation to the rebuilt rows.
        if saved_qv or saved_pv or saved_leans:
            new_q = {q.text: q for q in Question.objects.filter(section=qs)}
            new_p = {p.name: p for p in Position.objects.filter(section=ps)}
            revived_votes, revived_leans, dropped = [], [], 0
            for text, (user_id, skey, val) in saved_qv:
                if text in new_q:
                    revived_votes.append(
                        Vote(
                            question=new_q[text],
                            user_id=user_id,
                            session_key=skey,
                            value=val,
                        )
                    )
                else:
                    dropped += 1
            for name, (user_id, skey, val) in saved_pv:
                if name in new_p:
                    revived_votes.append(
                        Vote(
                            position=new_p[name],
                            user_id=user_id,
                            session_key=skey,
                            value=val,
                        )
                    )
                else:
                    dropped += 1
            for text, (user_id, skey, val) in saved_leans:
                if text in new_q:
                    revived_leans.append(
                        QuestionLean(
                            question=new_q[text],
                            user_id=user_id,
                            session_key=skey,
                            value=val,
                        )
                    )
                else:
                    dropped += 1
            Vote.objects.bulk_create(revived_votes)
            QuestionLean.objects.bulk_create(revived_leans)
            for q in new_q.values():
                Question.objects.filter(pk=q.pk).update(
                    votes=Vote.objects.filter(question=q).count()
                )
            for p in new_p.values():
                Position.objects.filter(pk=p.pk).update(
                    importance=Vote.objects.filter(position=p).count()
                )
            msg = (
                f"participation preserved: "
                f"{len(revived_votes) + len(revived_leans)} row(s) re-attached"
            )
            if dropped:
                self.stderr.write(
                    self.style.WARNING(
                        msg + f"; {dropped} dropped (their question text / "
                        "position name changed in this draft)"
                    )
                )
            else:
                self.stdout.write(msg)

        # Wire related-topic edges from the catalog for this slug. load_universe
        # does this for the whole catalog at seed time; a topic loaded after that
        # run would otherwise ship with no "Connects to" chips (wildfires' edges
        # had to be created by hand). Idempotent, both directions.
        catalog_path = Path("research/catalog/topic-universe.json")
        if catalog_path.exists():
            entries = json.loads(catalog_path.read_text())["catalog"]
            edges = 0
            for e in entries:
                e_slug = e.get("slug") or slugify(e["title"])
                rels = e.get("related_slugs", [])
                if e_slug == o["slug"]:
                    for rel in rels:
                        tgt = (
                            Topic.objects.filter(slug=rel).exclude(pk=topic.pk).first()
                        )
                        if tgt:
                            _, made = TopicEdge.objects.get_or_create(
                                source=topic, target=tgt, kind=TopicEdge.RELATES_TO
                            )
                            edges += made
                elif o["slug"] in rels:
                    src = Topic.objects.filter(slug=e_slug).exclude(pk=topic.pk).first()
                    if src:
                        _, made = TopicEdge.objects.get_or_create(
                            source=src, target=topic, kind=TopicEdge.RELATES_TO
                        )
                        edges += made
            if edges:
                self.stdout.write(f"related edges wired from catalog: {edges}")

        self.stdout.write(
            self.style.SUCCESS(
                f"loaded '{topic.title}' [{o['slug']}] status={o['status']} — "
                f"{bs.stats.count()} stats, {qs.questions.count()} questions, "
                f"{ps.positions.count()} positions, {acts.actions.count()} actions, "
                f"3 prompts"
            )
        )
