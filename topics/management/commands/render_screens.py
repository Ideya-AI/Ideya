"""Capture full-page topic screenshots at desktop + mobile widths with headless
Chrome — the automated replacement for the manual 390px/320px review sweeps.
Mirrors render_social/render_poster's plumbing (running dev server + Chrome on
PATH required); output feeds the stage-4 view-verification critics.

  manage.py render_screens --slug housing-affordability-crisis
      -> research/reviews/housing-affordability-crisis/desktop-1440.png, mobile-390.png, mobile-320.png
  manage.py render_screens --slug x --widths 1440,390
"""

import asyncio
import base64
import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from PIL import Image

from topics.models import Topic

CHROME_CANDIDATES = [
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
]
# Headless --screenshot clips to the window height, so capture very tall and
# trim the dead background below the content in post (these pages run long —
# a fixed cap silently clipped the Crux/Actions sections). Expanded captures
# force every detail layer visible and run far taller still.
# 12000 clipped a 9-position / 10-action topic's 320px capture
# (social-media-youth-mental-health, 2026-09-04); the near-cap guard fired as
# designed. The unexpanded page scales with position count too.
CAPTURE_HEIGHT = 20000
# 45000 silently clipped a 10-position topic's 320px expanded capture
# (ai-alignment needed ~49000); a clipped capture reaching the view critics
# looks complete, so the near-cap guard below is a hard error, not a warning.
CAPTURE_HEIGHT_EXPANDED = 80000
# Per-section captures (--sections): one image per `section.sec` (plus the
# header above the first), each tiled to at most SECTION_TILE px tall. A full
# 320px expanded page runs 50,000-70,000px and reaches an agent downsampled to
# ~10px wide — unreadable — so the view critics and the PM read these instead.
SECTION_TILE = 2000


def _capture_sections(chrome, url, width, out_dir):
    """Drive headless Chrome over the DevTools protocol and screenshot each
    `.sec` element (tiled) at `width`. Returns the list of files written."""
    import requests
    import websockets

    # A free port from the OS, not a clock-derived one: two renders started in
    # the same second collided and one captured the other's topic (2026-09-23).
    import socket

    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    td = tempfile.mkdtemp()
    proc = subprocess.Popen(
        [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         f"--remote-debugging-port={port}", f"--user-data-dir={td}", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    async def run():
        tabs = None
        for _ in range(100):
            try:
                tabs = requests.get(f"http://127.0.0.1:{port}/json", timeout=2).json()
                break
            except Exception:
                time.sleep(0.2)
        if not tabs:
            raise CommandError("render_screens: Chrome did not open its debugging port")
        ws_url = [t for t in tabs if t["type"] == "page"][0]["webSocketDebuggerUrl"]
        files = []
        async with websockets.connect(ws_url, max_size=None) as ws:
            n = [0]

            async def call(method, **params):
                n[0] += 1
                await ws.send(json.dumps({"id": n[0], "method": method, "params": params}))
                while True:
                    m = json.loads(await ws.recv())
                    if m.get("id") == n[0]:
                        if "error" in m:
                            raise CommandError(f"CDP {method}: {m['error']}")
                        return m

            await call("Emulation.setDeviceMetricsOverride", width=width, height=1200,
                       deviceScaleFactor=1, mobile=width < 1024)
            await call("Page.enable")
            await call("Page.navigate", url=url)
            await asyncio.sleep(4)  # load + fonts + Alpine
            r = await call("Runtime.evaluate", returnByValue=True, expression=r"""
                (() => { const secs=[...document.querySelectorAll('section.sec')];
                  const out=[]; let top=secs.length? secs[0].getBoundingClientRect().top+scrollY : document.body.scrollHeight;
                  if (top>0) out.push({id:'top', x:0, y:0, w:innerWidth, h:Math.round(top)});
                  for (const s of secs){ const r=s.getBoundingClientRect(); out.push({id:s.id||'sec', x:0, y:Math.round(r.top+scrollY), w:innerWidth, h:Math.round(r.height)}); }
                  return JSON.stringify(out); })()""")
            regions = json.loads(r["result"]["result"]["value"])
            for i, reg in enumerate(regions):
                tiles = max(1, -(-reg["h"] // SECTION_TILE))
                for k in range(tiles):
                    y = reg["y"] + k * SECTION_TILE
                    h = min(SECTION_TILE, reg["y"] + reg["h"] - y)
                    if h <= 0:
                        continue
                    shot = await call("Page.captureScreenshot", format="png", captureBeyondViewport=True,
                                      clip={"x": 0, "y": y, "width": reg["w"], "height": h, "scale": 1})
                    name = f"{i:02d}-{reg['id']}" + (f"-{k + 1}" if tiles > 1 else "") + ".png"
                    path = out_dir / name
                    path.write_bytes(base64.b64decode(shot["result"]["data"]))
                    files.append(path)
        return files

    try:
        return asyncio.run(run())
    finally:
        proc.terminate()
        shutil.rmtree(td, ignore_errors=True)


def _pretty(path):
    try:
        return path.relative_to(settings.BASE_DIR)
    except ValueError:
        return path


def _trim_bottom(png_path):
    """Crop the trailing background (whatever colour the page ends on) so the
    tall capture becomes a real full-page shot without a slab of dead space."""
    im = Image.open(png_path).convert("RGB")
    w, h = im.size
    bg = im.getpixel((2, h - 2))  # bottom-left is always page background
    px = im.load()
    last = 0
    for y in range(h - 1, -1, -1):
        row_bg = True
        for x in range(0, w, max(1, w // 40)):  # sample ~40 columns per row
            p = px[x, y]
            if max(abs(p[i] - bg[i]) for i in range(3)) > 8:
                row_bg = False
                break
        if not row_bg:
            last = y
            break
    if last and last < h - 40:
        im.crop((0, 0, w, min(h, last + 40))).save(png_path)


class Command(BaseCommand):
    help = "Capture full-page topic screenshots at desktop/mobile widths."

    def add_arguments(self, parser):
        parser.add_argument(
            "--slug",
            required=True,
            help="Topic slug (use the -draft staging slug for a new topic).",
        )
        parser.add_argument(
            "--widths",
            default="1440,390,320",
            help="Comma-separated viewport widths (default: 1440,390,320).",
        )
        parser.add_argument(
            "--base-url",
            required=True,
            help="Origin of a RUNNING dev server (e.g. http://localhost:8641). "
            "Required: a wrong default silently captures error pages.",
        )
        parser.add_argument(
            "--out",
            default=None,
            help="Output dir (default: research/reviews/<slug>/).",
        )
        parser.add_argument(
            "--sections",
            action="store_true",
            help="Also capture one image per page section (tiled at "
            f"{SECTION_TILE}px) into <out>/sections/<tag>-<width>[-expanded]/ — "
            "the readable form the view critics and the PM consume.",
        )
        parser.add_argument(
            "--expanded",
            action="store_true",
            help="Capture with ?expanded=1 (DEBUG-only page mode that forces "
            "all Go-deeper extras and detail regions visible) — files get an "
            "-expanded suffix.",
        )

    def handle(self, *args, **opts):
        chrome = next(
            (path for c in CHROME_CANDIDATES if (path := shutil.which(c))), None
        )
        if not chrome:
            raise CommandError(f"No Chrome binary found (tried {CHROME_CANDIDATES}).")

        slug = opts["slug"]
        if not Topic.objects.filter(slug=slug).exists():
            raise CommandError(f"No topic with slug {slug!r}.")
        try:
            widths = [int(w) for w in opts["widths"].split(",") if w.strip()]
        except ValueError:
            raise CommandError(f"--widths must be integers, got {opts['widths']!r}.")

        out_dir = Path(opts["out"] or settings.BASE_DIR / "research" / "reviews" / slug)
        out_dir.mkdir(parents=True, exist_ok=True)
        base = opts["base_url"].rstrip("/")

        suffix = "-expanded" if opts["expanded"] else ""
        query = "?expanded=1" if opts["expanded"] else ""
        height = CAPTURE_HEIGHT_EXPANDED if opts["expanded"] else CAPTURE_HEIGHT
        for w in widths:
            tag = "desktop" if w >= 1024 else "mobile"
            png = out_dir / f"{tag}-{w}{suffix}.png"
            subprocess.run(
                [
                    chrome,
                    "--headless=new",
                    "--disable-gpu",
                    f"--window-size={w},{height}",
                    "--hide-scrollbars",
                    "--virtual-time-budget=10000",
                    f"--screenshot={png}",
                    f"{base}/{slug}/{query}",
                ],
                check=True,
                capture_output=True,
                timeout=120,
            )
            _trim_bottom(png)
            with Image.open(png) as shot:
                if shot.size[1] > height - 200:
                    raise CommandError(
                        f"{png.name} is within 200px of the {height}px capture "
                        "window — the page bottom is likely clipped; raise "
                        "CAPTURE_HEIGHT(_EXPANDED). A clipped capture handed to "
                        "the view critics reads as a complete render."
                    )
            self.stdout.write(f"  {slug} [{w}px] -> {_pretty(png)}")
            if opts["sections"]:
                sec_dir = out_dir / "sections" / f"{tag}-{w}{suffix}"
                if sec_dir.exists():
                    for old_file in sec_dir.glob("*.png"):
                        old_file.unlink()
                sec_dir.mkdir(parents=True, exist_ok=True)
                files = _capture_sections(chrome, f"{base}/{slug}/{query}", w, sec_dir)
                self.stdout.write(f"  {slug} [{w}px] sections -> {_pretty(sec_dir)} ({len(files)} image(s))")
        self.stdout.write(self.style.SUCCESS(f"{len(widths)} screenshot(s) captured."))
