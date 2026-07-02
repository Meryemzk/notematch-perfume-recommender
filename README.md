# NoteMatch — Luxury Perfume Recommendation Platform

A polished Django perfume recommendation platform for, built from the original NoteMatch survey project and designed for undergraduate deployment on GitHub + Render without changing the server stack.

## What is included

- Luxury responsive UI with black, gold, cream, charcoal and soft beige styling
- Home page with premium hero, use cases, trending perfumes, brand cloud, testimonials and newsletter UI
- Professional perfume search with autocomplete, brand, GBP price, note, season, Occasion, intensity, sorting, pagination, grid/list modes, empty states and mobile filter drawer
- Smart multi-step recommendation quiz for fragrance style, age range, season, weather, occasion, budget, intensity, longevity, notes liked/disliked, favourite brands, perfumes already liked, personality and lifestyle
- Results page with 5–10 recommendations, match percentage, reasons, strengths, weaknesses, season, occasion, longevity, projection, GBP price and retailer guidance
- Perfume detail pages with product-style visuals, notes, longevity, projection, sillage, scent ratings, Suitability, similar perfumes and retailer links
- Comparison page for 2–4 perfumes
- Brands page, fragrance notes page, favourites page, login, registration and user dashboard
- Staff-only custom admin panel plus Django admin for user, perfume, quiz and catalogue management
- About, Contact, FAQ, Terms and Privacy pages
- Session favourites, protected admin routes, Django password hashing, CSRF protection and standard Django validation
- Seed command with sample perfumes, survey questions, moods and notes

## Project architecture

```text
NoteMatch-4-4/
├── backend/
│   ├── config/          # Django settings and project URLs
│   ├── core/            # Home and static pages
│   ├── perfumes/        # Catalogue, details, compare, brands, notes, favourites, admin panel
│   ├── survey/          # Quiz, scoring and seed data
│   ├── users/           # Registration and dashboard
│   └── manage.py
├── frontend/
│   ├── static/css/style.css
│   ├── static/js/luxury.js
│   ├── static/images/
│   └── templates/
├── render.yaml
└── README.md
```

## Local setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_survey
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Render deployment

This version keeps the existing Django + Render architecture. Do not switch to Next.js or Prisma for this project unless your supervisor asks for a full rebuild.

Recommended Render build command:

```bash
cd backend && pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py seed_survey && python manage.py collectstatic --noinput
```

Recommended start command:

```bash
cd backend && gunicorn config.wsgi:application
```

Set these environment variables in Render:

```text
SECRET_KEY=your-secure-secret
DEBUG=False
ALLOWED_HOSTS=your-service.onrender.com,.onrender.com
CSRF_TRUSTED_ORIGINS=https://your-service.onrender.com
DATABASE_URL=your-postgres-url-if-used
```

## Admin access

1. Create a superuser locally or on Render:

```bash
python manage.py createsuperuser
```

2. Use `/admin/` for Django admin CRUD.
3. Use `/perfumes/admin-panel/` for the custom luxury analytics dashboard.

## Test commands

```bash
python manage.py check
python manage.py smoke_test
```

The smoke test checks the home page, perfume catalogue, quiz, recommendation result flow and admin login page.

## Notes for your undergraduate report

The platform uses Django templates, Bootstrap, custom CSS, Django sessions, Django authentication, ORM queries and a weighted recommendation algorithm. The recommendation score rewards matching preferred notes, season, weather, budget, gender/fragrance style, occasion, intensity, longevity, lifestyle, personality and favourite brands. It penalises disliked notes and sorts the result by the highest match.

Perfume prices are prototype estimates in GBP and should not be presented as live retail prices.
