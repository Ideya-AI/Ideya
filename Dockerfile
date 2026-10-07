FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Dependencies first for layer caching.
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Bake hashed + compressed static files into the image. collectstatic needs
# DEBUG off (manifest storage) and a SECRET_KEY present, but neither the key nor
# a real host matters for gathering files — use throwaway values for the build.
RUN DJANGO_DEBUG=false DJANGO_SECRET_KEY=build-only-not-used \
    python manage.py collectstatic --noinput

RUN chmod +x entrypoint.sh

# Run as the host user that owns /srv/ideya-data, so the SQLite WAL side files
# stay writable by host-side tools (dev server, backups).
USER 1000:1000
ENV HOME=/tmp

EXPOSE 8000
CMD ["./entrypoint.sh"]
