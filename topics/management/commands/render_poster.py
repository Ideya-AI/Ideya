"""Render topic posters to print-ready 18×24in PDFs with headless Chrome, and
fit-check each one first — the poster is a fixed-size sheet that clips, so a
topic whose content runs past the canvas would otherwise print truncated with
no warning. The fit signal comes from the poster view's ``?fit=1`` mode, which
stamps the pixel overflow onto ``<html data-fit="...">`` (<=0 means it fits).

Needs a running dev server (the poster page pulls static fonts/art the same
way the social-card capture does) and a Chrome binary on PATH.

  manage.py render_poster --slug nuclear-energy      # -> static/posters/nuclear-energy.pdf
  manage.py render_poster --all                      # every published topic with sections
  manage.py render_poster --all --check-only         # fit-check only, write nothing

Exits non-zero if any requested topic overflows, so it can gate a batch run.
"""

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count

from topics.models import Topic

# Same binary hunt order as the social-card capture notes; first hit wins.
CHROME_CANDIDATES = [
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
]

# --virtual-time-budget lets webfonts (Plus Jakarta Sans, Phosphor icons)
# finish loading before Chrome prints; without it every icon vanishes.
CHROME_FLAGS = [
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    "--virtual-time-budget=10000",
]

FIT_RE = re.compile(r'data-fit="(-?\d+)"')


class Command(BaseCommand):
    help = "Fit-check and render topic posters to 18x24in PDFs via headless Chrome."

    def add_arguments(self, parser):
        parser.add_argument("--slug", help="Render a single topic by slug.")
        parser.add_argument(
            "--all",
            action="store_true",
            help="Render every published topic that has sections.",
        )
        parser.add_argument(
            "--check-only",
            action="store_true",
            help="Only report per-topic fit; write no PDFs.",
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
            help="Output directory (default: static/posters/).",
        )

    def handle(self, *args, **opts):
        chrome = next(
            (path for c in CHROME_CANDIDATES if (path := shutil.which(c))), None
        )
        if not chrome:
            raise CommandError(f"No Chrome binary found (tried {CHROME_CANDIDATES}).")

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

        out_dir = Path(opts["out"] or settings.BASE_DIR / "static" / "posters")
        base = opts["base_url"].rstrip("/")
        overflowed = []

        for topic in topics:
            url = f"{base}/{topic.slug}/poster/"
            over = self._fit_overflow(chrome, url)
            if over is None:
                overflowed.append(topic.slug)
                self.stderr.write(f"  {topic.slug}: fit-check failed (no data-fit)")
                continue
            if over > 0:
                overflowed.append(topic.slug)
                self.stderr.write(
                    self.style.WARNING(
                        f"  {topic.slug}: OVERFLOWS by {over}px — skipped"
                    )
                )
                continue

            if opts["check_only"]:
                self.stdout.write(f"  {topic.slug}: fits ({-over}px slack)")
                continue

            out_dir.mkdir(parents=True, exist_ok=True)
            pdf = out_dir / f"{topic.slug}.pdf"
            subprocess.run(
                [chrome, *CHROME_FLAGS, f"--print-to-pdf={pdf}", url],
                check=True,
                capture_output=True,
                timeout=120,
            )
            try:
                shown = pdf.relative_to(settings.BASE_DIR)
            except ValueError:
                shown = pdf
            self.stdout.write(f"  {topic.slug}: fits ({-over}px slack) -> {shown}")

        if overflowed:
            raise CommandError(
                f"{len(overflowed)} poster(s) overflow the 18x24 canvas: "
                + ", ".join(overflowed)
            )
        self.stdout.write(self.style.SUCCESS(f"{len(topics)} poster(s) OK."))

    def _fit_overflow(self, chrome, url):
        """Pixels of vertical overflow reported by ``?fit=1`` (<=0 fits)."""
        sep = "&" if "?" in url else "?"
        with tempfile.TemporaryDirectory() as td:
            res = subprocess.run(
                [
                    chrome,
                    *CHROME_FLAGS,
                    f"--user-data-dir={td}",
                    "--dump-dom",
                    f"{url}{sep}fit=1",
                ],
                capture_output=True,
                text=True,
                timeout=120,
            )
        m = FIT_RE.search(res.stdout)
        return int(m.group(1)) if m else None
