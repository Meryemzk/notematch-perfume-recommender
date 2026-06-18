from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("perfumes", "0002_perfume_preference_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="perfume",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="perfume",
            name="price_source",
            field=models.CharField(blank=True, default="Demo UK price book", max_length=120),
        ),
        migrations.AddField(
            model_name="perfume",
            name="is_featured",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="perfume",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="perfume",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="perfume",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterModelOptions(
            name="perfume",
            options={"ordering": ["brand", "name"]},
        ),
    ]
