# Downvotes retired 2026-08-01: drop the -1 rows and rebase the denormalized
# counters (Question.votes / Position.importance) to plain upvote counts.

from django.db import migrations
from django.db.models import Count, Q


def retire_downvotes(apps, schema_editor):
    Vote = apps.get_model("topics", "Vote")
    Question = apps.get_model("topics", "Question")
    Position = apps.get_model("topics", "Position")

    Vote.objects.filter(value=-1).delete()

    q_counts = dict(
        Vote.objects.filter(question__isnull=False)
        .values_list("question_id")
        .annotate(n=Count("id"))
    )
    for q in Question.objects.all():
        n = q_counts.get(q.id, 0)
        if q.votes != n:
            Question.objects.filter(pk=q.pk).update(votes=n)

    p_counts = dict(
        Vote.objects.filter(position__isnull=False)
        .values_list("position_id")
        .annotate(n=Count("id"))
    )
    for p in Position.objects.all():
        n = p_counts.get(p.id, 0)
        if p.importance != n:
            Position.objects.filter(pk=p.pk).update(importance=n)


class Migration(migrations.Migration):
    dependencies = [
        ("topics", "0021_alter_vote_value_delete_stance"),
    ]

    operations = [
        migrations.RunPython(retire_downvotes, migrations.RunPython.noop),
    ]
