from django.conf import settings
from django.db import models


class Mood(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class UserPreferenceProfile(models.Model):
    """Saved long-term perfume preferences for each registered user.

    These values are used by the recommendation engine until the user chooses
    to update them from the profile page or from the survey form.
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

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="preference_profile")
    favourite_perfume_1 = models.CharField(max_length=120)
    favourite_perfume_2 = models.CharField(max_length=120)
    favourite_perfume_3 = models.CharField(max_length=120)
    preferred_gender = models.CharField(max_length=20, choices=GENDER_PREFERENCE_CHOICES, default="no_preference")
    style_preference = models.CharField(max_length=20, choices=STYLE_PREFERENCE_CHOICES, default="both")
    budget_range = models.CharField(max_length=20, choices=BUDGET_CHOICES, default="no_preference")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preference profile for {self.user}"

    @property
    def favourite_names(self):
        return [self.favourite_perfume_1, self.favourite_perfume_2, self.favourite_perfume_3]


class SurveyQuestion(models.Model):
    """A question shown in the mood and scent survey."""
    text = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.order}. {self.text}"


class SurveyOption(models.Model):
    """Options for each question.

    Each option contributes points to energic/relaxation and an optional note tag.
    """
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=255)
    energic_points = models.IntegerField(default=0)
    relax_points = models.IntegerField(default=0)
    note_tag = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.question.order}) {self.text}"


class SurveySubmission(models.Model):
    """One submission per time a user takes the survey.

    This stores the mood quiz result and a snapshot of the saved preference
    profile used at the time of recommendation.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # Consent and ethics evidence for the academic project
    age_confirmed = models.BooleanField(default=False)
    consent_given = models.BooleanField(default=False)
    privacy_acknowledged = models.BooleanField(default=False)

    total_energic = models.IntegerField(default=0)
    total_relax = models.IntegerField(default=0)
    result_mood = models.ForeignKey(Mood, on_delete=models.SET_NULL, null=True, blank=True)
    top_note_tags = models.CharField(max_length=255, blank=True)

    # Snapshot of the saved preference profile used for this result
    favourite_perfume_1 = models.CharField(max_length=120, blank=True)
    favourite_perfume_2 = models.CharField(max_length=120, blank=True)
    favourite_perfume_3 = models.CharField(max_length=120, blank=True)
    preferred_gender = models.CharField(max_length=20, choices=UserPreferenceProfile.GENDER_PREFERENCE_CHOICES, default="no_preference")
    style_preference = models.CharField(max_length=20, choices=UserPreferenceProfile.STYLE_PREFERENCE_CHOICES, default="both")
    budget_range = models.CharField(max_length=20, choices=UserPreferenceProfile.BUDGET_CHOICES, default="no_preference")

    def __str__(self):
        return f"{self.user} @ {self.created_at}"

    @property
    def favourite_names(self):
        return [self.favourite_perfume_1, self.favourite_perfume_2, self.favourite_perfume_3]


class SurveyAnswer(models.Model):
    submission = models.ForeignKey(SurveySubmission, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    option = models.ForeignKey(SurveyOption, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.submission.user} -> {self.question.order}"


class RecommendationFeedback(models.Model):
    """User feedback after seeing recommendation results.

    These records can be used later as training data for a machine-learning
    recommendation model.
    """
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    submission = models.OneToOneField(SurveySubmission, on_delete=models.CASCADE, related_name="feedback")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    was_useful = models.BooleanField(default=True)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user} - {self.rating}/5"
