from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("survey", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="surveysubmission",
            name="favourite_perfume_1",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name="surveysubmission",
            name="favourite_perfume_2",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name="surveysubmission",
            name="favourite_perfume_3",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name="surveysubmission",
            name="preferred_gender",
            field=models.CharField(
                choices=[("female", "Female"), ("male", "Male"), ("unisex", "Unisex"), ("no_preference", "No preference")],
                default="no_preference",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="surveysubmission",
            name="style_preference",
            field=models.CharField(
                choices=[("new", "New / Modern"), ("classic", "Classic"), ("both", "Both")],
                default="both",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="surveysubmission",
            name="budget_range",
            field=models.CharField(
                choices=[("under_30", "Under £30"), ("30_60", "£30–£60"), ("60_100", "£60–£100"), ("over_100", "Over £100"), ("no_preference", "No preference")],
                default="no_preference",
                max_length=20,
            ),
        ),
    ]
