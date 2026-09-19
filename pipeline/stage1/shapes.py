"""Stage 1's unit return shapes (PIPELINE.md, stage 1, "The shapes the units share").

Every unit returns one of these; the runner constrains the call to its schema
and validates the return. Retrieval units return structure, writing units
return content plus a sidecar of hard claims, checking units return verdicts.
"""

from typing import Literal

from pydantic import Field

from ..shapes import Claim, Shape, SourceClass

# -- Phase A: the map -----------------------------------------------------


class Dimension(Shape):
    axis: str
    poles: list[str]


class SeedSource(Shape):
    url: str
    why: str


class FramerReturn(Shape):
    dimensions: list[Dimension]
    affected: list[str] = Field(description="populations materially affected")
    frame_question: str = Field(
        description="how a camp might reject the question as posed"
    )
    seed_sources: list[SeedSource] = Field(
        description="the Wikipedia article and two or three landmark explainers"
    )
    search_terms: list[str]


class Claimant(Shape):
    name: str
    org: str = ""
    kind: Literal["institution", "person"]
    claim: str = Field(description="verbatim sentence from the fetched source")
    source: str = Field(description="source id from fetch_source")
    date: str = ""
    argues_against: list[str] = Field(
        default_factory=list,
        description="everyone this document argues against, by name",
    )


class Fact(Shape):
    statement: str
    quote: str = Field(description="verbatim from the fetched source")
    source: str


class ScoutReturn(Shape):
    claimants: list[Claimant]
    facts: list[Fact]
    notes: str = ""


class Adherent(Shape):
    name: str
    org: str = ""
    kind: Literal["institution", "person"]
    quote: str
    source: str


class Camp(Shape):
    key: str = Field(description="short lowercase slug, stable across revisions")
    name: str
    wants: str = Field(description="one sentence, in the affirmative")
    distinguishing: str = Field(
        description="a proposition this camp affirms and another denies"
    )
    rank: int
    rank_reason: str
    adherents: list[Adherent]
    sources: list[str]
    variation: str = Field(
        default="",
        description="secondary-aspect differences merged here, recorded, not split",
    )


class AgreedFact(Shape):
    statement: str
    quote: str
    source: str
    cited_by_camps: list[str] = Field(default_factory=list)


class StatEntry(Shape):
    label: str = Field(description="the metric, not a sentence; at most 60 characters")
    viz: Literal["bar", "radial", "ranked", "range", "sparkline"]
    from_fact: int = Field(description="index into agreed_facts")
    wide: bool = False


class ControversialStatement(Shape):
    statement: str
    held_by: list[str] = Field(description="camp keys")
    denied_by: list[str] = Field(description="camp keys")


GapKind = Literal["second_adherent", "affected_unvoiced", "single_source", "empty_cell"]


class Gap(Shape):
    kind: GapKind
    about: str
    filled: bool = False


class FrameRejection(Shape):
    exists: bool
    note: str = ""


class Map(Shape):
    dimensions: list[Dimension]
    affected: list[str]
    frame_rejection: FrameRejection
    camps: list[Camp]
    agreed_facts: list[AgreedFact]
    stat_list: list[StatEntry]
    controversial_statements: list[ControversialStatement]
    gaps: list[Gap]


# -- Phase B: the sections ------------------------------------------------


class SeriesRow(Shape):
    label: str
    value: str
    highlight: bool = False


class StatOut(Shape):
    label: str
    value: str = Field(
        default="",
        description="headline number as displayed, at most 24 characters; empty for ranked",
    )
    unit: str = Field(
        default="",
        description="display token, e.g. %, TWh, per year; at most 24 characters",
    )
    viz: Literal["bar", "radial", "ranked", "range", "sparkline"]
    wide: bool = False
    series: list[SeriesRow] = Field(
        default_factory=list, description="ranked or sparkline rows, in display order"
    )
    range_min: str = ""
    range_max: str = ""
    note: str = Field(description="one or two sentences under the number")
    detail: str = Field(description="the expanded explanation")
    source_label: str
    source_url: str
    source_published: str = ""
    quote: str = Field(
        description="verbatim from the source text, containing the value"
    )


class StatWriterReturn(Shape):
    stats: list[StatOut]
    claims: list[Claim] = Field(default_factory=list, description="every hard claim in the notes and details, item = the tile's label")


class QuestionOut(Shape):
    text: str
    kind: Literal["empirical", "value"]
    why: str = Field(description="why it is contested, one or two sentences")
    detail: str
    lean_label_a: str = ""
    lean_label_b: str = ""
    lean_pct_a: int | None = None
    from_statement: int = Field(description="index into controversial_statements")


class QuestionsReturn(Shape):
    questions: list[QuestionOut]
    claims: list[Claim]


class PositionReturn(Shape):
    name: str
    steelman: str
    description: str
    detail: str
    representative_name: str = ""
    representative_note: str = ""
    proponents: str = ""
    claims: list[Claim]


class Placement(Shape):
    camp: str
    side: Literal["empirical", "values", "both"]
    note: str


class CruxReturn(Shape):
    lead: str
    lead_highlight: str
    subtitle: str
    empirical: str
    values: str
    placement: list[Placement]
    claims: list[Claim]


class Overview(Shape):
    summary: str
    scope_covered: str
    scope_excluded: str
    why_now: str


class ActionOut(Shape):
    kind: Literal["learn_more", "donate", "volunteer", "policy", "local"]
    title: str
    description: str
    url: str
    for_position: str = Field(
        default="",
        description="camp key when the action belongs to one side, else empty",
    )
    source: str = Field(description="source id from fetch_source for this URL")


class OverviewActionsReturn(Shape):
    overview: Overview
    volatility: Literal["fast", "medium", "slow"]
    actions: list[ActionOut]
    claims: list[Claim]


# -- Phase C: the ledger and the checks -----------------------------------


class ExtractorReturn(Shape):
    claims: list[Claim]


class Verdict(Shape):
    claim: str = Field(description="claim id")
    verdict: Literal["supported", "partial", "unsupported", "attributed"]
    note: str = ""


class VerifierReturn(Shape):
    verdicts: list[Verdict]


class RepairReturn(Shape):
    move: Literal["cut", "soften", "attribute"]
    text: str = Field(description="the whole field, rewritten")
    claims: list[Claim] = Field(
        default_factory=list,
        description="hard claims in the new text that were not in the ledger",
    )
