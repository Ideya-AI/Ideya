"""Pre-publish link checker: find dead, placeholder, or broken external links.

Scans every user-facing URL in the topic content tree — the primary target is
`Action.url`, plus the supporting `Stat.source_url` — and classifies each:

    placeholder  empty or "#" (a link that still needs to be authored)
    ok           reachable, final HTTP status 2xx
    redirect     reachable after one or more 3xx hops (final URL is reported so
                 an editor can update the stored link)
    blocked      401/403/429, or a network failure to a known bot-walled host
                 (e.g. *.gov). Live, but unverifiable by a script — needs a
                 manual check. NOT counted as dead.
    dead         other 4xx/5xx, DNS failure, or timeout

Networking is stdlib-only (urllib), with a browser-like User-Agent, redirect
following, and a HEAD-then-GET fallback. All fetching funnels through the single
module-level `_probe()` so tests can monkeypatch it and stay network-free.

Examples:
    manage.py check_links
    manage.py check_links --topic nuclear-energy
    manage.py check_links --fail-on-dead          # exit 1 if any dead link (CI)
    manage.py check_links --timeout 30
"""

import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from dataclasses import dataclass
from itertools import groupby
from typing import Optional

from django.core.management.base import BaseCommand

from topics.models import Action, Stat, Topic

# A browser-like identity — many hosts 403 or hang on the default urllib UA.
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Hosts known to wall off scripted clients while being perfectly live for
# browsers. A network-level failure (or 403) to one of these is "needs manual
# check", not "dead". The .gov suffix already covers these two; they are listed
# for documentation and as a home for any future non-.gov additions.
_BOT_WALLED_HOSTS = {
    "regulations.gov",
    "nrc.gov",
    "mckinsey.com",
    # Refuses scripted clients at the network level (connect times out even
    # from a browser UA); the series pages are live. Matching here is by exact
    # hostname, not registrable domain, so subdomains are listed individually.
    "fred.stlouisfed.org",
}

# HEAD outcomes that mean "the server didn't really answer" — retry with GET.
# (A clean 2xx, a 410, a 429, or a timeout are trusted as-is: retrying would
# be wasteful or would worsen rate limiting.)
# 404 IS retried: some hosts answer HEAD with 404 on a page that GETs 200 —
# ourworldindata.org grapher pages do exactly this, and trusting the HEAD sent a
# live, correctly-cited source to the packet as "dead" (economic-inequality,
# 2026-09-02). One wasted GET per genuinely-dead link is far cheaper than a false
# dead verdict, which blocks the stage-4.5 gate and sends a human chasing a
# working link.
_GET_FALLBACK_CODES = {400, 403, 404, 405, 406, 500, 501, 502, 503, 504}

# status -> Django style attribute. placeholder + dead use ERROR so they stand
# out; redirect + blocked use WARNING (attention, not failure).
_STATUS_STYLE = {
    "ok": "SUCCESS",
    "redirect": "WARNING",
    "blocked": "WARNING",
    "placeholder": "ERROR",
    "dead": "ERROR",
}

# Report order for the summary line and grouping.
_STATUS_ORDER = ["ok", "redirect", "blocked", "placeholder", "dead"]

# Left-pad for the URL detail line, aligning it under the title.
_PAD = " " * 14


@dataclass
class ProbeResult:
    """Outcome of a single network probe (the boundary tests monkeypatch)."""

    status_code: Optional[int]  # final HTTP status, or None if no response
    final_url: str  # URL after following redirects
    redirected: bool  # whether any 3xx hop occurred
    error: Optional[str]  # human-readable failure reason, else None
    error_kind: Optional[str]  # "http" | "timeout" | "dns" | "connection" | None


@dataclass
class LinkCheck:
    """Classified result for one stored URL."""

    status: str
    url: str  # the URL as stored (stripped)
    final_url: str  # final URL after redirects (== url when not redirected)
    note: str  # short reason, e.g. "HTTP 404", "timeout", "redirected"


@dataclass
class LinkItem:
    """One URL-bearing content row to check."""

    topic_label: str  # group header, e.g. "Nuclear Energy"
    topic_slug: Optional[str]
    field: str  # "Action" or "Source"
    title: str
    url: str


def is_placeholder(url: str) -> bool:
    """An unauthored link: empty, whitespace-only, or a bare "#"/fragment."""
    s = (url or "").strip()
    return s == "" or s.startswith("#")


def _is_bot_walled(url: str) -> bool:
    """True for hosts that block scripts but serve browsers (treat as manual)."""
    host = (urllib.parse.urlsplit(url).hostname or "").lower()
    if host.endswith(".gov"):
        return True
    base = host[4:] if host.startswith("www.") else host
    return base in _BOT_WALLED_HOSTS


class _CountingRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Records each 3xx hop so we can tell a redirect from a direct hit."""

    def __init__(self) -> None:
        super().__init__()
        self.redirect_codes: list[int] = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.redirect_codes.append(code)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _request(url: str, method: str, timeout: float) -> ProbeResult:
    """Issue one HTTP request, following redirects, and map it to a ProbeResult.

    Never raises: every failure becomes a ProbeResult with an error_kind so a
    single bad URL can't crash the run.
    """
    redirects = _CountingRedirectHandler()
    opener = urllib.request.build_opener(redirects)
    req = urllib.request.Request(url, method=method, headers=_HEADERS)
    try:
        with opener.open(req, timeout=timeout) as resp:
            code = getattr(resp, "status", None) or resp.getcode()
            return ProbeResult(
                status_code=code,
                final_url=resp.geturl(),
                redirected=bool(redirects.redirect_codes),
                error=None,
                error_kind=None,
            )
    except urllib.error.HTTPError as exc:
        # Non-2xx final response (redirects, if any, were already followed).
        return ProbeResult(
            status_code=exc.code,
            final_url=getattr(exc, "url", None) or url,
            redirected=bool(redirects.redirect_codes),
            error=f"HTTP {exc.code}",
            error_kind="http",
        )
    except urllib.error.URLError as exc:
        reason = exc.reason
        if isinstance(reason, socket.gaierror):
            return ProbeResult(None, url, False, "DNS failure", "dns")
        if isinstance(reason, (socket.timeout, TimeoutError)):
            return ProbeResult(None, url, False, "timeout", "timeout")
        return ProbeResult(
            None, url, False, str(reason) or "connection error", "connection"
        )
    except (socket.timeout, TimeoutError):
        return ProbeResult(None, url, False, "timeout", "timeout")
    except Exception as exc:  # last-resort guard: never let one URL abort the run
        return ProbeResult(None, url, False, str(exc) or "error", "connection")


def _probe(url: str, timeout: float) -> ProbeResult:
    """Fetch a URL: HEAD first, falling back to GET when HEAD looks rejected.

    This is the single network boundary — tests monkeypatch it.
    """
    res = _request(url, "HEAD", timeout)
    head_rejected = res.error_kind == "connection" or (
        res.status_code is not None and res.status_code in _GET_FALLBACK_CODES
    )
    if head_rejected:
        res = _request(url, "GET", timeout)
    return res


def classify(probe: ProbeResult, bot_walled: bool) -> str:
    """Map a ProbeResult to a status (placeholder is decided before probing)."""
    code = probe.status_code
    if probe.error_kind is None and code is not None and 200 <= code < 300:
        return "redirect" if probe.redirected else "ok"
    if code in (401, 403, 429):
        return "blocked"
    if probe.error_kind in ("timeout", "connection") and bot_walled:
        return "blocked"
    # Everything else: other 4xx/5xx, DNS failure, timeout, plain connection.
    return "dead"


def _note_for(status: str, probe: ProbeResult) -> str:
    if status == "ok":
        return ""
    if status == "redirect":
        return "redirected"
    if probe.status_code is not None:
        return f"HTTP {probe.status_code}"
    return probe.error or "error"


def check_one(url: str, timeout: float, cache: Optional[dict] = None) -> LinkCheck:
    """Classify a single stored URL. `cache` (keyed by URL) avoids re-probing
    the same link twice within a run."""
    raw = (url or "").strip()
    if is_placeholder(raw):
        return LinkCheck("placeholder", raw, raw, "empty" if raw == "" else "fragment")
    if cache is not None and raw in cache:
        return cache[raw]
    probe = _probe(raw, timeout)
    status = classify(probe, _is_bot_walled(raw))
    result = LinkCheck(status, raw, probe.final_url or raw, _note_for(status, probe))
    if cache is not None:
        cache[raw] = result
    return result


def _topic_of(section) -> tuple[str, Optional[str]]:
    if section.topic_id:
        return section.topic.title, section.topic.slug
    if section.category_id:
        return f"{section.category.name} (category)", None
    return "(orphan)", None


def collect_links(topic_slug: Optional[str]) -> list[LinkItem]:
    """Gather every URL-bearing row. External actions are always listed (an
    empty/# url is a placeholder to author) — the internal submit-view CTA is
    skipped; Stats only when a source URL is set — a stat with no source is a
    content choice, not a broken link.

    Module-level so other commands can reuse the collection without reaching
    into the Command class."""
    items: list[LinkItem] = []

    # submit_view is the internal "Add your view" CTA — no external URL by
    # design, so it is not a link to check.
    actions = Action.objects.exclude(kind=Action.SUBMIT_VIEW).select_related(
        "section__topic", "section__category"
    )
    stats = Stat.objects.select_related("section__topic", "section__category")
    if topic_slug:
        actions = actions.filter(section__topic__slug=topic_slug)
        stats = stats.filter(section__topic__slug=topic_slug)

    for a in actions:
        label, slug = _topic_of(a.section)
        items.append(
            LinkItem(
                label, slug, "Action", a.title or f"Action #{a.pk}", a.url or ""
            )
        )
    for s in stats:
        label, slug = _topic_of(s.section)
        if (s.source_url or "").strip():
            items.append(
                LinkItem(
                    label, slug, "Source", s.label or f"Stat #{s.pk}", s.source_url
                )
            )
        # Ranked rows may carry their own source when it differs from the
        # stat-level one (added 2026-08-02) — the pre-publish gate must
        # cover those too.
        for row in s.series or []:
            url = (row.get("source_url") or "").strip() if isinstance(row, dict) else ""
            if url:
                items.append(
                    LinkItem(
                        label,
                        slug,
                        "Source",
                        f"{s.label or f'Stat #{s.pk}'} · row {row.get('label', '?')}",
                        url,
                    )
                )
    topics = Topic.objects.exclude(why_now_source_url="")
    if topic_slug:
        topics = topics.filter(slug=topic_slug)
    for t in topics:
        items.append(LinkItem(t.title, t.slug, "Source", "Why it matters now", t.why_now_source_url))
    return items


class Command(BaseCommand):
    help = (
        "Check external links (Action.url, Stat.source_url) for dead/placeholder URLs."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--topic",
            dest="topic",
            help="Limit the scan to a single topic, by slug.",
        )
        parser.add_argument(
            "--fail-on-dead",
            action="store_true",
            dest="fail_on_dead",
            help="Exit with status 1 if any link is classified 'dead' (for CI).",
        )
        parser.add_argument(
            "--timeout",
            type=float,
            default=15.0,
            help="Per-URL network timeout in seconds (default: 15).",
        )

    def handle(self, *args, **options):
        topic_slug = options.get("topic")
        timeout = options["timeout"]
        fail_on_dead = options["fail_on_dead"]

        if topic_slug and not Topic.objects.filter(slug=topic_slug).exists():
            self.stderr.write(self.style.ERROR(f"No topic with slug '{topic_slug}'."))
            return

        items = self._collect(topic_slug)
        if not items:
            scope = f" for topic '{topic_slug}'" if topic_slug else ""
            self.stdout.write(f"No external links found{scope}.")
            return

        self.stdout.write(f"Checking {len(items)} link(s) (timeout {timeout:g}s) ...\n")

        cache: dict = {}
        counts: Counter = Counter()
        # Stable order: by topic, then field, then title — so grouping is clean.
        items.sort(key=lambda i: (i.topic_label.lower(), i.field, i.title.lower()))
        for label, group in groupby(items, key=lambda i: i.topic_label):
            group = list(group)
            slug = group[0].topic_slug
            heading = f"{label}" + (f"  ({slug})" if slug else "")
            self.stdout.write(self.style.MIGRATE_HEADING(heading))
            for item in group:
                check = check_one(item.url, timeout, cache)
                counts[check.status] += 1
                self._render_line(item, check)
            self.stdout.write("")

        self._render_summary(counts)

        if fail_on_dead and counts.get("dead"):
            self.stderr.write(
                self.style.ERROR(f"FAIL: {counts['dead']} dead link(s) found.")
            )
            sys.exit(1)

    # -- collection ----------------------------------------------------------

    def _collect(self, topic_slug: Optional[str]) -> list[LinkItem]:
        return collect_links(topic_slug)

    @staticmethod
    def _topic_of(section) -> tuple[str, Optional[str]]:
        return _topic_of(section)

    # -- rendering -----------------------------------------------------------

    def _render_line(self, item: LinkItem, check: LinkCheck):
        style = getattr(self.style, _STATUS_STYLE[check.status])
        tag = style(f"{check.status.upper():<11}")
        suffix = f"  [{check.note}]" if check.status in ("dead", "blocked") else ""
        self.stdout.write(f"  {tag} {item.field} · {item.title}{suffix}")

        if check.status == "placeholder":
            shown = "(empty)" if check.url == "" else check.url
            self.stdout.write(f"{_PAD}{shown}")
        elif check.status == "redirect":
            self.stdout.write(f"{_PAD}{check.url}")
            self.stdout.write(f"{_PAD}→ {check.final_url}")
        else:
            self.stdout.write(f"{_PAD}{check.url}")

    def _render_summary(self, counts: Counter):
        total = sum(counts.values())
        parts = [f"{total} links"]
        for status in _STATUS_ORDER:
            n = counts.get(status, 0)
            label = f"{n} {status}"
            if n and status in ("placeholder", "dead"):
                label = self.style.ERROR(label)
            parts.append(label)
        self.stdout.write("Summary: " + "  ·  ".join(parts))
