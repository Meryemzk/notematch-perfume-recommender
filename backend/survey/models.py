from django.conf import settings
from django.db import models


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
    Stores both mood answers and the new preference-profile inputs.
    """
    GENDER_PREFERENCE_CHOICES = [
        ("female", "Female"),
        ("male", "Male"),
        ("unisex", "Unisex"),
        ("no_preference", "No preference"),
    ]

    STYLE_PREFERENCE_CHOICES = [
        ("new", "New / Modern"),
        ("classic", "Classic"),
        ("both", "Both"),
    ]

    BUDGET_CHOICES = [
        ("under_30", "Under £30"),
        ("30_60", "£30–£60"),
        ("60_100", "£60–£100"),
        ("over_100", "Over £100"),
        ("no_preference", "No preference"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    total_energic = models.IntegerField(default=0)
    total_relax = models.IntegerField(default=0)
    result_mood = models.ForeignKey(Mood, on_delete=models.SET_NULL, null=True, blank=True)

    # store top note tags as comma-separated (simple)
    top_note_tags = models.CharField(max_length=255, blank=True)

    # New personal preference inputs
    favourite_perfume_1 = models.CharField(max_length=120, blank=True)
    favourite_perfume_2 = models.CharField(max_length=120, blank=True)
    favourite_perfume_3 = models.CharField(max_length=120, blank=True)
    preferred_gender = models.CharField(max_length=20, choices=GENDER_PREFERENCE_CHOICES, default="no_preference")
    style_preference = models.CharField(max_length=20, choices=STYLE_PREFERENCE_CHOICES, default="both")
    budget_range = models.CharField(max_length=20, choices=BUDGET_CHOICES, default="no_preference")

    def __str__(self):
        return f"{self.user} @ {self.created_at}"


class SurveyAnswer(models.Model):
    submission = models.ForeignKey(SurveySubmission, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    option = models.ForeignKey(SurveyOption, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.submission.user} -> {self.question.order}"
