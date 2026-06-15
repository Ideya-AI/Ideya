from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import (
    MIN_STANCE_SAMPLE,
    Position,
    Question,
    Section,
    Stance,
    Submission,
    Topic,
    Vote,
)


class ParticipationTests(TestCase):
    """Vote + Stance backbone (P2): idempotent, retractable, session-keyed.
    Uses the Nuclear Energy fixture from the seed migration."""

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

    # ---- stances -----------------------------------------------------------

    def test_stance_set_switch_retract(self):
        url = reverse("topics:stance", args=[self.position.id])

        self.client.post(url, {"value": "agree"})
        stance = Stance.objects.get(position=self.position)
        self.assertEqual(stance.value, "agree")

        self.client.post(url, {"value": "disagree"})  # switch
        stance.refresh_from_db()
        self.assertEqual(stance.value, "disagree")
        self.assertEqual(Stance.objects.filter(position=self.position).count(), 1)

        self.client.post(url, {"value": "disagree"})  # same again → retract
        self.assertEqual(Stance.objects.filter(position=self.position).count(), 0)

    def test_stance_rejects_unknown_value(self):
        resp = self.client.post(
            reverse("topics:stance", args=[self.position.id]), {"value": "maybe"}
        )
        self.assertEqual(resp.status_code, 400)

    def test_ratio_gated_by_min_sample(self):
        for i in range(MIN_STANCE_SAMPLE - 1):
            Stance.objects.create(
                position=self.position, session_key=f"s{i}", value="agree"
            )
        self.assertFalse(self.position.stance_stats["shown"])

        Stance.objects.create(
            position=self.position, session_key="s-last", value="disagree"
        )
        stats = self.position.stance_stats
        self.assertTrue(stats["shown"])
        self.assertEqual(stats["total"], MIN_STANCE_SAMPLE)
        self.assertEqual(stats["pct_agree"], 90)

    # ---- submit flow ---------------------------------------------------------

    def test_submit_with_no_position(self):
        resp = self.client.post(
            reverse("topics:submit"),
            {"topic": self.topic.id, "position": "none", "stance": "neutral"},
        )
        self.assertEqual(resp.status_code, 200)
        sub = Submission.objects.latest("created_at")
        self.assertIsNone(sub.position)
        self.assertEqual(Stance.objects.count(), 0)

    def test_submit_upserts_stance_without_importance_bump(self):
        start = self.position.importance
        self.client.post(
            reverse("topics:submit"),
            {
                "topic": self.topic.id,
                "position": self.position.id,
                "stance": "agree",
                "importance": 4,
            },
        )
        self.position.refresh_from_db()
        self.assertEqual(self.position.importance, start)  # no conflated bump
        self.assertEqual(Stance.objects.get(position=self.position).value, "agree")

        # Submitting again with a different stance updates, not duplicates.
        self.client.post(
            reverse("topics:submit"),
            {
                "topic": self.topic.id,
                "position": self.position.id,
                "stance": "disagree",
            },
        )
        self.assertEqual(Stance.objects.filter(position=self.position).count(), 1)
        self.assertEqual(Stance.objects.get(position=self.position).value, "disagree")


class PageTests(TestCase):
    def test_core_pages_render(self):
        for url in ["/", "/about/", "/nuclear-energy/", "/category/energy/"]:
            self.assertEqual(self.client.get(url).status_code, 200, url)

    def test_stub_topic_renders_empty_state(self):
        resp = self.client.get("/solar-power/")
        self.assertContains(resp, "on the map, but not yet written")


class ContentManagementTests(TestCase):
    """Draft/published workflow (P2 task 7)."""

    def setUp(self):
        self.draft = Topic.objects.create(
            title="Carbon Capture", slug="carbon-capture", status=Topic.DRAFT
        )

    def test_draft_is_invisible_to_readers(self):
        self.assertEqual(self.client.get("/carbon-capture/").status_code, 404)
        self.assertNotContains(self.client.get("/"), "Carbon Capture")
        self.assertNotContains(
            self.client.get("/search/?q=carbon"), "Carbon Capture"
        )

    def test_staff_previews_draft_with_banner(self):
        staff = get_user_model().objects.create_user(
            "editor@example.com", "atlas-editor-9", is_staff=True
        )
        self.client.force_login(staff)
        resp = self.client.get("/carbon-capture/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Draft — only staff can see this page.")

    def test_seeded_topics_are_published(self):
        self.assertEqual(Topic.published.count(), Topic.objects.count() - 1)

    def test_missing_sections_tracks_spine(self):
        self.assertEqual(len(self.draft.missing_sections), 6)
        Section.objects.create(topic=self.draft, kind=Section.OVERVIEW)
        self.assertNotIn("overview", self.draft.missing_sections)
        nuclear = Topic.objects.get(slug="nuclear-energy")
        self.assertEqual(nuclear.missing_sections, [])


class LayeredReadingTests(TestCase):
    """Decision A: medium sets the base, per-section expanders go deeper."""

    def test_topic_page_has_expanders_not_global_toggle(self):
        resp = self.client.get("/nuclear-energy/")
        self.assertContains(resp, "Go deeper")
        self.assertNotContains(resp, "Reading depth")
        self.assertNotContains(resp, "data-depth")

    def test_sections_without_layers_get_no_expander(self):
        topic = Topic.objects.create(
            title="Bare", slug="bare", status=Topic.PUBLISHED
        )
        section = Section.objects.create(topic=topic, kind=Section.QUESTIONS)
        self.assertFalse(section.has_layer_normal)
        self.assertFalse(section.has_layer_deep)
        resp = self.client.get("/bare/")
        self.assertNotContains(resp, "Go deeper")


class SearchAndSeoTests(TestCase):
    """Task 13 (FTS5) + task 15 (states/SEO) coverage."""

    def test_fts_finds_topic_by_body_text(self):
        resp = self.client.get("/search/?q=fission")
        self.assertContains(resp, "Nuclear Energy")

    def test_fts_prefix_matching(self):
        resp = self.client.get("/search/?q=nucl")
        self.assertContains(resp, "Nuclear Energy")

    def test_fts_index_follows_edits(self):
        topic = Topic.objects.get(slug="nuclear-energy")
        topic.summary = "zephyrwordtest appears here"
        topic.save()
        self.assertContains(self.client.get("/search/?q=zephyrwordtest"), "Nuclear Energy")

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
        Topic.objects.create(title="Hidden", slug="hidden-draft", status=Topic.DRAFT)
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
