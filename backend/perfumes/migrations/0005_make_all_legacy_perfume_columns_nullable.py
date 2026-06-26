# Safety migration for live Render databases that were created from older
# NoteMatch versions. Earlier versions had extra NOT NULL columns such as
# description and best_for. The current model no longer writes those fields,
# so PostgreSQL blocks seed inserts unless the legacy columns are nullable.
from django.db import migrations


LEGACY_COLUMNS = [
    "description",
    "best_for",
    "gender",
    "image",
    "mood",
    "occasion",
    "intensity",
    "category",
    "short_description",
]


def make_legacy_columns_nullable(apps, schema_editor):
    table_name = "perfumes_perfume"
    try:
        with schema_editor.connection.cursor() as cursor:
            existing_columns = [
                col.name
                for col in schema_editor.connection.introspection.get_table_description(cursor, table_name)
            ]
            if schema_editor.connection.vendor == "postgresql":
                for column_name in LEGACY_COLUMNS:
                    if column_name in existing_columns:
                        cursor.execute(f'ALTER TABLE "{table_name}" ALTER COLUMN "{column_name}" DROP NOT NULL')
            # SQLite does not support ALTER COLUMN DROP NOT NULL directly.
            # Local SQLite databases normally do not have these legacy columns.
    except Exception:
        # Do not block deployment if a legacy column is already gone.
        pass


class Migration(migrations.Migration):
    dependencies = [
        ("perfumes", "0004_make_legacy_description_nullable"),
    ]

    operations = [
        migrations.RunPython(make_legacy_columns_nullable, migrations.RunPython.noop),
    ]
