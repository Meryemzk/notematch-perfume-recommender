# NoteMatch Final Live Fix - June 26

This version fixes the Render live database issues and the survey recommendation 500 error.

## What was fixed

- Added `repair_live_db` management command to repair old Render/PostgreSQL columns safely.
- Added migration `perfumes.0007_repair_render_legacy_columns_final`.
- Updated `seed_survey` so it repairs old columns before inserting perfume data.
- Confirmed local pages return HTTP 200:
  - `/`
  - `/perfumes/`
  - `/survey/`
  - `/survey/result/` after submitting the survey
- Confirmed recommendations show perfume prices with `£`.
- Kept professional UI buttons and footer styling.
- Improved deploy command in `render.yaml`.

## Render settings

Root Directory:

```txt
backend
```

Build Command:

```txt
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py repair_live_db && python manage.py migrate && python manage.py repair_live_db && python manage.py seed_survey
```

Start Command:

```txt
gunicorn config.wsgi:application
```

## Important

Do not type `Build Command:` inside the Render Build Command field.
Do not type `backend/ $` inside the field.
Do not type `cd backend` when Root Directory is already set to `backend`.
