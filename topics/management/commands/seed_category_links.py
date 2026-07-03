"""Seed the 'Connects to' adjacency between categories (idempotent).

The catalog (`topic-universe.json`) leaves category relationships null, and the
9 top-level categories are peers (no parent hierarchy), so the adjacency is an
editorial graph of intellectual neighbours — the pairs a reader browsing one
category would plausibly cross into. `Category.connects_to` is symmetrical, so
each undirected edge is declared once. Declarative: clears all links first, then
applies EDGES, so re-running reproduces exactly this graph.

  manage.py seed_category_links
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from topics.models import Category

# Undirected neighbour pairs (slugs). Symmetrical → declare each once.
EDGES = [
    ("global-risk", "ai"),
    ("global-risk", "bio-health"),
    ("global-risk", "climate-env"),
    ("global-risk", "governance"),
    ("ai", "digital"),
    ("ai", "economy"),
    ("ai", "ethics"),
    ("ai", "governance"),
    ("digital", "society"),
    ("digital", "governance"),
    ("climate-env", "economy"),
    ("climate-env", "governance"),
    ("bio-health", "ethics"),
    ("bio-health", "society"),
    ("economy", "governance"),
    ("economy", "society"),
    ("society", "ethics"),
    ("governance", "ethics"),
]


class Command(BaseCommand):
    help = "Seed symmetrical 'Connects to' links between categories (idempotent)."

    @transaction.atomic
    def handle(self, *args, **opts):
        by_slug = {c.slug: c for c in Category.objects.all()}
        missing = {s for e in EDGES for s in e if s not in by_slug}
        if missing:
            self.stderr.write(
                self.style.WARNING(
                    f"skipping edges for unknown slugs: {sorted(missing)}"
                )
            )

        # Declarative: wipe then reapply, so the graph == EDGES exactly.
        for c in by_slug.values():
            c.connects_to.clear()

        applied = 0
        for a, b in EDGES:
            if a in by_slug and b in by_slug:
                by_slug[a].connects_to.add(by_slug[b])
                applied += 1

        for c in Category.objects.all():
            n = c.connects_to.count()
            self.stdout.write(f"  {c.slug}: {n} link{'s' if n != 1 else ''}")
        self.stdout.write(self.style.SUCCESS(f"applied {applied} edges."))
