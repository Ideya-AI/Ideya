"""A readable digest of what readers did — the informative view of the
participation record (`ParticipationEvent`), for the editor.

  manage.py participation_report                      # every topic, all time, to stdout
  manage.py participation_report --topic nuclear-energy
  manage.py participation_report --since 2026-09-01 --out research/participation/2026-09-02.md

The digest is built from the append-only event log, not the current-state
tables, so it reads the same before and after a republish and covers readers
whose current-state row was later retired. "Current" answers are each
participant's LAST action per item + prompt: a retract or clear drops it, a
switch or re-save replaces it. Items are keyed by their text: the log is
denormalized at write time, so it records what the reader actually saw.

Runbook: research/PARTICIPATION.md.
"""

from collections import Counter, OrderedDict, defaultdict
from datetime import datetime, time

from django.core.management.base import BaseCommand
from django.utils import timezone

from topics.models import ParticipationEvent

KIND_ORDER = ["question", "position", "stat", "section", "topic"]
KIND_TITLE = {
    "question": "Questions",
    "position": "Positions",
    "stat": "Facts",
    "section": "Sections — Something missing?",
    "topic": "Topic — Add your view",
}
TRIGGER_TITLE = {
    "vote": "after upvote",
    "lean_a": "after lean",
    "lean_b": "after lean",
    "respond": "respond",
    "missing": "something missing",
    "": "add your view",
}


def _who(e):
    return ("u", e.user_id) if e.user_id else ("s", e.session_key)


def _latest(events, key):
    """Last event per (participant, key(event)); insertion order = first seen."""
    last = OrderedDict()
    for e in events:  # events are in id order
        last[(_who(e), key(e))] = e
    return last


def build_digest(events, since=None, header_date=None):
    """Return the Markdown digest for an id-ordered list of events."""
    lines = []
    day = (header_date or timezone.localdate()).isoformat()
    lines.append(f"# Participation digest — {day}")
    if since:
        lines.append(f"Window: since {since.isoformat()}")
    if not events:
        lines.append("\nNo participation recorded.")
        return "\n".join(lines) + "\n"

    by_kind = Counter(e.kind for e in events)
    by_action = Counter(f"{e.kind}:{e.action}" for e in events)
    participants = {_who(e) for e in events}
    first, last = events[0].created_at, events[-1].created_at
    lines.append(
        f"\n{len(events)} events · {len(participants)} participants · "
        f"{timezone.localtime(first):%Y-%m-%d} → {timezone.localtime(last):%Y-%m-%d}  "
        + " · ".join(f"{k} {n}" for k, n in sorted(by_kind.items()))
    )
    lines.append(
        "Actions: " + " · ".join(f"{k} {n}" for k, n in sorted(by_action.items()))
    )

    # ---- current state, per item -------------------------------------------
    item_key = lambda e: (e.target_kind, e.target_text)
    votes = _latest([e for e in events if e.kind == ParticipationEvent.VOTE], item_key)
    leans = _latest([e for e in events if e.kind == ParticipationEvent.LEAN], item_key)
    responses = _latest(
        [e for e in events if e.kind == ParticipationEvent.RESPONSE],
        lambda e: (e.target_kind, e.target_text, e.trigger, e.prompt_text),
    )

    # topic → kind → item text → {votes, leans, prompts: {(trigger, prompt): [events]}}
    tree = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {
        "votes": 0, "leans": Counter(), "prompts": defaultdict(list),
    })))
    for (_, (kind, text)), e in votes.items():
        if e.action == "cast":
            tree[e.topic_slug][kind][text]["votes"] += 1
    for (_, (kind, text)), e in leans.items():
        if e.action != "retract":
            tree[e.topic_slug][kind][text]["leans"][e.payload.get("label", "?")] += 1
    for (_, (kind, text, trig, ptext)), e in responses.items():
        if e.action == "save":
            tree[e.topic_slug][kind][text]["prompts"][(trig, ptext)].append(e)

    for slug in sorted(tree):
        lines.append(f"\n## {slug}")
        for kind in KIND_ORDER:
            items = tree[slug].get(kind)
            if not items:
                continue
            lines.append(f"\n### {KIND_TITLE.get(kind, kind)}")
            for text, item in items.items():
                head = [f"**{text}**"]
                if item["votes"]:
                    head.append(f"upvotes {item['votes']}")
                if item["leans"]:
                    head.append(
                        "lean: " + " / ".join(f"{l} {n}" for l, n in item["leans"].most_common())
                    )
                lines.append("- " + " — ".join(head))
                for (trig, ptext), evs in item["prompts"].items():
                    lines.extend(_prompt_lines(trig, ptext, evs))
    return "\n".join(lines) + "\n"


def _prompt_lines(trigger, prompt_text, evs):
    out = []
    picks, notes, texts, ratings, rank_points = Counter(), [], [], [], Counter()
    for e in evs:
        p = e.payload or {}
        for label in p.get("selected", []):
            picks[label] += 1
        for label, note in (p.get("notes") or {}).items():
            notes.append((label, note, e))
        if p.get("text"):
            texts.append((p["text"], e))
        if p.get("rating") is not None:
            ratings.append(p["rating"])
        order = p.get("ranking") or []
        for i, label in enumerate(order):
            rank_points[label] += len(order) - i
    label = f"{TRIGGER_TITLE.get(trigger, trigger)} · {prompt_text}"
    summary = []
    if picks:
        summary.append(", ".join(f"{l} {n}" for l, n in picks.most_common()))
    if ratings:
        summary.append(f"avg {sum(ratings) / len(ratings):.1f}/5 (n={len(ratings)})")
    if rank_points:
        summary.append("rank: " + " > ".join(l for l, _ in rank_points.most_common()))
    out.append(f"  - {label}: {' · '.join(summary) if summary else f'{len(evs)} answer(s)'}")
    for lab, note, e in notes:
        out.append(f"    - [{lab}] {_quote(note)} {_stamp(e)}")
    for text, e in texts:
        out.append(f"    - {_quote(text)} {_stamp(e)}")
    return out


def _quote(text):
    return "“" + " ".join(text.split()) + "”"


def _stamp(e):
    who = f"user {e.user_id}" if e.user_id else f"session {e.session_key[:6]}"
    return f"({who}, {timezone.localtime(e.created_at):%Y-%m-%d})"


class Command(BaseCommand):
    help = "Markdown digest of reader participation, built from the event log."

    def add_arguments(self, parser):
        parser.add_argument("--topic", help="Topic slug (default: every topic).")
        parser.add_argument("--since", help="YYYY-MM-DD — only events on/after this day.")
        parser.add_argument("--out", help="Write here instead of stdout.")

    def handle(self, *args, **opts):
        qs = ParticipationEvent.objects.order_by("id")
        since = None
        if opts["topic"]:
            qs = qs.filter(topic_slug=opts["topic"])
        if opts["since"]:
            since = datetime.strptime(opts["since"], "%Y-%m-%d").date()
            qs = qs.filter(
                created_at__gte=timezone.make_aware(datetime.combine(since, time.min))
            )
        digest = build_digest(list(qs), since=since)
        if opts["out"]:
            with open(opts["out"], "w") as fh:
                fh.write(digest)
            self.stdout.write(self.style.SUCCESS(f"wrote {opts['out']}"))
        else:
            self.stdout.write(digest)
