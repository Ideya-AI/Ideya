"""Stage 1, Phase A: the map (PIPELINE.md, stage 1, "Phase A").

framer -> four scouts by source class (a second round per class until code
says the class is saturated) -> camp scout seeded from the names harvested ->
cartographer -> gap scout -> cartographer final -> map check (code) -> merge
into evidence.json.

Every unit is a separate call, resumable from its return file. The map check
blocks the topic: a cartographer that invents an adherent is the failure this
phase exists to prevent.
"""

import json

from ..checks import lint_camp_name, normalize, quote_match
from ..prompts import assemble
from ..runner import Unit, run, run_unit, run_units
from ..sources import FETCH_TOOL_NAME, Store, fetch_tool, merge_into_evidence
from ..stages import CriteriaFailure
from ..topic import TopicDir
from .shapes import FramerReturn, Map, ScoutReturn

PHASE = "A"
CLASSES = {
    "reference": "ref",
    "explainer": "exp",
    "official": "off",
    "critique": "crit",
}
MISSION = {
    "reference": "Your job is the settled account: how reference works describe the debate, whom they name as holding each view, and the figures they cite.",
    "explainer": "Your job is the journalistic account: how major explainers lay out the debate, whom they quote on each side, and the figures they lead with.",
    "official": "Your job is the official record: what agencies, statistical bodies and regulators state as fact about this topic, and what positions official bodies have taken in their own words.",
    "critique": "Your job is the critics: documents whose purpose is to argue against a position by name. Critics have an incentive to name every opponent, so record everyone each document argues against.",
}
SATURATION_FLOOR = 6  # sources per class before saturation can end it
SATURATION_NEW = 0.05  # share of new claimant names in the last two sources
MAX_ROUNDS = 2


def done(topic: TopicDir) -> bool:
    ev = topic.load_evidence()
    return bool(ev.get("map")) and bool((ev.get("map_check") or {}).get("passed"))


def _index(doc):
    return {k: doc.get(k) for k in ("title", "scope", "primary_category", "categories")}


def _scout_unit(topic, store, idx, cls, frame, seeds, known, rnd):
    system, prompt = assemble(
        "stage1/scout",
        title=idx["title"],
        scope=idx["scope"],
        **{"class": cls},
        mission=MISSION[cls],
        frame=frame,
        seeds="\n".join(f"- {s}" for s in seeds) or "(none; search)",
        known="\n".join(f"- {n}" for n in known) or "(none yet)",
    )
    return Unit(
        name=f"scout-{cls}-{rnd}",
        phase=PHASE,
        model="sonnet",
        effort="medium",
        system=system,
        prompt=prompt,
        output=ScoutReturn,
        tools=["WebSearch", FETCH_TOOL_NAME],
        mcp={"sources": fetch_tool(store, CLASSES[cls], cls)},
        max_turns=80,
    )


def saturation(returns: list[ScoutReturn], store: Store, ns: str) -> dict:
    """Computed by code, never reported by the scout: distinct claimant names
    per source in fetch order; the class is saturated when the last two
    sources added under 5% new names and the floor is met."""
    ids = sorted(k for k in store.index()["sources"] if k.startswith(f"s-{ns}-"))
    by_source = {sid: set() for sid in ids}
    for r in returns:
        for c in r.claimants:
            if c.source in by_source:
                by_source[c.source].add(normalize(c.name))
    seen, new_per_source = set(), []
    for sid in ids:
        fresh = by_source[sid] - seen
        new_per_source.append(len(fresh))
        seen |= by_source[sid]
    total = len(seen) or 1
    last_two = sum(new_per_source[-2:])
    saturated = len(ids) >= SATURATION_FLOOR and last_two / total < SATURATION_NEW
    return {
        "sources": len(ids),
        "claimants": len(seen),
        "new_in_last_two": last_two,
        "saturated": saturated,
    }


def checked_harvest(per_class: dict, store: Store) -> tuple[dict, dict]:
    """The harvest the cartographer sees: every claimant and fact whose quote
    is in its cited source's text, by code. What fails is dropped and counted,
    so the cartographer cannot copy a bad quote into the map."""
    harvest, dropped = {}, {}
    for cls, rs in per_class.items():
        keep_c, keep_f, drop = [], [], []
        for r in rs:
            for c in r.claimants:
                ok = c.source in store.index()["sources"] and quote_match(c.claim, store.text(c.source)) != "none"
                (keep_c if ok else drop).append(c.model_dump())
            for f in r.facts:
                ok = f.source in store.index()["sources"] and quote_match(f.quote, store.text(f.source)) != "none"
                (keep_f if ok else drop).append(f.model_dump())
        harvest[cls] = {"claimants": keep_c, "facts": keep_f}
        dropped[cls] = drop
    return harvest, dropped


def drop_unverifiable_facts(m: Map, store: Store) -> tuple[Map, list[dict]]:
    """Remove agreed facts whose quote is not in their source, remapping the
    stat list's indices. Returns the map and what was dropped."""
    keep, dropped, remap = [], [], {}
    for i, f in enumerate(m.agreed_facts):
        ok = f.source in store.index()["sources"] and quote_match(f.quote, store.text(f.source)) != "none"
        if ok:
            remap[i] = len(keep)
            keep.append(f)
        else:
            dropped.append({"index": i, "statement": f.statement, "source": f.source})
    stats = [s.model_copy(update={"from_fact": remap[s.from_fact]}) for s in m.stat_list if s.from_fact in remap]
    return m.model_copy(update={"agreed_facts": keep, "stat_list": stats}), dropped


STAT_FLOOR = 10  # keep camp- and critique-sourced tiles only when dropping them would go under this


def prefer_reference_stats(m: Map, store: Store) -> tuple[Map, list[dict]]:
    """Basics speaks in the page's own voice, so a tile whose only source is a
    camp's or a critic's document is dropped when the reference, official and
    explainer tiles alone meet the floor."""

    def cls(e):
        return store.get(m.agreed_facts[e.from_fact].source).class_

    good = [e for e in m.stat_list if cls(e) in ("reference", "official", "explainer")]
    if len(good) < STAT_FLOOR:
        return m, []
    dropped = [{"label": e.label, "class": cls(e)} for e in m.stat_list if e not in good]
    return m.model_copy(update={"stat_list": good}), dropped


def check_map(m: Map, store: Store) -> tuple[list[str], int]:
    """Every camp has two adherents on distinct sources, one institutional, a
    wants line, a distinguishing proposition and a rank; every adherent quote
    and agreed fact is in its source's text. Returns (errors, near_matches)."""
    errors, near = [], 0
    texts = {}

    def text(sid):
        if sid not in texts:
            try:
                texts[sid] = store.text(sid)
            except (KeyError, FileNotFoundError):
                texts[sid] = None
        return texts[sid]

    def quoted(where, quote, sid):
        nonlocal near
        t = text(sid)
        if t is None:
            errors.append(f"{where}: source {sid} is not in the store")
            return
        m = quote_match(quote, t)
        if m == "none":
            errors.append(f"{where}: quote not found in {sid}: {quote[:80]!r}")
        elif m == "near":
            near += 1

    ranks = sorted(c.rank for c in m.camps)
    if ranks != list(range(1, len(m.camps) + 1)):
        errors.append(f"ranks are {ranks}, not 1..{len(m.camps)}")
    keys = {c.key for c in m.camps}
    for c in m.camps:
        w = f"camp {c.key}"
        if len(c.adherents) < 2:
            errors.append(f"{w}: {len(c.adherents)} adherent(s); a camp needs two")
        if len({a.source for a in c.adherents}) < 2:
            errors.append(f"{w}: adherents share one source")
        if not any(a.kind == "institution" for a in c.adherents):
            errors.append(f"{w}: no institutional adherent")
        for f in ("wants", "distinguishing", "rank_reason"):
            if not getattr(c, f).strip():
                errors.append(f"{w}: {f} is empty")
        errors += [str(d) for d in lint_camp_name(c.name, w)]
        for a in c.adherents:
            quoted(f"{w} adherent {a.name}", a.quote, a.source)
    for i, f in enumerate(m.agreed_facts):
        quoted(f"agreed_fact[{i}]", f.quote, f.source)
        for k in f.cited_by_camps:
            if k not in keys:
                errors.append(f"agreed_fact[{i}]: unknown camp key {k}")
    for i, s in enumerate(m.stat_list):
        if not 0 <= s.from_fact < len(m.agreed_facts):
            errors.append(f"stat_list[{i}]: from_fact {s.from_fact} out of range")
    for i, cs in enumerate(m.controversial_statements):
        for k in cs.held_by + cs.denied_by:
            if k not in keys:
                errors.append(f"controversial_statements[{i}]: unknown camp key {k}")
    return errors, near


async def _run(topic: TopicDir):
    doc = topic.load_topic()
    idx = _index(doc)
    store = Store(topic)

    # framer
    system, prompt = assemble(
        "stage1/framer",
        title=idx["title"],
        scope=idx["scope"],
        categories=", ".join([idx["primary_category"], *(idx["categories"] or [])]),
    )
    framer: FramerReturn = await run_unit(
        topic,
        Unit(
            name="framer",
            phase=PHASE,
            model="opus",
            effort="medium",
            system=system,
            prompt=prompt,
            output=FramerReturn,
            tools=["WebSearch"],
            max_turns=20,
        ),
    )
    frame = json.dumps(
        {
            "dimensions": [d.model_dump() for d in framer.dimensions],
            "affected": framer.affected,
            "frame_question": framer.frame_question,
        },
        ensure_ascii=False,
        indent=1,
    )
    seed_urls = [s.url for s in framer.seed_sources]
    seeds = {
        "reference": [u for u in seed_urls if "wikipedia.org" in u]
        + framer.search_terms[:4],
        "explainer": [u for u in seed_urls if "wikipedia.org" not in u]
        + framer.search_terms[:4],
        "official": framer.search_terms,
        "critique": framer.search_terms,
    }

    # scouts, round 1 in parallel, then a second round per unsaturated class
    round1 = [
        _scout_unit(topic, store, idx, cls, frame, seeds[cls], [], 1) for cls in CLASSES
    ]
    returns = dict(zip(CLASSES, await run_units(topic, round1, parallel=4)))
    scouting = {}
    per_class = {cls: [r] for cls, r in returns.items()}
    for rnd in range(2, MAX_ROUNDS + 1):
        again = [cls for cls in CLASSES if not saturation(per_class[cls], store, CLASSES[cls])["saturated"]]
        units = [
            _scout_unit(topic, store, idx, cls, frame, seeds[cls],
                        sorted({c.name for r in per_class[cls] for c in r.claimants}), rnd)
            for cls in again
        ]
        for cls, r in zip(again, await run_units(topic, units, parallel=4)):
            per_class[cls].append(r)
    for cls in CLASSES:
        scouting[cls] = {**saturation(per_class[cls], store, CLASSES[cls]), "rounds": len(per_class[cls])}

    # camp scout, seeded from everyone the others named
    names = set()
    for rs in per_class.values():
        for r in rs:
            for c in r.claimants:
                names.update(c.argues_against)
                if c.org:
                    names.add(c.org)
                elif c.kind == "person":
                    names.add(c.name)
    system, prompt = assemble(
        "stage1/camp_scout",
        title=idx["title"],
        scope=idx["scope"],
        names="\n".join(f"- {n}" for n in sorted(names)),
    )
    camp = await run_unit(
        topic,
        Unit(
            name="scout-camp-1",
            phase=PHASE,
            model="sonnet",
            effort="medium",
            system=system,
            prompt=prompt,
            output=ScoutReturn,
            tools=["WebSearch", FETCH_TOOL_NAME],
            mcp={"sources": fetch_tool(store, "camp", "camp")},
            max_turns=100,
        ),
    )
    per_class["camp"] = [camp]
    scouting["camp"] = {**saturation([camp], store, "camp"), "rounds": 1}

    # cartographer
    harvest, dropped = checked_harvest(per_class, store)
    for cls in scouting:
        scouting[cls]["dropped_by_quote_check"] = len(dropped.get(cls, []))
    system, prompt = assemble(
        "stage1/cartographer",
        title=idx["title"],
        scope=idx["scope"],
        frame=frame,
        scouts=harvest,
    )
    m: Map = await run_unit(
        topic,
        Unit(
            name="cartographer",
            phase=PHASE,
            model="opus",
            effort="high",
            system=system,
            prompt=prompt,
            output=Map,
            max_turns=4,
        ),
    )

    # gap round, once; the final cartographer also gets what the map check found
    errors, _ = check_map(m, store)
    open_gaps = [g.model_dump() for g in m.gaps if not g.filled]
    gap = None
    if open_gaps:
        system, prompt = assemble(
            "stage1/gap_scout", title=idx["title"], scope=idx["scope"], gaps=open_gaps
        )
        gap = await run_unit(
            topic,
            Unit(
                name="scout-gap-1",
                phase=PHASE,
                model="sonnet",
                effort="medium",
                system=system,
                prompt=prompt,
                output=ScoutReturn,
                tools=["WebSearch", FETCH_TOOL_NAME],
                mcp={"sources": fetch_tool(store, "gap", None)},
                max_turns=60,
            ),
        )
    if open_gaps or errors:
        gap_checked = checked_harvest({"gap": [gap]}, store)[0]["gap"] if gap else "(no gap search was run)"
        system, prompt = assemble(
            "stage1/cartographer_final",
            title=idx["title"],
            map=m.model_dump(),
            gap_return=gap_checked,
            check_errors="\n".join(f"- {e}" for e in errors) or "(none)",
        )
        m = await run_unit(
            topic,
            Unit(
                name="cartographer-final",
                phase=PHASE,
                model="opus",
                effort="high",
                system=system,
                prompt=prompt,
                output=Map,
                max_turns=4,
            ),
        )

    # the map is a checked artifact; a fact whose quote is not in its source
    # is dropped by code and recorded, an adherent whose quote is not blocks
    m, dropped_facts = drop_unverifiable_facts(m, store)
    m, dropped_stats = prefer_reference_stats(m, store)
    errors, near = check_map(m, store)
    ev = merge_into_evidence(topic)
    ev["map"] = m.model_dump()
    ev["scouting"] = scouting
    ev["map_check"] = {
        "passed": not errors,
        "errors": errors,
        "near_quotes": near,
        "dropped_facts": dropped_facts,
        "dropped_stats": dropped_stats,
    }
    topic.save_evidence(ev)
    if errors:
        raise CriteriaFailure(
            f"map check failed with {len(errors)} error(s): " + " | ".join(errors[:6]),
            "stage1",
        )


def run_phase(topic: TopicDir):
    run(_run(topic))
