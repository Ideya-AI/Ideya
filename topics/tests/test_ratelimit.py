"""Per-IP participation rate limiting (anti-vote-spam for the accountless flow)."""

from django.core.cache import cache
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from ..models import Question
from ..ratelimit import client_ip, rate_limited


class RateLimitHelperTests(TestCase):
    def setUp(self):
        cache.clear()  # LocMem cache is process-shared across tests
        self.rf = RequestFactory()

    def _req(self, ip="1.2.3.4"):
        return self.rf.post("/x", REMOTE_ADDR=ip)

    def test_allows_up_to_limit_then_blocks(self):
        req = self._req()
        # limit=3: first three pass, the fourth is blocked.
        self.assertFalse(rate_limited(req, "t", 3, 60))
        self.assertFalse(rate_limited(req, "t", 3, 60))
        self.assertFalse(rate_limited(req, "t", 3, 60))
        self.assertTrue(rate_limited(req, "t", 3, 60))

    def test_isolated_per_ip(self):
        a, b = self._req("10.0.0.1"), self._req("10.0.0.2")
        self.assertFalse(rate_limited(a, "t", 1, 60))  # a's one allowed
        self.assertTrue(rate_limited(a, "t", 1, 60))  # a now blocked
        self.assertFalse(rate_limited(b, "t", 1, 60))  # b is independent

    def test_isolated_per_scope(self):
        req = self._req()
        self.assertFalse(rate_limited(req, "votes", 1, 60))
        self.assertTrue(rate_limited(req, "votes", 1, 60))  # votes scope spent
        self.assertFalse(rate_limited(req, "text", 1, 60))  # text scope fresh

    def test_client_ip_prefers_forwarded_for(self):
        req = self.rf.post(
            "/x", REMOTE_ADDR="127.0.0.1", HTTP_X_FORWARDED_FOR="9.9.9.9, 127.0.0.1"
        )
        self.assertEqual(client_ip(req), "9.9.9.9")


@override_settings(PARTICIPATION_RATELIMIT=True)
class VoteRateLimitTests(TestCase):
    """The vote endpoint returns 429 once an IP blows past the participation cap,
    without ever recording the over-limit votes."""

    def setUp(self):
        cache.clear()
        self.q = Question.objects.order_by("id").first()
        self.url = reverse("topics:vote", args=["question", self.q.id])

    def test_over_cap_ip_gets_429(self):
        from ..ratelimit import PARTICIPATE_LIMIT

        # Fresh session per request (no cookie carried) simulates cookie-clearing
        # spam — the per-IP cap is what stops it.
        ok = 0
        for _ in range(PARTICIPATE_LIMIT + 5):
            resp = self.client.post(self.url, {"dir": "up"}, REMOTE_ADDR="203.0.113.7")
            if resp.status_code == 200:
                ok += 1
        self.assertEqual(ok, PARTICIPATE_LIMIT)  # exactly the cap got through
        self.assertEqual(
            self.client.post(
                self.url, {"dir": "up"}, REMOTE_ADDR="203.0.113.7"
            ).status_code,
            429,
        )
        # A different IP is unaffected.
        self.assertEqual(
            self.client.post(
                self.url, {"dir": "up"}, REMOTE_ADDR="203.0.113.8"
            ).status_code,
            200,
        )
