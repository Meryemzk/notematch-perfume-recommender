from django.db import migrations, models


def add_missing_perfume_columns(apps, schema_editor):
    """Add new columns only when they are not already present.

    This makes the migration safe on Render when a previous failed deploy has
    already added one or more columns but did not record the migration as applied.
    """
    Perfume = apps.get_model("perfumes", "Perfume")
    table_name = Perfume._meta.db_table
    connection = schema_editor.connection

    with connection.cursor() as cursor:
        existing_columns = {
            column.name
            for column in connection.introspection.get_table_description(cursor, table_name)
        }

    fields = [
        models.TextField(blank=True, name="description"),
        models.CharField(blank=True, default="Demo UK price book", max_length=120, name="price_source"),
        models.BooleanField(default=False, name="is_featured"),
        models.BooleanField(default=True, name="is_active"),
        models.DateTimeField(auto_now_add=True, null=True, name="created_at"),
        models.DateTimeField(auto_now=True, null=True, name="updated_at"),
    ]

    for field in fields:
        if field.name not in existing_columns:
            field.set_attributes_from_name(field.name)
            schema_editor.add_field(Perfume, field)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("perfumes", "0002_perfume_preference_fields"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(add_missing_perfume_columns, noop_reverse),
            ],
            state_operations=[
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
            ],
        ),
    ]
