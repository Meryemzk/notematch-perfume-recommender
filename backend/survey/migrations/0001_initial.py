from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Mood",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="SurveyQuestion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.CharField(max_length=255)),
                ("order", models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name="SurveySubmission",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("total_energic", models.IntegerField(default=0)),
                ("total_relax", models.IntegerField(default=0)),
                ("top_note_tags", models.CharField(blank=True, max_length=255)),
                ("result_mood", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="survey.mood")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="SurveyOption",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.CharField(max_length=255)),
                ("energic_points", models.IntegerField(default=0)),
                ("relax_points", models.IntegerField(default=0)),
                ("note_tag", models.CharField(blank=True, max_length=50)),
                ("question", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="options", to="survey.surveyquestion")),
            ],
        ),
        migrations.CreateModel(
            name="SurveyAnswer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("option", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="survey.surveyoption")),
                ("question", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="survey.surveyquestion")),
                ("submission", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="answers", to="survey.surveysubmission")),
            ],
        ),
    ]
