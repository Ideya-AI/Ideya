"""The shapes every stage shares (PIPELINE.md, "The shapes the units share").

Pydantic on purpose: one class both emits the JSON schema a unit's structured
output is constrained to and validates the return file on read, so the schema
and the check cannot drift. Stage-specific shapes (scout return, map, editor
returns) live with their stage and subclass `Shape`.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Shape(BaseModel):
    """Closed shapes: a unit may not add fields the schema does not name."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    @classmethod
    def output_format(cls) -> dict:
        """The `output_format` option for an SDK call returning this shape."""
        return {"type": "json_schema", "schema": cls.model_json_schema(by_alias=True)}


SourceClass = Literal["reference", "explainer", "camp", "official", "critique"]


class Source(Shape):
    """One entry in the sources store index."""

    id: str
    url: str
    title: str = ""
    publisher: str = ""
    published: str = ""
    fetched: str
    status: int
    class_: SourceClass = Field(alias="class")
    raw: str
    text: str
    text_chars: int


ClaimKind = Literal["fact", "inference"]
ClaimVerdict = Literal["supported", "partial", "unsupported", "attributed", "cut"]


class Claim(Shape):
    """A ledger claim. The sidecar a writer attaches is this minus `verdict`."""

    id: str = ""
    section: str = ""
    item: str = ""
    field: str
    quote: str
    claim: str
    kind: ClaimKind
    source: str
    source_quote: str
    verdict: ClaimVerdict | None = None
    note: str = ""


class Sidecar(Shape):
    """What a writing unit attaches: every hard claim in its prose."""

    claims: list[Claim] = []
