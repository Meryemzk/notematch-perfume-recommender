from django.conf import settings
from django.db import models


PRICE_RANGE_CHOICES = [
    ("any", "Any price"),
    ("under_80", "Under £80"),
    ("80_120", "£80 - £120"),
    ("120_160", "£120 - £160"),
    ("160_plus", "£160+"),
]


class Mood(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class SurveyQuestion(models.Model):
    """
    A question shown in the survey.
    Example: "When do you mostly use perfume?"
    """
    text = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.order}. {self.text}"


class SurveyOption(models.Model):
    """
    Options for each question.
    Each option can contribute points to energic/relaxation + optional note tag.
    """
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=255)

    # scoring
    energic_points = models.IntegerField(default=0)
    relax_points = models.IntegerField(default=0)

    # optional perfume note tag that user likes (e.g. citrus, lavender, vanilla)
    note_tag = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.question.order}) {self.text}"


class SurveySubmission(models.Model):
    """
    One submission per time user takes the survey.
    Guests can use the survey; logged-in users can save their results.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    total_energic = models.IntegerField(default=0)
    total_relax = models.IntegerField(default=0)
    result_mood = models.ForeignKey(Mood, on_delete=models.SET_NULL, null=True, blank=True)

    # store top note tags as comma-separated (simple)
    top_note_tags = models.CharField(max_length=255, blank=True)

    price_range = models.CharField(max_length=20, choices=PRICE_RANGE_CHOICES, default="any")
    favourite_perfume_1 = models.ForeignKey("perfumes.Perfume", on_delete=models.SET_NULL, null=True, blank=True, related_name="survey_favourite_1")
    favourite_perfume_2 = models.ForeignKey("perfumes.Perfume", on_delete=models.SET_NULL, null=True, blank=True, related_name="survey_favourite_2")
    favourite_perfume_3 = models.ForeignKey("perfumes.Perfume", on_delete=models.SET_NULL, null=True, blank=True, related_name="survey_favourite_3")

    def __str__(self):
        return f"{self.user or 'Guest'} @ {self.created_at}"

    @property
    def favourite_perfumes(self):
        return [p for p in [self.favourite_perfume_1, self.favourite_perfume_2, self.favourite_perfume_3] if p]


class SurveyAnswer(models.Model):
    submission = models.ForeignKey(SurveySubmission, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    option = models.ForeignKey(SurveyOption, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.submission.user or 'Guest'} -> {self.question.order}"
