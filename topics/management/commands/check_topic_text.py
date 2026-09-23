"""Mechanical rules over a topic FILE, before it is loaded.

    manage.py check_topic_text --slug <slug>
    manage.py check_topic_text --file path/to/topic.json

Two classes of finding. ERRORS exit 1: markup or straight quotes in content,
HTML entities, bad enums, over-cap fields the loader would truncate, structural
faults (lead_highlight not in lead, duplicate color_key, for_position that names
no position, missing source URL on a numbered stat, wide-tile packing that
reorders the fold). WARNINGS are printed for the editor's judgment: UK spellings
(capitalized hits may be proper nouns) and glance-layer length targets.

No network, no database. The plain-text rules exist nowhere else in code.
"""

import json
import re
from pathlib import Path

from django.core.management.base import BaseCommand

from topics.models import POS_COLORS, Action, Stat

POS_KEYS = [k for k, _ in POS_COLORS]
VIZ = {k for k, _ in Stat.VIZ_CHOICES}
ACTION_KINDS = {k for k, _ in Action.KIND_CHOICES} - {Action.SUBMIT_VIEW}

# Hard caps: the loader slices these (some silently). Over = ERROR.
CAPS = {
    "overview.summary": 400, "overview.scope_covered": 400, "overview.scope_excluded": 400,
    "stat.label": 120, "stat.value": 24, "stat.unit": 24, "stat.note": 400,
    "stat.source_label": 120, "stat.source_published": 40, "stat.range_min": 40, "stat.range_max": 40,
    "question.text": 400, "question.lean_label_a": 40, "question.lean_label_b": 40,
    "position.name": 120, "position.steelman": 400, "position.proponents": 400,
    "crux.lead": 240, "crux.lead_highlight": 80,
    "action.title": 200, "action.description": 400,
}
# Glance targets from the exemplar page. Outside = WARNING.
TARGETS = {
    "overview.summary": (80, 160), "overview.why_now": (150, 320),
    "stat.note": (90, 200), "stat.detail": (350, 1300),
    "question.text": (35, 110), "question.why": (140, 260), "question.detail": (500, 1400),
    "position.steelman": (100, 200), "position.detail": (500, 1800),
    "crux.lead": (40, 110), "crux.subtitle": (120, 320), "crux.empirical": (180, 450), "crux.values": (180, 450),
    "action.description": (100, 220),
}
COUNTS = {"stats": (10, 20), "questions": (5, 8), "positions": (3, 6), "actions": (6, 10)}

UK = re.compile(
    r"\b(colou?r(?:s|ed|ful|ing)?|favou?r(?:s|ed|ite|able|ing)?|honou?r(?:s|ed|able)?|labou?r(?:s|ed|ing)?|"
    r"behaviou?r(?:s|al)?|neighbou?r(?:s|hood|ing)?|harbou?r(?:s)?|rumou?r(?:s)?|humou?r|vigou?r|"
    r"centre(?:s|d)?|metres?|litres?|theatres?|fibres?|calibre|"
    r"defence|offence|licence|pretence|programmes?|catalogues?|"
    r"\w+is(?:e|ed|es|ing|ation|ations)|analys(?:e|ed|es|ing)|paralys(?:e|ed)|"
    r"grey(?:s|er|ish)?|aluminium|sceptic(?:s|al|ism)?|ageing|artefacts?|"
    r"travell(?:ed|ing|er|ers)|modell(?:ed|ing)|fuell(?:ed|ing)|labell(?:ed|ing)|signall(?:ed|ing)|totall(?:ed|ing)|"
    r"practis(?:e|ed|ing)|enrol(?:s|ment)?|fulfil(?:s|ment)?|instalments?|cheques?|kerbs?|tyres?|"
    r"moulds?|ploughs?|sulphur|foetus(?:es)?|foetal|oestrogen|paediatric(?:s)?|anaemi[ac]|haemo\w*|manoeuvr\w*|"
    r"whilst|amongst|towards|learnt|spelt|burnt|dreamt)\b"
)
# -ise words that are also correct US spelling; never flag.
UK_OK = {
    "advertise", "advise", "arise", "chastise", "comprise", "compromise", "concise", "demise",
    "despise", "devise", "disguise", "enterprise", "excise", "exercise", "expertise", "franchise",
    "improvise", "incise", "merchandise", "otherwise", "precise", "premise", "promise", "raise",
    "revise", "rise", "supervise", "surmise", "surprise", "televise", "wise", "likewise", "praise",
    "noise", "poise", "cruise", "bruise", "paradise", "practise", "reprise", "apprise", "treatise",
    "clockwise", "counterclockwise", "lengthwise", "sunrise", "moonrise", "anticlockwise",
}


def _uk_hits(text):
    hits = []
    for m in UK.finditer(text):
        w = m.group(0)
        low = w.lower()
        if "u" not in low and low.startswith(("color", "favor", "honor", "labor", "behavior", "neighbor", "harbor", "rumor", "humor", "vigor")):
            continue  # US form matched through the optional u
        stem = re.sub(r"(d|s|ing|ation|ations|es)$", "", low)
        if stem in UK_OK or stem.rstrip("e") + "e" in UK_OK or low in UK_OK:
            continue
        if low.endswith(("ise", "ised", "ises", "ising", "isation", "isations")) and len(low) <= 6:
            continue
        hits.append(w)
    return hits


class Check:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, where, msg):
        self.errors.append(f"{where}: {msg}")

    def warn(self, where, msg):
        self.warnings.append(f"{where}: {msg}")

    def text(self, where, key, value, url=False):
        if key.endswith((".id", ".color_key", ".viz", ".kind", ".wide", ".highlight")):
            return
        if not isinstance(value, str):
            if value is not None and not isinstance(value, (bool, int, float, list, dict)):
                self.err(where, "not a string")
            return
        if url:
            if value and not value.startswith(("http://", "https://")):
                self.err(where, f"not an http(s) URL: {value[:60]}")
            return
        if "'" in value or '"' in value:
            self.err(where, "straight quote; use ’ “ ”")
        if re.search(r"&(amp|lt|gt|quot|#\d+|nbsp);", value):
            self.err(where, "HTML entity; write the character itself")
        if re.search(r"<[a-zA-Z/]", value):
            self.err(where, "HTML tag")
        if re.search(r"(\*\*|`|^#{1,6} |^\s*[-*] |\[[^\]]+\]\([^)]+\))", value, re.M):
            self.err(where, "markdown")
        if "\\n" in value:
            self.err(where, "literal backslash-n")
        cap = CAPS.get(key)
        if cap and len(value) > cap:
            self.err(where, f"{len(value)} chars, loader cap {cap}")
        tgt = TARGETS.get(key)
        if tgt and value and not (tgt[0] <= len(value) <= tgt[1]):
            self.warn(where, f"{len(value)} chars, target {tgt[0]}-{tgt[1]}")
        for w in _uk_hits(value):
            self.warn(where, f"UK spelling? {w!r}" + (" (capitalized: proper noun?)" if w[0].isupper() else ""))

    def pack(self, stats):
        """Mirror Section.basics_tiles: 3 cells a row, wide costs 2. The fold is
        3 rows. If packing pulls a later tile forward inside the fold, array
        order is no longer display order."""
        pending = list(range(len(stats)))
        rows = []
        while pending:
            row, cells, i = [], 0, 0
            while i < len(pending) and cells < 3:
                w = 2 if stats[pending[i]].get("wide") else 1
                if cells + w <= 3:
                    row.append(pending.pop(i))
                    cells += w
                else:
                    i += 1
            rows.append(row)
        shown = [i for row in rows[:3] for i in row]
        if shown != sorted(shown):
            self.err("basics", f"wide-tile packing reorders the fold: display order {shown}; fix wide flags or order")
        return len(shown)


def run(doc, path):
    c = Check()
    d = doc.get("content")
    if not d:
        c.err("topic", "no content")
        return c
    if doc.get("status") not in ("not_started", "in_progress", "ready", "published"):
        c.err("topic", f"bad status {doc.get('status')!r}")
    if path.parent.parent.name == "topics" and doc.get("slug") != path.parent.name:
        c.err("topic", f"slug {doc.get('slug')!r} != directory {path.parent.name!r}")
    ov = d.get("overview") or {}
    if not ov.get("why_now_source_url"):
        c.err("overview.why_now_source_url", "missing: why-now names a dated event, so it names a source a reader can follow")
    else:
        c.text("overview.why_now_source_url", "overview.why_now_source_url", ov["why_now_source_url"], url=True)
    if not ov.get("why_now_source_label"):
        c.err("overview.why_now_source_label", "missing")
    for k in ("summary", "scope_covered", "scope_excluded", "why_now"):
        v = (d.get("overview") or {}).get(k)
        if not v:
            c.err(f"overview.{k}", "missing")
        c.text(f"overview.{k}", f"overview.{k}", v)

    stats = (d.get("basics") or {}).get("stats") or []
    for n, s in enumerate(stats):
        w = f"stat[{n}] {s.get('label', '')[:30]!r}"
        for k in ("label", "note", "detail", "source_label"):
            if not s.get(k):
                c.err(w, f"{k} missing")
        for k, v in s.items():
            c.text(f"{w}.{k}", f"stat.{k}", v, url=(k == "source_url"))
        viz = s.get("viz")
        if viz == "sparkline":
            c.err(w, "the tile template draws no sparkline (it falls back to a bare number); use ranked for a short series or bar for one value")
        if viz not in VIZ:
            c.err(w, f"viz {viz!r} not in {sorted(VIZ)}")
        series = s.get("series") or []
        if viz in ("ranked", "sparkline"):
            if len(series) < 2:
                c.err(w, f"{viz} needs a series of 2+ rows")
            if viz == "ranked" and not s.get("wide"):
                c.err(w, "ranked tiles are wide")
            for r in series:
                if re.search(r"\d\s*(to|–|—)\s*\d", str(r.get("value", ""))):
                    c.err(w, f"series row {r.get('label')!r} holds a range ({r.get('value')!r}); a bar draws one number, so it draws the low end. Use one number per row, or split into low and high rows")
            nums = []
            for r in series:
                m = re.search(r"-?\d+(?:\.\d+)?", str(r.get("value", "")).replace(",", ""))
                if m:
                    nums.append(float(m.group()))
            if len(series) == 2 and len(nums) == 2 and min(nums) > 0 and min(nums) / max(nums) < 0.01:
                c.err(w, "a two-row ranked chart whose small value is under 1 percent of the large one draws the small bar as an empty track beside a full one; use a bar tile with the large value and the small one in the note")
            if any(str(r.get("value", "")).strip().startswith(("-", "−", "–")) for r in series):
                c.err(w, "a series row is negative; bars cannot show sign (a negative renders as no bar). Use magnitudes with the sign in the label, or a bar tile with the value in the headline")
            for r in series:
                c.text(f"{w}.series", "series.label", r.get("label"))
                if len(r.get("label") or "") > 24:
                    c.warn(w, f"series label {r.get('label')!r} is {len(r['label'])} chars; the poster's label column wraps past ~24")
        elif series:
            c.err(w, f"series given but viz is {viz}")
        if viz == "range" and not (s.get("range_min") and s.get("range_max")):
            c.err(w, "range needs range_min and range_max")
        elif viz == "range":
            nums = [float(m.group()) for m in re.finditer(r"-?\d+(?:\.\d+)?", str(s.get("value", "")).replace(",", ""))]
            lo = re.search(r"-?\d+(?:\.\d+)?", str(s.get("range_min")).replace(",", ""))
            hi = re.search(r"-?\d+(?:\.\d+)?", str(s.get("range_max")).replace(",", ""))
            if lo and hi and nums:
                lo, hi = float(lo.group()), float(hi.group())
                if hi <= lo:
                    c.err(w, "range_max must exceed range_min")
                elif min(nums) <= lo and max(nums) >= hi:
                    c.err(w, "range ends equal the value span, so the marker fills the whole track; the ends are the scale the value sits on, not the value")
        if viz != "ranked" and not s.get("value"):
            c.err(w, "value missing")
        if viz == "radial" and re.search(r"\d\s*(to|–|-|—)\s*\d", str(s.get("value", ""))):
            c.err(w, "a radial shows one share; a range value wraps its unit at desktop width. Use a bar tile for a range, or one number")
        if len(s.get("unit") or "") > 12:
            c.warn(w, f"unit {s.get('unit')!r} is long; it wraps under the number on the poster")
        if not s.get("source_url"):
            c.err(w, "source_url missing: every stat names a source a reader can follow")
        acc = s.get("source_accessed")
        if acc and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", acc):
            c.err(w, f"source_accessed {acc!r} is not YYYY-MM-DD")
    shown = c.pack(stats)
    wides = [i for i, s in enumerate(stats[:shown]) if s.get("wide")]
    if any(b == a + 1 for a, b in zip(wides, wides[1:])):
        c.err("basics", "two wide tiles back to back inside the fold")

    questions = d.get("questions") or []
    for n, q in enumerate(questions):
        w = f"question[{n}] {q.get('text', '')[:30]!r}"
        for k in ("text", "why", "detail", "lean_label_a", "lean_label_b"):
            if not q.get(k):
                c.err(w, f"{k} missing")
        for k, v in q.items():
            c.text(f"{w}.{k}", f"question.{k}", v)
        if q.get("kind") not in ("empirical", "value"):
            c.err(w, f"kind {q.get('kind')!r} must be empirical or value")
        if q.get("text") and not q["text"].rstrip().endswith("?"):
            c.warn(w, "question text does not end with ?")

    positions = d.get("positions") or []
    names = [p.get("name") for p in positions]
    keys = [p.get("color_key") for p in positions]
    for n, p in enumerate(positions):
        w = f"position[{n}] {p.get('name', '')[:30]!r}"
        for k in ("name", "steelman", "detail", "proponents"):
            if not p.get(k):
                c.err(w, f"{k} missing")
        for k, v in p.items():
            c.text(f"{w}.{k}", f"position.{k}", v)
        if p.get("color_key") not in POS_KEYS:
            c.err(w, f"color_key {p.get('color_key')!r} not in {POS_KEYS}")
        elif keys.count(p["color_key"]) > 1:
            c.err(w, f"color_key {p['color_key']!r} used twice")
        if re.search(r"\b(skeptics?|advocates?|pragmatists?|realists?|optimists?|pessimists?|hawks?|doves?|defenders?|critics?)\b", p.get("name", ""), re.I):
            c.warn(w, "name looks like a posture label; camps are named by what they want")

    crux = d.get("crux") or {}
    for k in ("lead", "lead_highlight", "subtitle", "empirical", "values"):
        if not crux.get(k):
            c.err(f"crux.{k}", "missing")
        c.text(f"crux.{k}", f"crux.{k}", crux.get(k))
    if crux.get("lead") and crux.get("lead_highlight") and crux["lead_highlight"] not in crux["lead"]:
        c.err("crux.lead_highlight", "not a verbatim substring of lead")

    actions = d.get("actions") or []
    for n, a in enumerate(actions):
        w = f"action[{n}] {a.get('title', '')[:30]!r}"
        for k in ("title", "description", "url"):
            if not a.get(k):
                c.err(w, f"{k} missing")
        for k, v in a.items():
            c.text(f"{w}.{k}", f"action.{k}", v, url=(k == "url"))
        if a.get("kind") not in ACTION_KINDS:
            c.err(w, f"kind {a.get('kind')!r} not in {sorted(ACTION_KINDS)}")
        fp = a.get("for_position")
        if fp and fp not in names:
            c.err(w, f"for_position {fp!r} matches no position name")

    # Say it once: an eight-word run shared by two different fields is a
    # sentence the reader meets twice. Warning, not error: a proper name or a
    # quoted figure can legitimately recur; the editor judges.
    fields = []
    for k, v in (d.get("overview") or {}).items():
        fields.append((f"overview.{k}", v))
    for n, x in enumerate(stats):
        for k in ("note", "detail"):
            fields.append((f"stat[{n}].{k}", x.get(k)))
    for n, x in enumerate(questions):
        for k in ("why", "detail"):
            fields.append((f"question[{n}].{k}", x.get(k)))
    for n, x in enumerate(positions):
        for k in ("steelman", "detail"):
            fields.append((f"position[{n}].{k}", x.get(k)))
    for k in ("subtitle", "empirical", "values"):
        fields.append((f"crux.{k}", crux.get(k)))
    for n, x in enumerate(actions):
        fields.append((f"action[{n}].description", x.get("description")))
    seen = {}
    reported = set()
    for name, text in fields:
        if not isinstance(text, str):
            continue
        words = re.findall(r"[a-z0-9$%.,’']+", text.lower())
        for i in range(len(words) - 7):
            gram = " ".join(words[i:i + 8])
            other = seen.setdefault(gram, name)
            if other != name and (other, name) not in reported:
                reported.add((other, name))
                c.warn(f"{name}", f"repeats {other}: “{gram} …”")

    for key, items in (("stats", stats), ("questions", questions), ("positions", positions), ("actions", actions)):
        lo, hi = COUNTS[key]
        if not (lo <= len(items) <= hi):
            c.err(key, f"{len(items)} items, schema says {lo}-{hi}")
    return c


class Command(BaseCommand):
    help = "Mechanical plain-text, length, enum and structure rules over a topic file."

    def add_arguments(self, p):
        p.add_argument("--slug")
        p.add_argument("--file")
        p.add_argument("--glance-hash", action="store_true",
                       help="print a hash of everything a render can show (all but detail text) and exit")

    def handle(self, *a, **o):
        if not (o["slug"] or o["file"]):
            self.stderr.write("give --slug or --file")
            raise SystemExit(2)
        path = Path(o["file"]) if o["file"] else Path("research/topics") / o["slug"] / "topic.json"
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            self.stderr.write(self.style.ERROR(f"{path}: {e}"))
            raise SystemExit(1)
        if o["glance_hash"]:
            import hashlib

            def strip(node):
                if isinstance(node, dict):
                    return {k: strip(v) for k, v in sorted(node.items())
                            if k not in ("detail", "id", "source_accessed")}
                if isinstance(node, list):
                    return [strip(v) for v in node]
                return node

            view = {k: doc.get(k) for k in ("title", "icon", "primary_category", "related")}
            view["content"] = strip(doc.get("content") or {})
            self.stdout.write(hashlib.sha256(json.dumps(view, sort_keys=True).encode()).hexdigest()[:16])
            return
        c = run(doc, path.resolve())
        for w in c.warnings:
            self.stdout.write(self.style.WARNING(f"WARN  {w}"))
        for e in c.errors:
            self.stdout.write(self.style.ERROR(f"ERROR {e}"))
        self.stdout.write(f"{len(c.errors)} errors, {len(c.warnings)} warnings in {path}")
        if c.errors:
            raise SystemExit(1)
