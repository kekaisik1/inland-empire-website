# Inland Empire Appliance Repair

A Django/Wagtail website for Inland Empire Appliance Repair. The application includes English and Spanish content, service and city pages, brand hubs, blog publishing, contact/search flows, first-party tracking controls, SEO/schema endpoints, and Railway-ready deployment configuration.

The interface intentionally uses Inland Empire's own dark charcoal and yellow design. LOWL supplied product-behavior reference material only; this repository does not use LOWL branding, deployment configuration, or Git history.

## Local development

Requirements: Python 3.12+, Node 20+, and PostgreSQL for production-equivalent development. SQLite is supported for local checks.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm ci
npm run build:css
cp .env.example .env
python scripts/compile_translations.py
python manage.py migrate
python manage.py runserver
```

Set a local `SECRET_KEY`, `DATABASE_URL`, and `ALLOWED_HOSTS` in `.env` before using production settings. Never commit `.env`.

## Verification

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
ruff check blog home locations mysite pages search services tracking scripts
node --test mysite/static/js/tests/*.test.js
npm run build:css
python scripts/verify_deployment_contract.py
```

## Content bootstrap

`predeploy.sh` applies migrations and runs the idempotent content commands in their required order. Railway runs it as the pre-deploy command. For a fresh direct-container database, set `RUN_STARTUP_SEEDS=true` on the first start.

Regional city/service pages are seeded as drafts and stay out of public navigation and sitemaps until an editor explicitly publishes them.

## Railway

Deploy the GitHub repository with the root `Dockerfile` and `railway.json`. Attach PostgreSQL and configure a unique `SECRET_KEY` of at least 50 characters plus `TRUST_PROXY_HEADERS=true`. Keep the default single Gunicorn worker unless a shared cache and its reviewed Python client are added.

See [docs/deployment/railway.md](docs/deployment/railway.md) for the complete variable, first-deploy, verification, and rollback guide.
