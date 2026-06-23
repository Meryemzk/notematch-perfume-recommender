# Deploy NoteMatch to a real server with Render + Supabase

This project is now prepared for real deployment.

## What was fixed

- Added production packages: `gunicorn`, `whitenoise`, `dj-database-url`, `python-dotenv`, `psycopg2-binary`.
- Updated `settings.py` so local development still works with SQLite.
- Added support for `DATABASE_URL` so the project can connect to Supabase PostgreSQL.
- Added static file support for deployment using WhiteNoise.
- Added `Procfile`, `runtime.txt`, `.env.example`, `.gitignore`, and `render.yaml`.
- Removed the need to rely on the local Django server only.

## Important idea

Supabase is your real database server.
Render is your real Django website server.

User browser -> Render Django website -> Supabase PostgreSQL database

## Step 1: Test locally on your Mac

Open Terminal in VS Code and run:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_survey
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Step 2: Create Supabase database

1. Go to Supabase.
2. Create a new project.
3. Go to Project Dashboard -> Connect.
4. Copy the PostgreSQL connection string.
5. It should look like:

```text
postgresql://postgres:YOUR_PASSWORD@db.xxxxx.supabase.co:5432/postgres
```

Keep this private.

## Step 3: Push project to GitHub

From the main project folder:

```bash
git init
git add .
git commit -m "Prepare NoteMatch for deployment"
```

Create a GitHub repository, then push using the commands GitHub gives you.

## Step 4: Deploy on Render

1. Go to Render.
2. New -> Web Service.
3. Connect your GitHub repository.
4. Use these settings:

```text
Root Directory: backend
Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
Start Command: gunicorn config.wsgi:application
```

## Step 5: Add Render environment variables

In Render, add:

```text
DEBUG=False
SECRET_KEY=make-a-long-random-secret-key
DATABASE_URL=your-supabase-postgresql-url
ALLOWED_HOSTS=your-render-app-name.onrender.com
CSRF_TRUSTED_ORIGINS=https://your-render-app-name.onrender.com
```

Do not include `https://` in `ALLOWED_HOSTS`.
Do include `https://` in `CSRF_TRUSTED_ORIGINS`.

## Step 6: Create admin user on Render

After the first successful deployment, open Render Shell and run:

```bash
python manage.py createsuperuser
python manage.py seed_survey
```

Then open:

```text
https://your-render-app-name.onrender.com/admin/
```

## Local `.env` example

Inside `backend`, copy `.env.example` to `.env` if you want to connect your local Mac to Supabase:

```bash
cp .env.example .env
```

Then edit `.env` and paste your real `DATABASE_URL`.

If `DATABASE_URL` is empty, the project uses local SQLite.
