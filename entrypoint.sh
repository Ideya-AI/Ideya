#!/usr/bin/env sh
# Container start: bring the DB schema up to date (creates db.sqlite3 on the
# mounted volume on first boot), then hand off to gunicorn. Static files are
# already baked into the image at build time (see Dockerfile).
set -e

python manage.py migrate --noinput

exec gunicorn ideya.wsgi:application \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers "${WEB_CONCURRENCY:-2}" \
  --access-logfile - \
  --error-logfile -
