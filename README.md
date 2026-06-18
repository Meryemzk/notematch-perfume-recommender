# NoteMatch — Mood and Preference Perfume Recommendation System

NoteMatch is a Django web application for an undergraduate development project. It recommends perfumes using a combination of mood answers and a saved user preference profile.

## Main features

- User sign up, login and profile pages.
- Friendly greeting that shows the user name only, without an email domain or @ sign.
- Saved preference profile for each user. Three favourite perfumes, gender preference, new/classic style preference and budget remain saved until the user chooses to update them.
- Mood and scent survey with admin-editable questions and options.
- Recommendation scoring using mood, scent-note keywords, favourite-perfume evidence, gender category, style category and budget.
- Catalogue with more than 100 seeded perfume records and prices shown in pounds.
- Professional responsive interface with shared templates, reusable includes and a detailed footer.
- Admin controls for perfumes, questions, user preference profiles and survey submissions.

## Local run

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_survey
python manage.py createsuperuser
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Admin:

```text
http://127.0.0.1:8000/admin/
```

## Render deployment

This project includes `render.yaml`, `Procfile`, `runtime.txt`, WhiteNoise static-file support and PostgreSQL/Supabase support through `DATABASE_URL`.

In Render, set these environment variables:

```text
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-app-name.onrender.com
CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com
DATABASE_URL=optional-postgres-url
```

The Render build command runs migrations and seeds the survey/perfume data automatically.

## Important note about prices

The seeded perfume prices are prototype/demo UK pound prices for project testing and comparison. For a commercial website, prices should be checked against live retailer data before publishing.
