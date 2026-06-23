# Render deployment fix for NoteMatch

Use this when Render shows `No module named config` or cannot find `requirements.txt`.

## Correct project layout

```text
NoteMatch/
├── backend/
│   ├── manage.py
│   ├── config/
│   ├── requirements.txt
│   ├── Procfile
│   └── runtime.txt
├── frontend/
└── render.yaml
```

## Render manual deployment settings

```text
Root Directory: backend
Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
Start Command: gunicorn config.wsgi:application
```

## Why this fixes it

`config` is inside the `backend` folder. If Render starts from the repository root, Gunicorn cannot import `config.wsgi`. Setting Root Directory to `backend` fixes that.

## Environment variables

```text
DEBUG=False
SECRET_KEY=your-long-secret-key
ALLOWED_HOSTS=your-service-name.onrender.com,.onrender.com
CSRF_TRUSTED_ORIGINS=https://your-service-name.onrender.com
```
