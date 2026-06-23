from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("perfumes", "0003_ensure_price_scent_columns"),
        ("survey", "0002_guest_survey"),
    ]

    operations = [
        migrations.AddField(
            model_name="surveysubmission",
            name="price_range",
            field=models.CharField(choices=[("any", "Any price"), ("under_80", "Under £80"), ("80_120", "£80 - £120"), ("120_160", "£120 - £160"), ("160_plus", "£160+")], default="any", max_length=20),
        ),
        migrations.AddField(
            model_name="surveysubmission",
            name="favourite_perfume_1",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="survey_favourite_1", to="perfumes.perfume"),
        ),
        migrations.AddField(
            model_name="surveysubmission",
            name="favourite_perfume_2",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="survey_favourite_2", to="perfumes.perfume"),
        ),
        migrations.AddField(
            model_name="surveysubmission",
            name="favourite_perfume_3",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="survey_favourite_3", to="perfumes.perfume"),
        ),
    ]
