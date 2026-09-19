"""The sources store and the in-process fetch tool (PIPELINE.md §11, stage 1
"How units interact").

A unit that must ground a claim calls `fetch_source(url)`. Code does the fetch:
raw bytes to disk, text by a deterministic extractor (HTML via trafilatura, PDF
via pypdf), an index entry, and the rule that decides what counts as fetched:

    "Fetched" means extracted text over a floor length with a 200 status.

A bot wall, a paywall stub or a JS shell is not a source, and the agent is told
so and can try another URL. Agents never write the store, so a unit cannot
cite a source that was not fetched.

Layout under the topic directory:

    run/sources/index.json      id -> Source (shapes.Source), plus "failed"
    run/sources/<id>.raw        the bytes as served
    run/sources/<id>.txt        the extracted text

Ids are namespaced by the unit that fetched them (`s-crit-03`), so parallel
units never collide.
"""

import datetime
import io
import json
import logging
import re
from urllib.parse import urlsplit, urlunsplit

import httpx
import trafilatura
from claude_agent_sdk import ToolAnnotations, create_sdk_mcp_server, tool

from .shapes import Source
from .topic import TopicDir, read_json, write_json

logging.getLogger("pypdf").setLevel(logging.ERROR)

TEXT_FLOOR = 1200  # chars of extracted text below which a page is not a source
MAX_BYTES = 20 * 1024 * 1024
TIMEOUT = 30.0
RETURN_CAP = 60_000  # chars of text handed back to the agent in one call
UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/128.0 Safari/537.36"
)
HEADERS = {"User-Agent": UA, "Accept": "text/html,application/pdf,*/*;q=0.8"}


def canonical(url: str) -> str:
    """One id per page: scheme and host lowercased, fragment dropped, trailing
    slash trimmed."""
    p = urlsplit(url.strip())
    path = p.path.rstrip("/") or "/"
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), path, p.query, ""))


def extract(content_type: str, raw: bytes, url: str) -> dict:
    """{title, text, publisher, published} from a fetched body, deterministically."""
    if "pdf" in content_type or raw[:5] == b"%PDF-":
        from pypdf import PdfReader

        reader = PdfReader(io.BytesIO(raw))
        text = "\n\n".join((p.extract_text() or "") for p in reader.pages)
        title = (reader.metadata or {}).get("/Title", "") or ""
        return {
            "title": str(title),
            "text": text.strip(),
            "publisher": "",
            "published": "",
        }
    html = raw.decode("utf-8", errors="replace")
    meta = trafilatura.extract_metadata(html, default_url=url)
    text = (
        trafilatura.extract(
            html,
            url=url,
            include_comments=False,
            include_tables=True,
            favor_recall=True,
        )
        or ""
    )
    title = (meta.title if meta else "") or ""
    if not title:
        m = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
        title = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
    return {
        "title": title,
        "text": text.strip(),
        "publisher": (meta.sitename if meta else "") or "",
        "published": "" if "wikipedia.org" in url else ((meta.date if meta else "") or ""),
    }


def resolve_url(url: str) -> tuple[bool, int]:
    """Does the URL answer 2xx. Used wherever a URL is written into the product."""
    try:
        with httpx.Client(follow_redirects=True, timeout=TIMEOUT, headers=HEADERS) as c:
            r = c.head(url)
            if r.status_code in (403, 405, 501):
                r = c.get(url)
            return 200 <= r.status_code < 300, r.status_code
    except httpx.HTTPError:
        return False, 0


class Store:
    def __init__(self, topic: TopicDir):
        self.dir = topic.run_dir / "sources"
        self.index_path = self.dir / "index.json"

    def index(self) -> dict:
        return read_json(self.index_path, {"sources": {}, "failed": []}) or {
            "sources": {},
            "failed": [],
        }

    def _save(self, idx: dict):
        write_json(self.index_path, idx)

    def sources(self) -> dict[str, Source]:
        return {k: Source.model_validate(v) for k, v in self.index()["sources"].items()}

    def get(self, sid: str) -> Source:
        return Source.model_validate(self.index()["sources"][sid])

    def text(self, sid: str) -> str:
        return (self.dir / f"{sid}.txt").read_text(encoding="utf-8")

    def by_url(self, url: str) -> Source | None:
        c = canonical(url)
        for v in self.index()["sources"].values():
            if canonical(v["url"]) == c:
                return Source.model_validate(v)
        return None

    def _next_id(self, idx: dict, ns: str) -> str:
        n = sum(1 for k in idx["sources"] if k.startswith(f"s-{ns}-")) + 1
        return f"s-{ns}-{n:02d}"

    def fetch(self, url: str, ns: str, cls: str) -> Source | dict:
        """A Source on success, else {"error": …, "status": …}. Refetching a URL
        already in the store returns the existing entry."""
        have = self.by_url(url)
        if have:
            return have
        try:
            with httpx.Client(
                follow_redirects=True, timeout=TIMEOUT, headers=HEADERS
            ) as c:
                r = c.get(url)
        except httpx.HTTPError as e:
            return self._fail(url, 0, f"fetch failed: {type(e).__name__}")
        if r.status_code in (401, 403, 429, 503) and "web.archive.org" not in url:
            # a bot wall; the Wayback Machine's copy of the page is the same text
            try:
                with httpx.Client(
                    follow_redirects=True, timeout=TIMEOUT, headers=HEADERS
                ) as c:
                    r2 = c.get(f"https://web.archive.org/web/2/{url}")
                if r2.status_code == 200:
                    r = r2
            except httpx.HTTPError:
                pass
        if r.status_code != 200:
            return self._fail(url, r.status_code, f"HTTP {r.status_code}")
        raw = r.content[:MAX_BYTES]
        ext = extract(r.headers.get("content-type", ""), raw, str(r.url))
        if len(ext["text"]) < TEXT_FLOOR:
            return self._fail(
                url,
                200,
                f"only {len(ext['text'])} chars of text extracted (floor {TEXT_FLOOR}); "
                "likely a bot wall, paywall stub or JS shell",
            )
        idx = self.index()
        sid = self._next_id(idx, ns)
        self.dir.mkdir(parents=True, exist_ok=True)
        (self.dir / f"{sid}.raw").write_bytes(raw)
        (self.dir / f"{sid}.txt").write_text(ext["text"], encoding="utf-8")
        src = Source(
            id=sid,
            url=str(r.url),
            title=ext["title"],
            publisher=ext["publisher"],
            published=ext["published"],
            fetched=datetime.date.today().isoformat(),
            status=200,
            **{"class": cls},
            raw=f"run/sources/{sid}.raw",
            text=f"run/sources/{sid}.txt",
            text_chars=len(ext["text"]),
        )
        idx["sources"][sid] = src.model_dump(by_alias=True)
        self._save(idx)
        return src

    def _fail(self, url, status, error):
        idx = self.index()
        idx["failed"].append({"url": url, "status": status, "error": error})
        self._save(idx)
        return {"error": error, "status": status}


CLASSES = ("reference", "explainer", "camp", "official", "critique")


def fetch_tool(store: Store, ns: str, cls: str | None):
    """The `fetch_source` tool bound to one unit's namespace, as an in-process
    MCP server. With `cls` the class is fixed; with None the agent names the
    class of each page it fetches (the gap scout crosses classes). Allow it
    in a unit as `mcp__sources__fetch_source`."""

    @tool(
        "fetch_source",
        "Fetch a web page or PDF into the sources store and return its extracted "
        "text with a source id. Only a source fetched this way may be cited. "
        "A page that returns no usable text is not a source; try another URL."
        + ("" if cls else " Name the page's class: reference (encyclopedias, reference sites), "
           "explainer (journalism), official (agencies, statistical bodies), camp (an "
           "organization's or person's own statement of a view), critique (a document arguing "
           "against a position)."),
        {"url": str} if cls else {"url": str, "class": str},
        # Claude Code persists a large tool result to a file and shows the agent
        # a 2KB preview unless the tool raises this ceiling. A scout that sees a
        # preview quotes from memory, which the map check then rejects.
        annotations=ToolAnnotations(readOnlyHint=True, maxResultSizeChars=RETURN_CAP + 4_000),
    )
    async def fetch_source(args):
        c = cls or (args.get("class") if args.get("class") in CLASSES else "explainer")
        res = store.fetch(args["url"], ns, c)
        if isinstance(res, dict):
            body = f"NOT A SOURCE: {res['error']}\nurl: {args['url']}"
        else:
            text = store.text(res.id)
            clipped = text[:RETURN_CAP]
            more = (
                f"\n[… {len(text) - RETURN_CAP} more chars not shown]"
                if len(text) > RETURN_CAP
                else ""
            )
            body = (
                f"source id: {res.id}\nurl: {res.url}\ntitle: {res.title}\n"
                f"publisher: {res.publisher}\npublished: {res.published}\n"
                f"chars: {res.text_chars}\n\n{clipped}{more}"
            )
        return {"content": [{"type": "text", "text": body}]}

    return create_sdk_mcp_server("sources", tools=[fetch_source])


FETCH_TOOL_NAME = "mcp__sources__fetch_source"


def merge_into_evidence(topic: TopicDir):
    """Copy the store index into `evidence.json` under `sources`, so the
    durable record names every page a stage fetched (§7: evidence is not
    process)."""
    ev = topic.load_evidence()
    ev["sources"] = Store(topic).index()["sources"]
    topic.save_evidence(ev)
    return ev


def dump_index(topic: TopicDir) -> str:
    return json.dumps(Store(topic).index(), ensure_ascii=False, indent=1)
