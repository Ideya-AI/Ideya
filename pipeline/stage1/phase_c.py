"""Stage 1, Phase C: the ledger and the checks (PIPELINE.md, stage 1, "Phase C").

extract (one unit per section) -> coverage check (code) -> quote and URL
check (code) -> verifiers (one unit per source) -> attribution rule (code)
-> lint (code) -> one grounded repair round (one unit per failing field) ->
the changed sections back through the same checks -> what is still open is
cut and logged -> section minimums -> the gate verdict.

Code checks before any model judges: a hallucinated URL or an invented quote
is structurally impossible. The verifier stands against the rest: a true
quote that does not support the claim.
"""

import hashlib
import json
import re
from collections import Counter

from ..checks import Defect, lint_camp_name, lint_position_text, lint_text, normalize, quote_match, tidy_draft
from ..prompts import assemble
from ..runner import Unit, run, run_units
from ..sources import Store, resolve_url
from ..stages import CriteriaFailure
from ..topic import TopicDir, now
from .shapes import ExtractorReturn, RepairReturn, VerifierReturn

PHASE = "C"
PROSE = {
    "basics": ("label", "note", "detail"),
    "questions": ("text", "why", "detail"),
    "positions": (
        "name",
        "steelman",
        "description",
        "detail",
        "representative_note",
    ),
    "crux": ("lead", "subtitle", "empirical", "values"),
    "overview": ("summary", "scope_covered", "scope_excluded", "why_now"),
    "actions": (),  # an action's proof is its URL; the text is lint-only
}
PAGE_VOICE = {"basics", "questions", "crux", "overview"}
LINT_ONLY = {"positions": ("proponents",), "actions": ("title", "description")}
# the loader's hard caps; a repair may not push a field past them
CAPS = {
    ("basics", "label"): 120, ("basics", "note"): 400,
    ("questions", "text"): 400,
    ("positions", "name"): 120, ("positions", "steelman"): 400,
    ("positions", "representative_note"): 300, ("positions", "proponents"): 400,
    ("crux", "lead"): 240,
    ("overview", "summary"): 400, ("overview", "scope_covered"): 400,
    ("overview", "scope_excluded"): 400,
    ("actions", "title"): 200, ("actions", "description"): 400,
}
REPAIR_GROWTH = 1.3  # a repair may grow a field this much, never more


def bound(section, f, original):
    return min(CAPS.get((section, f), 10_000), int(len(original) * REPAIR_GROWTH) + 40)  # map-checked fields that still get lint
MINIMUMS = {"basics": 8, "questions": 5, "positions": 3, "actions": 6}
CERTIFIED = [
    "topic:draft",
    "evidence:map",
    "evidence:ledger",
    "evidence:crux_placement",
]

HARD = re.compile(
    r"(“[^”]{3,}”)"  # a quoted span
    r"|(\b(?:[A-Z][\w&.’-]+(?:\s+(?:of|the|for|and|de|&)\s+)?){1,5}\s+(?:said|says|found|finds|estimates|estimated|argues|argued|reported|reports|warned|warns|projected|concluded|concludes)\b)"
    r"|((?<![A-Za-z])\d+(?:,\d{3})*(?:\.\d+)?%?)"  # a number or a year, not the 2 in CO2
)
ATTRIBUTED = re.compile(
    r"\b(according to|says|said|argues|argued|estimates|estimated|cites|cited|reports|reported|claims|claimed|"
    r"per|by|in the words of|contends|contended|maintains|puts it at|figure|camp|counts|counted|records|recorded|"
    r"notes|noted|finds|found|states|stated|lists|listed|tracks|tracked|tallies|documents|shows|showed|"
    r"projects|projected|calculates|calculated|warns|warned|writes|wrote|publishes|published)\b",
    re.I,
)
STOP = {"the", "of", "and", "for", "a", "an", "on", "in", "report", "world", "status", "international", "association"}


def names_source(sentence: str, src) -> bool:
    """The sentence names its source's publisher or title by a distinctive word."""
    words = set(normalize(f"{src.publisher} {src.title}").split()) - STOP
    return any(len(w) > 3 and w in normalize(sentence).split() for w in words)


def h(*parts) -> str:
    """Eight hex chars over the inputs, so a unit's return file is reused only
    while what it was handed is unchanged."""
    blob = json.dumps(parts, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(blob.encode()).hexdigest()[:8]


def draft_key(draft: dict) -> str:
    """What proving depends on: the prose of every section and the action
    URLs. Presentation fields can move through a save without changing it."""
    return h([items(draft, s) for s in PROSE], [a.get("url") for a in draft.get("actions", [])])


def items(draft: dict, section: str) -> list[dict]:
    """[{id, <prose fields>}] for a section, crux and overview as one item."""
    if section == "basics":
        rows = draft.get("basics", {}).get("stats", [])
    elif section in ("crux", "overview"):
        rows = [dict(draft.get(section, {}), id=section)]
    else:
        rows = draft.get(section, [])
    return [
        {"id": r.get("id", ""), **{f: r.get(f, "") for f in PROSE[section] if r.get(f)}}
        for r in rows
    ]


def field_ref(draft: dict, section: str, item: str):
    """(container dict, key) for one prose field's home, so a repair can be written back."""
    if section in ("crux", "overview"):
        return draft[section]
    rows = draft["basics"]["stats"] if section == "basics" else draft[section]
    return next(r for r in rows if r.get("id") == item)


def lint(draft: dict) -> list[Defect]:
    """Lint the prose fields only, located as section/item/field so a repairer
    can be pointed at the field."""
    out = []
    for section in PROSE:
        rows = draft["basics"]["stats"] if section == "basics" else draft.get(section)
        for it in items(draft, section):
            extra = {}
            if section in LINT_ONLY:
                row = next(r for r in rows if r.get("id") == it["id"])
                extra = {f: row.get(f, "") for f in LINT_ONLY[section] if row.get(f)}
            for f, text in {**it, **extra}.items():
                if f == "id":
                    continue
                where = f"{section}/{it['id']}/{f}"
                if section == "positions":
                    out += lint_position_text(text, where)
                    if f == "name":
                        out += lint_camp_name(text, where)
                else:
                    out += lint_text(text, where)
    return out


def check_proponents(draft: dict, camps: list[dict]) -> list[dict]:
    """Every name in a position's proponents, and its representative, is an
    adherent of that camp in the map. Unknown names are cut by code and
    recorded; the map is the source for who holds a view."""
    cuts = []
    for pos, camp in zip(draft["positions"], camps):
        known = [normalize(a["name"]) for a in camp["adherents"]] + [
            normalize(a["org"]) for a in camp["adherents"] if a.get("org")
        ]

        def adherent(name):
            n = normalize(name)
            return any(n in k or k in n for k in known if k)

        kept = [n.strip() for n in pos.get("proponents", "").split(",") if n.strip()]
        gone = [n for n in kept if not adherent(n)]
        if gone:
            pos["proponents"] = ", ".join(n for n in kept if adherent(n))
            cuts.append({"section": "positions", "item": pos["id"], "field": "proponents",
                         "claim": "; ".join(gone), "why": "not an adherent of this camp in the map"})
        rep = pos.get("representative_name", "")
        if rep and not adherent(rep):
            cuts.append({"section": "positions", "item": pos["id"], "field": "representative_name",
                         "claim": rep, "why": "not an adherent of this camp in the map"})
            pos["representative_name"] = pos["representative_note"] = ""
    return cuts


def coverage(draft: dict, ledger: list[dict]) -> list[dict]:
    """Every hard-claim pattern in every prose field must fall inside some
    ledger claim's quote for that field. Returns the misses."""
    misses = []
    for section in PROSE:
        for it in items(draft, section):
            for f, text in it.items():
                if f == "id" or (section, f) == ("basics", "label"):
                    continue
                # per item, not per field: a figure the note claims and the
                # detail repeats is one claim, verified once
                quotes = [
                    normalize(c["quote"])
                    for c in ledger
                    if c["section"] == section and c["item"] == it["id"]
                ]
                for m in HARD.finditer(text):
                    span = m.group(0)
                    if not any(normalize(span) in q for q in quotes):
                        misses.append(
                            {
                                "section": section,
                                "item": it["id"],
                                "field": f,
                                "span": span,
                            }
                        )
    return misses


def code_check(claim: dict, store: Store, draft: dict) -> str | None:
    """Why a claim fails before any model looks, or None."""
    sid = claim.get("source") or ""
    if sid not in store.index()["sources"]:
        return "no fetched source"
    if claim["section"] == "actions":
        url = claim["claim"].split(" ")[0]
        if store.by_url(url):
            return None  # fetched into the store, possibly through the archive fallback
        ok, status = resolve_url(url)
        return None if ok else f"URL does not resolve ({status})"
    if not claim.get("source_quote"):
        return "no source quote"
    if quote_match(claim["source_quote"], store.text(sid)) == "none":
        return "source quote not found in the source text"
    if claim["section"] == "basics" and claim["field"] == "note":
        st = field_ref(draft, "basics", claim["item"])
        sq = re.sub(r"[^\d.]", "", claim["source_quote"])
        for tok in re.findall(r"\d+(?:\.\d+)?", st.get("value", "").replace(",", "")):
            if tok not in sq:
                return f"value {st['value']!r} is not in the source quote"
        if not store.by_url(st.get("source_url", "")):
            ok, status = resolve_url(st.get("source_url", ""))
            if not ok:
                return f"source_url does not resolve ({status})"
    return None


def needs_attribution(claim: dict, store: Store, ledger: list[dict]) -> bool:
    """A camp's own number is attributed, not asserted, unless a reference or
    official source corroborates it or the sentence already names who says it."""
    if claim["section"] not in PAGE_VOICE or claim["kind"] != "fact":
        return False
    cls = store.get(claim["source"]).class_
    if cls not in ("camp", "critique"):
        return False
    corroborated = any(
        c is not claim
        and c["section"] == claim["section"]
        and c["item"] == claim["item"]
        and normalize(c["claim"]) == normalize(claim["claim"])
        and c.get("source") in store.index()["sources"]
        and store.get(c["source"]).class_ in ("reference", "official")
        for c in ledger
    )
    return (
        not corroborated
        and not ATTRIBUTED.search(claim["quote"])
        and not names_source(claim["quote"], store.get(claim["source"]))
    )


async def extract(topic, draft, sidecars, sections, rnd, misses=None):
    units, direct = [], []
    for section in sections:
        side = sidecars.get(section, [])
        if not PROSE[section]:
            direct += [dict(c, section=section) for c in side]  # sidecar is the ledger
            continue
        if misses:
            side = {
                "sidecar": side,
                "spans_that_must_be_claims": [
                    m for m in misses if m["section"] == section
                ],
            }
        system, prompt = assemble(
            "stage1/extractor",
            section=section,
            text=items(draft, section),
            sidecar=side,
        )
        units.append(
            Unit(
                name=f"extract-{section}-{rnd}-{h(items(draft, section), side)}",
                phase=PHASE,
                model="sonnet",
                effort="low",
                system=system,
                prompt=prompt,
                output=ExtractorReturn,
                max_turns=3,
            )
        )
    out = direct
    for section, r in zip([x for x in sections if PROSE[x]], await run_units(topic, units, parallel=6)):
        claims = [dict(c.model_dump(), section=section) for c in r.claims]
        # a gloss, a claim with no figure, date, quote or attribution in its own
        # text, is dropped unless its quote is the only coverage of a figure
        hard = [d for d in claims if HARD.search(d["claim"])]
        covered = {(d["item"], normalize(m.group(0))) for d in hard for m in HARD.finditer(d["quote"])}
        for d in claims:
            if d in hard:
                continue
            spans = {(d["item"], normalize(m.group(0))) for m in HARD.finditer(d["quote"])}
            if spans - covered:
                hard.append(d)
                covered |= spans
        for d in hard:
            if not d.get("source"):
                adopt_sidecar_source(d, sidecars.get(section, []))
            out.append(d)
    return out


def adopt_sidecar_source(claim: dict, sidecar: list[dict]):
    """An extracted claim the extractor left unsourced takes the source of a
    sidecar claim on the same item that shares its sentence or its figures."""
    q = normalize(claim["quote"])
    nums = set(re.findall(r"\d+(?:\.\d+)?", claim["quote"]))
    best = None
    for s in sidecar:
        if not s.get("source"):
            continue  # writers label items their own way; the sentence is the match
        sq = normalize(s.get("quote", ""))
        if sq and (sq in q or q in sq):
            best = s
            break
        snums = set(re.findall(r"\d+(?:\.\d+)?", s.get("quote", "")))
        if nums and nums & snums and best is None:
            best = s
    if best:
        claim["source"] = best["source"]
        claim["source_quote"] = claim.get("source_quote") or best.get("source_quote", "")


async def verify(topic, claims, store, rnd):
    by_source = {}
    for c in claims:
        by_source.setdefault(c["source"], []).append(c)
    units, groups = [], []
    for sid, cs in by_source.items():
        s = store.get(sid)
        system, prompt = assemble(
            "stage1/verifier",
            source={
                "id": sid,
                "title": s.title,
                "publisher": s.publisher,
                "published": s.published,
                "class": s.class_,
            },
            claims=[
                {
                    "id": f"k{n}",
                    "claim": c["claim"],
                    "kind": c["kind"],
                    "source_quote": c["source_quote"],
                }
                for n, c in enumerate(cs, 1)
            ],
            text=store.text(sid)[:120_000],
        )
        units.append(
            Unit(
                name=f"verify-{sid}-{h('k', [(c['claim'], c['source_quote']) for c in cs])}",
                phase=PHASE,
                model="sonnet",
                effort="low",
                system=system,
                prompt=prompt,
                output=VerifierReturn,
                max_turns=3,
            )
        )
        groups.append(cs)
    for cs, r in zip(groups, await run_units(topic, units, parallel=6)):
        got = {v.claim: v for v in r.verdicts}
        for n, c in enumerate(cs, 1):
            v = got.get(f"k{n}")
            c["verdict"] = v.verdict if v else "unsupported"
            c["note"] = v.note if v else "verifier returned no verdict for this claim"


async def prove(topic, draft, sidecars, sections, store, ledger, rnd) -> list[dict]:
    """Extract, cover, code-check and verify the given sections. Replaces those
    sections' claims in `ledger`; returns the failures as (claim) dicts."""
    new = await extract(topic, draft, sidecars, sections, rnd)
    misses = [m for m in coverage(draft, new) if m["section"] in sections]
    if misses:
        redo = sorted({m["section"] for m in misses})
        again = await extract(topic, draft, sidecars, redo, f"{rnd}b", misses)
        new = [c for c in new if c["section"] not in redo] + again
        misses = [m for m in coverage(draft, new) if m["section"] in sections]
    if misses:
        raise CriteriaFailure(
            f"extraction recall: {len(misses)} hard-claim span(s) not in any ledger quote, e.g. "
            + "; ".join(
                f"{m['section']}/{m['item']}/{m['field']}: {m['span']!r}"
                for m in misses[:5]
            ),
            "stage1",
        )
    ledger[:] = [c for c in ledger if c["section"] not in sections]
    start = max((int(c["id"][1:]) for c in ledger), default=0)
    for n, c in enumerate(new, start + 1):
        c["id"] = f"c{n}"
    to_verify = []
    for c in new:
        why = code_check(c, store, draft)
        if why:
            c["verdict"], c["note"] = "unsupported", why
        elif c["section"] == "actions":
            c["verdict"], c["note"] = "supported", "URL resolves"
        else:
            to_verify.append(c)
    await verify(topic, to_verify, store, rnd)
    ledger.extend(new)
    for c in new:
        if c["verdict"] == "supported" and needs_attribution(c, store, ledger):
            c["verdict"], c["note"] = (
                "partial",
                "a camp or critique source in the page's own voice; attribute it",
            )
    return [c for c in new if c["verdict"] in ("partial", "unsupported")]


async def repair(
    topic, draft, failures, lint_defects, store, sidecars, rnd, move="choose"
):
    """One repairer per failing field. Returns the sections touched."""
    by_field = {}
    for c in failures:
        by_field.setdefault((c["section"], c["item"], c["field"]), []).append(
            {
                "claim": c["claim"],
                "quote": c["quote"],
                "source": c["source"],
                "source_quote": c["source_quote"],
                "finding": f"{c['verdict']}: {c['note']}",
            }
        )
    for d in lint_defects:
        m = re.match(r"(\w+)(?:\[(\d+)\])?\.(?:stats\[(\d+)\]\.)?(\w+)$", d.where)
        if not m:
            continue
        section, i, si, f = m.groups()
        idx = si if section == "basics" else i
        item = (
            section
            if section in ("crux", "overview")
            else items(draft, section)[int(idx)]["id"]
        )
        by_field.setdefault((section, item, f), []).append(
            {
                "claim": "",
                "quote": d.detail,
                "source": "",
                "source_quote": "",
                "finding": f"lint {d.rule}: {d.detail}; rewrite without it",
            }
        )
    units, keys = [], []
    for (section, item, f), probs in by_field.items():
        if section == "actions":  # no rewrite can fix a dead link; the action goes
            units.append(None)
            keys.append((section, item, f))
            continue
        home = field_ref(draft, section, item)
        srcs = "\n\n".join(
            f"=== {p['source']}\n{store.text(p['source'])[:30_000]}"
            for p in probs
            if p["source"] in store.index()["sources"]
        )
        system, prompt = assemble(
            "stage1/repairer",
            section=section,
            field=f,
            bound=bound(section, f, home.get(f, "")),
            text=home.get(f, ""),
            voice=(
                "the camp's voice; the camp is the attribution"
                if section == "positions"
                else "the page's own voice; name who asserts it"
            ),
            claim=probs,
            finding="\n".join(p["finding"] for p in probs),
            source_text=srcs or "(none)",
            move=(
                "choose the move that keeps the most of what the source supports"
                if move == "choose"
                else move
            ),
        )
        units.append(
            Unit(
                name=f"repair-{section}-{item}-{f}-{h(home.get(f, ''), probs)}",
                phase=PHASE,
                model="opus",
                effort="medium",
                system=system,
                prompt=prompt,
                output=RepairReturn,
                max_turns=3,
            )
        )
        keys.append((section, item, f))
    touched = set()
    live = [u for u in units if u is not None]
    results = iter(await run_units(topic, live, parallel=4))
    for (section, item, f), u in zip(keys, units):
        r = next(results) if u is not None else None
        if section == "actions":
            draft["actions"] = [a for a in draft["actions"] if a.get("id") != item]
            touched.add(section)
            continue
        home = field_ref(draft, section, item)
        if len(r.text) > bound(section, f, home.get(f, "")):
            # an oversized repair is no repair: keep the field, leave the claim open
            continue
        home[f] = r.text
        sidecars.setdefault(section, []).extend(
            dict(c.model_dump(), section=section, item=item, field=f) for c in r.claims
        )
        touched.add(section)
    return touched


async def _run(topic: TopicDir):
    store = Store(topic)
    doc = topic.load_topic()
    draft = tidy_draft(doc["draft"])
    ev = topic.load_evidence()
    sidecars = ev.get("sidecars", {})
    ledger: list[dict] = []
    cuts = check_proponents(draft, sorted(ev["map"]["camps"], key=lambda c: c["rank"]))
    doc["draft"] = draft
    topic.save_topic(doc)

    # resume: a draft already proven to this exact text needs no re-proving,
    # and a draft checkpointed after the first repair round resumes at the recheck
    proven = ev.get("proven")
    checkpoint = ev.get("prove_checkpoint")
    if proven and proven.get("draft_hash") == draft_key(draft) and ev.get("ledger"):
        ledger = ev["ledger"]
        cuts = ev.get("cuts", [])
        failures, defects = [], lint(draft)
        touched = []
    elif checkpoint and checkpoint.get("draft_hash") == draft_key(draft):
        ledger = checkpoint["ledger"]
        sidecars = checkpoint["sidecars"]
        cuts = checkpoint["cuts"]
        touched = checkpoint["touched"]
        failures, defects = [True], lint(draft)  # force the recheck path
    else:
        failures = await prove(topic, draft, sidecars, list(PROSE), store, ledger, 1)
        defects = lint(draft)
        touched = None
    if failures or defects:
        if touched is None:
            touched = await repair(topic, draft, failures, defects, store, sidecars, 1)
            tidy_draft(draft)
            doc["draft"] = draft
            topic.save_topic(doc)
            ev = topic.load_evidence()
            ev["prove_checkpoint"] = {
                "draft_hash": draft_key(draft), "ledger": ledger, "sidecars": sidecars,
                "cuts": cuts, "touched": sorted(touched), "at": now(),
            }
            topic.save_evidence(ev)
        failures = await prove(
            topic, draft, sidecars, sorted(touched), store, ledger, 2
        )
        defects = lint(draft)
        if failures:
            # still open after the grounded round: cut and log, never block
            await repair(topic, draft, failures, defects, store, sidecars, 2, move="cut")
            for c in failures:
                c["verdict"] = "cut"
                cuts.append(
                    {
                        "id": c["id"],
                        "section": c["section"],
                        "item": c["item"],
                        "field": c["field"],
                        "claim": c["claim"],
                        "why": c["note"],
                    }
                )
            tidy_draft(draft)
            doc["draft"] = draft
            topic.save_topic(doc)
            defects = lint(draft)
    ev = topic.load_evidence()
    ev["ledger"] = ledger
    ev["cuts"] = cuts
    ev["sidecars"] = sidecars
    ev["proven"] = {"draft_hash": draft_key(draft), "at": now()}
    ev.pop("prove_checkpoint", None)
    ev["ledger_summary"] = {
        "claims": len(ledger),
        "verdicts": dict(Counter(c["verdict"] for c in ledger)),
        "cuts_by_reason": dict(Counter(c["why"][:40] for c in cuts)),
        "lint_open": [str(d) for d in defects],
    }
    topic.save_evidence(ev)
    if defects:
        raise CriteriaFailure(
            "lint: " + "; ".join(str(d) for d in defects[:8]), "stage1"
        )

    counts = {
        "basics": len(draft["basics"]["stats"]),
        "questions": len(draft["questions"]),
        "positions": len(draft["positions"]),
        "actions": len(draft["actions"]),
    }
    short = [
        f"{k} has {counts[k]}, minimum {v}"
        for k, v in MINIMUMS.items()
        if counts[k] < v
    ]
    if short:
        raise CriteriaFailure("section minimums: " + "; ".join(short), "stage1")
    camps = {c["key"] for c in ev["map"]["camps"]}
    placed = {p["camp"] for p in ev["crux_placement"]["placement"]}
    if camps - placed:
        raise CriteriaFailure(
            f"crux placement misses camps: {sorted(camps - placed)}", "stage1"
        )

    topic.certify("stage1", CERTIFIED, f"{len(ledger)} claims, {len(cuts)} cut")


def run_phase(topic: TopicDir):
    run(_run(topic))
