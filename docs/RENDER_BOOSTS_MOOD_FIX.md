# Render boosts_mood fix

The Render error was:

```text
django.db.utils.IntegrityError: null value in column "boosts_mood" of relation "perfumes_perfume" violates not-null constraint
```

This happened because the live Render PostgreSQL database still had old columns from previous NoteMatch versions. The current Django `Perfume` model does not use those old columns, so Django did not write values for them when creating seed perfume rows.

The fix is:

- `backend/perfumes/migrations/0006_relax_all_live_perfume_not_null_constraints.py`
- Updated `seed_survey.py` to relax old live database constraints before adding perfume data.

Keep the Render settings:

```text
Root Directory: backend
Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py seed_survey
Start Command: gunicorn config.wsgi:application
```
