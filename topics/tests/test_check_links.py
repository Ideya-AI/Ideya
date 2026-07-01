"""Tests for the check_links management command.

Network-free: the single fetch boundary (`check_links._probe`) is monkeypatched
so no test touches the real internet. Covers classification of every status, the
placeholder short-circuit (which never probes), and the command end to end —
including the --fail-on-dead exit code.
"""

from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.test import TestCase

from topics.management.commands import check_links
from topics.management.commands.check_links import (
    ProbeResult,
    _is_bot_walled,
    check_one,
    classify,
    is_placeholder,
)
from topics.models import Action, Section, Stat, Topic

# Short alias for building probe results in the classification tests.
_OK = ProbeResult(200, "https://example.com", False, None, None)


def _probe_returning(result):
    """Patch the network boundary to return `result` for any URL."""
    return mock.patch.object(check_links, "_probe", return_value=result)


class IsPlaceholderTests(TestCase):
    def test_empty_and_hash_are_placeholders(self):
        for value in ("", "   ", "#", "#section", None):
            self.assertTrue(is_placeholder(value), value)

    def test_real_url_is_not_placeholder(self):
        self.assertFalse(is_placeholder("https://ourworldindata.org/energy"))


class BotWalledTests(TestCase):
    def test_gov_hosts_are_bot_walled(self):
        for url in (
            "https://www.regulations.gov/doc",
            "https://nrc.gov/reactors",
            "https://energy.ca.gov/",
        ):
            self.assertTrue(_is_bot_walled(url), url)

    def test_ordinary_host_is_not_bot_walled(self):
        self.assertFalse(_is_bot_walled("https://ourworldindata.org/energy"))


class CheckOneTests(TestCase):
    """check_one() drives classification; _probe is mocked so it never hits the net."""

    def test_hash_url_is_placeholder_without_probing(self):
        # No patch: if check_one tried to probe "#", it would hit the network.
        with mock.patch.object(check_links, "_probe", side_effect=AssertionError):
            self.assertEqual(check_one("#", timeout=1).status, "placeholder")
            self.assertEqual(check_one("", timeout=1).status, "placeholder")

    def test_2xx_is_ok(self):
        with _probe_returning(ProbeResult(200, "https://x", False, None, None)):
            self.assertEqual(check_one("https://x", timeout=1).status, "ok")

    def test_404_is_dead(self):
        with _probe_returning(ProbeResult(404, "https://x", False, "HTTP 404", "http")):
            self.assertEqual(check_one("https://x", timeout=1).status, "dead")

    def test_redirect_reports_final_url(self):
        with _probe_returning(ProbeResult(200, "https://final", True, None, None)):
            result = check_one("https://x", timeout=1)
        self.assertEqual(result.status, "redirect")
        self.assertEqual(result.final_url, "https://final")

    def test_403_is_blocked(self):
        with _probe_returning(ProbeResult(403, "https://x", False, "HTTP 403", "http")):
            self.assertEqual(check_one("https://x", timeout=1).status, "blocked")

    def test_500_is_dead(self):
        with _probe_returning(ProbeResult(500, "https://x", False, "HTTP 500", "http")):
            self.assertEqual(check_one("https://x", timeout=1).status, "dead")

    def test_network_failure_on_gov_host_is_blocked_not_dead(self):
        probe = ProbeResult(
            None, "https://nrc.gov", False, "connection error", "connection"
        )
        with _probe_returning(probe):
            self.assertEqual(
                check_one("https://www.nrc.gov/x", timeout=1).status, "blocked"
            )

    def test_connection_failure_on_ordinary_host_is_dead(self):
        probe = ProbeResult(None, "https://x", False, "connection error", "connection")
        with _probe_returning(probe):
            self.assertEqual(
                check_one("https://example.com/x", timeout=1).status, "dead"
            )

    def test_timeout_is_dead(self):
        with _probe_returning(
            ProbeResult(None, "https://x", False, "timeout", "timeout")
        ):
            self.assertEqual(check_one("https://x", timeout=1).status, "dead")

    def test_cache_avoids_second_probe(self):
        cache: dict = {}
        with mock.patch.object(check_links, "_probe", return_value=_OK) as probe:
            check_one("https://same", timeout=1, cache=cache)
            check_one("https://same", timeout=1, cache=cache)
        self.assertEqual(probe.call_count, 1)


class ClassifyTests(TestCase):
    def test_429_is_blocked(self):
        self.assertEqual(
            classify(
                ProbeResult(429, "u", False, "HTTP 429", "http"), bot_walled=False
            ),
            "blocked",
        )

    def test_dns_failure_is_dead(self):
        self.assertEqual(
            classify(
                ProbeResult(None, "u", False, "DNS failure", "dns"), bot_walled=False
            ),
            "dead",
        )


class CheckLinksCommandTests(TestCase):
    """End-to-end command run with a mocked fetcher over real fixtures.

    Uses a dedicated slug (not 'nuclear-energy', which the seed migration owns)
    so these fixtures stay isolated from seeded content.
    """

    def setUp(self):
        self.topic = Topic.objects.create(
            title="Link Fixture", slug="link-fixture", status=Topic.PUBLISHED
        )
        self.section = Section.objects.create(topic=self.topic, kind=Section.ACTIONS)
        Action.objects.create(
            section=self.section,
            title="Good link",
            url="https://good.example",
            kind=Action.LEARN_MORE,
        )
        Action.objects.create(
            section=self.section,
            title="Broken link",
            url="https://dead.example",
            kind=Action.LEARN_MORE,
        )
        Action.objects.create(
            section=self.section,
            title="Unwritten",
            url="#",
            kind=Action.LEARN_MORE,
        )
        # A Stat with a source URL is checked; one without is skipped entirely.
        basics = Section.objects.create(topic=self.topic, kind=Section.BASICS)
        Stat.objects.create(
            section=basics,
            label="Sourced figure",
            value="42",
            source_url="https://good.example/data",
        )
        Stat.objects.create(section=basics, label="Unsourced figure", value="7")

    @staticmethod
    def _fake_probe(url, timeout):
        if "dead" in url:
            return ProbeResult(404, url, False, "HTTP 404", "http")
        return ProbeResult(200, url, False, None, None)

    def test_report_groups_and_summarizes(self):
        out = StringIO()
        with mock.patch.object(check_links, "_probe", side_effect=self._fake_probe):
            call_command("check_links", topic="link-fixture", timeout=1, stdout=out)
        text = out.getvalue()
        self.assertIn("Link Fixture", text)
        self.assertIn("PLACEHOLDER", text)
        self.assertIn("DEAD", text)
        self.assertIn("OK", text)
        self.assertIn("Summary:", text)
        # Sourced stat checked; unsourced stat skipped → 3 actions + 1 stat = 4.
        self.assertIn("4 links", text)

    def test_unknown_topic_reports_and_skips(self):
        out, err = StringIO(), StringIO()
        call_command("check_links", topic="no-such-topic", stdout=out, stderr=err)
        self.assertIn("No topic with slug", err.getvalue())

    def test_fail_on_dead_exits_nonzero(self):
        out, err = StringIO(), StringIO()
        with mock.patch.object(check_links, "_probe", side_effect=self._fake_probe):
            with self.assertRaises(SystemExit) as ctx:
                call_command(
                    "check_links",
                    topic="link-fixture",
                    fail_on_dead=True,
                    timeout=1,
                    stdout=out,
                    stderr=err,
                )
        self.assertEqual(ctx.exception.code, 1)

    def test_no_fail_when_no_dead(self):
        out = StringIO()
        # Every URL resolves 200 → no dead links → no SystemExit.
        with mock.patch.object(check_links, "_probe", return_value=_OK):
            call_command(
                "check_links",
                topic="link-fixture",
                fail_on_dead=True,
                timeout=1,
                stdout=out,
            )
        self.assertIn("0 dead", out.getvalue())
