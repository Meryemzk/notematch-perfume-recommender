# Generated manually for NoteMatch deployment improvements
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ("perfumes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="perfume",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="perfume",
            name="best_for",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="perfume",
            name="boosts_mood",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name="perfume",
            unique_together={("brand", "name")},
        ),
    ]
