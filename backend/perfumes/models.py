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
    description = models.TextField(blank=True)
    moods = models.ManyToManyField(Mood, related_name="perfumes", blank=True)

    gender_category = models.CharField(max_length=20, choices=GENDER_CHOICES, default="unisex")
    style_category = models.CharField(max_length=20, choices=STYLE_CHOICES, default="new")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    price_source = models.CharField(max_length=120, default="Demo UK price book", blank=True)

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["brand", "name"]

    def __str__(self):
        return f"{self.name} ({self.brand})" if self.brand else self.name
