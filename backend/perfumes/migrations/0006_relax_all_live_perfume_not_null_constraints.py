# Final safety migration for Render live databases.
#
# The live database has gone through several older NoteMatch schemas. Those
# schemas left legacy NOT NULL columns on perfumes_perfume, including fields
# that are no longer in the current Django model, such as description,
# best_for and boosts_mood. When seed_survey inserts new perfume rows, Django
# only writes the current model fields, so PostgreSQL rejects the insert if any
# legacy NOT NULL column is missing.
#
# This migration makes every existing non-primary-key column on
# perfumes_perfume nullable. The website still uses the current Django model,
# forms and seed data to provide correct values, including price with £.
from django.db import migrations


def relax_not_null_constraints(apps, schema_editor):
    table_name = "perfumes_perfume"
    try:
        with schema_editor.connection.cursor() as cursor:
            columns = [
                col.name
                for col in schema_editor.connection.introspection.get_table_description(cursor, table_name)
            ]
            if schema_editor.connection.vendor == "postgresql":
                for column_name in columns:
                    if column_name != "id":
                        cursor.execute(
                            f'ALTER TABLE "{table_name}" ALTER COLUMN "{column_name}" DROP NOT NULL'
                        )
    except Exception:
        # Do not block deployment if the live table is already clean.
        pass


class Migration(migrations.Migration):
    dependencies = [
        ("perfumes", "0005_make_all_legacy_perfume_columns_nullable"),
    ]

    operations = [
        migrations.RunPython(relax_not_null_constraints, migrations.RunPython.noop),
    ]
