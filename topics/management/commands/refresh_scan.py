"""Phase 0 of a refresh: take stock deterministically, before any agent runs.

A refresh used to open by re-verifying every element of a topic against the web,
which costs the same whether anything moved or not. This command answers, for
free, the question that scopes the whole run: *what actually needs looking at?*

Four signals, one work order:

    clock       volatility cadence vs `reviewed_at` (the `topics_due` question)
    links       dead / placeholder / redirected URLs (reuses `check_links`)
    lint        register + shape findings on the topic JSON
    staleness   every stat's `source_accessed` age against a floor of
                2x the topic's review interval

The staleness floor is the backstop that makes scoped verification honest: a
durable figure is not re-verified every run, but nothing goes unchecked forever.
Stats with NO `source_accessed` sort to the top — an undated figure cannot be
shown to be current, and a re-confirmation that does not stamp the date leaves
the next run just as blind (nuclear-energy carried 5 of 12 undated after two
refreshes).

    manage.py refresh_scan --slug nuclear-energy
    manage.py refresh_scan --slug nuclear-energy --json     # run args for phase 1
    manage.py refresh_scan --slug nuclear-energy --skip-links
"""

import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path

from django.core.management.base import BaseCommand

from topics.models import Stat, Topic

from .check_links import check_one, collect_links

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/workflows"))

# Link states that are work; `blocked` is live-but-unverifiable and `ok` is fine.
LINK_WORK = {"dead", "placeholder", "redirect"}

# Staleness buckets, in report order. `undated` leads because it is the only one
# that cannot be reasoned about at all.
BUCKETS = ["undated", "past_floor", "aging", "fresh"]


def bucket_for(accessed, today, cadence, floor):
    """Where a stat's verification date sits against the cadence."""
    if accessed is None:
        return "undated", None
    age = (today - accessed).days
    if age >= floor:
        return "past_floor", age
    if age >= cadence:
        return "aging", age
    return "fresh", age


class Command(BaseCommand):
    help = "Deterministic pre-refresh scan: clock, links, lint, staleness, work order."

    def add_arguments(self, p):
        p.add_argument("--slug", required=True, help="Topic to scan.")
        p.add_argument("--json", action="store_true", help="Emit the run args as JSON.")
        p.add_argument("--skip-links", action="store_true", help="Skip network probes.")
        p.add_argument("--timeout", type=float, default=15.0, help="Per-URL timeout.")

    def handle(self, *a, **o):
        slug = o["slug"]
        topic = Topic.objects.filter(slug=slug).first()
        if not topic:
            self.stderr.write(self.style.ERROR(f"No topic with slug '{slug}'."))
            sys.exit(1)

        today = date.today()
        cadence = topic.review_interval_days
        floor = cadence * 2
        report = {
            "slug": slug,
            "title": topic.title,
            "status": topic.status,
            "volatility": topic.volatility,
            "cadence_days": cadence,
            "staleness_floor_days": floor,
            "today": today.isoformat(),
            "last_touched": (
                topic.last_touched.date().isoformat() if topic.last_touched else None
            ),
            "days_overdue": None if topic.last_touched is None else topic.days_overdue,
        }

        report["stats"] = self._stats(topic, today, cadence, floor)
        report["links"] = self._links(slug, o["timeout"], o["skip_links"])
        report["lint"] = self._lint(slug, len(report["stats"]))
        report["work_order"] = self._work_order(report)
        report["deterministic_verdict"] = (
            "work_found" if report["work_order"] else "clean"
        )

        if o["json"]:
            self.stdout.write(json.dumps(report, indent=2, ensure_ascii=False))
            return
        self._render(report)

    # -- signals -------------------------------------------------------------

    def _stats(self, topic, today, cadence, floor):
        rows = []
        qs = Stat.objects.filter(section__topic=topic).select_related("section")
        for s in qs.order_by("order", "id"):
            b, age = bucket_for(s.source_accessed, today, cadence, floor)
            rows.append(
                {
                    "label": s.label,
                    "value": f"{s.value}{s.unit}",
                    "viz": s.viz,
                    "wide": s.wide,
                    "series_rows": len(s.series or []),
                    "source_label": s.source_label,
                    "source_published": s.source_published,
                    "source_accessed": (
                        s.source_accessed.isoformat() if s.source_accessed else None
                    ),
                    "age_days": age,
                    "bucket": b,
                }
            )
        return rows

    def _links(self, slug, timeout, skip):
        if skip:
            return {"skipped": True, "counts": {}, "items": []}
        items = collect_links(slug)
        cache, counts, out = {}, Counter(), []
        for item in items:
            c = check_one(item.url, timeout, cache)
            counts[c.status] += 1
            if c.status in LINK_WORK:
                out.append(
                    {
                        "field": item.field,
                        "title": item.title,
                        "url": c.url,
                        "final_url": c.final_url,
                        "status": c.status,
                        "note": c.note,
                    }
                )
        return {
            "skipped": False,
            "total": len(items),
            "counts": dict(counts),
            "items": out,
        }

    def _lint(self, slug, db_stat_count):
        """Lint the topic JSON, and flag file/DB drift while we have both.

        Drift is the case Runbook B's export step exists to catch: an admin edit
        that never made it back to the JSON. A scan that read one and reported on
        the other would hide exactly that.
        """
        from lint_draft import lint  # noqa: PLC0415 — path is wired at import time

        path = ROOT / "research/topics" / f"{slug}.json"
        if not path.exists():
            return {"path": None, "findings": None, "drift": None}
        _, findings = lint(path, fix=False)
        doc = json.loads(path.read_text())
        draft = doc.get("draft", doc)
        file_stats = len((draft.get("basics") or {}).get("stats") or [])
        return {
            "path": str(path.relative_to(ROOT)),
            "findings": len(findings),
            "detail": findings,
            "drift": (
                None
                if file_stats == db_stat_count
                else f"{file_stats} stats in JSON vs {db_stat_count} in DB — export first"
            ),
        }

    # -- the work order ------------------------------------------------------

    def _work_order(self, r):
        """What phases 1-2 are allowed to scope themselves to.

        Deliberately narrow: broken links and figures that cannot be shown to be
        current. Everything else a refresh might change has to be justified by a
        development the scout finds, not by an agent's appetite for rewriting.
        """
        work = []
        for s in r["stats"]:
            if s["bucket"] == "undated":
                work.append(
                    {
                        "section": "basics",
                        "item": s["label"],
                        "reason": "no source_accessed — cannot be shown current",
                        "priority": 1,
                    }
                )
            elif s["bucket"] == "past_floor":
                work.append(
                    {
                        "section": "basics",
                        "item": s["label"],
                        "reason": f"verified {s['age_days']}d ago, past the "
                        f"{r['staleness_floor_days']}d floor",
                        "priority": 1,
                    }
                )
            elif s["bucket"] == "aging":
                work.append(
                    {
                        "section": "basics",
                        "item": s["label"],
                        "reason": f"verified {s['age_days']}d ago, over one cadence",
                        "priority": 2,
                    }
                )
        for l in r["links"]["items"]:
            work.append(
                {
                    "section": "actions" if l["field"] == "Action" else "basics",
                    "item": l["title"],
                    "reason": f"link {l['status']}"
                    + (f" ({l['note']})" if l["note"] else ""),
                    "priority": 1,
                }
            )
        work.sort(key=lambda w: (w["priority"], w["section"], w["item"]))
        return work

    # -- rendering -----------------------------------------------------------

    def _render(self, r):
        w, e, h = self.style.WARNING, self.style.ERROR, self.style.MIGRATE_HEADING
        out = self.stdout.write

        out(h(f"\n{r['title']}  ({r['slug']})"))
        od = r["days_overdue"]
        clock = (
            "never reviewed"
            if od is None
            else f"last touched {r['last_touched']} · "
            + (f"{od}d overdue" if od >= 0 else f"due in {-od}d")
        )
        out(
            f"  {r['status']} · {r['volatility']} cadence {r['cadence_days']}d · "
            f"staleness floor {r['staleness_floor_days']}d"
        )
        out(f"  {clock}")

        out(h("\nLinks"))
        if r["links"]["skipped"]:
            out("  skipped (--skip-links)")
        else:
            counts = r["links"]["counts"]
            summary = "  ·  ".join(f"{n} {k}" for k, n in sorted(counts.items()))
            out(f"  {r['links']['total']} links — {summary or 'none'}")
            for l in r["links"]["items"]:
                out(e(f"  {l['status'].upper():<12} {l['field']} · {l['title']}"))
                out(f"{' ' * 15}{l['url']}")
                if l["status"] == "redirect":
                    out(f"{' ' * 15}→ {l['final_url']}")

        out(h("\nLint"))
        li = r["lint"]
        if li["findings"] is None:
            out(w("  no topic JSON on disk — export first"))
        else:
            out(f"  {li['findings']} finding(s) in {li['path']}")
            if li["drift"]:
                out(e(f"  DRIFT: {li['drift']}"))

        out(h("\nStaleness"))
        byb = Counter(s["bucket"] for s in r["stats"])
        out("  " + "  ·  ".join(f"{byb.get(b, 0)} {b}" for b in BUCKETS))
        for s in r["stats"]:
            if s["bucket"] == "fresh":
                continue
            age = "never" if s["age_days"] is None else f"{s['age_days']}d"
            line = f"  {s['bucket']:<11} {age:<7} {s['label']}"
            out(e(line) if s["bucket"] in ("undated", "past_floor") else w(line))

        out(h("\nWork order"))
        if not r["work_order"]:
            out(
                self.style.SUCCESS(
                    "  Nothing mechanical to fix. If the scout finds no new "
                    "development, this is the light path: stamp reviewed_at."
                )
            )
            return
        for item in r["work_order"]:
            out(f"  p{item['priority']} [{item['section']}] {item['item']}")
            out(f"       {item['reason']}")
