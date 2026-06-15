from django.db import migrations


def create_and_fill(apps, schema_editor):
    if schema_editor.connection.vendor != "sqlite":
        return
    with schema_editor.connection.cursor() as c:
        c.execute(
            "CREATE VIRTUAL TABLE IF NOT EXISTS search_fts "
            "USING fts5(kind UNINDEXED, obj_id UNINDEXED, title, body)"
        )
        Topic = apps.get_model("topics", "Topic")
        Category = apps.get_model("topics", "Category")
        Position = apps.get_model("topics", "Position")
        for t in Topic.objects.all():
            body = " ".join(filter(None, [t.summary, t.scope_covered, t.why_now]))
            c.execute(
                "INSERT INTO search_fts (kind, obj_id, title, body) VALUES (%s, %s, %s, %s)",
                ["topic", t.id, t.title, body],
            )
        for cat in Category.objects.all():
            c.execute(
                "INSERT INTO search_fts (kind, obj_id, title, body) VALUES (%s, %s, %s, %s)",
                ["category", cat.id, cat.name, cat.description],
            )
        for p in Position.objects.all():
            c.execute(
                "INSERT INTO search_fts (kind, obj_id, title, body) VALUES (%s, %s, %s, %s)",
                ["position", p.id, p.name, p.steelman],
            )


def drop(apps, schema_editor):
    if schema_editor.connection.vendor != "sqlite":
        return
    with schema_editor.connection.cursor() as c:
        c.execute("DROP TABLE IF EXISTS search_fts")


class Migration(migrations.Migration):

    dependencies = [
        ("topics", "0006_topic_status"),
    ]

    operations = [
        migrations.RunPython(create_and_fill, drop),
    ]
