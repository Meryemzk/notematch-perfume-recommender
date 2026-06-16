# Generated manually for NoteMatch survey improvements
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ("survey", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="surveyoption",
            name="target_mood",
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
