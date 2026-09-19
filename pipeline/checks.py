"""Code checks shared by stages: quote matching and lint (PIPELINE.md §11, stage 1
"Lint", stage 2 "Satisfied when").

Lint is a phrase list on purpose: it is cheap, it cannot be anchored the way a
prompt prohibition can, and a defect is a fact about the text rather than a
model's opinion. Stages extend the lists; nothing here judges quality.
"""

import re
import unicodedata
from dataclasses import dataclass

# -- normalised quote match ------------------------------------------------

_QUOTES = {
    "‘": "'",
    "’": "'",
    "‚": "'",
    "‛": "'",
    "“": '"',
    "”": '"',
    "„": '"',
    "‟": '"',
    "‐": "-",
    "‑": "-",
    "‒": "-",
    "–": "-",
    "—": "-",
    "−": "-",
    " ": " ",
}
_STRIP = re.compile(r"[^\w\s]")
_WS = re.compile(r"\s+")


def normalize(text: str) -> str:
    """Case, whitespace, quote style and punctuation folded away, so a quote
    survives smart-quote and hyphenation differences between the draft and a
    page's extracted text."""
    text = unicodedata.normalize("NFKC", text or "")
    text = "".join(_QUOTES.get(c, c) for c in text)
    text = _STRIP.sub(" ", text.lower())
    return _WS.sub(" ", text).strip()


def quote_in_text(quote: str, text: str) -> bool:
    q = normalize(quote)
    return bool(q) and q in normalize(text)


NEAR_SHINGLE = 6
NEAR_PREFIX = 12  # a quote whose first twelve words are contiguous in the text is from the text
NEAR_SHARE = 0.6  # a page number or footnote spliced into a PDF sentence breaks a few shingles


def quote_match(quote: str, text: str) -> str:
    """"exact" when the normalised quote is a substring of the normalised text;
    "near" when at least 80% of its six-word shingles are, which is a quote
    copied through two units with an ellipsis or a dropped word; else "none"."""
    q, t = normalize(quote), normalize(text)
    if not q:
        return "none"
    if q in t:
        return "exact"
    words = q.split()
    if len(words) >= NEAR_PREFIX and " ".join(words[:NEAR_PREFIX]) in t:
        return "near"
    if len(words) < NEAR_SHINGLE:
        return "none"
    shingles = [" ".join(words[i : i + NEAR_SHINGLE]) for i in range(len(words) - NEAR_SHINGLE + 1)]
    hits = sum(1 for s in shingles if s in t)
    return "near" if hits / len(shingles) >= NEAR_SHARE else "none"


# -- lint ------------------------------------------------------------------


@dataclass
class Defect:
    where: str
    rule: str
    detail: str

    def __str__(self):
        return f"{self.where}: {self.rule} ({self.detail})"


HTML_ENTITY = re.compile(r"&(#\d+|#x[0-9a-f]+|[a-z]+);", re.I)
MARKUP = re.compile(r"(\*\*|__|^#{1,6}\s|</?[a-z][^>]*>|\[[^\]]+\]\([^)]+\))", re.M)
STRAIGHT_QUOTE = re.compile(r"[\"']")

# CLAUDE.md: US spelling except inside proper nouns. A modest list of the
# spellings that actually appear in drafts; extend as they turn up.
US_FIX = {
    "colour": "color", "colours": "colors", "behaviour": "behavior", "behaviours": "behaviors",
    "organisation": "organization", "organisations": "organizations", "organise": "organize",
    "organised": "organized", "favour": "favor", "favours": "favors", "favourable": "favorable",
    "labour": "labor", "centre": "center", "centres": "centers", "defence": "defense",
    "licence": "license", "licences": "licenses", "programme": "program", "programmes": "programs",
    "analyse": "analyze", "analysed": "analyzed", "recognise": "recognize", "recognised": "recognized",
    "realise": "realize", "realised": "realized", "prioritise": "prioritize", "prioritised": "prioritized",
    "travelling": "traveling", "modelling": "modeling", "catalogue": "catalog", "ageing": "aging",
    "judgement": "judgment", "sceptic": "skeptic", "sceptical": "skeptical", "sceptics": "skeptics",
    "grey": "gray", "kilometre": "kilometer", "kilometres": "kilometers", "litre": "liter",
    "litres": "liters", "metre": "meter", "metres": "meters", "fibre": "fiber", "theatre": "theater",
    "tyre": "tire", "tyres": "tires", "cheque": "check", "mould": "mold", "plough": "plow",
    "aluminium": "aluminum", "paediatric": "pediatric", "foetus": "fetus", "oestrogen": "estrogen",
    "haemorrhage": "hemorrhage", "anaemia": "anemia", "sulphur": "sulfur", "kerb": "curb",
    "neighbour": "neighbor", "neighbours": "neighbors", "honour": "honor", "harbour": "harbor",
    "artefact": "artifact", "artefacts": "artifacts", "authorise": "authorize", "authorised": "authorized",
    "subsidise": "subsidize", "subsidised": "subsidized", "minimise": "minimize", "maximise": "maximize",
    "emphasise": "emphasize", "emphasised": "emphasized", "criticise": "criticize", "criticised": "criticized",
}
# Lowercase forms only: a capitalized one is likely a proper noun, which keeps its spelling.
UK_SPELLINGS = re.compile(r"\b(" + "|".join(sorted(US_FIX, key=len, reverse=True)) + r")\b")

# The page's own voice hedging (stage 1 lint list). Inside a position these
# are the writer stepping outside the camp's voice.
HEDGES = [
    "the argument goes",
    "from this view",
    "from this perspective",
    "some would say",
    "it could be argued",
    "one could argue",
]
# In the page's own voice these attribute; inside a position they are the
# writer stepping outside the camp, so they lint only there.
POSITION_HEDGES = [
    "proponents argue",
    "proponents claim",
    "supporters argue",
    "adherents argue",
    "adherents hold",
    "the camp argues",
    "this camp argues",
]

# Self-rebuttal inside a position: the camp arguing against itself.
SELF_REBUTTAL = [
    re.compile(r"\bcritics (counter|note|point out|argue|respond|say)\b", re.I),
    re.compile(r"\bopponents (counter|note|point out|argue|respond|say)\b", re.I),
    re.compile(r"\bbut\b[^.]{0,80}\bis real too\b", re.I),
    re.compile(r"\bto be fair\b", re.I),
    re.compile(r"\bon the other hand\b", re.I),
    re.compile(r"\bthat said\b", re.I),
    re.compile(r"\badmittedly\b", re.I),
]

# Posture labels are not camp names (stage 1, "Camps are named by what they want").
POSTURE_LABELS = re.compile(
    r"\b(skeptic|skeptics|sceptic|realist|realists|pragmatist|pragmatists|alarmist|alarmists|"
    r"advocate|advocates|optimist|optimists|pessimist|pessimists|moderate|moderates|"
    r"hardliner|hardliners|purist|purists|denier|deniers|doomer|doomers|booster|boosters)\b",
    re.I,
)


def lint_text(text: str, where: str) -> list[Defect]:
    """The plain-text invariants every content field must meet."""
    out = []
    if not isinstance(text, str):
        return out
    if HTML_ENTITY.search(text):
        out.append(Defect(where, "html-entity", HTML_ENTITY.search(text).group(0)))
    if MARKUP.search(text):
        out.append(Defect(where, "markup", MARKUP.search(text).group(0)))
    if STRAIGHT_QUOTE.search(text):
        out.append(Defect(where, "straight-quote", "use typographic quotes"))
    m = UK_SPELLINGS.search(text)
    if m:
        out.append(Defect(where, "uk-spelling", m.group(0)))
    low = text.lower()
    for h in HEDGES:
        if h in low:
            out.append(Defect(where, "hedge", h))
    return out


def lint_position_text(text: str, where: str) -> list[Defect]:
    out = lint_text(text, where)
    low = (text or "").lower()
    for h in POSITION_HEDGES:
        if h in low:
            out.append(Defect(where, "hedge", h))
    for pat in SELF_REBUTTAL:
        m = pat.search(text or "")
        if m:
            out.append(Defect(where, "self-rebuttal", m.group(0)))
    return out


def lint_camp_name(name: str, where: str) -> list[Defect]:
    m = POSTURE_LABELS.search(name or "")
    return [Defect(where, "posture-label", m.group(0))] if m else []


def walk_strings(doc, prefix=""):
    """Every string leaf in a nested dict/list, with its dotted path."""
    if isinstance(doc, dict):
        for k, v in doc.items():
            yield from walk_strings(v, f"{prefix}.{k}" if prefix else k)
    elif isinstance(doc, list):
        for i, v in enumerate(doc):
            yield from walk_strings(v, f"{prefix}[{i}]")
    elif isinstance(doc, str):
        yield prefix, doc


# Fields that are not prose and so are exempt from the plain-text rules.
NOT_PROSE = re.compile(
    r"(^|\.)(id|url|source_url|kind|viz|color_key|icon|for_position|key|source)$"
)


def lint_draft(draft: dict) -> list[Defect]:
    """Lint every prose field of a draft, positions under the stricter rules."""
    out = []
    for path, text in walk_strings(draft):
        if NOT_PROSE.search(path):
            continue
        if path.startswith("positions"):
            out += lint_position_text(text, path)
            if path.endswith(".name"):
                out += lint_camp_name(text, path)
        else:
            out += lint_text(text, path)
    return out


# -- mechanical tidy --------------------------------------------------------

_ENTITIES = {"&amp;": "&", "&quot;": '"', "&#39;": "'", "&apos;": "'", "&lt;": "<", "&gt;": ">", "&nbsp;": " "}


def tidy(text: str) -> str:
    """The plain-text fixes code can make safely: entities decoded, straight
    quotes made typographic. Everything else lint reports and a repairer fixes."""
    if not isinstance(text, str):
        return text
    for k, v in _ENTITIES.items():
        text = text.replace(k, v)
    text = UK_SPELLINGS.sub(lambda m: US_FIX[m.group(0)], text)
    text = re.sub(r"(?<=\w)'(?=\w)", "\u2019", text)  # apostrophe inside a word
    text = re.sub(r"(?<=\d)'", "\u2019", text)
    text = re.sub(r"'(?=\d)", "\u2019", text)  # ’90s
    text = re.sub(r"(^|[\s(\[])'", "\\1\u2018", text)
    text = text.replace("'", "\u2019")
    text = re.sub(r'(^|[\s(\[])"', "\\1\u201c", text)
    text = text.replace('"', "\u201d")
    return text


def tidy_draft(draft):
    """Apply `tidy` to every prose field in place."""
    if isinstance(draft, dict):
        for k, v in draft.items():
            if isinstance(v, str) and not NOT_PROSE.search(k):
                draft[k] = tidy(v)
            else:
                tidy_draft(v)
    elif isinstance(draft, list):
        for v in draft:
            tidy_draft(v)
    return draft
