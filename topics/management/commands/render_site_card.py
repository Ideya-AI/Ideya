"""Capture the site-wide OG card to PNG with headless Chrome — the committed
asset behind base.html's default og:image (any page without its own card: home,
search, stub topics). Mirrors `render_category_cards`: one 1200x630 card
captured at 2x (2400x1260) to static/img/social/site.png. Needs a running dev
server + Chrome on PATH.

  manage.py render_site_card
"""

import shutil
import subprocess
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

CHROME_CANDIDATES = [
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
]


def _pretty(path):
    try:
        return path.relative_to(settings.BASE_DIR)
    except ValueError:
        return path


class Command(BaseCommand):
    help = "Capture the site-wide OG share card to PNG via headless Chrome."

    def add_arguments(self, parser):
        parser.add_argument(
            "--base-url",
            default="http://localhost:8000",
            help="Origin of a running dev server (default: %(default)s).",
        )
        parser.add_argument("--out", default=None, help="Output dir.")

    def handle(self, *args, **opts):
        chrome = next(
            (path for c in CHROME_CANDIDATES if (path := shutil.which(c))), None
        )
        if not chrome:
            raise CommandError(f"No Chrome binary found (tried {CHROME_CANDIDATES}).")

        out_dir = Path(opts["out"] or settings.BASE_DIR / "static" / "img" / "social")
        out_dir.mkdir(parents=True, exist_ok=True)
        png = out_dir / "site.png"
        base = opts["base_url"].rstrip("/")
        subprocess.run(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--window-size=1200,630",
                "--force-device-scale-factor=2",
                "--hide-scrollbars",
                "--virtual-time-budget=10000",
                f"--screenshot={png}",
                f"{base}/share/?render=og",
            ],
            check=True,
            capture_output=True,
            timeout=120,
        )
        self.stdout.write(self.style.SUCCESS(f"site card -> {_pretty(png)}"))
