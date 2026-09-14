"""SQLite FTS5 index behind site search. Filled by `manage.py rebuild_search`."""

from django.db import migrations


def create(apps, schema_editor):
    if schema_editor.connection.vendor != "sqlite":
        return
    with schema_editor.connection.cursor() as c:
        c.execute(
            "CREATE VIRTUAL TABLE IF NOT EXISTS search_fts "
            "USING fts5(kind UNINDEXED, obj_id UNINDEXED, title, body)"
        )


def drop(apps, schema_editor):
    if schema_editor.connection.vendor != "sqlite":
        return
    with schema_editor.connection.cursor() as c:
        c.execute("DROP TABLE IF EXISTS search_fts")


class Migration(migrations.Migration):
    dependencies = [("topics", "0001_initial")]
    operations = [migrations.RunPython(create, drop)]
