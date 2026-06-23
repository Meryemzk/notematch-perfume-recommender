from django.db import migrations, connection


def drop_legacy_target_mood(apps, schema_editor):
    """
    Older Render databases may still have a legacy NOT NULL column named
    target_mood on survey_surveyoption. The current model does not use it.
    Leaving it in place breaks seed_survey because Django does not insert a
    value for that old column. Drop it safely if it exists.
    """
    table_name = "survey_surveyoption"
    column_name = "target_mood"

    existing_columns = []
    try:
        with connection.cursor() as cursor:
            description = connection.introspection.get_table_description(cursor, table_name)
            existing_columns = [col.name for col in description]
    except Exception:
        existing_columns = []

    if column_name not in existing_columns:
        return

    vendor = connection.vendor
    statements = []
    if vendor == "postgresql":
        statements = [f'ALTER TABLE "{table_name}" DROP COLUMN IF EXISTS "{column_name}" CASCADE']
    else:
        statements = [f'ALTER TABLE "{table_name}" DROP COLUMN "{column_name}"']

    with connection.cursor() as cursor:
        for sql in statements:
            try:
                cursor.execute(sql)
            except Exception:
                # Do not block deployment if the column has already been removed
                # or the database backend cannot drop it.
                pass


class Migration(migrations.Migration):

    dependencies = [
        ("survey", "0003_preferences"),
    ]

    operations = [
        migrations.RunPython(drop_legacy_target_mood, migrations.RunPython.noop),
    ]
