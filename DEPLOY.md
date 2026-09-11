# Deploying Ideya

The app is production-ready: 12-factor settings (everything secret or
host-specific comes from the environment), WhiteNoise for static files, gunicorn
as the server, and secure-by-default headers whenever `DJANGO_DEBUG` is off. The
only thing you need before going live is a **domain**; once you have it, filling
in three environment variables is the whole "point it at the domain" step.

## 1. Environment variables

Set these as env vars on the host (or in a local `.env`, which settings reads
automatically — do **not** commit it):

| Variable | Required | What it is |
|---|---|---|
| `DJANGO_SECRET_KEY` | ✅ (prod) | Generate: `python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"` |
| `DJANGO_ALLOWED_HOSTS` | ✅ (prod) | Your domain(s), comma-separated: `ideya1.org,www.ideya1.org,ideya1.com,www.ideya1.com` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | ✅ (prod) | Same host(s) **with scheme**: `https://ideya1.org` |
| `PUBLIC_ORIGIN` | recommended | `https://ideya1.org` — baked into poster QR codes and social-card URLs |
| `GA_MEASUREMENT_ID` | optional | Google Analytics 4 id (`G-…`). Unset → no analytics markup rendered at all. Set in prod.env + restart to enable |
| `DJANGO_DB_PATH` | recommended | Absolute SQLite path on a **persistent volume**, e.g. `/data/db.sqlite3` |
| `DJANGO_DEBUG` | — | Leave unset/`false` in production |
| `WEB_CONCURRENCY` | — | gunicorn worker count (default 2 — see the rate-limit note below) |

**Domains: `ideya1.org` (primary) + `ideya1.com`.** Both are listed in
`ALLOWED_HOSTS`/`CSRF_TRUSTED_ORIGINS` above so either resolves; canonicalize at
the proxy/DNS layer with a 301 from `ideya1.com` (and both `www.` hosts) to
`https://ideya1.org` so search engines and shares see one origin.
`PUBLIC_ORIGIN` is always the `.org`. `ALLOWED_HOSTS` is empty by default, so the
site returns 400 for every request until it's set; that's the intended
secure-by-default behavior, not a bug.

## 2. Deploy — pick one path

### A. Docker (any VPS or container host)

```sh
docker build -t ideya .
docker run -d -p 80:8000 \
  -v /srv/ideya-data:/data \
  -e DJANGO_SECRET_KEY=... \
  -e DJANGO_ALLOWED_HOSTS=ideya1.org,www.ideya1.org,ideya1.com,www.ideya1.com \
  -e DJANGO_CSRF_TRUSTED_ORIGINS=https://ideya1.org,https://www.ideya1.org,https://ideya1.com,https://www.ideya1.com \
  -e PUBLIC_ORIGIN=https://ideya1.org \
  -e DJANGO_DB_PATH=/data/db.sqlite3 \
  ideya
```

The image bakes hashed/compressed static files at build time; the container runs
`migrate` on start (creating the DB on the mounted volume on first boot) then
serves via gunicorn. Put a TLS-terminating reverse proxy (Caddy, nginx, or your
host's load balancer) in front — it forwards `X-Forwarded-Proto`, which settings
already trusts for HTTPS detection.

### B. Buildpack platform (Railway / Render / Heroku-style)

Create a `Procfile` (`release: python manage.py migrate --noinput`, `web:` the
gunicorn line from `entrypoint.sh`) and a `.python-version` containing `3.12`.
Set the build command to install deps and collect static:

```
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

Set the env vars from the table, and attach a **persistent disk** mounted where
`DJANGO_DB_PATH` points (platforms with an ephemeral filesystem will otherwise
reset the DB on every deploy — see "Database" below).

### C. Self-host from the desktop via Cloudflare Tunnel (the launch plan)

Run the Docker container locally and publish it through a **Cloudflare Tunnel**
— no port-forwarding, no exposed home IP, works behind CGNAT/dynamic IPs, free.
Cloudflare terminates TLS at the edge and forwards `X-Forwarded-Proto: https`,
which settings already trusts, so no code or env changes beyond the table above.

1. **Cloudflare setup (once):** add both `ideya1.org` and `ideya1.com` as sites
   on a free plan and switch their nameservers to Cloudflare at the registrar.
2. **Run the app** (same image as path A, loopback-only since the tunnel is the
   only way in):

   ```sh
   docker build -t ideya .
   docker run -d --name ideya --restart unless-stopped \
     -p 127.0.0.1:8642:8000 \
     -v /srv/ideya-data:/data \
     --env-file /srv/ideya-data/prod.env \
     ideya
   ```

   Host port **8642** is deliberately uncommon so day-to-day dev servers
   (8000/8080/3000/…) never collide with the live site. Put the production env
   values (table above) in `/srv/ideya-data/prod.env` — do **not** reuse the
   repo's dev `.env` (it sets `DJANGO_DEBUG=true`).
3. **Wire the tunnel.** An existing cloudflared tunnel can serve this too —
   add a hostname block to its ingress and route the domain to it:

   ```yaml
   # in the existing tunnel's config.yml, above the http_status:404 catch-all
   - hostname: ideya1.org
     service: http://localhost:8642
   ```

   ```sh
   cloudflared tunnel route dns <existing-tunnel-name> ideya1.org
   sudo systemctl restart cloudflared
   ```

   (Starting fresh instead: `cloudflared tunnel login && cloudflared tunnel
   create ideya && cloudflared tunnel route dns ideya ideya1.org`, same ingress
   block, then `sudo cloudflared service install`.)
4. **Redirects at the edge:** in Cloudflare, add Redirect Rules (dynamic, 301)
   sending `ideya1.com`, `www.ideya1.com`, and `www.ideya1.org` to
   `https://ideya1.org` + the original path. (For the `.com` zone, the rule
   needs a proxied placeholder DNS record — e.g. an `A` record to `192.0.2.1`,
   orange-clouded — so requests reach Cloudflare to be redirected.)
5. **Desktop realities:** disable suspend/hibernate (`systemctl mask sleep.target
   suspend.target`), rely on `--restart unless-stopped` + the cloudflared service
   after reboots, and back up `/srv/ideya-data/db.sqlite3` (it's the only
   state). In place since 2026-08-10: a weekly cron (`crontab -l`, Sun 03:45)
   runs `/srv/ideya-data/backup-db.sh` — a consistent `sqlite3 .backup` gzipped
   into `/srv/ideya-data/backups/`, newest 12 kept. Same-disk only: it covers
   corruption and bad writes, not disk death — offsite (Litestream→R2 or a
   periodic copy elsewhere) is still open. Uptime is
   the machine's uptime; that's the accepted trade-off until this moves to a
   host, which is just "run the same image elsewhere and repoint the tunnel."

#### Day-to-day operations

```sh
docker stop ideya      # take the site down (visitors get a Cloudflare error)
docker start ideya     # bring it back (also auto-starts after reboot)
docker logs -f ideya   # tail the app
```

**Update the live site** (code and static files are baked into the image, so
redeploy = rebuild and swap; the DB on `/srv/ideya-data` survives, and
`entrypoint.sh` migrates on start):

```sh
docker build -t ideya .
docker stop ideya && docker rm ideya
docker run -d --name ideya --restart unless-stopped \
  -p 127.0.0.1:8642:8000 \
  -v /srv/ideya-data:/data \
  --env-file /srv/ideya-data/prod.env \
  ideya
```

The tunnel half is a systemd service and normally never needs touching:
`sudo systemctl status|restart cloudflared`. Local dev is separate from all of
this: `.venv/bin/python manage.py runserver` on port 8000 with the repo's dev
`.env` and `db.sqlite3`.

## 3. Seed the content

A fresh database has schema only — content lives outside migrations, in
`research/topics/<slug>.json` — one file per topic, cradle to grave, the single
source of truth — plus `research/categories.json` for the taxonomy. Two ways to
populate production:

- **Already done on the launch box (simplest):** there is one database, at
  `/srv/ideya-data/db.sqlite3`, shared by the authoring session and the container.
  Nothing needs shipping. The public only ever sees *published* topics, so
  everything still being worked on stays invisible — just harmless rows.
- **Reproducible seed from scratch:** after `migrate`, run

  ```
  python manage.py load_universe          # taxonomy + every topic file
  python manage.py seed_category_overviews
  python manage.py seed_category_links
  python manage.py rebuild_search
  ```

  `load_universe` reads `research/categories.json` and then every file in
  `research/topics/`, so it rebuilds the taxonomy and all 136 topics at whatever
  stop each one's file records — including which are published. Participation
  prompts are seeded per topic by the loader as it goes.

  The database is derived by design: delete it, migrate, run the above, and the
  atlas is back. The one thing that does not reproduce is reader participation,
  which exists only in the database.

### Publish one topic to the live site (the standing flow)

**There is one database.** The authoring session and the live container share
`/srv/ideya-data/db.sqlite3` — the container mounts it at `/data/db.sqlite3`, and
the repo's `.env` points local Django at the same file. So a topic you publish
locally is live the moment you flip the switch: there is no content push, no
second loader run, and nothing to keep in sync.

```sh
manage.py publish_topic --slug <slug> --confirm     # that is the whole thing
```

**The one thing that still needs a redeploy is artwork.** `collectstatic` bakes
static files into the image, so a topic whose primary art and OG card are new
needs the image rebuilt before those images resolve. Content does not.

```sh
git add research/topics/<slug>.json research/runs/<slug>/record.json \
    research/icons/<slug>.md research/reviews/<slug>/ \
    static/img/topics/<slug>.png static/img/social/<slug>.png
git commit -m 'Publish <slug>'
docker build -t ideya . && docker restart ideya     # only when static files changed

# Confirm it actually landed. A just-published topic missing from the live site
# is a known failure mode (ENGINE.md §11) and nothing used to check for it.
curl -s -o /dev/null -w '%{http_code}\n' https://<live-host>/<slug>/   # expect 200
```

**Taking a topic back down** is the same switch: `publish_topic --slug <slug>
--off --confirm`. It needs no readiness, because pulling something off the site is
always allowed.

**Editing a topic that is already live** needs `--allow-published` on the loader:
it refuses by default to overwrite a page readers are on, and nothing re-certifies
the topic afterwards. Prefer taking it off the site, editing, then publishing again.

Reloading a topic updates its rows in place: every stat, question, position and
action is matched by the frozen `id` its content file carries, so votes, leans and
reader responses survive any amount of rewording. Only an item the file no longer
carries is retired, and its participation goes with it.

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
