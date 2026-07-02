from django.db import models
from survey.models import Mood


GENDER_CATEGORY_CHOICES = [
    ("feminine", "Feminine (W / ladies)"),
    ("masculine", "Masculine (M / men)"),
    ("unisex", "Unisex"),
]

SEASON_CHOICES = [
    ("all", "All year"), ("spring", "Spring"), ("summer", "Summer"),
    ("autumn", "Autumn"), ("winter", "Winter"), ("rainy", "Rainy weather"),
]

OCCASION_CHOICES = [
    ("daily", "Daily wear"), ("office", "Office / work"), ("formal", "Formal event"),
    ("date", "Date night"), ("wedding", "Wedding guest"), ("party", "Party / evening"),
    ("commute", "Commuting"), ("weekend", "Casual weekend"), ("gift", "Gifting"),
]


SCENT_CHOICES = [
    ("citrus", "Citrus"),
    ("fresh", "Fresh"),
    ("floral", "Floral"),
    ("rose", "Rose"),
    ("jasmine", "Jasmine"),
    ("lavender", "Lavender"),
    ("vanilla", "Vanilla"),
    ("amber", "Amber"),
    ("woody", "Woody"),
    ("musk", "Musk"),
    ("spicy", "Spicy"),
    ("leather", "Leather"),
    ("fruity", "Fruity"),
    ("aquatic", "Aquatic"),
    ("powdery", "Powdery"),
    ("sweet", "Sweet"),
    ("oriental", "Oriental"),
    ("green", "Green"),
    ("tobacco", "Tobacco"),
    ("oud", "Oud"),
]



# Exact category labels taken from the annotated best-seller sheets supplied for the project.
# W = feminine, M = masculine, unisex = suitable for any style preference.
EXPLICIT_GENDER_CATEGORY_BY_NAME = {
    # Sheet W-26 and annotated best-seller pages
    "COCO MAD EDP 35ML CLS": "feminine",
    "BURBERRY HERO EDTV50ML": "masculine",
    "YSL LIBRE EDPV50ML": "feminine",
    "FLORA GORG ORCHID EDPV100": "feminine",
    "GUCCI BAMBOO EDTV75ML": "feminine",
    "FAHRENHEIT EDT V 100ML": "masculine",
    "MOMENT EDPV100ML": "feminine",
    "PARADOXE INT EDP RF50": "feminine",
    "BOSS THE SCENT M EDT100": "masculine",
    "YSL LIBRE INTNSE EDP30ML": "feminine",
    "GOOD GIRL EDP 80": "feminine",
    "RAB 1 MILL NIT ELIX PRF50": "masculine",
    "GA CODE LE PARFUM V50": "masculine",
    "CH LA BOMBA EDPA50": "feminine",
    "YSL MYSLF L ABSOLU PRF100": "masculine",
    "NO 5 EDP V 100ML CLS": "feminine",
    "MONTBLANC EXPLORER EDP200": "masculine",
    "B BOTTLED UNLTD EDT100": "masculine",
    "VLNTNO BIR UOMO INT EDP50": "masculine",
    "MONTBLANC EXPLORER EDP30": "masculine",
    "DIAMONDS W EDP V 100ML": "feminine",
    "EXPLORER EXTREME EDP100": "masculine",
    "SAUVAGE LE PARFUM 60ML": "masculine",
    "BLEU CHANEL EDTV50ML": "masculine",
    "TF BLK ORCHID EDP100": "unisex",

    "PARADOXE INT EDP RF90": "feminine",
    "PRADA PARADOXE EDPV30": "feminine",
    "MONTBLANC EXPLORER EDP60": "masculine",
    "COCO MADEM EDP V50ML": "feminine",
    "SAUVAGE LE PARFUM 100ML": "masculine",
    "HB BOTTLED PARFUM V50ML": "masculine",
    "MJ DAISY WILD EDPV100": "feminine",
    "JPG LE BEAU NARCIS EDP125": "masculine",
    "TF OMBRE LEATHER EDP50ML": "unisex",
    "MOSC TOYBOY EDP V 100ML": "unisex",
    "CH GG BLU POLKA PARAD EDP80": "feminine",
    "FLORA GORG ORCHID EDPV50": "feminine",
    "BOSS BOTT INFINITE EDP100": "masculine",
    "1 MILLION EDT V100ML": "masculine",
    "YSL MYSLF EDPR 100ML": "masculine",
    "GENTLEMAN SOCIETY EDP60": "masculine",
    "BOSS SCENT ABSLT M EDP100": "masculine",
    "JPG SCANDAL PH EDTV100ML": "masculine",
    "BLEU CHANEL EDPV150ML": "masculine",
    "ADG PROFONDO PRF100": "masculine",
    "RABANNE INVICTUS EDT100&TSX": "masculine",
    "VERSACE EROS EDPV100ML": "masculine",
    "EA STRONGER INTENS EDP50": "masculine",
    "SAUVAGE EDP200": "masculine",
    "BOSS BTTL SRK LAVEN EDP50": "masculine",

    "MJ DAISY LOVE EAU EDT50": "feminine",
    "RAB 1 MILL NIT ELX PRF100": "masculine",
    "BOSS BTTL SRK LAVN EDP100": "masculine",
    "PRADA PARADOXE EDPV50": "feminine",
    "YSL MYSLF EDP100&TS10X": "masculine",
    "BOSS BOTTLD ABSOLU EDP100": "masculine",
    "BOSS BOTTLED EDT100ML": "masculine",
    "BLEU CHANEL EDPV50ML": "masculine",
    "YSL Y EDP 100ML": "masculine",
    "GUCCI OUD INT EDPV90ML": "unisex",
    "GOOD GIRL EDP 50": "feminine",
    "ISSEY M EDT V 125ML": "masculine",
    "PRADA PARADME EDP30": "masculine",
    "EA STRONGER INTENS EDP100": "masculine",
    "BLEU CHANEL PARFUM 100": "masculine",
    "TF OMBRE LEATHER EDP100ML": "unisex",
    "JPG MALE EDT V 75ML": "masculine",
    "GUCCI BAMBOO EDP50ML": "feminine",
    "JOOP! EDT V 200ML": "masculine",
    "PRADA PARADOXE EDPV90": "feminine",
    "TOUCH M EDT V 100ML": "masculine",
    "VLTNO BIR UOMO INT EDP100": "masculine",
    "YSL LIBRE EDPV30ML": "feminine",

    "PRADA PARADIGME EDPV100": "masculine",
    "PRADA PARADIGME EDP50": "masculine",
    "BOSS BOTT NGT EDT200ML": "masculine",
    "INVIC VICT ELIX PARFUM 100": "masculine",
    "DIOR SAUVAGE EDP100": "masculine",
    "1 MILLION LUCKY EDT100": "masculine",
    "GG ESSENCE PH EDT90": "masculine",
    "V DYLAN BLUE EDT100ML": "masculine",
    "DIOR SAUVAGE EDP60": "masculine",
    "MONTBLANC EXPLORER EDP100": "masculine",
    "SAUVAGE ELIX 100ML": "masculine",
    "YSL MYSLF EDPRFA60": "masculine",
    "DIOR SAUVAGE EDT100ML": "masculine",
    "EA STRONGER YOU EDT150": "masculine",
    "BLEU CHANEL EDPV100ML": "masculine",
    "JPG LE MALE PARFUM EDP75": "masculine",
    "LA VIE EST BELLE EDP100ML": "feminine",
    "BOSS BOTT TONIC EDT100ML": "masculine",
    "BAD BOY EDT V50ML": "masculine",
    "DIOR SAUVAGE EDT60ML": "masculine",
    "RABANNE 1 MILLION EDT50&TSX": "masculine",
    "COCO MADEM EDPV100ML": "feminine",
    "PHANTOM EDT V100ML": "masculine",
    "DIOR SAUVAGE ELIX60ML": "masculine",
}


def _normalise_perfume_name(name):
    return " ".join((name or "").upper().replace(".", "").split())


FEMININE_NAME_KEYWORDS = [
    "LIBRE", "COCO", "MADEM", "PARADOXE", "PARADOX", "PARADME", "FLORA",
    "GOOD GIRL", "DAISY", "LA VIE", "BAMBOO", "NO 5", "DIAMONDS W",
    "MOMENT", "LA BOMBA", "GG ESSENCE", "GG BLU", "SCANDAL PH", "MISS",
]

MASCULINE_NAME_KEYWORDS = [
    "SAUVAGE", "BLEU CHANEL", "BOSS", "BOTTLED", "THE SCENT M", "HERO",
    "EXPLORER", "MONTBLANC", "1 MILLION", "INVICT", "EROS", "LE MALE",
    "BAD BOY", "FAHRENHEIT", "MYSLF", "Y EDP", "DYLAN BLUE", "PROFONDO",
    "GENTLEMAN", "UOMO", "STRONGER YOU", "PHANTOM", "TOUCH M", "LE BEAU",
    "JPG MALE", "PRADA PARADIGME", "PARADIGME", "B BOTTLED", "ADG", "BTTL", "BOTT",
]

UNISEX_NAME_KEYWORDS = [
    "BLACK ORCHID", "BLK ORCHID", "OMBRE LEATHER", "GUCCI OUD", "OUD INT",
    "TOYBOY",
]


def infer_perfume_gender_category(perfume):
    """Return feminine, masculine, or unisex using catalogue naming and notes.

    The original undergraduate project does not store a dedicated gender field,
    so this keeps the fix migration-free and safe for Render. The rules favour
    explicit best-seller names first, then use note families as a fallback.
    """
    name = _normalise_perfume_name(perfume.name)
    notes = {perfume.scent_1, perfume.scent_2, perfume.scent_3}

    explicit_category = EXPLICIT_GENDER_CATEGORY_BY_NAME.get(name)
    if explicit_category:
        return explicit_category

    if any(keyword in name for keyword in UNISEX_NAME_KEYWORDS):
        return "unisex"
    if any(keyword in name for keyword in FEMININE_NAME_KEYWORDS):
        return "feminine"
    if any(keyword in name for keyword in MASCULINE_NAME_KEYWORDS):
        return "masculine"

    feminine_notes = {"floral", "rose", "jasmine", "fruity", "powdery", "sweet"}
    masculine_notes = {"leather", "tobacco", "woody", "spicy", "aquatic"}
    unisex_notes = {"amber", "musk", "oud", "green", "citrus", "fresh", "vanilla", "oriental"}

    if notes & feminine_notes and not notes & {"leather", "tobacco"}:
        return "feminine"
    if notes & masculine_notes and len(notes & feminine_notes) == 0:
        return "masculine"
    if notes & unisex_notes:
        return "unisex"
    return "unisex"


def perfume_gender_label(category):
    return {
        "feminine": "Feminine",
        "masculine": "Masculine",
        "unisex": "Unisex",
    }.get(category, "Unisex")


class Perfume(models.Model):
    name = models.CharField(max_length=120)
    brand = models.CharField(max_length=120, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    # This is now a real database field so the admin can control recommendation category.
    # W on your sheets = feminine, M = masculine, unisex = separate mixed category.
    gender_category = models.CharField(max_length=20, choices=GENDER_CATEGORY_CHOICES, default="unisex", db_index=True)

    image_url = models.URLField(blank=True, help_text="Optional product image URL")
    description = models.TextField(blank=True)
    scent_1 = models.CharField(max_length=30, choices=SCENT_CHOICES, default="floral", verbose_name="Top note")
    scent_2 = models.CharField(max_length=30, choices=SCENT_CHOICES, default="musk", verbose_name="Heart note")
    scent_3 = models.CharField(max_length=30, choices=SCENT_CHOICES, default="amber", verbose_name="Base note")
    notes = models.TextField(blank=True, help_text="Extra description or note details")
    suitable_season = models.CharField(max_length=20, choices=SEASON_CHOICES, default="all")
    occasion = models.CharField(max_length=20, choices=OCCASION_CHOICES, default="daily")
    longevity = models.PositiveSmallIntegerField(default=7, help_text="1-10 score")
    projection = models.PositiveSmallIntegerField(default=6, help_text="1-10 score")
    sillage = models.PositiveSmallIntegerField(default=6, help_text="1-10 score")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    country_of_origin = models.CharField(max_length=80, blank=True)
    year_released = models.PositiveSmallIntegerField(null=True, blank=True)
    availability_status = models.CharField(max_length=120, default="Available")
    purchase_link = models.URLField(blank=True)
    retailer = models.CharField(max_length=120, blank=True, help_text="Optional stockist or retailer")
    moods = models.ManyToManyField(Mood, related_name="perfumes", blank=True)

    class Meta:
        ordering = ["brand", "name"]

    def __str__(self):
        return f"{self.name} ({self.brand})" if self.brand else self.name

    @property
    def scent_list(self):
        return [self.get_scent_1_display(), self.get_scent_2_display(), self.get_scent_3_display()]

    @property
    def searchable_notes(self):
        return ", ".join([self.scent_1, self.scent_2, self.scent_3, self.notes or "", self.description or ""]).lower()

    @property
    def gender_display(self):
        return perfume_gender_label(self.gender_category)
