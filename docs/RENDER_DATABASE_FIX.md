# Render database fix

The live Render PostgreSQL database was created from an older NoteMatch model. It still contains legacy `perfumes_perfume` columns such as `description` and `best_for` with `NOT NULL` constraints. The current Django model does not write those columns, so seeding perfumes can fail.

This version adds migration:

`perfumes/migrations/0005_make_all_legacy_perfume_columns_nullable.py`

It makes legacy columns nullable before `seed_survey` inserts the perfume catalogue.

Use these Render settings:

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

Then run:

`Manual Deploy → Clear build cache & deploy`
