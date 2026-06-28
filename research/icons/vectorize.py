#!/usr/bin/env python
"""Vectorize a generated topic icon (raster) into a duotone-in-code SVG.

Turns a single-hue line+fill raster (e.g. an AI-generated concept) into a clean
SVG whose linework is `currentColor` and whose masses are the same colour at a
soft opacity. Because both tones derive from `currentColor`, the page recolours
the icon per category by setting `color:` on the container.

Pipeline: classify pixels into line (saturated hue) vs ink (any non-white),
trace each layer with vtracer in binary mode, then stack fill-under / line-over.

Usage:
    .venv/bin/python research/icons/vectorize.py IN.png OUT.svg [--preview]

Tunables below are conservative defaults calibrated on Nuclear Energy (#1).
"""

import argparse
import re

import vtracer
from PIL import Image, ImageMath, ImageOps

# --- pixel classification thresholds -------------------------------------
LINE_GREENNESS = 22  # g-(r+b)/2 at/above this = saturated stroke ("line")
WHITE_MIN = 248  # min(r,g,b) above this = background (knocked out)
# --- output --------------------------------------------------------------
FILL_OPACITY = 0.16  # soft second tone on the masses (Phosphor-duotone logic)
# --- vtracer (lower precision / higher speckle = smaller file) ------------
PRECISION = 1
SPECKLE = 8


def _masks(src, tmp):
    im = Image.open(src).convert("RGB")
    r, g, b = im.split()
    ev = ImageMath.unsafe_eval
    green = ev("convert(g - (r+b)/2, 'L')", r=r, g=g, b=b)
    minch = ev("convert(min(min(r,g),b),'L')", r=r, g=g, b=b)
    line = green.point(lambda v: 255 if v >= LINE_GREENNESS else 0)
    ink = minch.point(lambda v: 0 if v > WHITE_MIN else 255)
    # vtracer binary wants the shape BLACK on a WHITE ground
    ImageOps.invert(line).convert("L").save(f"{tmp}/mask_line.png")
    ImageOps.invert(ink).convert("L").save(f"{tmp}/mask_fill.png")


def _trace(tmp, name):
    out = f"{tmp}/{name}.svg"
    vtracer.convert_image_to_svg_py(
        f"{tmp}/{name}.png",
        out,
        colormode="binary",
        mode="spline",
        filter_speckle=SPECKLE,
        corner_threshold=60,
        length_threshold=4.0,
        path_precision=PRECISION,
    )
    svg = open(out).read()
    return "\n".join(
        re.sub(r'\s*fill="[^"]*"', "", p)
        for p in re.findall(r"<path\b.*?/>", svg, re.S)
    )


def build(src, dst, tmp="/tmp/icn"):
    import os

    os.makedirs(tmp, exist_ok=True)
    _masks(src, tmp)
    fill = _trace(tmp, "mask_fill")
    line = _trace(tmp, "mask_line")
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" '
        'fill="currentColor" role="img" aria-label="Nuclear energy">\n'
        f'<g fill-opacity="{FILL_OPACITY}">\n{fill}\n</g>\n<g>\n{line}\n</g>\n</svg>\n'
    )
    open(dst, "w").write(svg)
    return svg


def preview(svg, path="/tmp/icn/contact.png"):
    import cairosvg
    from PIL import ImageDraw

    ctx = [
        ("surface", "#ffffff", "#4a9d6c"),
        ("dark band", "#141813", "#4a9d6c"),
        ("recolor rose", "#ffffff", "#b0567f"),
    ]
    S, pad, cap = 256, 16, 22
    sheet = Image.new("RGB", (len(ctx) * (S + pad) + pad, S + pad + cap), "#cccccc")
    d = ImageDraw.Draw(sheet)
    for i, (lab, bg, ink) in enumerate(ctx):
        p = f"/tmp/icn/p{i}.png"
        cairosvg.svg2png(
            bytestring=svg.replace("currentColor", ink).encode(),
            write_to=p,
            background_color=bg,
            output_width=S,
            output_height=S,
        )
        x = pad + i * (S + pad)
        sheet.paste(Image.open(p), (x, cap))
        d.text((x, 4), lab, fill="#111111")
    sheet.save(path)
    return path


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--preview", action="store_true")
    a = ap.parse_args()
    svg = build(a.src, a.dst)
    print(f"wrote {a.dst}  ({len(svg)} bytes)")
    if a.preview:
        print("preview:", preview(svg))
