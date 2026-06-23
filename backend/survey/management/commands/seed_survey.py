from django.core.management.base import BaseCommand
from django.db import transaction, connection

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


SEED_DATA = [
    {
        "order": 1,
        "text": "How do you want to feel after wearing your perfume today?",
        "options": [
            {"text": "Energised and confident", "energic": 3, "relax": 0, "tag": "fresh"},
            {"text": "Calm and relaxed", "energic": 0, "relax": 3, "tag": "musk"},
            {"text": "Romantic and soft", "energic": 1, "relax": 2, "tag": "floral"},
            {"text": "Powerful and noticeable", "energic": 3, "relax": 0, "tag": "spicy"},
        ],
    },
    {
        "order": 2,
        "text": "What is the main reason you are choosing a perfume?",
        "options": [
            {"text": "Daily use / work / university", "energic": 2, "relax": 1, "tag": "fresh"},
            {"text": "Date or romantic occasion", "energic": 1, "relax": 2, "tag": "floral"},
            {"text": "Evening, party or special event", "energic": 3, "relax": 0, "tag": "amber"},
            {"text": "Comfort, self-care or relaxing at home", "energic": 0, "relax": 3, "tag": "vanilla"},
        ],
    },
    {
        "order": 3,
        "text": "Which scent family attracts you most?",
        "options": [
            {"text": "Fresh or citrus", "energic": 3, "relax": 0, "tag": "citrus"},
            {"text": "Floral", "energic": 1, "relax": 2, "tag": "floral"},
            {"text": "Sweet vanilla or amber", "energic": 1, "relax": 2, "tag": "vanilla"},
            {"text": "Woody, leather or oud", "energic": 2, "relax": 1, "tag": "woody"},
        ],
    },
    {
        "order": 4,
        "text": "How strong should your perfume be?",
        "options": [
            {"text": "Light and clean", "energic": 1, "relax": 2, "tag": "musk"},
            {"text": "Medium and balanced", "energic": 2, "relax": 1, "tag": "floral"},
            {"text": "Strong and long-lasting", "energic": 3, "relax": 0, "tag": "amber"},
        ],
    },
    {
        "order": 5,
        "text": "Which season or weather do you imagine wearing it in?",
        "options": [
            {"text": "Spring / fresh weather", "energic": 2, "relax": 1, "tag": "floral"},
            {"text": "Summer / warm weather", "energic": 3, "relax": 0, "tag": "citrus"},
            {"text": "Autumn / cosy weather", "energic": 1, "relax": 2, "tag": "woody"},
            {"text": "Winter / cold weather", "energic": 1, "relax": 2, "tag": "amber"},
        ],
    },
    {
        "order": 6,
        "text": "Which description fits your personality best?",
        "options": [
            {"text": "Bright, social and energetic", "energic": 3, "relax": 0, "tag": "fruity"},
            {"text": "Elegant, romantic and soft", "energic": 1, "relax": 2, "tag": "rose"},
            {"text": "Calm, minimal and clean", "energic": 0, "relax": 3, "tag": "musk"},
            {"text": "Bold, confident and mysterious", "energic": 3, "relax": 0, "tag": "leather"},
        ],
    },
    {
        "order": 7,
        "text": "Which note would you choose first?",
        "options": [
            {"text": "Bergamot, lemon or orange", "energic": 3, "relax": 0, "tag": "citrus"},
            {"text": "Rose or jasmine", "energic": 1, "relax": 2, "tag": "jasmine"},
            {"text": "Vanilla or caramel", "energic": 1, "relax": 2, "tag": "vanilla"},
            {"text": "Cedar, sandalwood or leather", "energic": 2, "relax": 1, "tag": "woody"},
        ],
    },
    {
        "order": 8,
        "text": "What type of recommendation do you prefer?",
        "options": [
            {"text": "Popular best sellers", "energic": 2, "relax": 1, "tag": "fresh"},
            {"text": "Luxury and premium", "energic": 2, "relax": 1, "tag": "amber"},
            {"text": "Soft and easy to wear", "energic": 0, "relax": 3, "tag": "musk"},
            {"text": "Unique and memorable", "energic": 3, "relax": 0, "tag": "spicy"},
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

    @transaction.atomic
    def handle(self, *args, **options):
        drop_legacy_target_mood_column()

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

        from perfumes.models import Perfume

        created_perfumes = updated_perfumes = 0
        for name, brand, price, s1, s2, s3, moods in PERFUME_DATA:
            s1, s2, s3 = [SCENT_NORMALISE.get(s, s) for s in (s1, s2, s3)]
            perfume, created = Perfume.objects.get_or_create(name=name, defaults={"brand": brand})
            perfume.brand = brand
            perfume.price = price
            perfume.scent_1 = s1
            perfume.scent_2 = s2
            perfume.scent_3 = s3
            perfume.notes = f"Best-seller catalog item. Scent profile: {s1}, {s2}, {s3}."
            perfume.save()
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
