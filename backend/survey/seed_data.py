"""Starter content for NoteMatch.

This file keeps the public demo useful even when the production database is new.
It is safe to run more than once.
"""
from django.db import transaction

SURVEY_DATA = [
    {
        "order": 1,
        "text": "How are you feeling today?",
        "options": [
            {"text": "Happy and playful", "energic": 3, "relax": 0, "tag": "fruity", "mood": "Happy"},
            {"text": "Calm and peaceful", "energic": 0, "relax": 3, "tag": "lavender", "mood": "Calm"},
            {"text": "Romantic and elegant", "energic": 1, "relax": 2, "tag": "rose", "mood": "Romantic"},
            {"text": "Confident and powerful", "energic": 3, "relax": 0, "tag": "spicy", "mood": "Confident"},
        ],
    },
    {
        "order": 2,
        "text": "What do you want your perfume to improve?",
        "options": [
            {"text": "Energy and motivation", "energic": 3, "relax": 0, "tag": "citrus", "mood": "Energic"},
            {"text": "Stress relief and comfort", "energic": 0, "relax": 3, "tag": "musk", "mood": "Relaxation"},
            {"text": "Confidence for work or study", "energic": 3, "relax": 1, "tag": "woody", "mood": "Confident"},
            {"text": "A softer romantic feeling", "energic": 1, "relax": 2, "tag": "vanilla", "mood": "Romantic"},
        ],
    },
    {
        "order": 3,
        "text": "Where will you wear it most?",
        "options": [
            {"text": "University, office, or daytime", "energic": 2, "relax": 1, "tag": "fresh", "mood": "Fresh"},
            {"text": "A date or evening event", "energic": 1, "relax": 2, "tag": "amber", "mood": "Romantic"},
            {"text": "Gym, travel, or outdoor day", "energic": 3, "relax": 0, "tag": "aquatic", "mood": "Energic"},
            {"text": "Home, self-care, or quiet time", "energic": 0, "relax": 3, "tag": "powdery", "mood": "Calm"},
        ],
    },
    {
        "order": 4,
        "text": "Which scent family attracts you most?",
        "options": [
            {"text": "Floral: rose, jasmine, peony", "energic": 1, "relax": 2, "tag": "floral", "mood": "Romantic"},
            {"text": "Fresh: citrus, green, aquatic", "energic": 3, "relax": 0, "tag": "fresh", "mood": "Fresh"},
            {"text": "Sweet: vanilla, caramel, praline", "energic": 1, "relax": 2, "tag": "sweet", "mood": "Comfort"},
            {"text": "Woody/spicy: cedar, sandalwood, pepper", "energic": 3, "relax": 1, "tag": "woody", "mood": "Confident"},
        ],
    },
    {
        "order": 5,
        "text": "How strong should the perfume feel?",
        "options": [
            {"text": "Soft and close to skin", "energic": 0, "relax": 2, "tag": "musk", "mood": "Calm"},
            {"text": "Medium and wearable every day", "energic": 1, "relax": 1, "tag": "floral", "mood": "Balanced"},
            {"text": "Strong and noticeable", "energic": 3, "relax": 0, "tag": "amber", "mood": "Confident"},
        ],
    },
    {
        "order": 6,
        "text": "Choose the season that matches your mood.",
        "options": [
            {"text": "Spring: soft, floral, fresh", "energic": 1, "relax": 2, "tag": "peony", "mood": "Romantic"},
            {"text": "Summer: bright, clean, citrus", "energic": 3, "relax": 0, "tag": "citrus", "mood": "Fresh"},
            {"text": "Autumn: warm, spicy, cozy", "energic": 1, "relax": 2, "tag": "spicy", "mood": "Comfort"},
            {"text": "Winter: deep, amber, elegant", "energic": 2, "relax": 1, "tag": "amber", "mood": "Elegant"},
        ],
    },
    {
        "order": 7,
        "text": "Which words describe your personality today?",
        "options": [
            {"text": "Soft, caring, and romantic", "energic": 1, "relax": 2, "tag": "rose", "mood": "Romantic"},
            {"text": "Bold, ambitious, and confident", "energic": 3, "relax": 0, "tag": "patchouli", "mood": "Confident"},
            {"text": "Relaxed, gentle, and thoughtful", "energic": 0, "relax": 3, "tag": "lavender", "mood": "Calm"},
            {"text": "Fun, bright, and social", "energic": 3, "relax": 0, "tag": "fruity", "mood": "Happy"},
        ],
    },
    {
        "order": 8,
        "text": "Pick one note you usually enjoy.",
        "options": [
            {"text": "Bergamot or lemon", "energic": 3, "relax": 0, "tag": "bergamot", "mood": "Energic"},
            {"text": "Rose or jasmine", "energic": 1, "relax": 2, "tag": "jasmine", "mood": "Romantic"},
            {"text": "Vanilla or praline", "energic": 1, "relax": 2, "tag": "vanilla", "mood": "Comfort"},
            {"text": "Cedar, oud, or leather", "energic": 3, "relax": 1, "tag": "cedar", "mood": "Confident"},
            {"text": "Clean musk", "energic": 0, "relax": 3, "tag": "musk", "mood": "Calm"},
        ],
    },
    {
        "order": 9,
        "text": "What should your perfume communicate to others?",
        "options": [
            {"text": "I am fresh and approachable", "energic": 2, "relax": 1, "tag": "clean", "mood": "Fresh"},
            {"text": "I am elegant and polished", "energic": 2, "relax": 1, "tag": "iris", "mood": "Elegant"},
            {"text": "I am warm and comforting", "energic": 0, "relax": 3, "tag": "amber", "mood": "Comfort"},
            {"text": "I am bold and unforgettable", "energic": 3, "relax": 0, "tag": "spicy", "mood": "Confident"},
        ],
    },
    {
        "order": 10,
        "text": "Do you prefer modern or classic perfume style?",
        "options": [
            {"text": "Modern, clean, minimal", "energic": 2, "relax": 1, "tag": "clean", "mood": "Fresh"},
            {"text": "Classic, floral, feminine", "energic": 1, "relax": 2, "tag": "floral", "mood": "Elegant"},
            {"text": "Luxurious, rich, dramatic", "energic": 3, "relax": 1, "tag": "oud", "mood": "Confident"},
            {"text": "Sweet, youthful, fun", "energic": 2, "relax": 1, "tag": "sweet", "mood": "Happy"},
        ],
    },
]

PERFUME_DATA = [
    {"brand": "Dior", "name": "Miss Dior Blooming Bouquet", "notes": "peony, rose, white musk, fresh floral", "moods": ["Romantic", "Elegant"], "best_for": "romantic daytime, spring, soft elegant mood", "boosts": "romance, softness, elegance", "description": "A gentle floral style for users who want a polished and feminine impression."},
    {"brand": "Dior", "name": "J'adore", "notes": "jasmine, rose, ylang-ylang, floral", "moods": ["Elegant", "Romantic"], "best_for": "formal occasions, confident feminine style", "boosts": "elegance, confidence", "description": "A classic floral profile for a graceful and mature mood."},
    {"brand": "Chanel", "name": "Coco Mademoiselle", "notes": "orange, rose, patchouli, amber", "moods": ["Confident", "Elegant"], "best_for": "work, evenings, confident occasions", "boosts": "confidence, sophistication", "description": "A polished citrus-floral style with a confident warm base."},
    {"brand": "Chanel", "name": "Chance Eau Tendre", "notes": "grapefruit, jasmine, white musk, fruity floral", "moods": ["Happy", "Fresh"], "best_for": "everyday freshness, university, daytime", "boosts": "happiness, freshness", "description": "A light fruity floral direction for cheerful daily wear."},
    {"brand": "D&G", "name": "Light Blue", "notes": "lemon, apple, cedar, clean musk", "moods": ["Fresh", "Energic"], "best_for": "summer, travel, active daytime", "boosts": "energy, freshness", "description": "A bright citrus-fresh profile for an easy energetic mood."},
    {"brand": "D&G", "name": "The One", "notes": "peach, vanilla, amber, white flowers", "moods": ["Comfort", "Romantic"], "best_for": "evening, warm comfort, soft dates", "boosts": "warmth, romance", "description": "A warm floral-vanilla direction for cozy evening confidence."},
    {"brand": "YSL", "name": "Libre", "notes": "lavender, orange blossom, vanilla, musk", "moods": ["Confident", "Elegant"], "best_for": "presentations, nights out, confident days", "boosts": "confidence, freedom", "description": "A bold aromatic floral mood for users who want presence."},
    {"brand": "YSL", "name": "Black Opium", "notes": "coffee, vanilla, white flowers, sweet amber", "moods": ["Confident", "Comfort"], "best_for": "night events, bold mood, cold weather", "boosts": "boldness, warmth", "description": "A sweet warm style for dramatic and energetic evenings."},
    {"brand": "Lancôme", "name": "La Vie Est Belle", "notes": "iris, praline, vanilla, patchouli", "moods": ["Happy", "Comfort"], "best_for": "celebrations, joyful mood, cozy evenings", "boosts": "happiness, comfort", "description": "A sweet elegant direction for optimistic and warm feelings."},
    {"brand": "Lancôme", "name": "Idôle", "notes": "rose, jasmine, clean musk, pear", "moods": ["Fresh", "Elegant"], "best_for": "clean everyday elegance", "boosts": "freshness, self-belief", "description": "A clean modern floral style for a confident everyday profile."},
    {"brand": "Viktor & Rolf", "name": "Flowerbomb", "notes": "jasmine, orange blossom, patchouli, sweet floral", "moods": ["Romantic", "Happy"], "best_for": "dates, celebrations, expressive mood", "boosts": "romance, joy", "description": "A sweet floral explosion style for memorable occasions."},
    {"brand": "Viktor & Rolf", "name": "Bonbon", "notes": "caramel, orange, peach, amber", "moods": ["Comfort", "Happy"], "best_for": "playful sweet mood, cozy evenings", "boosts": "comfort, playfulness", "description": "A gourmand sweet profile for a fun and warm personality."},
    {"brand": "Marc Jacobs", "name": "Daisy", "notes": "violet, strawberry, jasmine, musk", "moods": ["Happy", "Fresh"], "best_for": "daytime, spring, cheerful mood", "boosts": "lightness, happiness", "description": "A youthful soft floral style for simple happy freshness."},
    {"brand": "Marc Jacobs", "name": "Perfect", "notes": "rhubarb, almond milk, daffodil, cedar", "moods": ["Happy", "Confident"], "best_for": "creative days, casual confidence", "boosts": "individuality, optimism", "description": "A playful modern profile for users who want something expressive."},
    {"brand": "Givenchy", "name": "L'Interdit", "notes": "white flowers, tuberose, patchouli, vetiver", "moods": ["Confident", "Elegant"], "best_for": "evening confidence, formal events", "boosts": "mystery, elegance", "description": "A deeper white floral direction for confident sophistication."},
    {"brand": "Givenchy", "name": "Irresistible", "notes": "rose, pear, ambrette, musk", "moods": ["Romantic", "Happy"], "best_for": "romantic daily wear, friendly mood", "boosts": "charm, positivity", "description": "A bright rose-fruity profile for a soft attractive impression."},
    {"brand": "Tom Ford", "name": "Black Orchid", "notes": "orchid, patchouli, chocolate, incense", "moods": ["Confident", "Elegant"], "best_for": "special nights, dramatic mood", "boosts": "power, mystery", "description": "A dark luxurious direction for users who want strong presence."},
    {"brand": "Tom Ford", "name": "Soleil Blanc", "notes": "coconut, amber, white flowers, solar notes", "moods": ["Fresh", "Elegant"], "best_for": "holiday mood, summer luxury", "boosts": "brightness, glamour", "description": "A warm solar style for fresh but luxurious occasions."},
    {"brand": "Creed", "name": "Aventus", "notes": "pineapple, bergamot, birch, musk", "moods": ["Confident", "Energic"], "best_for": "ambitious days, smart occasions", "boosts": "confidence, motivation", "description": "A fruity-woody profile often chosen for bold confidence."},
    {"brand": "Creed", "name": "Silver Mountain Water", "notes": "bergamot, green tea, musk, blackcurrant", "moods": ["Fresh", "Calm"], "best_for": "clean daily freshness, study days", "boosts": "clarity, calm", "description": "A crisp clean style for a peaceful and refreshed mood."},
    {"brand": "Armani", "name": "Sí", "notes": "blackcurrant, rose, vanilla, patchouli", "moods": ["Elegant", "Confident"], "best_for": "work, dinner, polished confidence", "boosts": "elegance, strength", "description": "A warm fruity-floral direction for mature confidence."},
    {"brand": "Armani", "name": "My Way", "notes": "orange blossom, tuberose, vanilla, cedar", "moods": ["Romantic", "Happy"], "best_for": "day-to-night, optimistic mood", "boosts": "positivity, romance", "description": "A bright white floral style for open and friendly energy."},
    {"brand": "Paco Rabanne", "name": "Lady Million", "notes": "raspberry, jasmine, honey, patchouli", "moods": ["Confident", "Happy"], "best_for": "parties, confident social mood", "boosts": "glamour, fun", "description": "A sweet floral style for bold and social confidence."},
    {"brand": "Paco Rabanne", "name": "Olympea", "notes": "vanilla, salt, jasmine, ambergris", "moods": ["Confident", "Comfort"], "best_for": "summer nights, warm confidence", "boosts": "strength, warmth", "description": "A salty vanilla direction for a powerful but warm impression."},
    {"brand": "Prada", "name": "Paradoxe", "notes": "neroli, amber, musk, white flowers", "moods": ["Elegant", "Fresh"], "best_for": "modern elegance, everyday polish", "boosts": "fresh confidence, elegance", "description": "A modern floral-amber style for clean sophistication."},
    {"brand": "Prada", "name": "Candy", "notes": "caramel, musk, benzoin, sweet powder", "moods": ["Comfort", "Happy"], "best_for": "sweet cozy mood, casual evenings", "boosts": "comfort, playfulness", "description": "A sweet powdery profile for users who enjoy cozy warmth."},
]

MOODS = ["Energic", "Relaxation", "Happy", "Calm", "Romantic", "Confident", "Fresh", "Elegant", "Comfort", "Balanced"]

@transaction.atomic
def ensure_starter_content():
    from survey.models import Mood, SurveyQuestion, SurveyOption
    from perfumes.models import Perfume

    for mood_name in MOODS:
        Mood.objects.get_or_create(name=mood_name)

    for q in SURVEY_DATA:
        question, _ = SurveyQuestion.objects.update_or_create(
            order=q["order"],
            defaults={"text": q["text"]},
        )
        SurveyOption.objects.filter(question=question).delete()
        for opt in q["options"]:
            SurveyOption.objects.create(
                question=question,
                text=opt["text"],
                energic_points=opt["energic"],
                relax_points=opt["relax"],
                note_tag=opt["tag"],
                target_mood=opt.get("mood", ""),
            )

    for item in PERFUME_DATA:
        perfume, _ = Perfume.objects.update_or_create(
            brand=item["brand"],
            name=item["name"],
            defaults={
                "notes": item["notes"],
                "description": item["description"],
                "best_for": item["best_for"],
                "boosts_mood": item["boosts"],
            },
        )
        perfume.moods.clear()
        for mood_name in item["moods"]:
            mood, _ = Mood.objects.get_or_create(name=mood_name)
            perfume.moods.add(mood)

    return {
        "questions": len(SURVEY_DATA),
        "perfumes": len(PERFUME_DATA),
        "moods": len(MOODS),
    }
