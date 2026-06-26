from django.db import migrations


def repair_render_perfume_table(apps, schema_editor):
    table = "perfumes_perfume"
    connection = schema_editor.connection
    if connection.vendor != "postgresql":
        return

    with connection.cursor() as cursor:
        try:
            cursor.execute(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = current_schema()
                  AND table_name = %s
                  AND column_name <> 'id'
                ORDER BY ordinal_position
                """,
                [table],
            )
            columns = [row[0] for row in cursor.fetchall()]
        except Exception:
            columns = []

        for column in columns:
            try:
                cursor.execute(f'ALTER TABLE "{table}" ALTER COLUMN "{column}" DROP NOT NULL')
            except Exception:
                # Keep migration deploy-safe even if a column has already been fixed.
                pass


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("perfumes", "0006_relax_all_live_perfume_not_null_constraints"),
    ]

    operations = [
        migrations.RunPython(repair_render_perfume_table, migrations.RunPython.noop),
    ]
