# Render final deploy steps

Use these settings on Render:

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

Then choose **Manual Deploy → Clear build cache & deploy**.

This version includes a migration that removes the old legacy `target_mood` column from the Render database if it exists, then seeds the survey questions and perfume price catalog.
