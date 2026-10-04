from django.db import migrations, models


def to_semicolons(apps, schema_editor):
    Position = apps.get_model("topics", "Position")
    for p in Position.objects.exclude(proponents=""):
        p.proponents = "; ".join(x.strip() for x in p.proponents.split(",") if x.strip())
        p.save(update_fields=["proponents"])


class Migration(migrations.Migration):

    dependencies = [
        ("topics", "0005_why_now_source"),
    ]

    operations = [
        migrations.AlterField(
            model_name="position",
            name="proponents",
            field=models.CharField(
                blank=True, help_text="Semicolon-separated notable proponents.", max_length=400
            ),
        ),
        migrations.RunPython(to_semicolons, migrations.RunPython.noop),
    ]
