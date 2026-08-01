#!/usr/bin/env python3
"""Normalize a chosen icon candidate into the committed primary-art PNG.

Nano Banana returns a 1264x848 JPEG drawn on a near-white ground. The committed
asset at static/img/topics/<slug>.png is a 1035x690 (3:2) RGB PNG on pure white
with uniform optical padding. This does that deterministically: flatten onto
white, trim the near-white margins to the drawn content, re-pad to a uniform
margin, fit onto a 3:2 white canvas, and save. Also writes a 40px thumbnail
beside the source so the legibility check has something to look at.

Usage:
    python research/icons/postprocess_icon.py --slug housing-affordability-crisis \
        --src research/icons/candidates/housing-affordability-crisis/<file>.jpg
    # --out defaults to static/img/topics/<slug>.png
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageChops

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

OUT_W, OUT_H = 1035, 690  # committed 3:2 primary-art size
PAD_FRAC = 0.08  # uniform optical padding as a fraction of the shorter side
NEAR_WHITE = 244  # pixels at/above this on all channels count as background


def flatten_white(im: Image.Image) -> Image.Image:
    """Composite any alpha onto a pure-white background; return RGB."""
    im = im.convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    return Image.alpha_composite(bg, im).convert("RGB")


def content_bbox(im: Image.Image):
    """Bounding box of the non-(near-white) content, or None if the image is blank."""
    # Difference from a white canvas, thresholded so faint JPEG noise in the
    # margins doesn't count as content.
    diff = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255)))
    mask = diff.convert("L").point(lambda p: 255 if p > (255 - NEAR_WHITE) else 0)
    return mask.getbbox()


def normalize(src: Path, out: Path) -> None:
    im = flatten_white(Image.open(src))
    bbox = content_bbox(im)
    if bbox is None:
        sys.exit(f"{src} looks blank (no content found above the white threshold).")
    content = im.crop(bbox)

    # Fit the trimmed content into the padded interior of a 3:2 white canvas.
    pad = int(round(min(OUT_W, OUT_H) * PAD_FRAC))
    inner_w, inner_h = OUT_W - 2 * pad, OUT_H - 2 * pad
    scale = min(inner_w / content.width, inner_h / content.height)
    new_w = max(1, int(round(content.width * scale)))
    new_h = max(1, int(round(content.height * scale)))
    content = content.resize((new_w, new_h), Image.LANCZOS)

    canvas = Image.new("RGB", (OUT_W, OUT_H), (255, 255, 255))
    canvas.paste(content, ((OUT_W - new_w) // 2, (OUT_H - new_h) // 2))

    # Sanity: corners must be pure white (uniform ground, no stray frame).
    for xy in [(0, 0), (OUT_W - 1, 0), (0, OUT_H - 1), (OUT_W - 1, OUT_H - 1)]:
        if canvas.getpixel(xy) != (255, 255, 255):
            sys.exit(
                f"Corner {xy} is not white after normalize — check the source art."
            )

    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, "PNG", optimize=True)
    print(f"wrote {out}  ({OUT_W}x{OUT_H} RGB)")

    # 40px legibility thumbnail beside the source candidate.
    thumb = canvas.copy()
    thumb.thumbnail((40, 40), Image.LANCZOS)
    thumb_path = src.with_suffix(".40px.png")
    thumb.save(thumb_path, "PNG")
    print(
        f"wrote {thumb_path}  ({thumb.width}x{thumb.height}) — Read it to check legibility"
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--slug", required=True)
    ap.add_argument("--src", required=True, help="the chosen candidate JPEG")
    ap.add_argument("--out", default="", help="default static/img/topics/<slug>.png")
    args = ap.parse_args()
    out = (
        Path(args.out)
        if args.out
        else REPO / "static" / "img" / "topics" / f"{args.slug}.png"
    )
    normalize(Path(args.src), out)


if __name__ == "__main__":
    main()
