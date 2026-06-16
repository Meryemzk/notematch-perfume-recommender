from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("survey", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Perfume",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("brand", models.CharField(blank=True, max_length=120)),
                ("notes", models.TextField(blank=True)),
                ("moods", models.ManyToManyField(blank=True, related_name="perfumes", to="survey.mood")),
            ],
        ),
    ]
