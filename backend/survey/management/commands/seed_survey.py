from django.core.management.base import BaseCommand
from django.db import transaction

from survey.models import Mood, SurveyQuestion, SurveyOption


SEED_DATA = [
    {
        "order": 1,
        "text": "What do you want your perfume to help with right now?",
        "options": [
            {"text": "Boost my energy / feel active", "energic": 3, "relax": 0, "tag": "citrus"},
            {"text": "Calm down / reduce stress", "energic": 0, "relax": 3, "tag": "lavender"},
            {"text": "Both (balanced)", "energic": 2, "relax": 2, "tag": "musk"},
        ],
    },
    {
        "order": 2,
        "text": "When do you mostly apply perfume?",
        "options": [
            {"text": "Morning", "energic": 2, "relax": 0, "tag": "citrus"},
            {"text": "Afternoon", "energic": 1, "relax": 1, "tag": "woody"},
            {"text": "Evening / Night", "energic": 0, "relax": 2, "tag": "vanilla"},
        ],
    },
    {
        "order": 3,
        "text": "What weather/season do you use it in most?",
        "options": [
            {"text": "Warm / Summer", "energic": 2, "relax": 0, "tag": "fresh"},
            {"text": "Cold / Winter", "energic": 0, "relax": 2, "tag": "amber"},
            {"text": "Mild / All seasons", "energic": 1, "relax": 1, "tag": "musk"},
        ],
    },
    {
        "order": 4,
        "text": "Which scent style do you prefer?",
        "options": [
            {"text": "Fresh/Citrus (clean, bright)", "energic": 3, "relax": 0, "tag": "citrus"},
            {"text": "Aromatic/Lavender (soothing)", "energic": 0, "relax": 3, "tag": "lavender"},
            {"text": "Soft Musky/Powdery", "energic": 1, "relax": 2, "tag": "musk"},
            {"text": "Warm Sweet (vanilla)", "energic": 1, "relax": 2, "tag": "vanilla"},
            {"text": "Woody (cedar/sandal)", "energic": 1, "relax": 2, "tag": "woody"},
        ],
    },
    {
        "order": 5,
        "text": "How strong do you want the perfume to feel?",
        "options": [
            {"text": "Light (very soft)", "energic": 0, "relax": 2, "tag": "musk"},
            {"text": "Medium", "energic": 1, "relax": 1, "tag": "woody"},
            {"text": "Strong (noticeable)", "energic": 2, "relax": 0, "tag": "spicy"},
        ],
    },
    {
        "order": 6,
        "text": "If you choose “Energic”, what type of energy?",
        "options": [
            {"text": "Sporty & active", "energic": 3, "relax": 0, "tag": "fresh"},
            {"text": "Happy & bright", "energic": 3, "relax": 0, "tag": "citrus"},
            {"text": "Confident & powerful", "energic": 2, "relax": 0, "tag": "spicy"},
        ],
    },
    {
        "order": 7,
        "text": "If you choose “Relaxation”, what kind of calm?",
        "options": [
            {"text": "Before sleep", "energic": 0, "relax": 3, "tag": "lavender"},
            {"text": "During a stressful day", "energic": 0, "relax": 3, "tag": "musk"},
            {"text": "Warm comfort", "energic": 0, "relax": 3, "tag": "vanilla"},
        ],
    },
    {
        "order": 8,
        "text": "Choose the note you like most (pick one).",
        "options": [
            {"text": "Bergamot/Lemon/Orange", "energic": 3, "relax": 0, "tag": "citrus"},
            {"text": "Lavender", "energic": 0, "relax": 3, "tag": "lavender"},
            {"text": "Vanilla", "energic": 1, "relax": 2, "tag": "vanilla"},
            {"text": "Cedar/Sandalwood", "energic": 1, "relax": 2, "tag": "woody"},
            {"text": "Amber", "energic": 0, "relax": 2, "tag": "amber"},
            {"text": "Ginger/Pepper", "energic": 3, "relax": 0, "tag": "spicy"},
        ],
    },
    {
        "order": 9,
        "text": "Do you like sweet perfumes?",
        "options": [
            {"text": "Yes, I love sweet", "energic": 1, "relax": 2, "tag": "vanilla"},
            {"text": "Sometimes", "energic": 1, "relax": 1, "tag": "amber"},
            {"text": "No, I prefer fresh", "energic": 2, "relax": 0, "tag": "fresh"},
        ],
    },
    {
        "order": 10,
        "text": "Do you like “clean/soapy” scents?",
        "options": [
            {"text": "Yes, very much", "energic": 2, "relax": 1, "tag": "fresh"},
            {"text": "Neutral", "energic": 1, "relax": 1, "tag": "musk"},
            {"text": "No", "energic": 0, "relax": 1, "tag": "amber"},
        ],
    },
]


PERFUME_DATA = [
    {"name": "Citrus Bloom", "brand": "NoteMatch", "notes": "citrus, bergamot, lemon, fresh musk", "moods": ["Energic"], "gender": "unisex", "style": "new", "price": "28.00"},
    {"name": "Fresh Energy", "brand": "NoteMatch", "notes": "fresh, orange, green notes, clean musk", "moods": ["Energic"], "gender": "unisex", "style": "new", "price": "45.00"},
    {"name": "Spice Confidence", "brand": "NoteMatch", "notes": "spicy ginger, pepper, amber, woody", "moods": ["Energic"], "gender": "male", "style": "new", "price": "72.00"},
    {"name": "Lavender Calm", "brand": "NoteMatch", "notes": "lavender, soft musk, powdery notes", "moods": ["Relaxation"], "gender": "unisex", "style": "classic", "price": "35.00"},
    {"name": "Vanilla Comfort", "brand": "NoteMatch", "notes": "vanilla, amber, warm musk", "moods": ["Relaxation"], "gender": "female", "style": "classic", "price": "62.00"},
    {"name": "Woody Serenity", "brand": "NoteMatch", "notes": "sandalwood, cedar, musk, amber", "moods": ["Relaxation"], "gender": "unisex", "style": "classic", "price": "110.00"},
    {"name": "Rose Memory", "brand": "NoteMatch", "notes": "rose, floral, musk, soft amber", "moods": ["Relaxation"], "gender": "female", "style": "classic", "price": "55.00"},
    {"name": "Modern Amber", "brand": "NoteMatch", "notes": "amber, vanilla, spicy, woody", "moods": ["Energic", "Relaxation"], "gender": "unisex", "style": "new", "price": "95.00"},
]


class Command(BaseCommand):
    help = "Seed Survey questions/options and core moods (Energic/Relaxation). Safe to run multiple times."

    @transaction.atomic
    def handle(self, *args, **options):
        # Ensure moods exist
        Mood.objects.get_or_create(name="Energic")
        Mood.objects.get_or_create(name="Relaxation")

        created_q = 0
        updated_q = 0
        total_opts = 0

        for q in SEED_DATA:
            question, created = SurveyQuestion.objects.get_or_create(
                order=q["order"],
                defaults={"text": q["text"]},
            )

            # If exists but text changed, update it
            if not created and question.text != q["text"]:
                question.text = q["text"]
                question.save()
                updated_q += 1
            elif created:
                created_q += 1

            # Replace options to keep scoring consistent
            SurveyOption.objects.filter(question=question).delete()

            for opt in q["options"]:
                SurveyOption.objects.create(
                    question=question,
                    text=opt["text"],
                    energic_points=opt["energic"],
                    relax_points=opt["relax"],
                    note_tag=opt["tag"],
                )
                total_opts += 1

        # Seed a small starter perfume catalog so recommendations work immediately.
        from perfumes.models import Perfume

        created_perfumes = 0
        for item in PERFUME_DATA:
            perfume, perfume_created = Perfume.objects.get_or_create(
                name=item["name"],
                defaults={
                    "brand": item["brand"],
                    "notes": item["notes"],
                },
            )
            perfume.brand = item["brand"]
            perfume.notes = item["notes"]
            perfume.gender_category = item.get("gender", "unisex")
            perfume.style_category = item.get("style", "new")
            perfume.price = item.get("price", "0.00")
            perfume.save()
            if perfume_created:
                created_perfumes += 1

            perfume.moods.clear()
            for mood_name in item["moods"]:
                mood, _ = Mood.objects.get_or_create(name=mood_name)
                perfume.moods.add(mood)

        self.stdout.write(self.style.SUCCESS("✅ Survey and perfume seed completed"))
        self.stdout.write(f"Questions created: {created_q}")
        self.stdout.write(f"Questions updated: {updated_q}")
        self.stdout.write(f"Options inserted: {total_opts}")
        self.stdout.write(f"Perfumes created: {created_perfumes}")
        