# Just NoteMatch

NoteMatch is a Django mood-based perfume recommendation system. This version includes the requested design, survey, perfume catalog and admin improvements.

## What is included

- Public home page: visitors can use the survey without registration.
- Optional registration: users only need an account if they want to keep using profile features.
- NoteMatch logo and main-page image added from the provided NM pictures.
- Survey questions rewritten so mood, occasion, scent, strength and personality relate to each other.
- Best-seller perfume catalog seeded from the provided perfume report photos, including UK prices with £ display and 3 scent tags per perfume.
- Admin page improved so perfumes can be added, edited and deleted, with dropdown choices for scent 1, scent 2, scent 3, and mood selection.
- Project kept in clear folders: `backend/`, `frontend/`, `frontend/static/`, `frontend/templates/`, and `docs/`.

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

Open the website:

```text
http://127.0.0.1:8000/
```

Open admin:

```text
http://127.0.0.1:8000/admin/
```

## Important command

Run this after migrations to add the survey questions and perfume list:

```bash
python manage.py seed_survey
```

## Deployment

For Render and Supabase deployment, read:

```text
docs/DEPLOY_RENDER_SUPABASE.md
```
