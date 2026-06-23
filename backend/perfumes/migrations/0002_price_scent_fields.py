# Generated for NoteMatch improvements
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("perfumes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="perfume",
            name="price",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AddField(
            model_name="perfume",
            name="scent_1",
            field=models.CharField(choices=[("citrus", "Citrus"), ("fresh", "Fresh"), ("floral", "Floral"), ("rose", "Rose"), ("jasmine", "Jasmine"), ("lavender", "Lavender"), ("vanilla", "Vanilla"), ("amber", "Amber"), ("woody", "Woody"), ("musk", "Musk"), ("spicy", "Spicy"), ("leather", "Leather"), ("fruity", "Fruity"), ("aquatic", "Aquatic"), ("powdery", "Powdery"), ("sweet", "Sweet"), ("oriental", "Oriental"), ("green", "Green"), ("tobacco", "Tobacco"), ("oud", "Oud")], default="floral", max_length=30),
        ),
        migrations.AddField(
            model_name="perfume",
            name="scent_2",
            field=models.CharField(choices=[("citrus", "Citrus"), ("fresh", "Fresh"), ("floral", "Floral"), ("rose", "Rose"), ("jasmine", "Jasmine"), ("lavender", "Lavender"), ("vanilla", "Vanilla"), ("amber", "Amber"), ("woody", "Woody"), ("musk", "Musk"), ("spicy", "Spicy"), ("leather", "Leather"), ("fruity", "Fruity"), ("aquatic", "Aquatic"), ("powdery", "Powdery"), ("sweet", "Sweet"), ("oriental", "Oriental"), ("green", "Green"), ("tobacco", "Tobacco"), ("oud", "Oud")], default="musk", max_length=30),
        ),
        migrations.AddField(
            model_name="perfume",
            name="scent_3",
            field=models.CharField(choices=[("citrus", "Citrus"), ("fresh", "Fresh"), ("floral", "Floral"), ("rose", "Rose"), ("jasmine", "Jasmine"), ("lavender", "Lavender"), ("vanilla", "Vanilla"), ("amber", "Amber"), ("woody", "Woody"), ("musk", "Musk"), ("spicy", "Spicy"), ("leather", "Leather"), ("fruity", "Fruity"), ("aquatic", "Aquatic"), ("powdery", "Powdery"), ("sweet", "Sweet"), ("oriental", "Oriental"), ("green", "Green"), ("tobacco", "Tobacco"), ("oud", "Oud")], default="amber", max_length=30),
        ),
    ]
