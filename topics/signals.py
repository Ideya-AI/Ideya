"""Keep the FTS5 index in step with content edits (admin or pipeline)."""

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from . import search
from .models import Category, Position, Topic


@receiver(post_save, sender=Topic)
def _topic_saved(sender, instance, **kwargs):
    search.upsert("topic", instance.id, instance.title, search.topic_body(instance))


@receiver(post_delete, sender=Topic)
def _topic_deleted(sender, instance, **kwargs):
    search.remove("topic", instance.id)


@receiver(post_save, sender=Category)
def _category_saved(sender, instance, **kwargs):
    search.upsert("category", instance.id, instance.name, instance.description)


@receiver(post_delete, sender=Category)
def _category_deleted(sender, instance, **kwargs):
    search.remove("category", instance.id)


@receiver(post_save, sender=Position)
def _position_saved(sender, instance, **kwargs):
    search.upsert("position", instance.id, instance.name, instance.steelman)


@receiver(post_delete, sender=Position)
def _position_deleted(sender, instance, **kwargs):
    search.remove("position", instance.id)
