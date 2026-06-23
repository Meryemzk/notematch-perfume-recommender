# Render live fix for NoteMatch

Use these exact settings in Render:

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

Then click:

```text
Manual Deploy -> Clear build cache & deploy
```

This version includes safe perfume migrations, so the old Render error below should be fixed:

```text
column "price" of relation "perfumes_perfume" already exists
```

The build also runs `seed_survey`, which adds the survey questions and bestseller perfume list with prices.
