"""Lightweight per-IP rate limiting for the anonymous participation endpoints.

Participation is intentionally accountless, so a session key is the only identity
and it's cheap to reset (clear cookies, incognito, or script requests with no
cookie). That can't be made spam-*proof* without accounts, but a per-IP write
cap makes it spam-*resistant*: it crushes scripted mass-voting (thousands of
requests) while a real reader clicking around never approaches the ceiling.

Backed by the Django cache, a file cache shared by every gunicorn worker. Its
increment is not atomic across processes, so a burst can slip a few requests
past the cap; for a soft limit that is fine.
"""

from django.core.cache import cache

# Per-IP ceiling on participation writes (votes, stances, leans, prompt answers).
# Generous for an enthusiastic human; murderous for a script.
PARTICIPATE_LIMIT = 20
PARTICIPATE_WINDOW = 60  # seconds
# Daily ceiling: a script pacing itself under the per-minute cap all day.
PARTICIPATE_DAY_LIMIT = 300
PARTICIPATE_DAY_WINDOW = 24 * 60 * 60


def client_ip(request) -> str:
    """Client IP. Cloudflare sets CF-Connecting-IP and overwrites any value the
    client sends; the tunnel is the only way in, so it cannot be forged. Not
    X-Forwarded-For: Cloudflare appends to it, leaving the first hop
    client-controlled. Without the header (local dev) it is the socket peer."""
    return (
        request.META.get("HTTP_CF_CONNECTING_IP")
        or request.META.get("REMOTE_ADDR", "")
        or "unknown"
    )


def rate_limited(request, scope: str, limit: int, window: int) -> bool:
    """Fixed-window counter: True once this IP exceeds `limit` hits on `scope`
    within `window` seconds. The window does not slide — the TTL is set once when
    the counter is created, so incrementing never extends it."""
    key = f"rl:{scope}:{client_ip(request)}"
    if cache.get(key, 0) >= limit:
        return True
    # add() sets the counter (with TTL) only if absent; else bump it in place.
    if not cache.add(key, 1, window):
        try:
            cache.incr(key)
        except ValueError:  # expired between the get and the incr — restart it
            cache.set(key, 1, window)
    return False
