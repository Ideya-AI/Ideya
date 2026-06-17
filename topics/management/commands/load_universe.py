"""Load the curated topic universe (research/catalog/topic-universe.json) into the DB:
create the proposed category taxonomy, load every catalog topic (+ critic gaps) as a
DRAFT topic, remap the pre-existing topics into the new taxonomy, and wire related-topic
edges. Idempotent — safe to re-run. Existing topics keep their status + content."""

import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from topics.models import Category, Topic, TopicEdge

CATALOG = Path("research/catalog/topic-universe.json")

# New-taxonomy slug -> --cat-* colour key (see tokens.css / CAT_COLORS).
COLOR = {
    "global-risk": "risk",
    "ai": "tech",
    "digital": "digital",
    "climate-env": "energy",
    "bio-health": "bio",
    "economy": "econ",
    "governance": "gov",
    "society": "society",
    "ethics": "ethics",
}
# Phosphor icon per category (discovery-tier glyph).
CAT_ICON = {
    "global-risk": "warning-octagon",
    "ai": "cpu",
    "digital": "globe-hemisphere-west",
    "climate-env": "leaf",
    "bio-health": "heartbeat",
    "economy": "chart-line-up",
    "governance": "bank",
    "society": "users-three",
    "ethics": "scales",
}
# Pre-existing topics -> their home in the new taxonomy.
EXISTING_REMAP = {
    "nuclear-energy": "climate-env",
    "solar-power": "climate-env",
    "grid-storage": "climate-env",
    "geoengineering": "climate-env",
    "carbon-pricing": "economy",
    "gene-editing": "bio-health",
    "lab-grown-meat": "climate-env",
    "universal-basic-income": "economy",
    "ai-existential-risk": "global-risk",
}
# Gaps that duplicate a pre-existing topic — skip (existing covers them).
GAP_SKIP = {
    "Geoengineering: Solar Radiation Management",
    "Universal Basic Income vs. Targeted Welfare",
    "Nuclear Energy Expansion: Fission's Comeback",
}


class Command(BaseCommand):
    help = "Load the topic universe (categories + draft topics) from the catalog JSON."

    @transaction.atomic
    def handle(self, *args, **opts):
        data = json.loads(CATALOG.read_text())
        cats = data["proposed_categories"]
        new_slugs = {c["slug"] for c in cats}

        # 1) Categories — upsert the 9 proposed (updates reused slugs like ethics/governance).
        cat_by_slug = {}
        for c in cats:
            obj, _ = Category.objects.update_or_create(
                slug=c["slug"],
                defaults={
                    "name": c["name"],
                    "description": c["description"],
                    "color_key": COLOR.get(c["slug"], "energy"),
                    "icon": CAT_ICON.get(c["slug"], "squares-four"),
                },
            )
            cat_by_slug[c["slug"]] = obj

        # 2) Remap pre-existing topics into the new taxonomy (keep status + content).
        remapped = 0
        for slug, new_cat in EXISTING_REMAP.items():
            t = Topic.objects.filter(slug=slug).first()
            if t and new_cat in cat_by_slug:
                t.primary_category = cat_by_slug[new_cat]
                t.save(update_fields=["primary_category"])
                t.categories.set([cat_by_slug[new_cat]])
                remapped += 1
        existing_slugs = set(Topic.objects.values_list("slug", flat=True))

        # 3) Load catalog topics + selected gaps as DRAFT topics.
        def upsert(slug, title, summary, why_now, icon, primary, secondaries, dossier):
            if slug in existing_slugs:  # never clobber a pre-existing topic
                return None
            cat = cat_by_slug.get(primary)
            if not cat:
                return None
            t, _ = Topic.objects.update_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "summary": summary or "",
                    "why_now": why_now or "",
                    "icon": icon or "circle",
                    "status": Topic.DRAFT,
                    "primary_category": cat,
                    "research_dossier": dossier,
                },
            )
            sec = [cat] + [
                cat_by_slug[s] for s in secondaries if s in cat_by_slug and s != primary
            ]
            t.categories.set(sec)
            return t

        loaded = 0
        for e in data["catalog"]:
            slug = e.get("slug") or slugify(e["title"])
            t = upsert(
                slug,
                e["title"],
                e.get("summary"),
                e.get("why_now"),
                e.get("suggested_icon"),
                e["primary_category_slug"],
                e.get("secondary_category_slugs", []),
                {
                    "position_names": e.get("position_names", []),
                    "related_slugs": e.get("related_slugs", []),
                    "source": "universe-2026-06-16",
                },
            )
            if t:
                loaded += 1

        gaps_loaded = 0
        for g in data.get("missing", []):
            if g["title"] in GAP_SKIP:
                continue
            slug = slugify(g["title"])[:200]
            t = upsert(
                slug,
                g["title"],
                g.get("summary"),
                "",
                "circle",
                g.get("suggested_category_slug", ""),
                [],
                {
                    "position_names": [],
                    "related_slugs": [],
                    "source": "universe-gap-2026-06-16",
                },
            )
            if t:
                gaps_loaded += 1

        # 4) Wire related-topic edges from the catalog (relates_to).
        edges = 0
        slug_exists = set(Topic.objects.values_list("slug", flat=True))
        for e in data["catalog"]:
            src = Topic.objects.filter(
                slug=e.get("slug") or slugify(e["title"])
            ).first()
            if not src:
                continue
            for rel in e.get("related_slugs", []):
                if rel in slug_exists and rel != src.slug:
                    tgt = Topic.objects.filter(slug=rel).first()
                    if tgt:
                        _, made = TopicEdge.objects.get_or_create(
                            source=src, target=tgt, kind=TopicEdge.RELATES_TO
                        )
                        edges += made

        # 5) Remove now-orphaned old categories (slugs not in the new taxonomy).
        orphans = Category.objects.exclude(slug__in=new_slugs)
        orphan_names = list(orphans.values_list("slug", flat=True))
        orphans.delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"categories: {len(cats)} upserted | existing remapped: {remapped} | "
                f"catalog loaded: {loaded} | gaps loaded: {gaps_loaded} | edges: {edges} | "
                f"old categories removed: {orphan_names}"
            )
        )
        self.stdout.write(
            f"topics total: {Topic.objects.count()} "
            f"(published {Topic.objects.filter(status='published').count()}, "
            f"draft {Topic.objects.filter(status='draft').count()})"
        )
