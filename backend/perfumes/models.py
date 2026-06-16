from django.db import models
from survey.models import Mood

class Perfume(models.Model):
    name = models.CharField(max_length=120)
    brand = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)
    description = models.TextField(blank=True)
    best_for = models.CharField(max_length=255, blank=True)
    boosts_mood = models.CharField(max_length=255, blank=True)
    moods = models.ManyToManyField(Mood, related_name="perfumes", blank=True)

    class Meta:
        ordering = ["brand", "name"]
        unique_together = ("brand", "name")

    def __str__(self):
        return f"{self.name} ({self.brand})" if self.brand else self.name
