"""Capture category OG cards to PNG with headless Chrome — the committed assets
behind `Category.social_card` / og:image. Mirrors `render_social` (topics), but
for categories: one 1200x630 card each, captured at 2x (2400x1260) to
static/img/social/cat-<slug>.png. Needs a running dev server + Chrome on PATH.

  manage.py render_category_cards --slug climate-env
  manage.py render_category_cards --all
"""

import shutil
import subprocess
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from topics.models import Category

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
    help = "Capture category OG share cards to PNGs via headless Chrome."

    def add_arguments(self, parser):
        parser.add_argument("--slug", help="Capture a single category by slug.")
        parser.add_argument(
            "--all", action="store_true", help="Capture every category."
        )
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

        if opts["slug"]:
            cats = list(Category.objects.filter(slug=opts["slug"]))
            if not cats:
                raise CommandError(f"No category with slug {opts['slug']!r}.")
        elif opts["all"]:
            cats = list(Category.objects.order_by("slug"))
        else:
            raise CommandError("Pass --slug <slug> or --all.")

        out_dir = Path(opts["out"] or settings.BASE_DIR / "static" / "img" / "social")
        out_dir.mkdir(parents=True, exist_ok=True)
        base = opts["base_url"].rstrip("/")

        for cat in cats:
            png = out_dir / f"cat-{cat.slug}.png"
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
                    f"{base}/category/{cat.slug}/share/?render=og",
                ],
                check=True,
                capture_output=True,
                timeout=120,
            )
            self.stdout.write(f"  {cat.slug} -> {_pretty(png)}")
        self.stdout.write(self.style.SUCCESS(f"{len(cats)} card(s) captured."))
