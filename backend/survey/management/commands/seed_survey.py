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


def make_legacy_survey_question_columns_compatible():
    """Repair old live databases that still have legacy SurveyQuestion columns.

    Some previous deployments created an ``is_active`` column on
    survey_surveyquestion with NOT NULL but without a database default.
    The current model does not use that field, so Django inserts omit it and
    PostgreSQL rejects the row. This repair is safe to run repeatedly and fixes
    the live database before seed data is inserted.
    """
    table_name = "survey_surveyquestion"
    try:
        with connection.cursor() as cursor:
            tables = connection.introspection.table_names(cursor)
            if table_name not in tables:
                return

            columns = [col.name for col in connection.introspection.get_table_description(cursor, table_name)]
            if "is_active" not in columns:
                return

            if connection.vendor == "postgresql":
                cursor.execute(f'UPDATE "{table_name}" SET "is_active" = TRUE WHERE "is_active" IS NULL')
                cursor.execute(f'ALTER TABLE "{table_name}" ALTER COLUMN "is_active" SET DEFAULT TRUE')
                # Also drop NOT NULL so future model changes cannot block inserts.
                cursor.execute(f'ALTER TABLE "{table_name}" ALTER COLUMN "is_active" DROP NOT NULL')
    except Exception:
        # Never block deployment because of a legacy repair. Normal migrations/seed
        # will continue and show a clearer error if there is a different problem.
        pass


SEED_DATA = [
    {
        "order": 1,
        "text": "What emotional effect would you like your fragrance to create?",
        "options": [
            {"text": "Calm, relaxed and comforting", "energic": 0, "relax": 5, "tag": "lavender"},
            {"text": "Confident, polished and powerful", "energic": 5, "relax": 1, "tag": "amber"},
            {"text": "Fresh, clean and energetic", "energic": 5, "relax": 0, "tag": "citrus"},
            {"text": "Romantic, soft and elegant", "energic": 2, "relax": 4, "tag": "floral"},
            {"text": "Mysterious, deep and luxurious", "energic": 3, "relax": 2, "tag": "oud"},
        ],
    },
    {
        "order": 2,
        "text": "Which real-life situation matters most for this recommendation?",
        "options": [
            {"text": "Daily wear", "energic": 2, "relax": 2, "tag": "fresh"},
            {"text": "Office, university or professional setting", "energic": 2, "relax": 3, "tag": "musk"},
            {"text": "Formal event or luxury evening", "energic": 3, "relax": 2, "tag": "amber"},
            {"text": "Date night or romantic evening", "energic": 2, "relax": 4, "tag": "vanilla"},
            {"text": "Wedding, party or special celebration", "energic": 4, "relax": 1, "tag": "floral"},
            {"text": "Gifting for someone else", "energic": 2, "relax": 2, "tag": "clean"},
        ],
    },
    {
        "order": 3,
        "text": "Which weather or season should the perfume suit best?",
        "options": [
            {"text": "Warm or sunny weather", "energic": 5, "relax": 1, "tag": "citrus"},
            {"text": "Cold weather or winter evenings", "energic": 1, "relax": 4, "tag": "amber"},
            {"text": "Rainy, damp or cloudy days", "energic": 1, "relax": 4, "tag": "woody"},
            {"text": "Mild everyday weather", "energic": 2, "relax": 2, "tag": "fresh"},
            {"text": "A versatile scent for all year", "energic": 2, "relax": 3, "tag": "musk"},
        ],
    },
    {
        "order": 4,
        "text": "Which fragrance feeling sounds closest to your taste?",
        "options": [
            {"text": "Warm, sweet and creamy", "energic": 1, "relax": 4, "tag": "vanilla"},
            {"text": "Cool, aquatic and airy", "energic": 4, "relax": 1, "tag": "aquatic"},
            {"text": "Clean, powdery and soft", "energic": 1, "relax": 4, "tag": "powdery"},
            {"text": "Deep, woody and smoky", "energic": 3, "relax": 2, "tag": "smoky"},
            {"text": "Green, fresh and natural", "energic": 4, "relax": 2, "tag": "green"},
        ],
    },
    {
        "order": 5,
        "text": "How often do you normally wear perfume?",
        "options": [
            {"text": "Daily", "energic": 3, "relax": 2, "tag": "fresh"},
            {"text": "Several times a week", "energic": 2, "relax": 2, "tag": "floral"},
            {"text": "Occasionally", "energic": 1, "relax": 2, "tag": "musk"},
            {"text": "Rarely, mostly for special occasions", "energic": 1, "relax": 3, "tag": "amber"},
        ],
    },
    {
        "order": 6,
        "text": "What budget should the recommendation system prioritise for you?",
        "options": [
            {"text": "Affordable everyday perfume under £80", "energic": 2, "relax": 2, "tag": "fresh"},
            {"text": "Mid-range perfume between £80 and £120", "energic": 2, "relax": 3, "tag": "musk"},
            {"text": "Premium perfume between £120 and £160", "energic": 3, "relax": 2, "tag": "amber"},
            {"text": "Luxury perfume over £160", "energic": 3, "relax": 2, "tag": "oud"},
            {"text": "No strict budget, show the best match", "energic": 2, "relax": 2, "tag": "floral"},
        ],
    },
    {
        "order": 7,
        "text": "Which notes do you most associate with relaxation and comfort?",
        "options": [
            {"text": "Lavender", "energic": 0, "relax": 5, "tag": "lavender"},
            {"text": "Vanilla", "energic": 1, "relax": 5, "tag": "vanilla"},
            {"text": "Rose or soft florals", "energic": 1, "relax": 4, "tag": "rose"},
            {"text": "Woody notes", "energic": 1, "relax": 4, "tag": "woody"},
            {"text": "Musk or powdery notes", "energic": 0, "relax": 5, "tag": "musk"},
        ],
    },
    {
        "order": 8,
        "text": "Which notes do you most associate with confidence and energy?",
        "options": [
            {"text": "Citrus", "energic": 5, "relax": 0, "tag": "citrus"},
            {"text": "Fresh or green notes", "energic": 5, "relax": 1, "tag": "fresh"},
            {"text": "Spicy notes", "energic": 5, "relax": 0, "tag": "spicy"},
            {"text": "Amber", "energic": 4, "relax": 1, "tag": "amber"},
            {"text": "Leather, oud or smoky notes", "energic": 4, "relax": 1, "tag": "leather"},
        ],
    },
    {
        "order": 9,
        "text": "Which notes should the recommendation system avoid for you?",
        "options": [
            {"text": "Very sweet notes such as heavy vanilla or sugar", "energic": 1, "relax": 1, "tag": "fresh"},
            {"text": "Heavy smoky, leather or oud notes", "energic": 1, "relax": 2, "tag": "floral"},
            {"text": "Sharp citrus or very fresh aquatic notes", "energic": 0, "relax": 3, "tag": "amber"},
            {"text": "Strong spicy or woody notes", "energic": 1, "relax": 2, "tag": "powdery"},
            {"text": "Nothing specific, I am open to different notes", "energic": 2, "relax": 2, "tag": "musk"},
        ],
    },
    {
        "order": 10,
        "text": "What should the recommendation system focus on most when ranking perfumes for you?",
        "options": [
            {"text": "Closest match to my personality style", "energic": 2, "relax": 3, "tag": "musk"},
            {"text": "Best match for my lifestyle, such as work, study, commuting or social life", "energic": 3, "relax": 2, "tag": "fresh"},
            {"text": "Similar style to brands or perfumes I already like", "energic": 2, "relax": 2, "tag": "amber"},
            {"text": "Strong performance: longevity, projection and value for money", "energic": 4, "relax": 1, "tag": "woody"},
            {"text": "A balanced match across mood, notes, occasion, season and budget", "energic": 3, "relax": 3, "tag": "floral"},
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
        make_legacy_survey_question_columns_compatible()

        for mood_name in ["Energic", "Relaxation"]:
            Mood.objects.get_or_create(name=mood_name)

        active_orders = [q["order"] for q in SEED_DATA]
        # Keep the live survey exactly aligned with this seed file.
        # This removes old question wording from earlier zip versions.
        SurveyQuestion.objects.exclude(order__in=active_orders).delete()

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
