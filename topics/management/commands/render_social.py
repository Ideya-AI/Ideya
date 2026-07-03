"""Capture topic social cards to PNG with headless Chrome — the committed
assets behind ``Topic.social_card`` / ``og:image``. Replaces the manual
chrome-screenshot invocation the first card was made with, and mirrors
``render_poster``'s shape (running dev server + Chrome on PATH required).

The OG card (1200x630) is what link unfurls show and is captured at 2x
(2400x1260), matching the existing committed asset. ``--formats`` also takes
the square (sq, 1080x1080) and portrait/story (pt, 1080x1350) variants; those
save alongside as <slug>-<fmt>.png and are for manual posting, not og:image.

  manage.py render_social --slug nuclear-energy            # -> static/img/social/nuclear-energy.png
  manage.py render_social --all --formats og,sq,pt
"""

import shutil
import subprocess
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count

from topics.models import Topic

CHROME_CANDIDATES = [
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
]

# width, height, device-scale-factor; og stays 2x to match the shipped asset.
FORMATS = {
    "og": (1200, 630, 2),
    "sq": (1080, 1080, 2),
    "pt": (1080, 1350, 2),
}


def _pretty(path):
    """Repo-relative when inside BASE_DIR (the normal case), absolute otherwise."""
    try:
        return path.relative_to(settings.BASE_DIR)
    except ValueError:
        return path


class Command(BaseCommand):
    help = "Capture topic social-share cards to PNGs via headless Chrome."

    def add_arguments(self, parser):
        parser.add_argument("--slug", help="Capture a single topic by slug.")
        parser.add_argument(
            "--all",
            action="store_true",
            help="Capture every published topic that has sections.",
        )
        parser.add_argument(
            "--formats",
            default="og",
            help="Comma-separated card formats: og,sq,pt (default: og).",
        )
        parser.add_argument(
            "--base-url",
            default="http://localhost:8000",
            help="Origin of a running dev server (default: %(default)s).",
        )
        parser.add_argument(
            "--out",
            default=None,
            help="Output directory (default: static/img/social/).",
        )

    def handle(self, *args, **opts):
        chrome = next(
            (path for c in CHROME_CANDIDATES if (path := shutil.which(c))), None
        )
        if not chrome:
            raise CommandError(f"No Chrome binary found (tried {CHROME_CANDIDATES}).")

        formats = [f.strip() for f in opts["formats"].split(",") if f.strip()]
        unknown = [f for f in formats if f not in FORMATS]
        if unknown:
            raise CommandError(
                f"Unknown format(s) {unknown}; pick from {list(FORMATS)}."
            )

        if opts["slug"]:
            topics = list(Topic.objects.filter(slug=opts["slug"]))
            if not topics:
                raise CommandError(f"No topic with slug {opts['slug']!r}.")
        elif opts["all"]:
            topics = list(
                Topic.published.annotate(n=Count("sections"))
                .filter(n__gt=0)
                .order_by("slug")
            )
            if not topics:
                raise CommandError("No published topics with sections.")
        else:
            raise CommandError("Pass --slug <slug> or --all.")

        out_dir = Path(opts["out"] or settings.BASE_DIR / "static" / "img" / "social")
        out_dir.mkdir(parents=True, exist_ok=True)
        base = opts["base_url"].rstrip("/")

        for topic in topics:
            for fmt in formats:
                w, h, dsf = FORMATS[fmt]
                # The og PNG is the Topic.social_card asset and keeps the bare
                # <slug>.png name; other formats are suffixed.
                name = f"{topic.slug}.png" if fmt == "og" else f"{topic.slug}-{fmt}.png"
                png = out_dir / name
                subprocess.run(
                    [
                        chrome,
                        "--headless=new",
                        "--disable-gpu",
                        f"--window-size={w},{h}",
                        f"--force-device-scale-factor={dsf}",
                        "--hide-scrollbars",
                        "--virtual-time-budget=10000",
                        f"--screenshot={png}",
                        f"{base}/{topic.slug}/share/?render={fmt}",
                    ],
                    check=True,
                    capture_output=True,
                    timeout=120,
                )
                self.stdout.write(f"  {topic.slug} [{fmt}] -> {_pretty(png)}")
        self.stdout.write(self.style.SUCCESS(f"{len(topics)} topic(s) captured."))
