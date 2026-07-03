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

# slug -> overview body. Neutral, editorial, steelman voice: map the strongest
# cases across the domain, hold promise and peril in the same frame.
OVERVIEWS = {
    "ai": (
        "Artificial intelligence has gone from a research curiosity to a "
        "general-purpose technology reshaping work, warfare, science, and "
        "speech — often faster than anyone can govern it. The hard questions "
        "here are less about what AI can do than about who steers it, how we "
        "keep increasingly capable systems aligned with human intent, and what "
        "we owe the people and institutions it disrupts. These topics hold the "
        "promise and the peril in the same frame."
    ),
    "bio-health": (
        "Biology is becoming an engineering discipline: we can read, edit, and "
        "increasingly write the code of life, and medicine is being remade "
        "around it. That power forces genuinely new questions — what we should "
        "cure versus enhance, who gets access, and where the limits of the "
        "human body are a fact rather than a choice. These topics weigh the "
        "extraordinary upside against risks that are just as unprecedented."
    ),
    "climate-env": (
        "Climate and energy is where physics, economics, and politics collide "
        "on a planetary deadline. Almost everyone agrees the stakes are high; "
        "the real disagreements are about pace, cost, technology, and who pays "
        "— nuclear versus renewables, adaptation versus mitigation, growth "
        "versus restraint. These topics map those trade-offs rather than the "
        "caricatures of them."
    ),
    "digital": (
        "Networked technology rewired how billions of people speak, learn, "
        "work, and are watched — in barely two decades. The tensions are "
        "structural: open discourse versus moderation, connection versus "
        "surveillance, free platforms paid for with attention and data. These "
        "topics examine the information order we now live inside, and the "
        "choices still open to us."
    ),
    "economy": (
        "How a society organizes wealth, work, prices, and markets is among "
        "the oldest and most contested questions there is — and the evidence "
        "rarely settles it cleanly. Here you'll find the durable arguments over "
        "growth and inequality, markets and the state, automation and the "
        "future of work. The aim is to show where economists actually "
        "disagree, and why."
    ),
    "ethics": (
        "Underneath most hard issues sits a philosophical one: what is "
        "valuable, what we owe each other, and how to act under deep "
        "uncertainty. This category takes those foundations seriously on their "
        "own terms — moral status, the mind, justice, the good life — rather "
        "than treating them as decoration on policy fights. Expect the oldest "
        "questions, argued in their strongest forms."
    ),
    "global-risk": (
        "Some threats are unlikely in any given year but could end or "
        "permanently derail civilization — engineered pandemics, nuclear war, "
        "unaligned AI, and risks we haven't named yet. They're systematically "
        "under-attended precisely because they're rare and abstract. These "
        "topics take the tail seriously: what the real risks are, how large, "
        "and what actually reduces them."
    ),
    "governance": (
        "Governance is the machinery that turns competing interests into "
        "collective decisions — and every arrangement of it trades some values "
        "against others. The questions here are perennial and unresolved: how "
        "power should be constituted and constrained, how much the state "
        "should do, and how legitimacy is won and lost. These topics map the "
        "strongest cases across the spectrum, not a house line."
    ),
    "society": (
        "Societies are held together by shared identities, norms, and "
        "institutions that are always shifting and always contested. This "
        "category looks at how communities form and fracture — around "
        "demographics, culture, belonging, and the stories groups tell about "
        "themselves. It treats these debates as genuine disagreements about "
        "how to live together, argued in good faith."
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
