# Generated for NoteMatch catalogue/admin upgrade
from django.db import migrations, models


def normalise_name(name):
    return " ".join((name or "").upper().replace(".", "").split())


EXPLICIT = {
    "COCO MAD EDP 35ML CLS": "feminine", "BURBERRY HERO EDTV50ML": "masculine",
    "YSL LIBRE EDPV50ML": "feminine", "FLORA GORG ORCHID EDPV100": "feminine",
    "GUCCI BAMBOO EDTV75ML": "feminine", "FAHRENHEIT EDT V 100ML": "masculine",
    "MOMENT EDPV100ML": "feminine", "PARADOXE INT EDP RF50": "feminine",
    "BOSS THE SCENT M EDT100": "masculine", "YSL LIBRE INTNSE EDP30ML": "feminine",
    "GOOD GIRL EDP 80": "feminine", "RAB 1 MILL NIT ELIX PRF50": "masculine",
    "GA CODE LE PARFUM V50": "masculine", "CH LA BOMBA EDPA50": "feminine",
    "YSL MYSLF L ABSOLU PRF100": "masculine", "NO 5 EDP V 100ML CLS": "feminine",
    "MONTBLANC EXPLORER EDP200": "masculine", "B BOTTLED UNLTD EDT100": "masculine",
    "VLNTNO BIR UOMO INT EDP50": "masculine", "MONTBLANC EXPLORER EDP30": "masculine",
    "DIAMONDS W EDP V 100ML": "feminine", "EXPLORER EXTREME EDP100": "masculine",
    "SAUVAGE LE PARFUM 60ML": "masculine", "BLEU CHANEL EDTV50ML": "masculine",
    "TF BLK ORCHID EDP100": "unisex",
    "PARADOXE INT EDP RF90": "feminine", "PRADA PARADOXE EDPV30": "feminine",
    "MONTBLANC EXPLORER EDP60": "masculine", "COCO MADEM EDP V50ML": "feminine",
    "SAUVAGE LE PARFUM 100ML": "masculine", "HB BOTTLED PARFUM V50ML": "masculine",
    "MJ DAISY WILD EDPV100": "feminine", "JPG LE BEAU NARCIS EDP125": "masculine",
    "TF OMBRE LEATHER EDP50ML": "unisex", "MOSC TOYBOY EDP V 100ML": "unisex",
    "CH GG BLU POLKA PARAD EDP80": "feminine", "FLORA GORG ORCHID EDPV50": "feminine",
    "BOSS BOTT INFINITE EDP100": "masculine", "1 MILLION EDT V100ML": "masculine",
    "YSL MYSLF EDPR 100ML": "masculine", "GENTLEMAN SOCIETY EDP60": "masculine",
    "BOSS SCENT ABSLT M EDP100": "masculine", "JPG SCANDAL PH EDTV100ML": "masculine",
    "BLEU CHANEL EDPV150ML": "masculine", "ADG PROFONDO PRF100": "masculine",
    "RABANNE INVICTUS EDT100&TSX": "masculine", "VERSACE EROS EDPV100ML": "masculine",
    "EA STRONGER INTENS EDP50": "masculine", "SAUVAGE EDP200": "masculine",
    "BOSS BTTL SRK LAVEN EDP50": "masculine",
    "MJ DAISY LOVE EAU EDT50": "feminine", "RAB 1 MILL NIT ELX PRF100": "masculine",
    "BOSS BTTL SRK LAVN EDP100": "masculine", "PRADA PARADOXE EDPV50": "feminine",
    "YSL MYSLF EDP100&TS10X": "masculine", "BOSS BOTTLD ABSOLU EDP100": "masculine",
    "BOSS BOTTLED EDT100ML": "masculine", "BLEU CHANEL EDPV50ML": "masculine",
    "YSL Y EDP 100ML": "masculine", "GUCCI OUD INT EDPV90ML": "unisex",
    "GOOD GIRL EDP 50": "feminine", "ISSEY M EDT V 125ML": "masculine",
    "PRADA PARADME EDP30": "masculine", "EA STRONGER INTENS EDP100": "masculine",
    "BLEU CHANEL PARFUM 100": "masculine", "TF OMBRE LEATHER EDP100ML": "unisex",
    "JPG MALE EDT V 75ML": "masculine", "GUCCI BAMBOO EDP50ML": "feminine",
    "JOOP! EDT V 200ML": "masculine", "PRADA PARADOXE EDPV90": "feminine",
    "TOUCH M EDT V 100ML": "masculine", "VLTNO BIR UOMO INT EDP100": "masculine",
    "YSL LIBRE EDPV30ML": "feminine",
    "PRADA PARADIGME EDPV100": "masculine", "PRADA PARADIGME EDP50": "masculine",
    "BOSS BOTT NGT EDT200ML": "masculine", "INVIC VICT ELIX PARFUM 100": "masculine",
    "DIOR SAUVAGE EDP100": "masculine", "1 MILLION LUCKY EDT100": "masculine",
    "GG ESSENCE PH EDT90": "masculine", "V DYLAN BLUE EDT100ML": "masculine",
    "DIOR SAUVAGE EDP60": "masculine", "MONTBLANC EXPLORER EDP100": "masculine",
    "SAUVAGE ELIX 100ML": "masculine", "YSL MYSLF EDPRFA60": "masculine",
    "DIOR SAUVAGE EDT100ML": "masculine", "EA STRONGER YOU EDT150": "masculine",
    "BLEU CHANEL EDPV100ML": "masculine", "JPG LE MALE PARFUM EDP75": "masculine",
    "LA VIE EST BELLE EDP100ML": "feminine", "BOSS BOTT TONIC EDT100ML": "masculine",
    "BAD BOY EDT V50ML": "masculine", "DIOR SAUVAGE EDT60ML": "masculine",
    "RABANNE 1 MILLION EDT50&TSX": "masculine", "COCO MADEM EDPV100ML": "feminine",
    "PHANTOM EDT V100ML": "masculine", "DIOR SAUVAGE ELIX60ML": "masculine",
}


def infer_category(name):
    n = normalise_name(name)
    if n in EXPLICIT:
        return EXPLICIT[n]
    if any(k in n for k in ["LIBRE", "COCO", "PARADOXE", "FLORA", "GOOD GIRL", "DAISY", "LA VIE", "BAMBOO", "NO 5", "DIAMONDS W", "LA BOMBA"]):
        return "feminine"
    if any(k in n for k in ["OMBRE LEATHER", "BLK ORCHID", "BLACK ORCHID", "GUCCI OUD", "TOYBOY"]):
        return "unisex"
    return "masculine" if any(k in n for k in ["SAUVAGE", "BOSS", "BLEU CHANEL", "EXPLORER", "HERO", "MILLION", "MYSLF", "Y EDP", "UOMO", "LE MALE", "BAD BOY", "FAHRENHEIT", "BOTTLED", "BOTT", "BTTL"]) else "unisex"


def forwards(apps, schema_editor):
    Perfume = apps.get_model("perfumes", "Perfume")
    for perfume in Perfume.objects.all():
        perfume.gender_category = infer_category(perfume.name)
        if not perfume.description:
            perfume.description = perfume.notes or "Best-seller catalogue item."
        perfume.save(update_fields=["gender_category", "description"])


def add_columns_if_missing(apps, schema_editor):
    table = "perfumes_perfume"
    vendor = schema_editor.connection.vendor
    with schema_editor.connection.cursor() as cursor:
        existing = {col.name for col in schema_editor.connection.introspection.get_table_description(cursor, table)}
        def add(column, sql_type):
            if column in existing:
                return
            if vendor == "postgresql":
                cursor.execute(f'ALTER TABLE "{table}" ADD COLUMN "{column}" {sql_type}')
            else:
                cursor.execute(f'ALTER TABLE "{table}" ADD COLUMN "{column}" {sql_type}')
            existing.add(column)
        add("gender_category", "varchar(20) DEFAULT 'unisex' NOT NULL")
        add("image_url", "varchar(200) DEFAULT '' NOT NULL")
        add("description", "text DEFAULT '' NOT NULL")
        add("suitable_season", "varchar(20) DEFAULT 'all' NOT NULL")
        add("occasion", "varchar(20) DEFAULT 'daily' NOT NULL")
        add("longevity", "smallint DEFAULT 7 NOT NULL")
        add("projection", "smallint DEFAULT 6 NOT NULL")
        add("sillage", "smallint DEFAULT 6 NOT NULL")
        add("rating", "decimal(3,1) DEFAULT 4.5 NOT NULL")
        add("country_of_origin", "varchar(80) DEFAULT '' NOT NULL")
        add("year_released", "smallint NULL")
        add("availability_status", "varchar(120) DEFAULT 'Available' NOT NULL")
        add("purchase_link", "varchar(200) DEFAULT '' NOT NULL")
        add("retailer", "varchar(120) DEFAULT '' NOT NULL")


class Migration(migrations.Migration):
    dependencies = [("perfumes", "0007_repair_render_legacy_columns_final")]
    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[migrations.RunPython(add_columns_if_missing, migrations.RunPython.noop)],
            state_operations=[
                migrations.AddField("perfume", "gender_category", models.CharField(choices=[("feminine", "Feminine (W / ladies)"), ("masculine", "Masculine (M / men)"), ("unisex", "Unisex")], db_index=True, default="unisex", max_length=20)),
                migrations.AddField("perfume", "image_url", models.URLField(blank=True, help_text="Optional product image URL")),
                migrations.AddField("perfume", "description", models.TextField(blank=True)),
                migrations.AddField("perfume", "suitable_season", models.CharField(choices=[("all", "All year"), ("spring", "Spring"), ("summer", "Summer"), ("autumn", "Autumn"), ("winter", "Winter"), ("rainy", "Rainy weather")], default="all", max_length=20)),
                migrations.AddField("perfume", "occasion", models.CharField(choices=[("daily", "Daily wear"), ("office", "Office / work"), ("formal", "Formal event"), ("date", "Date night"), ("wedding", "Wedding guest"), ("party", "Party / evening"), ("commute", "Commuting"), ("weekend", "Casual weekend"), ("gift", "Gifting")], default="daily", max_length=20)),
                migrations.AddField("perfume", "longevity", models.PositiveSmallIntegerField(default=7, help_text="1-10 score")),
                migrations.AddField("perfume", "projection", models.PositiveSmallIntegerField(default=6, help_text="1-10 score")),
                migrations.AddField("perfume", "sillage", models.PositiveSmallIntegerField(default=6, help_text="1-10 score")),
                migrations.AddField("perfume", "rating", models.DecimalField(decimal_places=1, default=4.5, max_digits=3)),
                migrations.AddField("perfume", "country_of_origin", models.CharField(blank=True, max_length=80)),
                migrations.AddField("perfume", "year_released", models.PositiveSmallIntegerField(blank=True, null=True)),
                migrations.AddField("perfume", "availability_status", models.CharField(default="Available", max_length=120)),
                migrations.AddField("perfume", "purchase_link", models.URLField(blank=True)),
                migrations.AddField("perfume", "retailer", models.CharField(blank=True, help_text="Optional stockist or retailer", max_length=120)),
            ],
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
