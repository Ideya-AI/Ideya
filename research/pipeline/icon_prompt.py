"""Stage 3 tooling, first cut: the generation prompt is assembled, not written.

    .venv/bin/python research/pipeline/icon_prompt.py brief research/categories/ai/icon.md
        Print the assembled prompt for a brief (style template + the brief's
        Scene and Negatives sections + the category hex from tokens.css).

    .venv/bin/python research/pipeline/icon_prompt.py normalize in.png out.png [--ratio 1:1] [--size 512]
        Trim a generated image to its content, pad ~8%, fit the ratio on white,
        save an optimized PNG. Framing is fixed here, never trusted from the
        generator.

    .venv/bin/python research/pipeline/icon_prompt.py generate research/categories/ai/icon.md [--n 2] [--round 1]
                                                       [--edit candidates/r1-a.png --note "make the wires thicker"]
        Call the Gemini image API (GEMINI_API_KEY from the environment or .env)
        with the assembled prompt, or in edit mode with an incumbent image plus
        a rendering note. Candidates land in <brief dir>/candidates/r<round>-<n>.png;
        spend is appended to <brief dir>/candidates/spend.json.

A brief supplies only what the style sheet cannot: the scene, and any negatives
specific to the subject. Everything else is the constant template below, so
style cannot drift between briefs and a rule change reaches every future icon.
"""

import base64
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOKENS = ROOT / "static" / "css" / "tokens.css"
MODEL = "gemini-3-pro-image"
COST_PER_IMAGE = 0.134  # USD, 1K standard, per the design's budget table

STYLE = """\
A minimalist flat vector-style icon illustration, in a clean editorial line-art style: {scene}

Composition: one dominant focal mass with smaller supporting elements at clearly different scales (big, medium, small); at least one element overlaps another so the scene has depth; the ground is a gentle curve, never a flat line; one connective element runs across the frame to tie the pieces together. A single coherent scene, not a row of separate objects. Centered with generous, even padding.

Style: monoline line art with ONE uniform stroke weight on every element, including the thinnest wisps and lines. Rounded line caps and corners. Confident, slightly bold strokes so it stays legible when small. No fussy internal detail.

Color: a single hue, two tones only. Draw all lines in solid {hex}, and give every major mass a clearly visible soft fill of the same hue at about 15-18% opacity, so the duotone is obviously present rather than white interiors. No other colors, no gradients, no shadows, no 3D, no texture.

Important: NO border, NO frame, NO box or outline around the scene, just the illustration on a plain white background. No text, letters, or numbers. No human figures or faces. Calm, neutral, editorial mood: show the subject plainly, neither celebrating nor warning.{negatives}"""


def hex_for(slug):
    m = re.search(rf"--cat-{re.escape(slug)}:\s*(#[0-9a-fA-F]{{6}})", TOKENS.read_text())
    if not m:
        raise SystemExit(f"no --cat-{slug} token in {TOKENS}")
    return m[1].lower()


def section(text, name):
    m = re.search(rf"^## {name}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m[1].strip() if m else ""


def assemble(brief_path):
    text = Path(brief_path).read_text()
    slug = Path(brief_path).parent.name
    scene = " ".join(section(text, "Scene").split())
    neg = " ".join(section(text, "Negatives").split())
    return STYLE.format(
        scene=scene,
        hex=hex_for(slug),
        negatives=f" Also avoid: {neg}" if neg else "",
    )


def normalize(src, dst, ratio="1:1", size=512, pad=0.08):
    from PIL import Image, ImageChops

    im = Image.open(src).convert("RGB")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    diff = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 12 else 0)
    box = diff.getbbox()
    if not box:
        raise SystemExit(f"{src}: blank image")
    im = im.crop(box)
    w, h = im.size
    rw, rh = (int(x) for x in ratio.split(":"))
    cw, ch = w * (1 + 2 * pad), h * (1 + 2 * pad)
    if cw / ch < rw / rh:
        cw = ch * rw / rh
    else:
        ch = cw * rh / rw
    canvas = Image.new("RGB", (round(cw), round(ch)), (255, 255, 255))
    canvas.paste(im, ((canvas.width - w) // 2, (canvas.height - h) // 2))
    canvas = canvas.resize((size, round(size * rh / rw)), Image.LANCZOS)
    canvas.save(dst, optimize=True)
    return canvas.size


def _api_key():
    key = os.environ.get("GEMINI_API_KEY")
    if not key and (ROOT / ".env").exists():
        for line in (ROOT / ".env").read_text().splitlines():
            if line.startswith("GEMINI_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"')
    if not key:
        raise SystemExit("GEMINI_API_KEY is not set")
    return key


def generate(brief_path, n=2, rnd=1, edit=None, note="", ratio="1:1"):
    """One round: n samples of the assembled prompt, or n edits of an incumbent
    with a rendering note. Returns the written paths."""
    brief_path = Path(brief_path)
    out = brief_path.parent / "candidates"
    out.mkdir(exist_ok=True)
    if edit:
        text = (
            f"Using this image, keep the same composition, elements, and layout, "
            f"but make these changes: {note} Keep it flat, single hue, monoline with one "
            f"uniform stroke weight, soft 15-18% fills on the masses, no border, no text, "
            f"plain white background."
        )
        img = Path(edit).read_bytes()
        parts = [
            {"text": text},
            {"inlineData": {"mimeType": "image/png", "data": base64.b64encode(img).decode()}},
        ]
    else:
        parts = [{"text": assemble(brief_path)}]
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
    written = []
    for i in range(n):
        with urllib.request.urlopen(req, timeout=180) as r:
            resp = json.load(r)
        blobs = [
            p["inlineData"]["data"]
            for c in resp.get("candidates", [])
            for p in c.get("content", {}).get("parts", [])
            if "inlineData" in p
        ]
        if not blobs:
            raise SystemExit(f"no image in response: {json.dumps(resp)[:400]}")
        dst = out / f"r{rnd}-{'abcdef'[i]}.png"
        dst.write_bytes(base64.b64decode(blobs[0]))
        written.append(dst)
    log = out / "spend.json"
    entries = json.loads(log.read_text()) if log.exists() else []
    entries.append({"round": rnd, "images": n, "mode": "edit" if edit else "generate",
                    "note": note, "usd": round(n * COST_PER_IMAGE, 3)})
    log.write_text(json.dumps(entries, indent=1) + "\n")
    return written


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["brief"]:
        print(assemble(args[1]))
    elif args[:1] == ["generate"]:
        opts = dict(zip(args[2::2], args[3::2]))
        paths = generate(
            args[1], int(opts.get("--n", 2)), int(opts.get("--round", 1)),
            opts.get("--edit"), opts.get("--note", ""), opts.get("--ratio", "1:1"),
        )
        for p in paths:
            print(p)
    elif args[:1] == ["normalize"]:
        opts = dict(zip(args[3::2], args[4::2]))
        size = normalize(args[1], args[2], opts.get("--ratio", "1:1"), int(opts.get("--size", 512)))
        print(f"{args[2]} {size[0]}x{size[1]}")
    else:
        print(__doc__)
