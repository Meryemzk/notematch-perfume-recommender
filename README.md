# NoteMatch Semi-Pro — Deployment Ready

NoteMatch is a Django mood-based perfume recommendation system.

This version has been fixed so it can run locally on Mac and can also be deployed to a real server using Render with Supabase PostgreSQL.

## Local run on Mac

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

## Real server deployment

Read this file:

```text
DEPLOY_RENDER_SUPABASE.md
```

## Important files added/fixed

- `backend/config/settings.py` now supports environment variables and Supabase PostgreSQL.
- `backend/requirements.txt` now includes deployment and database packages.
- `backend/Procfile` tells the server how to start Django.
- `backend/runtime.txt` tells the server which Python version to use.
- `backend/.env.example` shows the environment variables you need.
- `render.yaml` provides optional Render deployment configuration.
- `DEPLOY_RENDER_SUPABASE.md` gives step-by-step deployment instructions.
