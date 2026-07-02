from django.core.management.base import BaseCommand
from django.db import connection

from survey.models import Mood, SurveyQuestion, SurveyOption


def drop_legacy_target_mood_column():
    """Remove old Render DB column that blocks seeding if it still exists."""
    table_name = "survey_surveyoption"
    column_name = "target_mood"
    try:
        with connection.cursor() as cursor:
            columns = [col.name for col in connection.introspection.get_table_description(cursor, table_name)]
            if column_name not in columns:
                return
            if connection.vendor == "postgresql":
                cursor.execute(f'ALTER TABLE "{table_name}" DROP COLUMN IF EXISTS "{column_name}" CASCADE')
            else:
                cursor.execute(f'ALTER TABLE "{table_name}" DROP COLUMN "{column_name}"')
    except Exception:
        pass


def make_legacy_perfume_columns_nullable():
    """Repair old live database columns before seed inserts.

    Older Render databases can still contain old NOT NULL columns such as
    description, best_for and boosts_mood. The current Django model no longer
    writes those columns, so this function makes all existing non-ID perfume
    columns nullable before the seed inserts run. It is safe to run repeatedly.
    """
    table_name = "perfumes_perfume"
    try:
        with connection.cursor() as cursor:
            tables = connection.introspection.table_names(cursor)
            if table_name not in tables:
                return

            if connection.vendor == "postgresql":
                cursor.execute(
                    """
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_schema = current_schema()
                      AND table_name = %s
                      AND column_name <> 'id'
                    ORDER BY ordinal_position
                    """,
                    [table_name],
                )
                columns = [row[0] for row in cursor.fetchall()]
                for column_name in columns:
                    try:
                        cursor.execute(f'ALTER TABLE "{table_name}" ALTER COLUMN "{column_name}" DROP NOT NULL')
                    except Exception:
                        pass
    except Exception:
        pass


SEED_DATA = [
    {
        "order": 1,
        "text": "Eligibility: please confirm that you are aged 18 or above before taking part in this academic perfume recommendation survey.",
        "options": [
            {"text": "Yes, I am 18 or above", "energic": 1, "relax": 1, "tag": "fresh"},
            {"text": "No, I am under 18", "energic": 0, "relax": 0, "tag": "musk"},
        ],
    },
    {
        "order": 2,
        "text": "Consent: do you agree for your anonymous answers to be used for academic research about mood-based perfume recommendations?",
        "options": [
            {"text": "Yes, I agree to participate", "energic": 1, "relax": 1, "tag": "fresh"},
            {"text": "No, I do not agree", "energic": 0, "relax": 0, "tag": "musk"},
        ],
    },
    {
        "order": 3,
        "text": "How often do you normally wear perfume, body mist, aftershave or fragrance?",
        "options": [
            {"text": "Every day", "energic": 3, "relax": 1, "tag": "fresh"},
            {"text": "Several times a week", "energic": 2, "relax": 1, "tag": "floral"},
            {"text": "Occasionally, mainly for plans or special moments", "energic": 1, "relax": 2, "tag": "musk"},
            {"text": "Rarely, but I am interested in finding the right scent", "energic": 0, "relax": 3, "tag": "vanilla"},
        ],
    },
    {
        "order": 4,
        "text": "When choosing a perfume, which factor usually matters most to you?",
        "options": [
            {"text": "Mood — how I want to feel", "energic": 1, "relax": 3, "tag": "musk"},
            {"text": "Occasion — work, date, party, formal event or gifting", "energic": 2, "relax": 1, "tag": "amber"},
            {"text": "Brand — designer, niche or a trusted name", "energic": 2, "relax": 1, "tag": "woody"},
            {"text": "Price — staying within my budget", "energic": 1, "relax": 1, "tag": "fresh"},
            {"text": "Recommendation — reviews, staff advice or online matching", "energic": 2, "relax": 2, "tag": "floral"},
            {"text": "Other personal reasons", "energic": 1, "relax": 1, "tag": "green"},
        ],
    },
    {
        "order": 5,
        "text": "Which fragrance direction feels most suitable when you want to feel relaxed, comfortable or calm?",
        "options": [
            {"text": "Lavender or aromatic clean notes", "energic": 0, "relax": 4, "tag": "lavender"},
            {"text": "Vanilla or soft sweet notes", "energic": 0, "relax": 4, "tag": "vanilla"},
            {"text": "Rose or gentle floral notes", "energic": 1, "relax": 3, "tag": "rose"},
            {"text": "Woody notes that feel warm and grounded", "energic": 1, "relax": 3, "tag": "woody"},
            {"text": "Musk or powdery skin-like notes", "energic": 0, "relax": 4, "tag": "musk"},
            {"text": "Fresh, clean and airy notes", "energic": 1, "relax": 2, "tag": "fresh"},
        ],
    },
    {
        "order": 6,
        "text": "Which fragrance direction makes you feel most confident, polished or memorable?",
        "options": [
            {"text": "Amber — warm, rich and elegant", "energic": 3, "relax": 1, "tag": "amber"},
            {"text": "Spicy notes — bold and attention-grabbing", "energic": 4, "relax": 0, "tag": "spicy"},
            {"text": "Woody notes — refined and professional", "energic": 3, "relax": 1, "tag": "woody"},
            {"text": "Musk — clean, intimate and sophisticated", "energic": 2, "relax": 2, "tag": "musk"},
            {"text": "Rose or floral notes — elegant and expressive", "energic": 2, "relax": 2, "tag": "rose"},
        ],
    },
    {
        "order": 7,
        "text": "Which fragrance direction do you associate most with energy, freshness and a positive start to the day?",
        "options": [
            {"text": "Citrus — bright, clean and uplifting", "energic": 4, "relax": 0, "tag": "citrus"},
            {"text": "Fresh notes — shower-clean and easy to wear", "energic": 4, "relax": 1, "tag": "fresh"},
            {"text": "Green notes — natural, crisp and outdoorsy", "energic": 3, "relax": 1, "tag": "green"},
            {"text": "Aquatic notes — cool, watery and airy", "energic": 3, "relax": 1, "tag": "aquatic"},
            {"text": "Light spicy notes — energetic but still refined", "energic": 3, "relax": 0, "tag": "spicy"},
        ],
    },
    {
        "order": 8,
        "text": "How strongly do you agree that certain scents can influence your mood, confidence or memory?",
        "options": [
            {"text": "Strongly disagree", "energic": 0, "relax": 0, "tag": "fresh"},
            {"text": "Disagree", "energic": 0, "relax": 1, "tag": "musk"},
            {"text": "Neither agree nor disagree", "energic": 1, "relax": 1, "tag": "floral"},
            {"text": "Agree", "energic": 2, "relax": 2, "tag": "amber"},
            {"text": "Strongly agree", "energic": 3, "relax": 3, "tag": "vanilla"},
        ],
    },
    {
        "order": 9,
        "text": "Have you ever had a scent trigger a specific memory, person, place or emotional moment?",
        "options": [
            {"text": "Yes, scent strongly connects with memories for me", "energic": 1, "relax": 3, "tag": "rose"},
            {"text": "Sometimes, but not always", "energic": 1, "relax": 2, "tag": "musk"},
            {"text": "No, I have not noticed this", "energic": 1, "relax": 1, "tag": "fresh"},
            {"text": "I am not sure", "energic": 1, "relax": 2, "tag": "powdery"},
        ],
    },
    {
        "order": 10,
        "text": "Would you use a website that recommends perfumes based on your mood, occasion, preferred notes, budget and fragrance style?",
        "options": [
            {"text": "Yes, definitely", "energic": 3, "relax": 3, "tag": "floral"},
            {"text": "Maybe, if the recommendations feel accurate", "energic": 2, "relax": 2, "tag": "musk"},
            {"text": "Only if it is quick and does not ask too much", "energic": 1, "relax": 1, "tag": "fresh"},
            {"text": "No, I prefer choosing perfumes myself", "energic": 0, "relax": 1, "tag": "green"},
        ],
    },
    {
        "order": 11,
        "text": "What concern would most affect your trust in a mood-based perfume recommendation website?",
        "options": [
            {"text": "Privacy of personal data", "energic": 0, "relax": 2, "tag": "musk"},
            {"text": "Security risks", "energic": 0, "relax": 2, "tag": "woody"},
            {"text": "Too much personal information required", "energic": 0, "relax": 2, "tag": "powdery"},
            {"text": "Lack of transparency about why perfumes are recommended", "energic": 1, "relax": 1, "tag": "green"},
            {"text": "Inaccurate or irrelevant recommendations", "energic": 1, "relax": 1, "tag": "citrus"},
            {"text": "No major concerns", "energic": 3, "relax": 2, "tag": "amber"},
        ],
    },
    {
        "order": 12,
        "text": "What would make the recommendation results feel most useful and trustworthy to you?",
        "options": [
            {"text": "A clear explanation for each perfume match", "energic": 2, "relax": 2, "tag": "woody"},
            {"text": "Visible privacy information and control over my answers", "energic": 1, "relax": 3, "tag": "musk"},
            {"text": "Real user reviews, ratings and popularity signals", "energic": 2, "relax": 1, "tag": "floral"},
            {"text": "Ability to edit preferences and retake the quiz", "energic": 2, "relax": 2, "tag": "fresh"},
            {"text": "Accurate matching for mood, budget, occasion and gender category", "energic": 3, "relax": 2, "tag": "amber"},
        ],
    },
]


PERFUME_DATA = [
    ("PRADA PARADIGME EDPV100", "Prada", "115.00", "woody", "amber", "musk", ["Energic"]),
    ("PRADA PARADIGME EDP50", "Prada", "85.00", "woody", "amber", "citrus", ["Energic"]),
    ("BOSS BOTT NGT EDT200ML", "Boss", "128.00", "woody", "spicy", "amber", ["Energic"]),
    ("INVIC VICT ELIX PARFUM 100", "Rabanne", "114.00", "fresh", "amber", "woody", ["Energic"]),
    ("DIOR SAUVAGE EDP100", "Dior", "122.00", "fresh", "spicy", "amber", ["Energic"]),
    ("1 MILLION LUCKY EDT100", "Rabanne", "90.00", "sweet", "woody", "amber", ["Energic"]),
    ("GG ESSENCE PH EDT90", "Gucci", "103.00", "floral", "jasmine", "musk", ["Relaxation"]),
    ("V DYLAN BLUE EDT100ML", "Versace", "96.00", "fresh", "aquatic", "woody", ["Energic"]),
    ("DIOR SAUVAGE EDP60", "Dior", "87.00", "fresh", "spicy", "amber", ["Energic"]),
    ("MONTBLANC EXPLORER EDP100", "Montblanc", "89.00", "woody", "leather", "fresh", ["Energic"]),
    ("SAUVAGE ELIX 100ML", "Dior", "206.00", "spicy", "amber", "woody", ["Energic"]),
    ("YSL MYSLF EDPRFA60", "YSL", "87.00", "fresh", "woody", "musk", ["Energic"]),
    ("DIOR SAUVAGE EDT100ML", "Dior", "107.00", "fresh", "citrus", "spicy", ["Energic"]),
    ("EA STRONGER YOU EDT150", "Emporio Armani", "110.00", "sweet", "vanilla", "amber", ["Relaxation"]),
    ("BLEU CHANEL EDPV100ML", "Chanel", "128.00", "woody", "citrus", "amber", ["Energic"]),
    ("JPG LE MALE PARFUM EDP75", "Jean Paul Gaultier", "81.00", "vanilla", "lavender", "amber", ["Relaxation"]),
    ("LA VIE EST BELLE EDP100ML", "Lancome", "130.00", "vanilla", "floral", "sweet", ["Relaxation"]),
    ("BOSS BOTT TONIC EDT100ML", "Boss", "89.00", "fresh", "citrus", "woody", ["Energic"]),
    ("BAD BOY EDT V50ML", "Carolina Herrera", "71.00", "spicy", "amber", "citrus", ["Energic"]),
    ("DIOR SAUVAGE EDT60ML", "Dior", "75.00", "fresh", "citrus", "spicy", ["Energic"]),
    ("RABANNE 1 MILLION EDT50&TSX", "Rabanne", "67.00", "spicy", "leather", "amber", ["Energic"]),
    ("COCO MADEM EDPV100ML", "Chanel", "152.00", "floral", "citrus", "amber", ["Relaxation"]),
    ("PHANTOM EDT V100ML", "Rabanne", "98.00", "citrus", "lavender", "vanilla", ["Energic"]),
    ("DIOR SAUVAGE ELIX60ML", "Dior", "143.00", "spicy", "amber", "woody", ["Energic"]),
    ("MJ DAISY LOVE EAU EDT50", "Marc Jacobs", "77.00", "floral", "fruity", "musk", ["Relaxation"]),
    ("RAB 1 MILL NIT ELX PRF100", "Rabanne", "109.00", "amber", "spicy", "woody", ["Energic"]),
    ("BOSS BTTL SRK LAVN EDP100", "Boss", "100.00", "lavender", "woody", "musk", ["Relaxation"]),
    ("PRADA PARADOXE EDPV50", "Prada", "107.00", "floral", "amber", "musk", ["Relaxation"]),
    ("YSL MYSLF EDP100&TS10X", "YSL", "123.00", "fresh", "woody", "musk", ["Energic"]),
    ("BOSS BOTTLD ABSOLU EDP100", "Boss", "109.00", "leather", "woody", "amber", ["Energic"]),
    ("BOSS BOTTLED EDT100ML", "Boss", "91.00", "woody", "citrus", "vanilla", ["Energic"]),
    ("BLEU CHANEL EDPV50ML", "Chanel", "92.00", "woody", "citrus", "amber", ["Energic"]),
    ("YSL Y EDP 100ML", "YSL", "115.00", "fresh", "spicy", "woody", ["Energic"]),
    ("EXPLR EDP100&TS2X7.5&SG", "Montblanc", "85.00", "woody", "leather", "fresh", ["Energic"]),
    ("GUCCI OUD INT EDPV90ML", "Gucci", "167.00", "oud", "amber", "woody", ["Relaxation"]),
    ("GOOD GIRL EDP 50", "Carolina Herrera", "98.00", "jasmine", "vanilla", "amber", ["Relaxation"]),
    ("ISSEY M EDT V 125ML", "Issey Miyake", "101.00", "aquatic", "citrus", "woody", ["Energic"]),
    ("PRADA PARADME EDP30", "Prada", "64.00", "woody", "amber", "musk", ["Energic"]),
    ("EA STRONGER INTENS EDP100", "Emporio Armani", "105.00", "vanilla", "amber", "woody", ["Relaxation"]),
    ("BLEU CHANEL PARFUM 100", "Chanel", "150.00", "woody", "amber", "fresh", ["Energic"]),
    ("TF OMBRE LEATHER EDP100ML", "Tom Ford", "155.00", "leather", "spicy", "amber", ["Energic"]),
    ("JPG MALE EDT V 75ML", "Jean Paul Gaultier", "74.00", "lavender", "vanilla", "mint", ["Relaxation"]),
    ("GUCCI BAMBOO EDP50ML", "Gucci", "90.00", "floral", "jasmine", "woody", ["Relaxation"]),
    ("JOOP! EDT V 200ML", "Joop", "90.00", "sweet", "citrus", "vanilla", ["Energic"]),
    ("PRADA PARADOXE EDPV90", "Prada", "147.00", "floral", "amber", "musk", ["Relaxation"]),
    ("TOUCH M EDT V 100ML", "Burberry", "54.99", "fresh", "spicy", "woody", ["Energic"]),
    ("VLTNO BIR UOMO INT EDP100", "Valentino", "110.00", "woody", "vanilla", "leather", ["Energic"]),
    ("YSL LIBRE EDPV30ML", "YSL", "75.00", "lavender", "orange blossom", "vanilla", ["Relaxation"]),
    ("PARADOXE INT EDP RF90", "Prada", "162.00", "floral", "amber", "musk", ["Relaxation"]),
    ("PRADA PARADOXE EDPV30", "Prada", "75.00", "floral", "amber", "musk", ["Relaxation"]),
    ("MONTBLANC EXPLORER EDP60", "Montblanc", "65.00", "woody", "leather", "fresh", ["Energic"]),
    ("COCO MADEM EDP V50ML", "Chanel", "112.00", "floral", "citrus", "amber", ["Relaxation"]),
    ("SAUVAGE LE PARFUM 100ML", "Dior", "147.00", "spicy", "amber", "woody", ["Energic"]),
    ("HB BOTTLED PARFUM V50ML", "Hugo Boss", "74.00", "woody", "leather", "amber", ["Energic"]),
    ("MJ DAISY WILD EDPV100", "Marc Jacobs", "117.00", "floral", "green", "banana blossom", ["Relaxation"]),
    ("JPG LE BEAU NARCIS EDP125", "Jean Paul Gaultier", "111.00", "coconut", "woody", "amber", ["Energic"]),
    ("TF OMBRE LEATHER EDP50ML", "Tom Ford", "108.00", "leather", "spicy", "amber", ["Energic"]),
    ("MOSC TOYBOY EDP V 100ML", "Moschino", "91.00", "rose", "spicy", "woody", ["Energic"]),
    ("CH GG BLU POLKA PARAD EDP80", "Carolina Herrera", "146.00", "floral", "jasmine", "amber", ["Relaxation"]),
    ("FLORA GORG ORCHID EDPV50", "Gucci", "105.00", "floral", "vanilla", "marine", ["Relaxation"]),
    ("BOSS BOTT INFINITE EDP100", "Boss", "94.00", "fresh", "woody", "citrus", ["Energic"]),
    ("1 MILLION EDT V100ML", "Rabanne", "94.00", "spicy", "leather", "amber", ["Energic"]),
    ("YSL MYSLF EDPR 100ML", "YSL", "120.00", "fresh", "woody", "musk", ["Energic"]),
    ("GENTLEMAN SOCIETY EDP60", "Givenchy", "85.00", "woody", "vanilla", "sage", ["Energic"]),
    ("BOSS SCENT ABSLT M EDP100", "Boss", "107.00", "leather", "ginger", "vanilla", ["Energic"]),
    ("JPG SCANDAL PH EDTV100ML", "Jean Paul Gaultier", "100.00", "sweet", "caramel", "spicy", ["Energic"]),
    ("BLEU CHANEL EDPV150ML", "Chanel", "156.00", "woody", "citrus", "amber", ["Energic"]),
    ("ADG PROFONDO PRF100", "Armani", "127.00", "aquatic", "fresh", "citrus", ["Energic"]),
    ("RABANNE INVICTUS EDT100&TSX", "Rabanne", "95.00", "fresh", "aquatic", "woody", ["Energic"]),
    ("VERSACE EROS EDPV100ML", "Versace", "105.00", "vanilla", "mint", "woody", ["Energic"]),
    ("EA STRONGER INTENS EDP50", "Emporio Armani", "77.00", "vanilla", "amber", "woody", ["Relaxation"]),
    ("SAUVAGE EDP200", "Dior", "183.00", "fresh", "spicy", "amber", ["Energic"]),
    ("BOSS BTTL SRK LAVEN EDP50", "Boss", "73.00", "lavender", "woody", "musk", ["Relaxation"]),
    ("COCO MAD EDP 35ML CLS", "Chanel", "78.00", "floral", "citrus", "amber", ["Relaxation"]),
    ("BURBERRY HERO EDTV50ML", "Burberry", "76.00", "woody", "fresh", "spicy", ["Energic"]),
    ("YSL LIBRE EDPV50ML", "YSL", "107.00", "lavender", "orange blossom", "vanilla", ["Relaxation"]),
    ("FLORA GORG ORCHID EDPV100", "Gucci", "146.00", "floral", "vanilla", "marine", ["Relaxation"]),
    ("GUCCI BAMBOO EDTV75ML", "Gucci", "111.00", "floral", "jasmine", "woody", ["Relaxation"]),
    ("FAHRENHEIT EDT V 100ML", "Dior", "107.00", "leather", "violet", "woody", ["Energic"]),
    ("MOMENT EDPV100ML", "One Direction", "42.99", "fruity", "floral", "musk", ["Relaxation"]),
    ("PARADOXE INT EDP RF50", "Prada", "117.00", "floral", "amber", "musk", ["Relaxation"]),
    ("BOSS THE SCENT M EDT100", "Boss", "90.00", "ginger", "leather", "spicy", ["Energic"]),
    ("YSL LIBRE INTNSE EDP30ML", "YSL", "82.00", "lavender", "vanilla", "amber", ["Relaxation"]),
    ("GOOD GIRL EDP 80", "Carolina Herrera", "128.00", "jasmine", "vanilla", "amber", ["Relaxation"]),
    ("RAB 1 MILL NIT ELIX PRF50", "Rabanne", "80.00", "amber", "spicy", "woody", ["Energic"]),
    ("GA CODE LE PARFUM V50", "Armani", "102.00", "iris", "woody", "amber", ["Relaxation"]),
    ("CH LA BOMBA EDPA50", "Carolina Herrera", "98.00", "fruity", "floral", "vanilla", ["Relaxation"]),
    ("YSL MYSLF L ABSOLU PRF100", "YSL", "140.00", "fresh", "woody", "spicy", ["Energic"]),
    ("NO 5 EDP V 100ML CLS", "Chanel", "156.00", "powdery", "floral", "aldehydic", ["Relaxation"]),
    ("MONTBLANC EXPLORER EDP200", "Montblanc", "130.00", "woody", "leather", "fresh", ["Energic"]),
    ("B BOTTLED UNLTD EDT100", "Boss", "86.00", "fresh", "mint", "woody", ["Energic"]),
    ("VLNTNO BIR UOMO INT EDP50", "Valentino", "81.00", "woody", "vanilla", "leather", ["Energic"]),
    ("MONTBLANC EXPLORER EDP30", "Montblanc", "40.00", "woody", "leather", "fresh", ["Energic"]),
    ("DIAMONDS W EDP V 100ML", "Armani", "80.00", "rose", "fruity", "vanilla", ["Relaxation"]),
    ("EXPLORER EXTREME EDP100", "Montblanc", "99.00", "woody", "leather", "amber", ["Energic"]),
    ("SAUVAGE LE PARFUM 60ML", "Dior", "107.00", "spicy", "amber", "woody", ["Energic"]),
    ("BLEU CHANEL EDTV50ML", "Chanel", "80.00", "fresh", "citrus", "woody", ["Energic"]),
    ("TF BLK ORCHID EDP100", "Tom Ford", "155.00", "oriental", "floral", "truffle", ["Relaxation"]),
]

# Keep only scent values that exist in the Perfume model choices.
SCENT_NORMALISE = {
    "mint": "fresh", "banana blossom": "floral", "orange blossom": "floral", "marine": "aquatic",
    "ginger": "spicy", "sage": "green", "caramel": "sweet", "violet": "powdery", "iris": "powdery",
    "aldehydic": "powdery", "coconut": "sweet", "truffle": "oriental",
}


class Command(BaseCommand):
    help = "Seed NoteMatch survey questions, moods and best-seller perfume catalog. Safe to run multiple times."

    def handle(self, *args, **options):
        # Repair old Render/Supabase columns before inserting seed data.
        drop_legacy_target_mood_column()
        make_legacy_perfume_columns_nullable()

        for mood_name in ["Energic", "Relaxation"]:
            Mood.objects.get_or_create(name=mood_name)

        created_q = updated_q = total_opts = 0
        for q in SEED_DATA:
            question, created = SurveyQuestion.objects.get_or_create(order=q["order"], defaults={"text": q["text"]})
            if not created and question.text != q["text"]:
                question.text = q["text"]
                question.save()
                updated_q += 1
            elif created:
                created_q += 1
            SurveyOption.objects.filter(question=question).delete()
            for opt in q["options"]:
                SurveyOption.objects.create(
                    question=question,
                    text=opt["text"],
                    energic_points=opt["energic"],
                    relax_points=opt["relax"],
                    note_tag=SCENT_NORMALISE.get(opt["tag"], opt["tag"]),
                )
                total_opts += 1

        from types import SimpleNamespace
        from perfumes.models import Perfume, infer_perfume_gender_category

        created_perfumes = updated_perfumes = 0
        for name, brand, price, s1, s2, s3, moods in PERFUME_DATA:
            s1, s2, s3 = [SCENT_NORMALISE.get(s, s) for s in (s1, s2, s3)]
            category = infer_perfume_gender_category(SimpleNamespace(name=name, scent_1=s1, scent_2=s2, scent_3=s3))
            perfume, created = Perfume.objects.update_or_create(
                name=name,
                defaults={
                    "brand": brand,
                    "price": price,
                    "gender_category": category,
                    "scent_1": s1,
                    "scent_2": s2,
                    "scent_3": s3,
                    "description": f"Best-seller catalogue perfume from the project data. Category: {category.title()}.",
                    "notes": f"Best-seller catalog item. Price £{price}. Scent profile: {s1}, {s2}, {s3}. Category: {category}.",
                    "suitable_season": "all",
                    "occasion": "daily",
                    "longevity": 8 if s3 in {"amber", "oud", "leather", "spicy", "oriental"} else 7,
                    "projection": 8 if s3 in {"amber", "oud", "leather", "spicy", "oriental"} else 6,
                    "sillage": 8 if s3 in {"amber", "oud", "leather", "spicy", "oriental"} else 6,
                    "rating": "4.5",
                    "availability_status": "Available",
                    "retailer": "The Perfume Shop / online retailers",
                },
            )
            perfume.moods.clear()
            for mood_name in moods:
                mood, _ = Mood.objects.get_or_create(name=mood_name)
                perfume.moods.add(mood)
            if created:
                created_perfumes += 1
            else:
                updated_perfumes += 1

        self.stdout.write(self.style.SUCCESS("✅ NoteMatch seed completed"))
        self.stdout.write(f"Questions created: {created_q}")
        self.stdout.write(f"Questions updated: {updated_q}")
        self.stdout.write(f"Options inserted: {total_opts}")
        self.stdout.write(f"Perfumes created: {created_perfumes}")
        self.stdout.write(f"Perfumes updated: {updated_perfumes}")
        self.stdout.write(f"Feminine / W perfumes: {Perfume.objects.filter(gender_category='feminine').count()}")
        self.stdout.write(f"Masculine / M perfumes: {Perfume.objects.filter(gender_category='masculine').count()}")
        self.stdout.write(f"Unisex perfumes: {Perfume.objects.filter(gender_category='unisex').count()}")
