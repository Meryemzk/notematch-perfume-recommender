# Latest Render Fix

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

This version includes a safe migration for older Render databases that still contain a legacy `description` column in `perfumes_perfume`.
