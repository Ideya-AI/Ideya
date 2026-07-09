#!/usr/bin/env python3
"""Generate topic-icon candidates via the Gemini image API (Nano Banana).

Reads the fresh-generation prompt from a topic's icon brief
(research/icons/<slug>.md — the first blockquote under "## Generation prompt"),
requests N candidates, and saves them for side-by-side review. The model is
always pinned explicitly so we control exactly which image model runs.

Models (2026):
    gemini-3-pro-image            Nano Banana Pro — DEFAULT: hero art is a one-shot
                                  brand asset, and Pro adheres best to the style
                                  constraints (uniform stroke, fill opacity, no frame)
    gemini-3.1-flash-image        Nano Banana 2 — cheaper workhorse (~$0.067 @1K)
    gemini-3.1-flash-lite-image   Nano Banana 2 Lite — fastest/cheapest
    gemini-2.5-flash-image        Nano Banana (legacy)

Auth: GEMINI_API_KEY env var (also read from the repo .env). Create a key at
https://aistudio.google.com/apikey — never commit it.

Examples:
    python research/icons/generate_icons.py --slug universal-basic-income --n 4
    python research/icons/generate_icons.py --slug x --model gemini-3-pro-image --n 2
    python research/icons/generate_icons.py --slug x --dry-run
"""

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"


def api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        env = REPO / ".env"
        if env.exists():
            for line in env.read_text().splitlines():
                m = re.match(r"\s*GEMINI_API_KEY\s*=\s*(.+?)\s*$", line)
                if m:
                    key = m.group(1).strip().strip("'\"")
    if not key:
        sys.exit(
            "GEMINI_API_KEY not set (env or .env). "
            "Create one at https://aistudio.google.com/apikey"
        )
    return key


def prompt_from_brief(slug: str) -> str:
    """First blockquote block after the '## Generation prompt' heading."""
    brief = HERE / f"{slug}.md"
    if not brief.exists():
        sys.exit(f"No brief at {brief} — write the art brief first.")
    lines = brief.read_text().splitlines()
    try:
        start = next(
            i
            for i, l in enumerate(lines)
            if l.lower().startswith("## generation prompt")
        )
    except StopIteration:
        sys.exit(f"{brief} has no '## Generation prompt' section.")
    block: list[str] = []
    in_block = False
    for line in lines[start:]:
        if line.startswith(">"):
            in_block = True
            block.append(line.lstrip("> ").rstrip())
        elif in_block and line.strip() == "":
            block.append("")  # paragraph break inside the quote
        elif in_block:
            break
    prompt = "\n".join(block).strip()
    if not prompt:
        sys.exit(f"Could not extract a blockquote prompt from {brief}.")
    return prompt


def generate_one(key: str, model: str, prompt: str, size: str, aspect: str) -> bytes:
    body = {
        "model": model,
        "input": [{"type": "text", "text": prompt}],
        "response_format": {
            "type": "image",
            "mime_type": "image/jpeg",
            "aspect_ratio": aspect,
            "image_size": size,
        },
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body).encode(),
        headers={"x-goog-api-key": key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:600]
        sys.exit(f"API error {exc.code}: {detail}")

    # Interactions shape: the image lives in steps[type=model_output]
    # .content[type=image].data (base64).
    data = None
    for step in payload.get("steps", []):
        if step.get("type") != "model_output":
            continue
        for item in step.get("content", []):
            if item.get("type") == "image" and item.get("data"):
                data = item["data"]
                break
        if data:
            break
    if data is None:
        sys.exit(
            "No image data in response — API shape may have moved. Raw keys: "
            + ", ".join(payload.keys())
        )
    return base64.b64decode(data)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--slug", required=True, help="icon brief slug (research/icons/<slug>.md)"
    )
    ap.add_argument("--model", default="gemini-3-pro-image")
    ap.add_argument("--n", type=int, default=4, help="number of candidates (default 4)")
    ap.add_argument("--size", default="1K", choices=["0.5K", "1K", "2K", "4K"])
    ap.add_argument("--aspect", default="3:2", help="primaries are 3:2 wide (framing is normalized in post anyway)")
    ap.add_argument("--out-dir", default=str(HERE / "candidates"))
    ap.add_argument("--dry-run", action="store_true", help="print the prompt and exit")
    args = ap.parse_args()

    prompt = prompt_from_brief(args.slug)
    if args.dry_run:
        print(
            f"model: {args.model} · size {args.size} · aspect {args.aspect} · n={args.n}"
        )
        print("--- prompt ---")
        print(prompt)
        return

    key = api_key()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    # Never overwrite an earlier run — number on from the highest existing index.
    existing = [
        int(m.group(1))
        for p in out_dir.glob(f"{args.slug}.{args.model}.*.jpg")
        if (m := re.search(r"\.(\d+)\.jpg$", p.name))
    ]
    base = max(existing, default=0)
    for i in range(base + 1, base + args.n + 1):
        png = generate_one(key, args.model, prompt, args.size, args.aspect)
        path = out_dir / f"{args.slug}.{args.model}.{i}.jpg"
        path.write_bytes(png)
        print(f"[{i - base}/{args.n}] {path}  ({len(png) // 1024} KB)")
    print(
        f"\nReview the candidates in {out_dir}/ and promote the winner to "
        f"static/img/topics/{args.slug}.png (normalize + convert in post)"
    )


if __name__ == "__main__":
    main()
