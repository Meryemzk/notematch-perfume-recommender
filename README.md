# NoteMatch

NoteMatch is a Django-based mood perfume recommendation web application. Users can complete a survey without registering, browse perfumes with prices and scent notes, and receive personalised perfume suggestions based on mood, occasion, season, and scent preferences.

## Folder structure

```text
NoteMatch/
├── backend/        # Django project, apps, settings, deployment files
├── frontend/       # Templates, CSS, images
├── docs/           # Deployment notes
├── render.yaml     # Render Blueprint configuration
└── README.md
```

## Local run

From the project root:

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver
```

## Render settings

If you deploy manually on Render, use these settings:

```text
Root Directory: backend
Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
Start Command: gunicorn config.wsgi:application
```

Add these environment variables in Render:

```text
DEBUG=False
SECRET_KEY=your-long-secret-key
ALLOWED_HOSTS=your-service-name.onrender.com,.onrender.com
CSRF_TRUSTED_ORIGINS=https://your-service-name.onrender.com
```

The important point is that Render must start inside `backend`, because `manage.py` and `config/` are both inside that folder.
