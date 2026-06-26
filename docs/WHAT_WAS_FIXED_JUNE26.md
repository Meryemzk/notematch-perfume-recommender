# What was fixed

Render failed with this error:

```text
django.db.utils.IntegrityError: null value in column "best_for" of relation "perfumes_perfume" violates not-null constraint
```

The issue was not the code for the current model. The live Render PostgreSQL database still had old columns from a previous version of the Perfume model. Columns such as `best_for` and `description` were still `NOT NULL`, but the current app no longer writes to them.

Fixes added:

- Added migration `perfumes/migrations/0005_make_all_legacy_perfume_columns_nullable.py`.
- The migration makes old legacy columns nullable so new perfume rows can be inserted safely.
- Updated `seed_survey.py` to run an extra database safety fix before seeding.
- Updated perfume seeding to save the uploaded price list values directly during create/update.
- Perfume catalog and recommendation result pages show prices with the £ symbol.

Render settings:

Root Directory:

```text
backend
```

Build Command:

```text
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py seed_survey
```

Start Command:

```text
gunicorn config.wsgi:application
```

After pushing to GitHub, use:

```text
Manual Deploy → Clear build cache & deploy
```
