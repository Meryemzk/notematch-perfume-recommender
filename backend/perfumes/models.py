from django.db import models
from survey.models import Mood


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


class Perfume(models.Model):
    name = models.CharField(max_length=120)
    brand = models.CharField(max_length=120, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    scent_1 = models.CharField(max_length=30, choices=SCENT_CHOICES, default="floral")
    scent_2 = models.CharField(max_length=30, choices=SCENT_CHOICES, default="musk")
    scent_3 = models.CharField(max_length=30, choices=SCENT_CHOICES, default="amber")
    notes = models.TextField(blank=True, help_text="Extra description or note details")
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
        return ", ".join([self.scent_1, self.scent_2, self.scent_3, self.notes or ""]).lower()
