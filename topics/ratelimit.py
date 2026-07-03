"""Lightweight per-IP rate limiting for the anonymous participation endpoints.

Participation is intentionally accountless, so a session key is the only identity
and it's cheap to reset (clear cookies, incognito, or script requests with no
cookie). That can't be made spam-*proof* without accounts, but a per-IP write
cap makes it spam-*resistant*: it crushes scripted mass-voting (thousands of
requests) while a real reader clicking around never approaches the ceiling.

Backed by the Django cache (default local-memory). Note: local-memory is
per-process, so under multiple gunicorn workers the effective limit is
multiplied by the worker count — fine for a small self-hosted deploy; point
CACHES at Redis or the database cache for a shared counter.
"""

from django.core.cache import cache

# Per-IP ceiling on participation writes (votes, stances, leans, prompt answers).
# Generous for an enthusiastic human; murderous for a script.
PARTICIPATE_LIMIT = 60
PARTICIPATE_WINDOW = 60  # seconds


def client_ip(request) -> str:
    """Best-effort client IP. Behind a reverse proxy the real client is the first
    X-Forwarded-For hop; otherwise the socket peer. (XFF is client-spoofable when
    not behind a trusted proxy — acceptable for a soft-signal rate cap.)"""
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "") or "unknown"


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
