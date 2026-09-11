import json
from io import StringIO
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse

from ..models import (
    Category,
    Position,
    Question,
    Section,
    Topic,
    Vote,
)


class NuclearFixtureMixin:
    """Seeds the Nuclear Energy topic the way fresh databases do now — through
    the loader from research/topics/nuclear-energy.json. (The old seed
    migration 0002 was retired/emptied 2026-07-10; content's single source of
    truth is the per-topic JSON.) Also creates a published section-less stub
    so the empty-state path stays covered."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        # Seed the REAL taxonomy, not one category: a topic file names its
        # secondaries too, and the loader (rightly) refuses a category it cannot
        # find. Hand-picking one here meant the fixture broke the moment a topic
        # gained a second category.
        for c in json.loads(
            (Path(settings.BASE_DIR) / "research/categories.json").read_text()
        ):
            Category.objects.get_or_create(
                slug=c["slug"],
                defaults={"name": c["name"], "color_key": "energy"},
            )
        call_command(
            "load_topic_draft",
            file=str(Path(settings.BASE_DIR) / "research/topics/nuclear-energy/topic.json"),
            slug="nuclear-energy",
            title="Nuclear Energy",
            category="climate-env",
            status="published",
            stdout=StringIO(),
            stderr=StringIO(),
        )
        Topic.objects.get_or_create(
            slug="solar-power",
            defaults={"title": "Solar Power", "status": Topic.PUBLISHED},
        )


class ParticipationTests(NuclearFixtureMixin, TestCase):
    """Upvote backbone (P2): idempotent, retractable, session-keyed.
    Runs against the Nuclear Energy fixture (NuclearFixtureMixin)."""

    def setUp(self):
        self.question = Question.objects.order_by("id").first()
        self.position = Position.objects.order_by("id").first()
        self.topic = self.position.section.topic

    # ---- importance votes -------------------------------------------------

    def test_vote_then_retract_question(self):
        start = self.question.votes
        url = reverse("topics:vote", args=["question", self.question.id])

        self.client.post(url)
        self.question.refresh_from_db()
        self.assertEqual(self.question.votes, start + 1)
        self.assertEqual(Vote.objects.filter(question=self.question).count(), 1)

        self.client.post(url)  # same session again → retract
        self.question.refresh_from_db()
        self.assertEqual(self.question.votes, start)
        self.assertEqual(Vote.objects.filter(question=self.question).count(), 0)

    def test_vote_then_retract_position(self):
        start = self.position.importance
        url = reverse("topics:vote", args=["position", self.position.id])

        self.client.post(url)
        self.position.refresh_from_db()
        self.assertEqual(self.position.importance, start + 1)

        self.client.post(url)
        self.position.refresh_from_db()
        self.assertEqual(self.position.importance, start)

    def test_distinct_sessions_count_separately(self):
        start = self.question.votes
        url = reverse("topics:vote", args=["question", self.question.id])
        self.client.post(url)
        Client().post(url)
        self.question.refresh_from_db()
        self.assertEqual(self.question.votes, start + 2)
        self.assertEqual(Vote.objects.filter(question=self.question).count(), 2)

    def test_unknown_vote_target_is_400(self):
        resp = self.client.post(
            reverse("topics:vote", args=["banana", self.question.id])
        )
        self.assertEqual(resp.status_code, 400)

    def test_downvote_rejected(self):
        resp = self.client.post(
            reverse("topics:vote", args=["question", self.question.id]),
            {"dir": "down"},
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(Vote.objects.filter(question=self.question).count(), 0)


class PageTests(NuclearFixtureMixin, TestCase):
    def test_core_pages_render(self):
        # /about/ retired at pre-launch cleanup — About is a home anchor now.
        for url in ["/", "/nuclear-energy/", "/category/climate-env/"]:
            self.assertEqual(self.client.get(url).status_code, 200, url)

    def test_stub_topic_renders_empty_state(self):
        resp = self.client.get("/solar-power/")
        self.assertContains(resp, "on the map, but not yet written")


class ContentManagementTests(NuclearFixtureMixin, TestCase):
    """Draft/published workflow (P2 task 7)."""

    def setUp(self):
        self.draft = Topic.objects.create(
            title="Carbon Capture", slug="carbon-capture", status=Topic.IN_PROGRESS
        )

    def test_draft_gets_coming_soon_stub_not_content(self):
        # Drafts are public teaser pages (2026-08-10): stub note + noindex,
        # never sections — and they stay out of home and search.
        resp = self.client.get("/carbon-capture/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "on the map, but not yet written")
        self.assertContains(resp, "noindex")
        self.assertNotContains(self.client.get("/"), "Carbon Capture")
        self.assertNotContains(self.client.get("/search/?q=carbon"), "Carbon Capture")

    def test_staff_previews_draft_with_banner(self):
        staff = get_user_model().objects.create_user(
            "editor@example.com", "atlas-editor-9", is_staff=True
        )
        self.client.force_login(staff)
        resp = self.client.get("/carbon-capture/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "In progress — not publicly visible.")

    def test_seeded_topics_are_published(self):
        self.assertEqual(Topic.published.count(), Topic.objects.count() - 1)

    def test_missing_sections_tracks_spine(self):
        self.assertEqual(len(self.draft.missing_sections), 6)
        Section.objects.create(topic=self.draft, kind=Section.OVERVIEW)
        self.assertNotIn("overview", self.draft.missing_sections)
        nuclear = Topic.objects.get(slug="nuclear-energy")
        self.assertEqual(nuclear.missing_sections, [])


class LayeredReadingTests(NuclearFixtureMixin, TestCase):
    """Decision A: medium sets the base, per-section expanders go deeper."""

    def test_topic_page_has_expanders_not_global_toggle(self):
        resp = self.client.get("/nuclear-energy/")
        self.assertContains(resp, "Go deeper")
        self.assertNotContains(resp, "Reading depth")
        self.assertNotContains(resp, "data-depth")

    def test_sections_without_layers_get_no_expander(self):
        topic = Topic.objects.create(title="Bare", slug="bare", status=Topic.PUBLISHED)
        section = Section.objects.create(topic=topic, kind=Section.QUESTIONS)
        self.assertFalse(section.has_layer_normal)
        self.assertFalse(section.has_layer_deep)
        resp = self.client.get("/bare/")
        self.assertNotContains(resp, "Go deeper")


class SearchAndSeoTests(NuclearFixtureMixin, TestCase):
    """Task 13 (FTS5) + task 15 (states/SEO) coverage."""

    def test_fts_finds_topic_by_body_text(self):
        resp = self.client.get("/search/?q=fission")
        self.assertContains(resp, "Nuclear Energy")

    def test_fts_prefix_matching(self):
        # The popup highlights the matched prefix (<mark>Nucl</mark>ear Energy),
        # so assert on the stable link target, not the split title string.
        resp = self.client.get("/search/?q=nucl")
        self.assertContains(resp, 'href="/nuclear-energy/"')

    def test_fts_index_follows_edits(self):
        topic = Topic.objects.get(slug="nuclear-energy")
        topic.summary = "zephyrwordtest appears here"
        topic.save()
        self.assertContains(
            self.client.get("/search/?q=zephyrwordtest"), "Nuclear Energy"
        )

    def test_search_hostile_input_is_safe(self):
        resp = self.client.get('/search/?q="; DROP TABLE--')
        self.assertEqual(resp.status_code, 200)

    def test_sitemap_and_robots(self):
        resp = self.client.get("/sitemap.xml")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "/nuclear-energy/")
        robots = self.client.get("/robots.txt")
        self.assertContains(robots, "Sitemap:")

    def test_sitemap_excludes_drafts(self):
        Topic.objects.create(title="Hidden", slug="hidden-draft", status=Topic.IN_PROGRESS)
        self.assertNotContains(self.client.get("/sitemap.xml"), "hidden-draft")

    def test_custom_404_page(self):
        with self.settings(DEBUG=False):
            resp = self.client.get("/definitely-not-a-real-page/")
        self.assertEqual(resp.status_code, 404)
        self.assertContains(resp, "isn't on the map", status_code=404)

    def test_topic_og_tags(self):
        resp = self.client.get("/nuclear-energy/")
        self.assertContains(resp, 'property="og:type" content="article"')
        self.assertContains(resp, 'property="og:title" content="Nuclear Energy')
