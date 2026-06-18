from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("perfumes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="perfume",
            name="gender_category",
            field=models.CharField(
                choices=[("female", "Female"), ("male", "Male"), ("unisex", "Unisex")],
                default="unisex",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="perfume",
            name="style_category",
            field=models.CharField(
                choices=[("new", "New / Modern"), ("classic", "Classic")],
                default="new",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="perfume",
            name="price",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]
