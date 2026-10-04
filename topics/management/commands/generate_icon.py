"""Stage 3 tool: assemble the icon prompt, call Gemini, normalize the pick.

    manage.py generate_icon brief --slug <slug>
        Print the assembled prompt: the constant style template, the brief's
        Scene and Negatives, and the primary category's hex from tokens.css.

    manage.py generate_icon generate --slug <slug> --round 1 [--n 2] [--scene "..."]
    manage.py generate_icon generate --slug <slug> --round 2 --edit <png> --note "..."
        One round. Generate mode samples the assembled prompt (or an explicit
        --scene, so round 1 can try several scenes without rewriting the brief).
        Edit mode sends an incumbent image plus a rendering note. Candidates land
        in research/topics/<slug>/candidates/r<round>-<letter>.png; spend is
        appended to candidates/spend.json.

    manage.py generate_icon normalize --slug <slug> --src <candidate.png>
        Flatten onto white, trim to content, pad 8%, fit 1035x690 on white, save
        static/img/topics/<slug>.png and a 40px thumbnail beside the source.

The brief at research/topics/<slug>/icon.md supplies only the scene and the
subject's own negatives; the style lives in STYLE below so it cannot drift.
The style template and request shape come from the removed pipeline/icon_prompt.py
(commit 04c827e); the 1035x690 normalize from research/icons/postprocess_icon.py
(commit 51a9443). Both were read in full before being carried over.
"""

import base64
import fcntl
import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

ROOT = Path(settings.BASE_DIR)
TOKENS = ROOT / "static" / "css" / "tokens.css"
TOPICS = ROOT / "research" / "topics"
MODEL = "gemini-3-pro-image"
# USD per 1M tokens, Standard tier (ai.google.dev/gemini-api/docs/pricing, 2026-10-02).
# A 1K output image is 1120 tokens, so $0.134.
PRICE_INPUT, PRICE_TEXT_OUT, PRICE_IMAGE_OUT = 2.00, 12.00, 120.00
OUT_W, OUT_H = 1035, 690  # the committed primary-art size, 3:2
PAD_FRAC = 0.08
NEAR_WHITE = 244

STYLE = """\
A minimalist flat vector-style icon illustration, in a clean editorial line-art style: {scene}

Composition: one dominant focal mass with smaller supporting elements at clearly different scales (big, medium, small); at least one element overlaps another so the scene has depth; the ground is a gentle curve, never a flat line; one connective element runs across the frame to tie the pieces together. A single coherent scene, not a row of separate objects. Centered with generous, even padding.

Style: monoline line art with ONE uniform stroke weight on every element, including the thinnest wisps and lines. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small. No fussy internal detail.

Color: a single hue, two tones only. Draw all lines in solid {hex}, and give every major mass a clearly visible soft fill of the same hue at about 15-18% opacity, so the duotone is obviously present rather than white interiors. No other colors, no gradients, no shadows, no 3D, no texture.

Important: NO border, NO frame, NO box or outline around the scene, just the illustration on a plain white background. No text, letters, or numbers. No human figures or faces. Calm, neutral, editorial mood: show the subject plainly, neither celebrating nor warning.{negatives}"""

EDIT = (
    "Using this image, keep the same composition, elements, and layout, but make "
    "these changes: {note} Keep it flat, single hue, monoline with one uniform stroke "
    "weight, soft 15-18% fills on the masses, no border, no text, plain white background."
)


def _topic(slug):
    path = TOPICS / slug / "topic.json"
    if not path.exists():
        raise CommandError(f"no topic at {path}")
    return json.loads(path.read_text())


def hex_for(category):
    m = re.search(
        rf"--cat-{re.escape(category)}:\s*(#[0-9a-fA-F]{{6}})", TOKENS.read_text()
    )
    if not m:
        raise CommandError(f"no --cat-{category} token in {TOKENS}")
    return m[1].lower()


def section(text, name):
    m = re.search(rf"^## {name}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m[1].strip() if m else ""


def assemble(slug, scene=None):
    brief = TOPICS / slug / "icon.md"
    text = brief.read_text() if brief.exists() else ""
    scene = " ".join((scene or section(text, "Scene")).split())
    if not scene:
        raise CommandError(f"no scene: write ## Scene in {brief} or pass --scene")
    neg = " ".join(section(text, "Negatives").split())
    return STYLE.format(
        scene=scene,
        hex=hex_for(_topic(slug)["primary_category"]),
        negatives=f" Also avoid: {neg}" if neg else "",
    )


def _api_key():
    key = os.environ.get("GEMINI_API_KEY")
    if not key and (ROOT / ".env").exists():
        for line in (ROOT / ".env").read_text().splitlines():
            if line.startswith("GEMINI_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"')
    if not key:
        raise CommandError("GEMINI_API_KEY is not set (environment or .env)")
    return key


def _call(parts, ratio):
    body = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": ratio, "imageSize": "1K"},
        },
    }
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": _api_key()},
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            resp = json.load(r)
    except urllib.error.HTTPError as e:
        raise CommandError(
            f"Gemini HTTP {e.code}: {e.read()[:400].decode(errors='replace')}"
        )
    blobs = [
        p["inlineData"]["data"]
        for c in resp.get("candidates", [])
        for p in c.get("content", {}).get("parts", [])
        if "inlineData" in p
    ]
    return (base64.b64decode(blobs[0]) if blobs else None), _tokens(resp), resp


def _tokens(resp):
    """Billed token counts from the response's usageMetadata. Thinking bills as text output."""
    u = resp.get("usageMetadata", {})
    image = sum(
        d.get("tokenCount", 0)
        for d in u.get("candidatesTokensDetails", [])
        if d.get("modality") == "IMAGE"
    )
    return {
        "input": u.get("promptTokenCount", 0),
        "image_out": image,
        "text_out": u.get("candidatesTokenCount", 0)
        - image
        + u.get("thoughtsTokenCount", 0),
    }


def _usd(t):
    return (
        t["input"] * PRICE_INPUT
        + t["text_out"] * PRICE_TEXT_OUT
        + t["image_out"] * PRICE_IMAGE_OUT
    ) / 1e6


def generate(slug, rnd, n=2, scene=None, edit=None, note="", ratio="3:2"):
    out = TOPICS / slug / "candidates"
    out.mkdir(exist_ok=True)
    if edit:
        if not note:
            raise CommandError("--edit needs --note saying what to change")
        img = Path(edit).read_bytes()
        parts = [
            {"text": EDIT.format(note=note)},
            {
                "inlineData": {
                    "mimeType": "image/png",
                    "data": base64.b64encode(img).decode(),
                }
            },
        ]
    else:
        parts = [{"text": assemble(slug, scene)}]
    written = []
    tokens = {"input": 0, "text_out": 0, "image_out": 0}
    calls = 0
    try:
        for _ in range(n):
            png, t, resp = _call(parts, ratio)
            calls += 1
            tokens = {k: tokens[k] + t[k] for k in tokens}
            if png is None:
                # Billed even without an image, so it is logged before failing.
                raise CommandError(f"no image in response: {json.dumps(resp)[:400]}")
            written.append(_claim(out, rnd, png))
    finally:
        if calls:
            total = _log_spend(
                out,
                {
                    "round": rnd,
                    "images": len(written),
                    "calls": calls,
                    "mode": "edit" if edit else "generate",
                    "scene": scene or "",
                    "note": note,
                    "tokens": tokens,
                    "usd": round(_usd(tokens), 4),
                },
            )
    return written, total


def _claim(out, rnd, png):
    # Claim the name only once the image is back, with an exclusive create,
    # so runs in parallel never overwrite each other's candidates.
    for c in "abcdefghijklmnopqrstuvwxyz":
        dst = out / f"r{rnd}-{c}.png"
        try:
            with open(dst, "xb") as f:
                f.write(png)
            return dst
        except FileExistsError:
            continue
    raise CommandError(f"round {rnd} has no free candidate names left")


def _log_spend(out, entry):
    with open(out / "spend.json", "a+") as log:
        fcntl.flock(log, fcntl.LOCK_EX)
        log.seek(0)
        body = log.read()
        entries = json.loads(body) if body.strip() else []
        entries.append(entry)
        log.seek(0)
        log.truncate()
        log.write(json.dumps(entries, indent=1) + "\n")
    return round(sum(e["usd"] for e in entries), 3)


def normalize(src, out):
    from PIL import Image, ImageChops

    im = Image.open(src).convert("RGBA")
    im = Image.alpha_composite(
        Image.new("RGBA", im.size, (255, 255, 255, 255)), im
    ).convert("RGB")
    diff = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255)))
    bbox = (
        diff.convert("L")
        .point(lambda p: 255 if p > (255 - NEAR_WHITE) else 0)
        .getbbox()
    )
    if bbox is None:
        raise CommandError(f"{src} looks blank")
    content = im.crop(bbox)
    pad = int(round(min(OUT_W, OUT_H) * PAD_FRAC))
    scale = min((OUT_W - 2 * pad) / content.width, (OUT_H - 2 * pad) / content.height)
    size = (max(1, round(content.width * scale)), max(1, round(content.height * scale)))
    content = content.resize(size, Image.LANCZOS)
    canvas = Image.new("RGB", (OUT_W, OUT_H), (255, 255, 255))
    canvas.paste(content, ((OUT_W - size[0]) // 2, (OUT_H - size[1]) // 2))
    for xy in [(0, 0), (OUT_W - 1, 0), (0, OUT_H - 1), (OUT_W - 1, OUT_H - 1)]:
        if canvas.getpixel(xy) != (255, 255, 255):
            raise CommandError(
                f"corner {xy} is not white after normalize; check the source art"
            )
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, "PNG", optimize=True)
    thumb = canvas.copy()
    thumb.thumbnail((40, 40), Image.LANCZOS)
    thumb_path = Path(src).with_suffix(".40px.png")
    thumb.save(thumb_path, "PNG")
    return out, thumb_path


class Command(BaseCommand):
    help = "Stage 3: assemble the icon prompt, call Gemini, normalize the pick."

    def add_arguments(self, p):
        p.add_argument("action", choices=["brief", "generate", "normalize"])
        p.add_argument("--slug", required=True)
        p.add_argument("--round", type=int, default=1)
        p.add_argument("--n", type=int, default=2)
        p.add_argument(
            "--scene", default=None, help="override the brief's Scene for this round"
        )
        p.add_argument("--edit", default=None, help="incumbent PNG to refine")
        p.add_argument(
            "--note", default="", help="what to change, in words (edit mode)"
        )
        p.add_argument("--ratio", default="3:2")
        p.add_argument("--src", default=None, help="candidate to normalize")

    def handle(self, *a, **o):
        slug = o["slug"]
        if o["action"] == "brief":
            self.stdout.write(assemble(slug, o["scene"]))
        elif o["action"] == "generate":
            paths, total = generate(
                slug, o["round"], o["n"], o["scene"], o["edit"], o["note"], o["ratio"]
            )
            for pth in paths:
                self.stdout.write(str(pth))
            self.stdout.write(f"spend so far: ${total:.2f}")
        else:
            if not o["src"]:
                raise CommandError("normalize needs --src")
            out, thumb = normalize(
                o["src"], ROOT / "static" / "img" / "topics" / f"{slug}.png"
            )
            self.stdout.write(f"wrote {out} ({OUT_W}x{OUT_H})")
            self.stdout.write(f"wrote {thumb}; read it to check legibility at 40px")
