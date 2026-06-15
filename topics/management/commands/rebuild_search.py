from django.core.management.base import BaseCommand

from topics import search


class Command(BaseCommand):
    help = "Rebuild the FTS5 search index from the database."

    def handle(self, *args, **options):
        if not search.available():
            self.stdout.write("search_fts table missing — run migrations first.")
            return
        search.rebuild()
        self.stdout.write(self.style.SUCCESS("Search index rebuilt."))
