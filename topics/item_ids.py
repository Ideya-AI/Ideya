"""Stable per-item identity for a topic draft.

Reader votes, leans and prompts attach to a question or a position. Before this
existed the loader rebuilt every section from scratch on each load and re-attached
participation by matching exact question text and position name, so an editorial
rewording silently dropped that item's votes.

An id is assigned ONCE, from the item's text at the time, and then frozen: it is
the item's identity, not a slug of its current wording. Rewording never changes
it. Reordering never changes it. Only removing the item retires it.

Plain Python on purpose, so the pipeline and the loader can never disagree
about identity.
"""

import re

# section key -> (draft list path, field the id is seeded from, prefix)
KINDS = (
    ("stats", lambda d: (d.get("basics") or {}).get("stats") or [], "label", "s"),
    ("questions", lambda d: d.get("questions") or [], "text", "q"),
    ("positions", lambda d: d.get("positions") or [], "name", "p"),
    ("actions", lambda d: d.get("actions") or [], "title", "a"),
)


def slugify(text, prefix, words=6):
    base = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    base = "-".join([w for w in base.split("-") if w][:words])[:70]
    return base or prefix


def ensure_ids(draft):
    """Assign `id` to every item that has none. Returns the number assigned."""
    assigned = 0
    for _, get, field, prefix in KINDS:
        items = get(draft)
        taken = {i["id"] for i in items if i.get("id")}
        for n, item in enumerate(items, 1):
            if item.get("id"):
                continue
            cand = slugify(item.get(field, ""), f"{prefix}{n}")
            uniq, i = cand, 2
            while uniq in taken:
                uniq, i = f"{cand}-{i}", i + 1
            item["id"] = uniq
            taken.add(uniq)
            assigned += 1
    return assigned


