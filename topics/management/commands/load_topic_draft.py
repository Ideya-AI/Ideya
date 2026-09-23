"""Load a research-pipeline draft (a TopicDraft JSON) into the DB as a topic:
Sections + typed children (Stat/Question/Position/Crux/Action), with position
colours, source dates, and the dossier. Items render in file order (§8). Idempotent —
rebuilds the topic's sections on each run. Use a distinct --slug to keep a gold
standard (e.g. nuclear-energy) intact while comparing.

Reads one topic file: `{slug, title, status, scope, primary_category,
categories, related}` plus
`content` once there is content. That file is the topic, cradle to grave — a topic
with only a title is the same object, earlier — and it is the ONLY source for a
topic's identity, placement and lifecycle. The engine's own output (gate
verdicts, the claim ledger, prescribed fixes) is process, lives in
research/runs/<slug>/record.json, and never enters the database.
"""

import datetime
import json
import re
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from django.utils.dateparse import parse_datetime
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


def image_prompt_from_brief(path: Path) -> str:
    """The '## Generation prompt' blockquote from an icon brief (same rule the
    generator reads), for provenance in Topic.primary_image_prompt."""
    lines = path.read_text().splitlines()
    try:
        start = next(
            i
            for i, l in enumerate(lines)
            if l.lower().startswith(("## generation prompt", "## prompt"))
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


def _num(text):
    """First number in a display string ("~6,500", "8.9%", "about 4"), or None."""
    m = re.search(r"-?\d+(?:\.\d+)?", str(text or "").replace(",", ""))
    return float(m.group()) if m else None


def derive_viz(s, viz, series):
    """The percentages the templates draw from, computed from the values so a
    file never authors them (SCHEMA.md, "Derived by code"). A value the file
    does carry wins, so exported files round-trip unchanged.

    ranked/sparkline: each row's pct is its share of the largest row.
    radial/bar: fill_pct is the value itself when the unit is a percentage.
    range: range_at is the value's position between range_min and range_max;
    a span value ("26–36") is left to Stat.range_band at render time."""
    if viz in ("ranked", "sparkline"):
        nums = [_num(r.get("value")) for r in series]
        top = max((n for n in nums if n is not None and n > 0), default=None)
        if top:
            for r, n in zip(series, nums):
                if r.get("pct") in (None, "") and n is not None:
                    r["pct"] = max(0, min(100, round(100 * n / top)))
    fill = s.get("fill_pct")
    if fill in (None, "") and viz in ("radial", "bar"):
        unit = str(s.get("unit") or "")
        n = _num(s.get("value"))
        if n is not None and ("%" in unit or "percent" in unit.lower()):
            fill = max(0, min(100, round(n)))
        else:
            fill = None
    at = s.get("range_at") if viz == "range" else None
    if at in (None, "") and viz == "range":
        v, lo, hi = _num(s.get("value")), _num(s.get("range_min")), _num(s.get("range_max"))
        span = re.search(r"\d\s*[–—-]\s*~?\d", str(s.get("value") or ""))
        if None not in (v, lo, hi) and hi > lo and not span:
            at = max(0, min(100, round(100 * (v - lo) / (hi - lo))))
        else:
            at = None
    return fill, at


def _index_of(path):
    """Top-level fields of a sibling topic file (cheap: the draft is skipped
    by never touching it)."""
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return {}


_PHOSPHOR = None


def _phosphor_has(name):
    global _PHOSPHOR
    if _PHOSPHOR is None:
        css = Path("static/vendor/phosphor-duotone.css").read_text()
        _PHOSPHOR = set(re.findall(r"\.ph-duotone\.ph-([a-z0-9-]+):before", css))
    return name in _PHOSPHOR


def wire_related(topic, doc, stderr=None):
    """Sync a topic's OUTGOING related edges to its file. Returns the number
    created. A target that does not exist yet is skipped (with a warning when
    `stderr` is given); `load_universe` runs a second pass once every topic
    exists, so forward references settle."""
    wanted = [r for r in (doc.get("related") or []) if r != topic.slug]
    want = set(wanted)
    have = {e.target.slug: e for e in topic.outgoing_edges.select_related("target")}
    edges = 0
    for i, rel in enumerate(wanted):
        if rel in have:
            if have[rel].order != i:  # file order is display order
                have[rel].order = i
                have[rel].save(update_fields=["order"])
            continue
        tgt = Topic.objects.filter(slug=rel).first()
        if tgt:
            TopicEdge.objects.update_or_create(
                source=topic, target=tgt, kind=TopicEdge.RELATES_TO, defaults={"order": i}
            )
            edges += 1
        elif stderr is not None:
            stderr.write(f"  related '{rel}' matches no topic — no edge created")
    for gone in set(have) - want:
        have[gone].delete()
    return edges


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
            help="Phosphor icon name (overrides the file's top-level `icon`).",
        )
        p.add_argument(
            "--image-brief",
            default="",
            help="path to research/topics/<slug>/icon.md; its '## Generation prompt' "
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
        """`primary_category` (shown in the header) then `categories` (the
        secondaries). The topic file is the only source: the
        separate catalog it used to fall back to is gone, so placement has one
        home and cannot disagree with itself."""
        primary = doc.get("primary_category") or ""
        if not primary:
            raise CommandError(
                f"no primary_category in {doc.get('slug')!r}. Every topic sits "
                "somewhere; the header shows exactly one category."
            )
        slugs = [primary] + [
            c for c in (doc.get("categories") or []) if c and c != primary
        ]
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
        return Topic.IN_PROGRESS if doc.get("content") else Topic.NOT_STARTED

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
        d = doc.get("content") or {}
        # Identity before anything else: every item must have a frozen id, so
        # the rows below are updated in place rather than rebuilt under the
        # reader participation that points at them.
        if d and ensure_ids(d):
            # Ids are assigned once and then frozen, so they belong in the file,
            # which is the source of truth. Written back only for the topic's
            # own file; a clone loaded from elsewhere is not the truth.
            src = Path(o["file"])
            if src.resolve().parent.parent == topics_dir().resolve():
                src.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
                self.stdout.write(f"  ids assigned and written to {src}")
        self._validate(doc, Path(o["file"]), o["slug"])
        title = o["title"] or self._resolve_title(doc)
        cat, extra_cats = self._resolve_categories(doc)
        if o["category"]:
            picked = Category.objects.filter(slug=o["category"]).first()
            if picked:
                cat, extra_cats = picked, [c for c in extra_cats if c.pk != picked.pk]

        ov = d.get("overview", {})
        # Icon: the file's top-level `icon`, which stage 3 writes (an explicit
        # --icon overrides). Blank is allowed — the page then wears the
        # category's glyph — but a name must be a real Phosphor glyph and must
        # not repeat within the primary category, where topics sit in a column.
        existing = Topic.objects.filter(slug=o["slug"]).first()
        icon = o["icon"] or doc.get("icon") or ""
        if icon:
            if not _phosphor_has(icon):
                raise CommandError(f"icon '{icon}' is not a Phosphor glyph")
            # Judged against the sibling FILES, not database rows: the
            # directory is the truth, and a rebuild loads in directory order,
            # so a row from the previous state must not count as a clash.
            clash = next(
                (
                    sib.parent.name
                    for sib in topics_dir().glob("*/topic.json")
                    if sib.parent.name != o["slug"]
                    and _index_of(sib).get("icon") == icon
                    and _index_of(sib).get("primary_category") == cat.slug
                ),
                None,
            )
            if clash:
                raise CommandError(
                    f"icon '{icon}' already used by '{clash}' in category "
                    f"'{cat.slug}' — glyphs must be unique within a category"
                )
        # Primary-art generation prompt: from --image-brief if given, else the
        # topic's own brief at the standard path, else keep what the topic
        # already had (never blow away provenance on a reload), else what the
        # draft carries. The path fallback is what lets publishing stay a pure
        # switch: attaching this used to be a flag only the publish step passed.
        image_prompt = doc.get("primary_image_prompt") or d.get("primary_image_prompt", "")
        brief_path = (
            Path(o["image_brief"])
            if o["image_brief"]
            else Path(f"research/topics/{o['slug']}/icon.md")
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
        if existing and existing.status == Topic.PUBLISHED and not o["allow_published"]:
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
            "why_now_source_label": (ov.get("why_now_source_label") or "")[:120],
            "why_now_source_url": ov.get("why_now_source_url") or "",
            "icon": icon,
            # The file's own lifecycle stamps: the authoring skill writes
            # authored_at, the human's publish writes published_at, and the
            # review skill appends to reviewed_at. The loader mirrors them.
            "authored_at": parse_datetime(str(doc.get("authored_at") or "")) or None,
            "published_at": parse_datetime(str(doc.get("published_at") or "")) or None,
            "reviewed_at": [s for s in (doc.get("reviewed_at") or []) if s],
        }
        if image_prompt:
            defaults["primary_image_prompt"] = image_prompt
        # --reviewed appends a review stamp in the same atomic transaction as the
        # load, so a publish cannot half-succeed into a state where the topic is
        # live but its review cadence still reads "never reviewed".
        if o["reviewed"]:
            defaults["reviewed_at"] = defaults["reviewed_at"] + [
                timezone.now().isoformat()
            ]
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
        bs = sec(Section.BASICS)  # Basics carries no intro; the tiles are the read
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
            fill_pct, range_at = derive_viz(s, viz, series)
            stat_keep.append(
                self._upsert(
                    Stat,
                    bs,
                    s.get("id", ""),
                    ("label", s.get("label", "")[:120]),
                    dict(
                        order=i,
                        label=s.get("label", "")[:120],
                        value=s.get("value", "")[:24],
                        unit=s.get("unit", "")[:24],
                        viz=viz,
                        wide=bool(s.get("wide")),
                        series=series if viz in ("ranked", "sparkline") else [],
                        range_min=str(s.get("range_min") or "")[:40],
                        range_max=str(s.get("range_max") or "")[:40],
                        range_at=range_at,
                        fill_pct=fill_pct,
                        note=self._cap(
                            s.get("note", ""), 400, "note", s.get("label", "")
                        ),
                        detail=s.get("detail", ""),
                        source_label=self._cap(
                            s.get("source_label", ""),
                            120,
                            "source_label",
                            s.get("label", ""),
                        ),
                        source_url=s.get("source_url", "") or "",
                        source_published=self._cap(
                            s.get("source_published", ""),
                            40,
                            "source_published",
                            s.get("label", ""),
                        ),
                        source_accessed=acc_date,
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
                    Question,
                    qs,
                    q.get("id", ""),
                    ("text", q_text),
                    dict(
                        order=i,
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
                    ),
                ).pk
            )

        retired += self._sweep(Question, qs, question_keep)

        # Positions — honour an explicit colour when the draft carries one (so an
        # exported topic round-trips its palette); else assign per index as
        # pipeline drafts have always relied on.
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
                    Position,
                    ps,
                    p.get("id", ""),
                    ("name", p.get("name", "")[:120]),
                    dict(
                        order=i,
                        name=p.get("name", "")[:120],
                        color_key=ck,
                        steelman=self._cap(
                            p.get("steelman", ""), 400, "steelman", p.get("name", "")
                        ),
                        detail=p.get("detail", ""),
                        proponents=self._cap(
                            p.get("proponents", ""),
                            400,
                            "proponents",
                            p.get("name", ""),
                        ),
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
                    Action,
                    acts,
                    a.get("id", ""),
                    ("title", a.get("title", "")[:200]),
                    dict(
                        order=i,
                        kind=kind if kind in ACTION_KINDS else "learn_more",
                        title=a.get("title", "")[:200],
                        description=self._cap(
                            a.get("description", ""),
                            400,
                            "description",
                            a.get("title", ""),
                        ),
                        url=a.get("url", "") or "",
                        position=Position_ref,
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
        kept_votes = (
            Vote.objects.filter(question__section__topic=topic).count()
            + Vote.objects.filter(position__section__topic=topic).count()
        )
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
        edges = wire_related(topic, doc, self.stderr)
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
