# Fix for older Render databases that still have a legacy NOT NULL
# perfumes_perfume.description column from an earlier version of NoteMatch.
# The current model uses `notes`, not `description`, so inserts can fail unless
# the legacy column allows NULL values.
from django.db import migrations


def make_legacy_description_nullable(apps, schema_editor):
    table_name = "perfumes_perfume"
    column_name = "description"
    try:
        with schema_editor.connection.cursor() as cursor:
            existing_columns = [
                col.name
                for col in schema_editor.connection.introspection.get_table_description(cursor, table_name)
            ]
            if column_name not in existing_columns:
                return
            if schema_editor.connection.vendor == "postgresql":
                cursor.execute(f'ALTER TABLE "{table_name}" ALTER COLUMN "{column_name}" DROP NOT NULL')
            # SQLite does not support ALTER COLUMN DROP NOT NULL directly.
            # Local SQLite installs normally do not have this legacy column.
    except Exception:
        # Do not block deployment if the legacy column does not exist or cannot be changed.
        pass


class Migration(migrations.Migration):
    dependencies = [
        ("perfumes", "0003_ensure_price_scent_columns"),
    ]

    operations = [
        migrations.RunPython(make_legacy_description_nullable, migrations.RunPython.noop),
    ]
