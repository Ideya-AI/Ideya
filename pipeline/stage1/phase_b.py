"""Stage 1, Phase B: the sections (PIPELINE.md, stage 1, "Phase B").

Stat writers (one per source), questions and position writers (one per camp)
run in parallel; the crux after them; overview and actions last. Code merges
the returns into `topic.json`, derives every presentation number, assigns
item ids, and files each writer's sidecar under `evidence.sidecars` for
Phase C.
"""

import asyncio
import json
import re

from ..prompts import assemble
from ..runner import Unit, run, run_unit, run_units
from ..sources import FETCH_TOOL_NAME, Store, fetch_tool
from ..stages import CriteriaFailure
from ..topic import TopicDir
from .shapes import (
    CruxReturn,
    Map,
    OverviewActionsReturn,
    PositionReturn,
    QuestionsReturn,
    StatWriterReturn,
)

PHASE = "B"
CEILINGS = {  # research-grade ceilings the prompts state; checked here, one rerun, then recorded
    "questions": {"text": 200, "why": 300, "detail": 1200},
    "position": {"steelman": 300, "description": 900, "detail": 1600, "representative_note": 250, "proponents": 350},
    "crux": {"lead": 200, "subtitle": 500, "empirical": 1800, "values": 1800},
}


CEILING_TOLERANCE = 0.10  # a breach inside this is recorded, not rerun


def _breach(entry: str) -> float:
    n, cap = (int(x) for x in re.findall(r"(\d+) > (\d+)", entry)[0])
    return n / cap - 1


def over_ceiling(kind, obj) -> list[str]:
    rows = obj.questions if kind == "questions" else [obj]
    out = []
    for i, r in enumerate(rows):
        for f, cap in CEILINGS[kind].items():
            n = len(getattr(r, f, "") or "")
            if n > cap:
                out.append(f"{kind}[{i}].{f}: {n} > {cap}")
    return out


async def run_bounded(topic, unit, kind):
    """Run a writing unit; if its return breaks a ceiling, run it once more
    and keep the return with fewer breaches. What is still over is recorded."""
    out = await run_unit(topic, unit)
    over = over_ceiling(kind, out)
    if over and any(_breach(o) > CEILING_TOLERANCE for o in over):
        first = topic.read_return(unit.phase, unit.name)
        again = await run_unit(topic, unit, force=True)
        if len(over_ceiling(kind, again)) < len(over):
            out, over = again, over_ceiling(kind, again)
        else:
            topic.write_return(unit.phase, unit.name, first)
    return out, over
SOURCE_TEXT_CAP = 40_000  # chars of one source handed to a writer
POSITION_SOURCES_CAP = 140_000
POLL = re.compile(
    r"\b(poll|polls|polled|survey|surveyed|respondents|gallup|pew|yougov|ipsos)\b", re.I
)


def done(topic: TopicDir) -> bool:
    d = topic.load_topic().get("draft") or {}
    return bool(
        (d.get("basics") or {}).get("stats")
        and d.get("questions")
        and d.get("positions")
        and (d.get("crux") or {}).get("lead")
        and (d.get("overview") or {}).get("summary")
        and d.get("actions")
    )


def _facts(m: Map):
    return [
        {"index": i, "statement": f.statement, "quote": f.quote, "source": f.source}
        for i, f in enumerate(m.agreed_facts)
    ]


def _source_block(store: Store, sid: str, cap: int) -> str:
    s = store.get(sid)
    text = store.text(sid)
    clipped = text[:cap] + (
        f"\n[… {len(text) - cap} more chars not shown]" if len(text) > cap else ""
    )
    return f"=== {sid}: {s.title} ({s.publisher}, {s.published or 'undated'}) {s.url}\n{clipped}\n"


def _num(s: str) -> float | None:
    m = re.search(r"-?\d[\d,]*\.?\d*", (s or "").replace("−", "-"))
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", ""))
    except ValueError:
        return None


def _pct(part, whole):
    if part is None or not whole:
        return None
    return max(0, min(100, int(round(100 * part / whole))))


def stat_row(st, source_fetched: str) -> dict:
    """A draft stat with every presentation number derived from the values."""
    fill = None
    if st.viz in ("bar", "radial") and "%" in st.unit:
        fill = _pct(_num(st.value), 100)
    series = []
    if st.viz in ("ranked", "sparkline"):
        vals = [_num(r.value) for r in st.series]
        top = max((v for v in vals if v is not None), default=None)
        series = [
            {
                "label": r.label,
                "value": r.value,
                "pct": _pct(v, top),
                "highlight": r.highlight,
            }
            for r, v in zip(st.series, vals)
        ]
    range_at = None
    if st.viz == "range":
        lo, hi, v = _num(st.range_min), _num(st.range_max), _num(st.value)
        if None not in (lo, hi, v) and hi != lo:
            range_at = _pct(v - lo, hi - lo)
    return {
        "label": st.label,
        "value": st.value,
        "unit": st.unit,
        "viz": st.viz,
        "wide": st.wide,
        "fill_pct": fill,
        "series": series,
        "range_min": st.range_min,
        "range_max": st.range_max,
        "range_at": range_at,
        "note": st.note,
        "detail": st.detail,
        "source_label": st.source_label,
        "source_url": st.source_url,
        "source_published": st.source_published,
        "source_accessed": source_fetched,
    }


async def _run(topic: TopicDir):
    doc = topic.load_topic()
    ev = topic.load_evidence()
    m = Map.model_validate(ev["map"])
    store = Store(topic)
    title, scope = doc["title"], doc["scope"]
    facts = _facts(m)

    # stat writers, one per source
    by_source: dict[str, list] = {}
    for i, e in enumerate(m.stat_list):
        f = m.agreed_facts[e.from_fact]
        by_source.setdefault(f.source, []).append(
            {
                "index": i,
                "label": e.label,
                "viz": e.viz,
                "wide": e.wide,
                "fact": f.statement,
                "quote": f.quote,
            }
        )
    stat_units = []
    for sid, entries in by_source.items():
        s = store.get(sid)
        system, prompt = assemble(
            "stage1/stat_writer",
            title=title,
            source={
                "id": sid,
                "title": s.title,
                "publisher": s.publisher,
                "published": s.published,
                "url": s.url,
            },
            entries=entries,
            text=store.text(sid)[:80_000],
        )
        stat_units.append(
            Unit(
                name=f"stats-{sid}",
                phase=PHASE,
                model="sonnet",
                effort="low",
                system=system,
                prompt=prompt,
                output=StatWriterReturn,
                max_turns=3,
            )
        )

    # questions
    polls = [f for f in facts if POLL.search(f["statement"] + " " + f["quote"])]
    system, prompt = assemble(
        "stage1/questions",
        title=title,
        scope=scope,
        statements=[
            {"index": i, **cs.model_dump()}
            for i, cs in enumerate(m.controversial_statements)
        ],
        dimensions=[d.model_dump() for d in m.dimensions],
        facts=facts,
        polls=polls or "(none: lean_pct_a is null on every question)",
    )
    q_unit = Unit(
        name="questions",
        phase=PHASE,
        model="opus",
        effort="medium",
        system=system,
        prompt=prompt,
        output=QuestionsReturn,
        max_turns=3,
    )

    # position writers, one per camp, blind to the other camps
    pos_units = []
    for c in sorted(m.camps, key=lambda c: c.rank):
        blocks, used = [], 0
        for sid in c.sources:
            if sid not in store.index()["sources"]:
                continue
            b = _source_block(
                store, sid, min(SOURCE_TEXT_CAP, POSITION_SOURCES_CAP - used)
            )
            blocks.append(b)
            used += len(b)
            if used >= POSITION_SOURCES_CAP:
                break
        system, prompt = assemble(
            "stage1/position",
            title=title,
            scope=scope,
            camp=c.model_dump(),
            facts=facts,
            sources="\n".join(blocks)
            or "(no source text available; write from the adherent quotes and agreed facts)",
        )
        pos_units.append(
            Unit(
                name=f"position-{c.key}",
                phase=PHASE,
                model="opus",
                effort="medium",
                system=system,
                prompt=prompt,
                output=PositionReturn,
                max_turns=3,
            )
        )

    stat_returns = await run_units(topic, stat_units, parallel=4)
    over_all = []
    questions, over = await run_bounded(topic, q_unit, "questions")
    over_all += over
    sem = asyncio.Semaphore(4)

    async def one(u):
        async with sem:
            return await run_bounded(topic, u, "position")

    positions = []
    for p, over in await asyncio.gather(*(one(u) for u in pos_units)):
        positions.append(p)
        over_all += over
    camps = sorted(m.camps, key=lambda c: c.rank)

    # crux, after positions and questions
    system, prompt = assemble(
        "stage1/crux",
        title=title,
        scope=scope,
        positions=[
            {
                "key": c.key,
                "name": p.name,
                "steelman": p.steelman,
                "description": p.description,
            }
            for c, p in zip(camps, positions)
        ],
        questions=[
            {"text": q.text, "kind": q.kind, "why": q.why} for q in questions.questions
        ],
        facts=facts,
    )
    crux, over = await run_bounded(
        topic,
        Unit(
            name="crux",
            phase=PHASE,
            model="opus",
            effort="high",
            system=system,
            prompt=prompt,
            output=CruxReturn,
            max_turns=3,
        ),
        "crux",
    )
    over_all += over

    # overview and actions, last
    explainers = topic.read_return("A", "scout-explainer-1") or {}
    system, prompt = assemble(
        "stage1/overview_actions",
        title=title,
        scope=scope,
        map={
            "camps": [{"key": c.key, "name": c.name, "wants": c.wants} for c in camps],
            "affected": m.affected,
        },
        explainers=explainers.get("output", {}),
    )
    ova: OverviewActionsReturn = await run_unit(
        topic,
        Unit(
            name="overview-actions",
            phase=PHASE,
            model="sonnet",
            effort="medium",
            system=system,
            prompt=prompt,
            output=OverviewActionsReturn,
            tools=[FETCH_TOOL_NAME],
            mcp={"sources": fetch_tool(store, "act", "reference")},
            max_turns=40,
        ),
    )

    merge(topic, m, stat_returns, questions, positions, crux, ova)
    ev = topic.load_evidence()
    ev["over_ceiling"] = over_all
    topic.save_evidence(ev)


def merge(topic, m: Map, stat_returns, questions, positions, crux, ova):
    store = Store(topic)
    camps = sorted(m.camps, key=lambda c: c.rank)
    stats = []
    stat_claims = []
    # stats in stat_list order; a tile the writer could not source is absent
    by_label = {}
    for sr, sid in zip(stat_returns, [s for s in _stat_sources(m)]):
        for st in sr.stats:
            by_label[st.label.strip().lower()] = (st, sid)
    for e in m.stat_list:
        hit = by_label.get(e.label.strip().lower())
        if not hit:
            continue
        st, sid = hit
        stats.append(stat_row(st, store.get(sid).fetched))
        stat_claims.append(
            {
                "section": "basics",
                "item": "",
                "field": "note",
                "label": st.label,
                "quote": st.note,
                "claim": f"{st.label}: {st.value} {st.unit}".strip(),
                "kind": "fact",
                "source": sid,
                "source_quote": st.quote,
            }
        )
    name_of = {c.key: p.name for c, p in zip(camps, positions)}
    draft = {
        "volatility": ova.volatility,
        "overview": ova.overview.model_dump(),
        "basics": {"stats": stats},
        "questions": [
            {
                "text": q.text,
                "kind": q.kind,
                "why": q.why,
                "detail": q.detail,
                "lean_label_a": q.lean_label_a,
                "lean_label_b": q.lean_label_b,
                "lean_pct_a": q.lean_pct_a,
                "votes": 0,
            }
            for q in questions.questions
        ],
        "positions": [
            {
                "name": p.name,
                "steelman": p.steelman,
                "description": p.description,
                "detail": p.detail,
                "representative_name": p.representative_name,
                "representative_note": p.representative_note,
                "proponents": p.proponents,
            }
            for p in positions
        ],
        "crux": {
            "lead": crux.lead,
            "lead_highlight": crux.lead_highlight,
            "subtitle": crux.subtitle,
            "empirical": crux.empirical,
            "values": crux.values,
        },
        "actions": [
            {
                "kind": a.kind,
                "title": a.title,
                "description": a.description,
                "url": a.url,
                "for_position": name_of.get(a.for_position) or None,
            }
            for a in ova.actions
        ],
    }
    doc = topic.load_topic()
    doc["draft"] = draft
    topic.save_topic(doc)  # assigns ids
    draft = topic.load_topic()["draft"]

    id_of = {c["label"].strip().lower(): c["id"] for c in draft["basics"]["stats"]}
    for s in stat_claims:
        s["item"] = id_of[s.pop("label").strip().lower()]
    for sr in stat_returns:
        for c in sr.claims:
            item = id_of.get(c.item.strip().lower())
            if item:
                stat_claims.append(dict(c.model_dump(), section="basics", item=item))
    sidecars = {
        "basics": stat_claims,
        "questions": [
            dict(c.model_dump(), section="questions") for c in questions.claims
        ],
        "positions": [
            dict(c.model_dump(), section="positions", item=item["id"])
            for p, item in zip(positions, draft["positions"])
            for c in p.claims
        ],
        "crux": [dict(c.model_dump(), section="crux") for c in crux.claims],
        "overview": [dict(c.model_dump(), section="overview") for c in ova.claims],
        "actions": [
            {
                "section": "actions",
                "item": item["id"],
                "field": "url",
                "quote": item["title"],
                "claim": f"{item['url']} resolves",
                "kind": "fact",
                "source": a.source,
                "source_quote": "",
            }
            for a, item in zip(ova.actions, draft["actions"])
        ],
    }
    ev = topic.load_evidence()
    ev["sidecars"] = sidecars
    ev["crux_placement"] = {
        "crux": crux.lead,
        "placement": [p.model_dump() for p in crux.placement],
    }
    ev["sources"] = store.index()["sources"]
    topic.save_evidence(ev)


def _stat_sources(m: Map):
    seen = []
    for e in m.stat_list:
        sid = m.agreed_facts[e.from_fact].source
        if sid not in seen:
            seen.append(sid)
    return seen


def run_phase(topic: TopicDir):
    run(_run(topic))
    if not done(topic):
        raise CriteriaFailure(
            "phase B merged but the draft is missing a section", "stage1"
        )
