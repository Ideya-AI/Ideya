"""RETIRED seed migration (2026-07-10). This used to hard-code the original
6-category taxonomy, the full Nuclear Energy topic, and 7 stub topics — a third
copy of content that drifted against the DB and the per-topic JSON. Content now
has a single source of truth outside migrations:

  - taxonomy + draft topic universe: research/catalog/topic-universe.json
    (loaded by `manage.py load_universe`)
  - full topics: research/topics/<slug>.json
    (loaded by `manage.py load_topic_draft`, exported by `manage.py export_topic`)

Fresh databases bootstrap via the recipe in DEPLOY.md §3 instead of this
migration. The file itself must remain (empty) so the migration chain that
existing databases already recorded stays intact.
"""

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("topics", "0001_initial")]
    operations = []
