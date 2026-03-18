#!/usr/bin/env bash
set -euo pipefail

echo "=== Running migrations ==="
python manage.py migrate --noinput

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

echo "=== Compiling translation files ==="
python -c "
import polib, pathlib
for po_path in pathlib.Path('locale').rglob('*.po'):
    mo_path = po_path.with_suffix('.mo')
    po = polib.pofile(str(po_path))
    po.save_as_mofile(str(mo_path))
    print(f'  Compiled {po_path} -> {mo_path}')
" 2>/dev/null || echo "  (skipped — polib not available or no .po files)"

echo "=== Setting up pages (if needed) ==="
python manage.py setup_pages 2>&1 || echo "WARNING: setup_pages failed (non-blocking)"

echo "=== Setting up Spanish pages (if needed) ==="
python manage.py setup_spanish_pages 2>&1 || echo "WARNING: setup_spanish_pages failed (non-blocking)"

echo "=== Updating service page content ==="
python manage.py update_service_content 2>&1 || echo "WARNING: update_service_content failed (non-blocking)"

echo "=== Populating Spanish service content ==="
python manage.py populate_spanish_content 2>&1 || echo "WARNING: populate_spanish_content failed (non-blocking)"

echo "=== Creating superuser (if env vars set) ==="
if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] && [ -n "${DJANGO_SUPERUSER_EMAIL:-}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
    python manage.py createsuperuser --noinput 2>/dev/null || echo "Superuser already exists"
fi

echo "=== Starting Gunicorn ==="
exec gunicorn mysite.wsgi:application \
    --bind "0.0.0.0:${PORT:-8000}" \
    --workers "${GUNICORN_WORKERS:-3}" \
    --timeout "${GUNICORN_TIMEOUT:-60}" \
    --access-logfile - \
    --error-logfile -
