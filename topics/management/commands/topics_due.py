"""Report topics whose content is due for review, on the shared cadence.

A topic falls due `review_interval_days` (fast 90 / medium 180 / slow 365) after
it was last touched (latest `reviewed_at`, else `authored_at`). Never-touched topics
are always due.

This is a REPORT, not a queue: nothing consumes it. A due topic is a note to the
human, who decides whether it is worth editing its content file or re-running the
engine on it. Pair it with `check_links` for the link half of staleness.
"""

import json

from django.core.management.base import BaseCommand

from topics.models import Topic


class Command(BaseCommand):
    help = "List topics whose content is due for review."

    def add_arguments(self, p):
        p.add_argument(
            "--all", action="store_true", help="Show every topic, not just those due."
        )
        p.add_argument(
            "--status",
            choices=[c for c, _ in Topic.STATUS_CHOICES],
            help="Limit to one status (draft|published).",
        )
        p.add_argument(
            "--json", action="store_true", help="Emit machine-readable JSON."
        )

    def handle(self, *args, **o):
        qs = Topic.objects.all()
        if o.get("status"):
            qs = qs.filter(status=o["status"])
        else:
            # The ~118 unauthored topics are "always due" —
            # they drowned the report (132 rows of noise). Staleness is about
            # published topics unless a status is asked for explicitly.
            qs = qs.filter(status=Topic.PUBLISHED)
        # Most overdue first; never-touched (large sentinel) sort to the top.
        topics = sorted(qs, key=lambda t: t.days_overdue, reverse=True)

        rows = []
        for t in topics:
            if not o["all"] and not t.is_review_due:
                continue
            lt = t.last_touched
            rows.append(
                {
                    "slug": t.slug,
                    "title": t.title,
                    "status": t.status,
                    "last_touched": lt.date().isoformat() if lt else None,
                    "review_due": (
                        t.review_due_at.date().isoformat() if t.review_due_at else None
                    ),
                    "days_overdue": None if lt is None else t.days_overdue,
                    "due": t.is_review_due,
                }
            )

        if o["json"]:
            self.stdout.write(json.dumps(rows, indent=2))
            return

        if not rows:
            self.stdout.write(self.style.SUCCESS("No topics due for review. 🎉"))
            return

        scope = "topic(s)" if o["all"] else "topic(s) due for review"
        self.stdout.write(
            self.style.MIGRATE_HEADING(f"{len(rows)} {scope} (most overdue first):\n")
        )
        for r in rows:
            if r["last_touched"] is None:
                when, age = "never reviewed", "needs first review"
            else:
                when = f"last {r['last_touched']}"
                od = r["days_overdue"]
                age = f"{od}d overdue" if od >= 0 else f"due in {-od}d"
            line = (
                f"  • {r['slug']:<30} "
                f"[{r['status']:<9}] "
                f"{when:<20} {age}"
            )
            self.stdout.write(self.style.WARNING(line) if r["due"] else line)
