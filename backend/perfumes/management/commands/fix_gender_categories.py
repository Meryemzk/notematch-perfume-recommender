from django.core.management.base import BaseCommand
from perfumes.models import Perfume, infer_perfume_gender_category


class Command(BaseCommand):
    help = "Repair perfume gender categories using the annotated W/M/unisex catalogue rules."

    def handle(self, *args, **options):
        counts = {"feminine": 0, "masculine": 0, "unisex": 0}
        changed = 0
        for perfume in Perfume.objects.all().order_by("brand", "name"):
            new_category = infer_perfume_gender_category(perfume)
            if perfume.gender_category != new_category:
                perfume.gender_category = new_category
                perfume.save(update_fields=["gender_category"])
                changed += 1
            counts[perfume.gender_category] = counts.get(perfume.gender_category, 0) + 1

        self.stdout.write(self.style.SUCCESS("✅ Gender categories repaired"))
        self.stdout.write(f"Changed: {changed}")
        self.stdout.write(f"Feminine / W: {counts.get('feminine', 0)}")
        self.stdout.write(f"Masculine / M: {counts.get('masculine', 0)}")
        self.stdout.write(f"Unisex: {counts.get('unisex', 0)}")
