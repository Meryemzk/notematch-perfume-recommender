from django.db import migrations, models


def add_column_if_missing(apps, schema_editor):
    table = "survey_surveysubmission"
    column = "selected_gender_style"
    with schema_editor.connection.cursor() as cursor:
        existing = {col.name for col in schema_editor.connection.introspection.get_table_description(cursor, table)}
        if column in existing:
            return
        cursor.execute(f'ALTER TABLE "{table}" ADD COLUMN "{column}" varchar(20) DEFAULT \'no_preference\' NOT NULL')


class Migration(migrations.Migration):
    dependencies = [("survey", "0004_drop_legacy_target_mood")]
    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[migrations.RunPython(add_column_if_missing, migrations.RunPython.noop)],
            state_operations=[
                migrations.AddField(
                    model_name="surveysubmission",
                    name="selected_gender_style",
                    field=models.CharField(
                        choices=[
                            ("feminine", "Feminine / W only"),
                            ("masculine", "Masculine / M only"),
                            ("unisex", "Unisex only"),
                            ("no_preference", "No preference"),
                        ],
                        db_index=True,
                        default="no_preference",
                        max_length=20,
                    ),
                ),
            ],
        ),
    ]
