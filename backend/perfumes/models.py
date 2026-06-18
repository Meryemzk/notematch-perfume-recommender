from django.db import models
from survey.models import Mood


class Perfume(models.Model):
    GENDER_CHOICES = [
        ("female", "Female"),
        ("male", "Male"),
        ("unisex", "Unisex"),
    ]

    STYLE_CHOICES = [
        ("new", "New / Modern"),
        ("classic", "Classic"),
    ]

    name = models.CharField(max_length=120)
    brand = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)
    moods = models.ManyToManyField(Mood, related_name="perfumes", blank=True)

    # New preference fields used by the improved recommendation logic
    gender_category = models.CharField(max_length=20, choices=GENDER_CHOICES, default="unisex")
    style_category = models.CharField(max_length=20, choices=STYLE_CHOICES, default="new")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} ({self.brand})" if self.brand else self.name
