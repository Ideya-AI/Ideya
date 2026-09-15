"""Seed the overview Section body for each top-level category (idempotent).

Category pages are pass-throughs to their topics, so a category needs only a
short, neutral framing of the domain — its central tension and what a reader
finds inside — not the steelman-per-position depth a topic gets. The page
renders ``sec.overview.body`` (falling back to the one-line ``description``),
so this fills that overview slot. Declarative + idempotent: update_or_create on
the (category, kind) unique constraint, so re-running just refreshes the text.

The one-line ``Category.description`` is left alone — it stays the tight
meta/OG blurb; these overviews are the richer on-page framing.
"""

from django.core.management.base import BaseCommand

from topics.models import Category, Section

# slug -> overview body. One descriptive sentence: what the category covers,
# named concretely, so a reader knows what is inside before opening it.
OVERVIEWS = {
    "ai": (
        "How advanced AI is built, governed, and understood: how fast "
        "capabilities are growing, how systems are kept aligned with human "
        "intent, how labs and governments regulate them, what they cost in "
        "energy and data, and whether machine minds could ever matter morally."
    ),
    "bio-health": (
        "Medicine and biotechnology at the edges of the human body: gene "
        "editing and embryo selection, drugs and how they are priced and "
        "approved, mental health, aging, reproduction, and the choices around "
        "the end of life."
    ),
    "climate-energy": (
        "The energy transition and the climate it is racing: which power "
        "sources to build, how to price and remove carbon, how fast to phase "
        "out fossil fuels, and what to do about tipping points, geoengineering, "
        "and the cost of it all."
    ),
    "digital": (
        "Life inside networked technology: online speech and moderation, "
        "privacy and surveillance, who owns data, encryption, automated "
        "decisions, and how deepfakes and algorithms shape what a society "
        "believes."
    ),
    "economy": (
        "How wealth and work are organized: inequality and wages, taxation, "
        "trade and industrial policy, housing, public debt, money and its "
        "future, the structure of firms and markets, and what automation does "
        "to jobs."
    ),
    "ethics": (
        "The foundations under everything else: whether moral facts are real, "
        "free will, personal identity, meaning, the moral status of animals and "
        "the unborn, and what we owe to strangers and to future generations."
    ),
    "food-land": (
        "How we feed ourselves and share the planet: farming methods, meat and "
        "its alternatives, animal welfare, land and water use, protected areas, "
        "wildfire, plastics, and how far to intervene in nature."
    ),
    "global-risk": (
        "Threats that could end or permanently derail civilization: engineered "
        "pandemics, nuclear war and nuclear winter, unaligned AI, asteroids and "
        "supervolcanoes, societal collapse, and how much to prioritize, slow, "
        "or surveil to prevent them."
    ),
    "governance": (
        "How power is constituted and constrained: democracy and its rivals, "
        "elections and courts, executive power, crime and drugs, immigration "
        "and borders, war and weapons, and the international order."
    ),
    "society": (
        "How communities and identities are changing: birth rates and family, "
        "education, religion, loneliness, identity and belonging, historical "
        "injustice, the media people trust, and the institutions that hold a "
        "society together."
    ),
}


class Command(BaseCommand):
    help = "Seed/refresh the overview text on each category page (idempotent)."

    def handle(self, *args, **options):
        by_slug = {c.slug: c for c in Category.objects.all()}
        written = 0
        for slug, body in OVERVIEWS.items():
            cat = by_slug.get(slug)
            if cat is None:
                self.stdout.write(self.style.WARNING(f"no category '{slug}' — skipped"))
                continue
            Section.objects.update_or_create(
                category=cat, kind=Section.OVERVIEW, defaults={"body": body}
            )
            written += 1
        self.stdout.write(
            self.style.SUCCESS(f"done — {written} category overview(s) set")
        )
