from django.core.management.base import BaseCommand
from survey.seed_data import ensure_starter_content

class Command(BaseCommand):
    help = "Seed a complete starter survey, moods, and perfume catalog. Safe to run multiple times."

    def handle(self, *args, **options):
        stats = ensure_starter_content()
        self.stdout.write(self.style.SUCCESS("✅ NoteMatch starter content is ready"))
        self.stdout.write(f"Questions: {stats['questions']}")
        self.stdout.write(f"Perfumes: {stats['perfumes']}")
        self.stdout.write(f"Moods: {stats['moods']}")
