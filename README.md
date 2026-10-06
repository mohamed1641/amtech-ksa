# AMTECH KSA

Django website for the AMTECH KSA product catalogue, customer enquiries,
product trial requests, job applications, and sales representative contracts.

## Features

- Product catalogue with search and filters.
- General enquiries and product trial requests.
- Careers page with PDF CV uploads.
- Permission-protected CV downloads through Django Admin.
- Sales representative authentication using the `Sales Reps` group.
- Contract creation and PDF generation using the original contract template.
- Arabic and English text support in contract PDFs.

## Local setup

Use Python 3.12 or later, compatible with the pinned dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

For a new checkout, copy `.env.example` to `.env`.
Do not overwrite an existing `.env`.

Generate a secret key locally:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

Put the generated value in `SECRET_KEY` inside `.env`.
Keep this value private.

Then run:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py check
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Pages

- `/` — Home
- `/products/` — Catalogue
- `/contact/` — Enquiries and trial requests
- `/careers/` — Job applications
- `/reps/` — Sales representative login
- `/admin/` — Administration

## Sales representatives

Create the `Sales Reps` group in Django Admin.
Create an active user and assign them to this group.

Ordinary representatives do not need staff or superuser status.

## Catalogue data

A fresh database does not include existing products or uploaded images.

The `import_products` management command contains catalogue seed data.
It updates matching products and deletes and recreates their variants
and specifications. Review it before use; do not run it on an existing
catalogue unless these replacements are intended.

Uploaded product images must be restored or uploaded separately.

## Files and backups

The following are excluded from Git:

- `.env` — private configuration
- `db.sqlite3` — local database
- `media/` — uploaded product images
- `private_media/` — private CV uploads
- `venv/` — Python environment
- `staticfiles/` — generated static output

GitHub stores source code, not a complete backup of the live application.
Back up the database, uploaded files, and private configuration separately.

Keep the original PDF templates in `static/pdfs/` and the PDF font
`static/fonts/DejaVuSans.ttf`; contract generation depends on them.

CV files must not be exposed through a public media URL.
Use the permission-protected Django Admin download endpoint.

## Deployment

Production hosting is not configured yet.

Before deployment, configure a separate production secret key,
`DEBUG=False`, domain-specific allowed hosts, HTTPS, secure cookies,
a production application server, static and media handling, and backups.

Run deployment checks against the production configuration:

```bash
python manage.py check --deploy
```

Do not use Django's development server for production.