from django.db import models
from survey.models import Mood

class Perfume(models.Model):
    name = models.CharField(max_length=120)
    brand = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)
    moods = models.ManyToManyField(Mood, related_name="perfumes", blank=True)

    def __str__(self):
        return f"{self.name} ({self.brand})" if self.brand else self.name
