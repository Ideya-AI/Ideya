"""Load a research-pipeline draft (a TopicDraft JSON) into the DB as a topic:
Sections + typed children (Stat/Question/Position/Crux/Action), with reveal levels,
position colours, prevalence/spectrum, source dates, and the dossier. Idempotent —
rebuilds the topic's sections on each run. Use a distinct --slug to keep a gold
standard (e.g. nuclear-energy) intact while comparing.

Reads one topic file: `{slug, title, status, scope, categories, related}` plus
`draft` once there is content. That file is the topic, cradle to grave — a topic
with only a title is the same object, earlier — and it is the ONLY source for a
topic's identity, placement and lifecycle. The engine's own output (gate
verdicts, the claim ledger, prescribed fixes) is process, lives in
research/runs/<slug>/record.json, and never enters the database.
"""

import datetime
import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from topics.item_ids import ensure_ids
from topics.item_status import topics_dir

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
            help="normally omitted: the topic file carries its own title.",
        )
        p.add_argument(
            "--category",
            default="",
            help="normally omitted: the topic file's `categories` are the "
            "source, primary first.",
        )
        p.add_argument(
            "--allow-published",
            action="store_true",
            help="permit overwriting the content of a PUBLISHED topic. Off by "
            "default: readers are looking at that page, and nothing re-certifies "
            "it afterwards. This is the flag the live-update flow passes.",
        )
        p.add_argument(
            "--status",
            default=None,
            choices=[c for c, _ in Topic.STATUS_CHOICES],
            help="normally omitted: loading content puts a topic IN_PROGRESS, "
            "withdraws READY, and leaves PUBLISHED alone. Reloading content is "
            "not a publishing decision.",
        )
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

    def _validate(self, doc, path, slug):
        """Cheap integrity on the file itself, before anything is written.

        A bad status is the dangerous case: it is not `published`, so the topic
        is invisible, and it is not `ready`, so it can never be published — a
        silent dead end nothing else reports.

        Identity is only ENFORCED for a file living in the topics directory,
        where the filename is the identity and a mismatch means the source of
        truth is corrupt. Loading some other file under a chosen slug is a clone
        and is allowed, with a note so it is never a surprise."""
        status = doc.get("status")
        valid = [c for c, _ in Topic.STATUS_CHOICES]
        if status and status not in valid:
            raise CommandError(
                f"'{slug}' has status {status!r}, which is not one of {valid}."
            )
        filed = doc.get("slug")
        if not filed or filed == slug:
            return
        if path.resolve().parent == topics_dir().resolve():
            raise CommandError(
                f"{path.name} says slug={filed!r}. In {topics_dir()}/ the "
                "filename IS the identity; fix one of them."
            )
        self.stdout.write(f"cloning {filed!r} as {slug!r}")

    @staticmethod
    def _resolve_title(doc):
        title = doc.get("title") or ""
        if not title:
            raise CommandError(
                f"no title in {doc.get('slug')!r} — a topic file must carry one "
                "from the moment it exists."
            )
        return title

    @staticmethod
    def _resolve_categories(doc):
        """Primary first, then the rest. The topic file is the only source: the
        separate catalog it used to fall back to is gone, so placement has one
        home and cannot disagree with itself."""
        slugs = [c for c in (doc.get("categories") or []) if c]
        if not slugs:
            raise CommandError(
                f"no categories in {doc.get('slug')!r}. Every topic sits "
                "somewhere; add at least a primary."
            )
        found = {c.slug: c for c in Category.objects.filter(slug__in=slugs)}
        missing = [c for c in slugs if c not in found]
        if missing:
            raise CommandError(
                f"unknown categor{'y' if len(missing) == 1 else 'ies'} "
                f"{missing} on '{doc.get('slug')}' — run load_universe to seed "
                "the taxonomy from research/categories.json."
            )
        return found[slugs[0]], [found[c] for c in slugs[1:]]

    @staticmethod
    def _status_after_load(existing, doc):
        """Where a topic sits once its file has been loaded: wherever the file
        says.

        The file is the source of truth, so loading it must reproduce it —
        otherwise rebuilding the database from the directory would silently
        demote every certified topic, which it did until this rule was fixed.

        Withdrawing readiness is therefore the job of whatever CHANGES the
        content, because that is what invalidates the certification, and the
        thing that changes content is the thing that writes the file. The engine
        sets `in_progress` when it persists a new draft. A hand edit should do
        the same; nothing can detect that for you.
        """
        filed = doc.get("status")
        if filed:
            return filed
        if existing is not None:
            return existing.status
        return Topic.IN_PROGRESS if doc.get("draft") else Topic.NOT_STARTED

    def _upsert(self, model, section, item_id, natural, fields):
        """One child row, found by its frozen id. Falling back to the natural
        key adopts a row loaded before ids existed (and any votes on it) exactly
        once, on the first load after the id landed."""
        obj = (
            model.objects.filter(section=section, item_id=item_id).first()
            if item_id
            else None
        )
        if obj is None and natural:
            field, value = natural
            obj = model.objects.filter(
                section=section, item_id="", **{field: value}
            ).first()
        if obj is None:
            return model.objects.create(section=section, item_id=item_id, **fields)
        obj.item_id = item_id
        for k, v in fields.items():
            setattr(obj, k, v)
        obj.save()
        return obj

    def _sweep(self, model, section, keep):
        """Retire children the draft no longer carries. Their votes go with
        them, which is the honest outcome: the item is gone."""
        gone = model.objects.filter(section=section).exclude(pk__in=keep)
        n = gone.count()
        gone.delete()
        return n

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
        # Atomic is load-bearing: the load upserts every section child and then
        # sweeps the ones the draft dropped; any later error must roll it back.
        doc = json.loads(Path(o["file"]).read_text())
        # One file per topic, cradle to grave: the index fields sit at the top
        # and `draft` appears once there is content. A topic with only a title
        # is the same object, earlier.
        d = doc.get("draft") or {}
        # Identity before anything else: every item must have a frozen id, so
        # the rows below are updated in place rather than rebuilt under the
        # reader participation that points at them.
        if d:
            ensure_ids(d)
        self._validate(doc, Path(o["file"]), o["slug"])
        title = o["title"] or self._resolve_title(doc)
        cat, extra_cats = self._resolve_categories(doc)
        if o["category"]:
            picked = Category.objects.filter(slug=o["category"]).first()
            if picked:
                cat, extra_cats = picked, [c for c in extra_cats if c.pk != picked.pk]

        ov = d.get("overview", {})
        # Icon: explicit --icon wins, then whatever stage 1 just produced
        # (draft root, or overview.icon), then the file's own top-level icon,
        # then the existing topic's on a reload, else 'atom'. The top-level entry
        # is what lets an UNAUTHORED topic carry a glyph at all — it has no
        # draft to hold one, and its stub page still renders an icon.
        existing = Topic.objects.filter(slug=o["slug"]).first()
        icon = (
            o["icon"]
            or d.get("icon")
            or ov.get("icon")
            or doc.get("icon")
            or (existing.icon if existing else "")
            or "atom"
        )
        # Primary-art generation prompt: from --image-brief if given, else the
        # topic's own brief at the standard path, else keep what the topic
        # already had (never blow away provenance on a reload), else what the
        # draft carries. The path fallback is what lets publishing stay a pure
        # switch: attaching this used to be a flag only the publish step passed.
        image_prompt = d.get("primary_image_prompt", "")
        brief_path = Path(o["image_brief"]) if o["image_brief"] else Path(
            f"research/icons/{o['slug']}.md"
        )
        if o["image_brief"] and not brief_path.exists():
            raise CommandError(f"--image-brief not found: {brief_path}")
        if brief_path.exists():
            image_prompt = image_prompt_from_brief(brief_path) or image_prompt
        if not image_prompt and existing:
            image_prompt = existing.primary_image_prompt
        # A published topic is one readers are currently reading, and loading
        # over it changes what they see while leaving it published — the ready
        # gate gets no say, because the topic never crosses back through it. So
        # overwriting live content is opt-in, which also keeps the authoring
        # engine (which never passes the flag) from ever touching a live page.
        if (
            existing
            and existing.status == Topic.PUBLISHED
            and not o["allow_published"]
        ):
            raise CommandError(
                f"'{o['slug']}' is PUBLISHED — refusing to overwrite live "
                "content. Take it off the site first "
                f"(`publish_topic --slug {o['slug']} --off --confirm`), or pass "
                "--allow-published if you mean to edit the page readers are on."
            )
        status = o["status"] or self._status_after_load(existing, doc)
        defaults = {
            "title": title,
            "status": status,
            # The seed line the planner is briefed with. Never rendered.
            "scope": doc.get("scope", ""),
            "primary_category": cat,
            "summary": ov.get("summary", ""),
            "scope_covered": ov.get("scope_covered", ""),
            "scope_excluded": ov.get("scope_excluded", ""),
            "why_now": ov.get("why_now", ""),
            "icon": icon,
            "researched_at": timezone.now(),
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
        if extra_cats:
            self.stdout.write(
                "  secondary categories: " + ", ".join(c.slug for c in extra_cats)
            )
        topic.categories.set([cat] + extra_cats)

        # Sections persist across loads (one per kind, enforced by the model);
        # only their children move. Nothing is deleted before the new content is
        # in place, so a Vote or a Response never loses the row it points at.
        def sec(kind, **kw):
            section, _ = Section.objects.update_or_create(
                topic=topic, kind=kind, defaults=kw
            )
            return section

        sec(Section.OVERVIEW)
        retired = 0
        stat_keep, question_keep, position_keep, action_keep = [], [], [], []

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
            stat_keep.append(
                self._upsert(
                    Stat, bs, s.get("id", ""), ("label", s.get("label", "")[:120]),
                    dict(
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
                    ),
                ).pk
            )

        retired += self._sweep(Stat, bs, stat_keep)

        # Questions
        qs = sec(Section.QUESTIONS)
        for i, q in enumerate(d.get("questions", [])):
            q_text = self._cap(
                q.get("text", ""), 400, "question text", q.get("text", "")
            )
            question_keep.append(
                self._upsert(
                    Question, qs, q.get("id", ""), ("text", q_text),
                    dict(
                        order=i,
                        tier=max(1, int(q.get("tier") or 1)),
                        text=q_text,
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
                    ),
                ).pk
            )

        retired += self._sweep(Question, qs, question_keep)

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
                # First unused colour, not index-modulo: an edit that swaps
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
            position_keep.append(
                self._upsert(
                    Position, ps, p.get("id", ""), ("name", p.get("name", "")[:120]),
                    dict(
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
                    ),
                ).pk
            )

        retired += self._sweep(Position, ps, position_keep)

        # Crux — one per section, so it updates in place.
        cx = sec(Section.CRUX)
        c = d.get("crux", {})
        if c.get("lead"):
            Crux.objects.update_or_create(
                section=cx,
                defaults=dict(
                    lead=c.get("lead", "")[:240],
                    lead_highlight=c.get("lead_highlight", "")[:80],
                    subtitle=c.get("subtitle", ""),
                    empirical=c.get("empirical", ""),
                    values=c.get("values", ""),
                ),
            )
        else:
            Crux.objects.filter(section=cx).delete()

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
            action_keep.append(
                self._upsert(
                    Action, acts, a.get("id", ""), ("title", a.get("title", "")[:200]),
                    dict(
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
                    ),
                ).pk
            )

        retired += self._sweep(Action, acts, action_keep)

        # Placeholder guard: every external action must arrive with a real URL
        # (submit_view is the internal CTA and has none by design). A "#" here
        # means the draft skipped link authoring — flag it at the boundary so
        # the authoring engine cannot ship it silently.
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
        # endcap. Upserted in place, so reader Responses to them survive a load.
        from .seed_example_prompts import seed_topic_prompts

        n_prompts = seed_topic_prompts(topic)

        # Vote counters are denormalized; recompute them for the rows that
        # survived this load rather than trusting a stale count.
        for q in Question.objects.filter(section=qs):
            Question.objects.filter(pk=q.pk).update(
                votes=Vote.objects.filter(question=q).count()
            )
        for pos in Position.objects.filter(section=ps):
            Position.objects.filter(pk=pos.pk).update(
                importance=Vote.objects.filter(position=pos).count()
            )
        kept_votes = Vote.objects.filter(question__section__topic=topic).count() + Vote.objects.filter(position__section__topic=topic).count()
        kept_leans = QuestionLean.objects.filter(question__section__topic=topic).count()
        if kept_votes or kept_leans or retired:
            self.stdout.write(
                f"participation: {kept_votes} vote(s), {kept_leans} lean(s) kept"
                + (f"; {retired} item(s) retired by this draft" if retired else "")
            )

        # This topic's OUTGOING related-topic edges, from its own file. Outgoing
        # only, and asymmetry is deliberate (2026-08-26): a niche topic may point
        # at a hub without being one of the hub's own best five. Incoming edges
        # are wired when the pointing topic is itself loaded, so `load_universe`
        # over the whole directory settles the graph.
        want = {r for r in (doc.get("related") or []) if r != o["slug"]}
        have = {e.target.slug: e for e in topic.outgoing_edges.select_related("target")}
        edges = 0
        for rel in want - set(have):
            tgt = Topic.objects.filter(slug=rel).first()
            if tgt:
                TopicEdge.objects.get_or_create(
                    source=topic, target=tgt, kind=TopicEdge.RELATES_TO
                )
                edges += 1
            else:
                self.stderr.write(
                    self.style.WARNING(
                        f"  related '{rel}' matches no topic — no edge created"
                    )
                )
        for gone in set(have) - want:
            have[gone].delete()
        if edges:
            self.stdout.write(f"related edges wired: {edges}")

        self.stdout.write(
            self.style.SUCCESS(
                f"loaded '{topic.title}' [{o['slug']}] status={status} — "
                f"{bs.stats.count()} stats, {qs.questions.count()} questions, "
                f"{ps.positions.count()} positions, {acts.actions.count()} actions, "
                f"{n_prompts} prompts"
            )
        )
