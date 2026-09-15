from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from ..models import Category, Section, Topic


class CategoryPageTests(TestCase):
    """The category page renders from category + topic data alone — it must NOT
    depend on Section rows (none are seeded for categories; a prior version
    rendered a blank page because all content lived inside a sections loop)."""

    def setUp(self):
        self.cat = Category.objects.create(
            slug="test-cat",
            name="Test Category",
            description="A category description that should appear in the hero.",
            color_key="climate-energy",
            icon="leaf",
        )
        self.topic = Topic.objects.create(
            slug="test-topic",
            title="Test Topic",
            summary="A published topic in the category.",
            status="published",
            primary_category=self.cat,
        )
        self.topic.categories.add(self.cat)
        # Public listings show only authored topics (a positions section
        # exists) — the guard below is about CATEGORY sections staying empty.
        Section.objects.create(topic=self.topic, kind=Section.POSITIONS)
        self.url = reverse("topics:category", args=[self.cat.slug])

    def test_renders_overview_and_topic_without_sections(self):
        # No Section rows exist for the category — this guards the blank bug.
        self.assertFalse(self.cat.sections.exists())
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        body = resp.content.decode()
        self.assertIn("Test Category", body)  # title
        self.assertIn("A category description", body)  # hero description
        self.assertIn("Test Topic", body)  # topic listed in the grid
        self.assertIn("1 topic", body)  # count in the eyebrow

    def test_draft_topics_excluded(self):
        Topic.objects.create(
            slug="draft-topic",
            title="Draft Topic",
            summary="Should not show.",
            status="in_progress",
            primary_category=self.cat,
        ).categories.add(self.cat)
        body = self.client.get(self.url).content.decode()
        self.assertNotIn("Draft Topic", body)
        self.assertIn("1 topic", body)

    def test_zero_topic_state(self):
        empty = Category.objects.create(
            slug="empty-cat", name="Empty Category", description="Nothing here yet."
        )
        body = self.client.get(
            reverse("topics:category", args=[empty.slug])
        ).content.decode()
        self.assertIn("No topics in this category yet", body)
        self.assertIn("0 topic", body)
        # The promo lead must be suppressed when the grid is empty.
        self.assertNotIn("Colour dots preview each debate", body)

    def test_connects_to_chip_renders(self):
        other = Category.objects.create(
            slug="neighbour", name="Neighbour Category", color_key="ai"
        )
        self.cat.connects_to.add(other)  # symmetrical
        body = self.client.get(self.url).content.decode()
        self.assertIn("Connects to", body)
        self.assertIn("Neighbour Category", body)

    def test_unknown_category_404(self):
        self.assertEqual(
            self.client.get(reverse("topics:category", args=["nope"])).status_code, 404
        )

    def test_share_card_renders(self):
        share = reverse("topics:category_share", args=[self.cat.slug])
        preview = self.client.get(share)
        self.assertEqual(preview.status_code, 200)
        self.assertIn("Test Category", preview.content.decode())
        og = self.client.get(share + "?render=og")
        self.assertEqual(og.status_code, 200)
        self.assertIn("card-only", og.content.decode())  # bare capture body

    def test_og_image_falls_back_without_card(self):
        # No committed card for this slug → social_card is None → the page keeps
        # the base default og:image rather than emitting nothing (the fallback
        # the block.super guard protects).
        self.assertIsNone(self.cat.social_card)
        self.assertIn('property="og:image"', self.client.get(self.url).content.decode())


class SeedCategoryOverviewsTests(TestCase):
    """seed_category_overviews fills each category's overview Section (shown on
    the page in place of the one-line description) and is safely idempotent."""

    def test_seeds_overview_and_is_idempotent(self):
        cat = Category.objects.create(slug="ai", name="AI", color_key="ai")

        call_command("seed_category_overviews")
        ov = Section.objects.get(category=cat, kind=Section.OVERVIEW)
        self.assertIn("How advanced AI is built", ov.body)

        # Re-running updates in place — no duplicate rows (unique constraint).
        call_command("seed_category_overviews")
        self.assertEqual(
            Section.objects.filter(category=cat, kind=Section.OVERVIEW).count(), 1
        )

    def test_overview_overrides_description_on_page(self):
        Category.objects.create(
            slug="ai", name="AI", color_key="ai", description="short blurb"
        )
        call_command("seed_category_overviews")
        body = self.client.get(reverse("topics:category", args=["ai"])).content.decode()
        self.assertIn("How advanced AI is built", body)
