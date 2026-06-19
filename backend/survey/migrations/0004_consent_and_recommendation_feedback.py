from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("survey", "0003_userpreferenceprofile_question_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="surveysubmission",
            name="age_confirmed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="surveysubmission",
            name="consent_given",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="surveysubmission",
            name="privacy_acknowledged",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="RecommendationFeedback",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("was_useful", models.BooleanField(default=True)),
                ("rating", models.PositiveSmallIntegerField(choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")], default=5)),
                ("comment", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("submission", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="feedback", to="survey.surveysubmission")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
