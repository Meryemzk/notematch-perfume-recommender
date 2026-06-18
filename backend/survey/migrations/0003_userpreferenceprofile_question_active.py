from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("survey", "0002_survey_preference_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="surveyquestion",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name="UserPreferenceProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("favourite_perfume_1", models.CharField(max_length=120)),
                ("favourite_perfume_2", models.CharField(max_length=120)),
                ("favourite_perfume_3", models.CharField(max_length=120)),
                ("preferred_gender", models.CharField(choices=[("female", "Female"), ("male", "Male"), ("unisex", "Unisex"), ("no_preference", "No preference")], default="no_preference", max_length=20)),
                ("style_preference", models.CharField(choices=[("new", "New / Modern"), ("classic", "Classic"), ("both", "Both")], default="both", max_length=20)),
                ("budget_range", models.CharField(choices=[("under_30", "Under £30"), ("30_60", "£30–£60"), ("60_100", "£60–£100"), ("over_100", "Over £100"), ("no_preference", "No preference")], default="no_preference", max_length=20)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="preference_profile", to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
