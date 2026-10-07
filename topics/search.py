"""SQLite FTS5 search index.

One virtual table holds every searchable thing as (kind, obj_id, title, body).
Created and seeded by migration 0007, kept in sync by signals, rebuildable via
`manage.py rebuild_search`. Every helper degrades gracefully when the table is
missing (non-SQLite backends, FTS5-less builds) — callers fall back to
icontains.
"""

import re

from django.db import connection

TABLE = "search_fts"


def available() -> bool:
    if connection.vendor != "sqlite":
        return False
    with connection.cursor() as c:
        c.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = %s",
            [TABLE],
        )
        return c.fetchone() is not None


def _match_expr(q: str) -> str:
    """Sanitized prefix-match expression: each word becomes a quoted prefix
    token, so FTS5 syntax characters in user input can't break the query."""
    tokens = re.findall(r"\w+", q)[:8]
    return " ".join(f'"{t}"*' for t in tokens)


def search_ids(q: str, kind: str, limit: int) -> list:
    expr = _match_expr(q)
    if not expr:
        return []
    with connection.cursor() as c:
        c.execute(
            f"SELECT obj_id FROM {TABLE} WHERE {TABLE} MATCH %s AND kind = %s "
            "ORDER BY rank LIMIT %s",
            [expr, kind, limit],
        )
        return [row[0] for row in c.fetchall()]


def upsert(kind: str, obj_id: int, title: str, body: str = ""):
    if not available():
        return
    with connection.cursor() as c:
        c.execute(
            f"DELETE FROM {TABLE} WHERE kind = %s AND obj_id = %s", [kind, obj_id]
        )
        c.execute(
            f"INSERT INTO {TABLE} (kind, obj_id, title, body) VALUES (%s, %s, %s, %s)",
            [kind, obj_id, title, body],
        )


def remove(kind: str, obj_id: int):
    if not available():
        return
    with connection.cursor() as c:
        c.execute(
            f"DELETE FROM {TABLE} WHERE kind = %s AND obj_id = %s", [kind, obj_id]
        )


def topic_body(topic) -> str:
    return " ".join(filter(None, [topic.summary, topic.scope_covered, topic.why_now]))


def rebuild():
    from .models import Category, Topic

    if not available():
        return
    with connection.cursor() as c:
        c.execute(f"DELETE FROM {TABLE}")
    for t in Topic.objects.all():
        upsert("topic", t.id, t.title, topic_body(t))
    for cat in Category.objects.all():
        upsert("category", cat.id, cat.name, cat.description)
