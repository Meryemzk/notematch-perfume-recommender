# Safe migration for NoteMatch perfume price and scent fields.
# It checks existing database columns before adding them, so Render/PostgreSQL
# does not fail if a column was created during an earlier deployment attempt.
from django.db import migrations, models

SCENT_CHOICES = [
    ("citrus", "Citrus"), ("fresh", "Fresh"), ("floral", "Floral"), ("rose", "Rose"),
    ("jasmine", "Jasmine"), ("lavender", "Lavender"), ("vanilla", "Vanilla"),
    ("amber", "Amber"), ("woody", "Woody"), ("musk", "Musk"), ("spicy", "Spicy"),
    ("leather", "Leather"), ("fruity", "Fruity"), ("aquatic", "Aquatic"),
    ("powdery", "Powdery"), ("sweet", "Sweet"), ("oriental", "Oriental"),
    ("green", "Green"), ("tobacco", "Tobacco"), ("oud", "Oud"),
]


def add_field_if_missing(apps, schema_editor, model, field):
    table_name = model._meta.db_table
    existing_columns = {
        col.name for col in schema_editor.connection.introspection.get_table_description(
            schema_editor.connection.cursor(), table_name
        )
    }
    if field.name not in existing_columns:
        field.set_attributes_from_name(field.name)
        schema_editor.add_field(model, field)


def forwards(apps, schema_editor):
    Perfume = apps.get_model("perfumes", "Perfume")
    add_field_if_missing(apps, schema_editor, Perfume, models.DecimalField(name="price", max_digits=7, decimal_places=2, default=0))
    add_field_if_missing(apps, schema_editor, Perfume, models.CharField(name="scent_1", max_length=30, choices=SCENT_CHOICES, default="floral"))
    add_field_if_missing(apps, schema_editor, Perfume, models.CharField(name="scent_2", max_length=30, choices=SCENT_CHOICES, default="musk"))
    add_field_if_missing(apps, schema_editor, Perfume, models.CharField(name="scent_3", max_length=30, choices=SCENT_CHOICES, default="amber"))


class Migration(migrations.Migration):

    dependencies = [
        ("perfumes", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[migrations.RunPython(forwards, migrations.RunPython.noop)],
            state_operations=[
                migrations.AddField(
                    model_name="perfume",
                    name="price",
                    field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
                ),
                migrations.AddField(
                    model_name="perfume",
                    name="scent_1",
                    field=models.CharField(choices=SCENT_CHOICES, default="floral", max_length=30),
                ),
                migrations.AddField(
                    model_name="perfume",
                    name="scent_2",
                    field=models.CharField(choices=SCENT_CHOICES, default="musk", max_length=30),
                ),
                migrations.AddField(
                    model_name="perfume",
                    name="scent_3",
                    field=models.CharField(choices=SCENT_CHOICES, default="amber", max_length=30),
                ),
            ],
        )
    ]
