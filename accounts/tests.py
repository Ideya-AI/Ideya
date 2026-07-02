from django.test import TestCase
from django.urls import reverse

from topics.models import Position, Question, Stance, Vote

from .models import User


class AccountFlowTests(TestCase):
    """Email-keyed accounts + the hybrid merge (decision B). Uses the Nuclear
    Energy fixture from the seed migration."""

    def setUp(self):
        self.question = Question.objects.order_by("id").first()
        self.position = Position.objects.order_by("id").first()

    def _vote_url(self, target, obj):
        return reverse("topics:vote", args=[target, obj.id])

    def test_signup_logs_in_and_merges_session(self):
        # Participate anonymously first.
        self.client.post(self._vote_url("question", self.question))
        self.client.post(
            reverse("topics:stance", args=[self.position.id]), {"value": "agree"}
        )

        resp = self.client.post(
            reverse("accounts:signup"),
            {
                "email": "reader@example.com",
                "password1": "atlas-reader-9",
                "password2": "atlas-reader-9",
            },
        )
        self.assertEqual(resp.status_code, 302)
        user = User.objects.get(email="reader@example.com")

        # The anonymous rows now belong to the account.
        self.assertEqual(Vote.objects.filter(user=user).count(), 1)
        self.assertEqual(Stance.objects.get(user=user).value, "agree")
        self.assertFalse(Vote.objects.filter(user__isnull=True).exists())

    def test_login_merge_drops_duplicate_vote_and_fixes_counter(self):
        user = User.objects.create_user("reader@example.com", "atlas-reader-9")
        Vote.objects.create(user=user, question=self.question)
        self.question.votes += 1
        self.question.save(update_fields=["votes"])
        counted = self.question.votes

        # Anonymous session votes on the same question…
        self.client.post(self._vote_url("question", self.question))
        self.question.refresh_from_db()
        self.assertEqual(self.question.votes, counted + 1)

        # …then logs in: the duplicate collapses and the count is undone.
        self.client.post(
            reverse("accounts:login"),
            {"username": "reader@example.com", "password": "atlas-reader-9"},
        )
        self.question.refresh_from_db()
        self.assertEqual(self.question.votes, counted)
        self.assertEqual(Vote.objects.filter(question=self.question).count(), 1)
        self.assertEqual(Vote.objects.get(question=self.question).user, user)

    def test_login_merge_session_stance_wins(self):
        user = User.objects.create_user("reader@example.com", "atlas-reader-9")
        Stance.objects.create(user=user, position=self.position, value="agree")

        self.client.post(
            reverse("topics:stance", args=[self.position.id]), {"value": "disagree"}
        )
        self.client.post(
            reverse("accounts:login"),
            {"username": "reader@example.com", "password": "atlas-reader-9"},
        )
        self.assertEqual(
            Stance.objects.get(position=self.position, user=user).value, "disagree"
        )
        self.assertEqual(Stance.objects.filter(position=self.position).count(), 1)

    def test_authenticated_vote_is_user_keyed_and_retractable(self):
        user = User.objects.create_user("reader@example.com", "atlas-reader-9")
        self.client.force_login(user)
        start = self.question.votes

        self.client.post(self._vote_url("question", self.question))
        self.assertEqual(Vote.objects.get(question=self.question).user, user)
        self.client.post(self._vote_url("question", self.question))
        self.question.refresh_from_db()
        self.assertEqual(self.question.votes, start)
        self.assertFalse(Vote.objects.filter(question=self.question).exists())

    def test_settings_requires_login(self):
        resp = self.client.get(reverse("accounts:settings"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("accounts:login"), resp.url)

    def test_delete_account_undoes_vote_counters(self):
        user = User.objects.create_user("reader@example.com", "atlas-reader-9")
        self.client.force_login(user)
        self.client.post(self._vote_url("position", self.position))
        self.position.refresh_from_db()
        counted = self.position.importance

        resp = self.client.post(reverse("accounts:delete"))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(User.objects.filter(email="reader@example.com").exists())
        self.position.refresh_from_db()
        self.assertEqual(self.position.importance, counted - 1)
