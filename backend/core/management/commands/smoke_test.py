from django.core.management.base import BaseCommand
from django.test import Client
from survey.models import SurveyQuestion
from perfumes.models import Perfume


class Command(BaseCommand):
    help = "Run a quick local smoke test for NoteMatch pages and survey recommendation flow."

    def handle(self, *args, **options):
        client = Client()
        for path in ["/", "/perfumes/", "/survey/", "/admin/login/"]:
            response = client.get(path)
            if response.status_code >= 400:
                raise SystemExit(f"Smoke test failed: {path} returned {response.status_code}")

        questions = SurveyQuestion.objects.prefetch_related("options").order_by("order")
        if not questions.exists():
            raise SystemExit("Smoke test failed: no survey questions. Run seed_survey first.")
        if not Perfume.objects.exists():
            raise SystemExit("Smoke test failed: no perfumes. Run seed_survey first.")

        post_data = {}
        for question in questions:
            option = question.options.first()
            if not option:
                raise SystemExit(f"Smoke test failed: question {question.id} has no options")
            post_data[f"q_{question.id}"] = str(option.id)
        post_data["price_range"] = "any"
        for index, perfume_id in enumerate(Perfume.objects.values_list("id", flat=True)[:3], start=1):
            post_data[f"favourite_perfume_{index}"] = str(perfume_id)

        response = client.post("/survey/", data=post_data)
        if response.status_code not in (301, 302):
            raise SystemExit(f"Smoke test failed: survey POST returned {response.status_code}")
        response = client.get("/survey/result/")
        if response.status_code != 200:
            raise SystemExit(f"Smoke test failed: result page returned {response.status_code}")
        self.stdout.write(self.style.SUCCESS("NoteMatch smoke test passed."))
