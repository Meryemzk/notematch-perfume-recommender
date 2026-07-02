# Render static files fix

The project keeps Django code in `backend/` and UI static assets in `frontend/static/`.

For Render, leave **Root Directory empty** so Render uploads both folders. Use:

Build command:

```bash
cd backend && pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py repair_live_db && python manage.py seed_survey && python manage.py collectstatic --noinput
```

Start command:

```bash
cd backend && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

Then use **Manual Deploy -> Clear build cache & deploy**.
