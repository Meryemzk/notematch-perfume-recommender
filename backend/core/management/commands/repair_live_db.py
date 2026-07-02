from django.core.management.base import BaseCommand
from django.db import connection


def _safe_execute(cursor, sql):
    try:
        cursor.execute(sql)
        return True
    except Exception:
        return False


def repair_perfume_table():
    table = "perfumes_perfume"
    vendor = connection.vendor
    with connection.cursor() as cursor:
        try:
            tables = connection.introspection.table_names(cursor)
        except Exception:
            tables = []
        if table not in tables:
            return 0

        if vendor == "postgresql":
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
            changed = 0
            for column in columns:
                if _safe_execute(cursor, f'ALTER TABLE "{table}" ALTER COLUMN "{column}" DROP NOT NULL'):
                    changed += 1
            return changed

        # SQLite/local fallback: no-op, local databases do not normally have legacy NOT NULL columns.
        return 0


def repair_survey_option_table():
    table = "survey_surveyoption"
    vendor = connection.vendor
    with connection.cursor() as cursor:
        try:
            tables = connection.introspection.table_names(cursor)
        except Exception:
            tables = []
        if table not in tables:
            return 0

        columns = [col.name for col in connection.introspection.get_table_description(cursor, table)]
        changed = 0
        if vendor == "postgresql":
            if "target_mood" in columns:
                if _safe_execute(cursor, f'ALTER TABLE "{table}" DROP COLUMN IF EXISTS "target_mood" CASCADE'):
                    changed += 1
            for column in columns:
                if column != "id" and column != "target_mood":
                    if _safe_execute(cursor, f'ALTER TABLE "{table}" ALTER COLUMN "{column}" DROP NOT NULL'):
                        changed += 1
        return changed


def repair_survey_question_table():
    table = "survey_surveyquestion"
    vendor = connection.vendor
    with connection.cursor() as cursor:
        try:
            tables = connection.introspection.table_names(cursor)
        except Exception:
            tables = []
        if table not in tables:
            return 0

        columns = [col.name for col in connection.introspection.get_table_description(cursor, table)]
        changed = 0
        if vendor == "postgresql" and "is_active" in columns:
            if _safe_execute(cursor, f'UPDATE "{table}" SET "is_active" = TRUE WHERE "is_active" IS NULL'):
                changed += 1
            if _safe_execute(cursor, f'ALTER TABLE "{table}" ALTER COLUMN "is_active" SET DEFAULT TRUE'):
                changed += 1
            if _safe_execute(cursor, f'ALTER TABLE "{table}" ALTER COLUMN "is_active" DROP NOT NULL'):
                changed += 1
        return changed


class Command(BaseCommand):
    help = "Repair old Render database columns left from previous NoteMatch deployments. Safe to run repeatedly."

    def handle(self, *args, **options):
        perfume_changes = repair_perfume_table()
        survey_option_changes = repair_survey_option_table()
        survey_question_changes = repair_survey_question_table()
        self.stdout.write(self.style.SUCCESS(
            f"Live database repair completed. Perfume column fixes: {perfume_changes}. "
            f"Survey option fixes: {survey_option_changes}. "
            f"Survey question fixes: {survey_question_changes}."
        ))
