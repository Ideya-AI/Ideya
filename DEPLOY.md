# Deploying Infinity

The app is production-ready: 12-factor settings (everything secret or
host-specific comes from the environment), WhiteNoise for static files, gunicorn
as the server, and secure-by-default headers whenever `DJANGO_DEBUG` is off. The
only thing you need before going live is a **domain**; once you have it, filling
in three environment variables is the whole "point it at the domain" step.

## 1. Environment variables

Copy `.env.example` and set real values (or set these as real env vars on your
host — do **not** commit a filled-in `.env`):

| Variable | Required | What it is |
|---|---|---|
| `DJANGO_SECRET_KEY` | ✅ (prod) | Generate: `python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"` |
| `DJANGO_ALLOWED_HOSTS` | ✅ (prod) | Your domain(s), comma-separated: `infinity.example.com,www.infinity.example.com` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | ✅ (prod) | Same host(s) **with scheme**: `https://infinity.example.com` |
| `PUBLIC_ORIGIN` | recommended | `https://infinity.example.com` — baked into poster QR codes and social-card URLs |
| `DJANGO_DB_PATH` | recommended | Absolute SQLite path on a **persistent volume**, e.g. `/data/db.sqlite3` |
| `DJANGO_DEBUG` | — | Leave unset/`false` in production |
| `WEB_CONCURRENCY` | — | gunicorn worker count (default 2 — see the rate-limit note below) |

**Getting a domain is the last blocker.** When you have it, the only change is
those three host variables (`ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`,
`PUBLIC_ORIGIN`) — no code edits. `ALLOWED_HOSTS` is empty by default, so the
site returns 400 for every request until it's set; that's the intended
secure-by-default behavior, not a bug.

## 2. Deploy — pick one path

### A. Docker (any VPS or container host)

```sh
docker build -t infinity .
docker run -d -p 80:8000 \
  -v /srv/infinity-data:/data \
  -e DJANGO_SECRET_KEY=... \
  -e DJANGO_ALLOWED_HOSTS=infinity.example.com \
  -e DJANGO_CSRF_TRUSTED_ORIGINS=https://infinity.example.com \
  -e PUBLIC_ORIGIN=https://infinity.example.com \
  -e DJANGO_DB_PATH=/data/db.sqlite3 \
  infinity
```

The image bakes hashed/compressed static files at build time; the container runs
`migrate` on start (creating the DB on the mounted volume on first boot) then
serves via gunicorn. Put a TLS-terminating reverse proxy (Caddy, nginx, or your
host's load balancer) in front — it forwards `X-Forwarded-Proto`, which settings
already trusts for HTTPS detection.

### B. Buildpack platform (Railway / Render / Heroku-style)

The `Procfile` (release = migrate, web = gunicorn) and `.python-version` are
already here. Set the build command to install deps and collect static:

```
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

Set the env vars from the table, and attach a **persistent disk** mounted where
`DJANGO_DB_PATH` points (platforms with an ephemeral filesystem will otherwise
reset the DB on every deploy — see "Database" below).

## 3. Seed the content

A fresh database has schema only — content lives outside migrations, in
`research/catalog/topic-universe.json` (taxonomy + draft universe) and
`research/topics/<slug>.json` (full topics, the single source of truth;
`export_topic` regenerates them from the DB). Two ways to populate production:

- **Ship your curated state (simplest):** copy your local `db.sqlite3` onto the
  volume at `DJANGO_DB_PATH`. It holds exactly what you see locally. The public
  only ever sees *published* topics, so the draft experiments in your local DB
  stay invisible — they're just harmless rows.
- **Reproducible seed from scratch:** after `migrate`, run

  ```
  python manage.py load_universe
  python manage.py load_topic_draft --file research/topics/nuclear-energy.json \
      --slug nuclear-energy --title 'Nuclear Energy' --category climate-env --status published
  python manage.py load_topic_draft --file research/topics/universal-basic-income.json \
      --slug universal-basic-income --title 'Universal Basic Income' --category economy --status published
  python manage.py seed_category_overviews
  python manage.py seed_category_links
  python manage.py seed_example_prompts
  python manage.py rebuild_search
  ```

  This rebuilds the taxonomy, catalog (as drafts), both published topics, the
  category overviews + adjacency graph, participation prompts, and the search
  index. (Vote counts, reader submissions, and the historical related-topic
  edges of the original seed are local-DB state — they don't reproduce.)

To use the local Django admin (optional — you publish/update locally), create a
superuser: `python manage.py createsuperuser`.

## 4. Notes worth knowing

- **Database:** SQLite is a good fit here (read-heavy atlas, low write volume),
  but the file must live on **persistent storage** and be backed up. Keep worker
  count modest (2–3) so concurrent writes don't hit "database is locked"; the DB
  uses WAL well under this load. If you outgrow it, switch `DATABASES` to Postgres
  — no other code changes.
- **Vote rate limiting** uses the local-memory cache, which is *per gunicorn
  worker*, so the effective per-IP cap is `60 × WEB_CONCURRENCY` per minute. For
  a strict shared cap, run a single worker (`WEB_CONCURRENCY=1`) or point
  `CACHES` at Redis / the database cache.
- **The reader-opinion summarizer** (`manage.py summarize_input`) is a local,
  occasional editorial job — it is **not** part of the web deploy. It needs
  `pip install anthropic` and `ANTHROPIC_API_KEY`, and only ever drafts summaries
  for you to approve. The web image intentionally omits the Anthropic SDK.
- **Verify before launch:** `python manage.py check --deploy` (with prod env)
  should report no security warnings.
