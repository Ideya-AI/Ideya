"""Capture full-page topic screenshots at desktop + mobile widths with headless
Chrome — the automated replacement for the manual 390px/320px review sweeps.
Mirrors render_social/render_poster's plumbing (running dev server + Chrome on
PATH required); output feeds the stage-4 view-verification critics.

  manage.py render_screens --slug housing-affordability-crisis
      -> research/reviews/housing-affordability-crisis/desktop-1440.png, mobile-390.png, mobile-320.png
  manage.py render_screens --slug x --widths 1440,390
"""

import shutil
import subprocess
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
CAPTURE_HEIGHT = 12000
CAPTURE_HEIGHT_EXPANDED = 22000


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
            self.stdout.write(f"  {slug} [{w}px] -> {_pretty(png)}")
        self.stdout.write(self.style.SUCCESS(f"{len(widths)} screenshot(s) captured."))
