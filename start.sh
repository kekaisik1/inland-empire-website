#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-mysite.settings.production}"

echo "=== Applying final migration safety check ==="
python manage.py migrate --noinput

startup_seed_mode="${RUN_STARTUP_SEEDS:-false}"
case "${startup_seed_mode,,}" in
    1|true|yes|on)
        echo "=== Running direct-container content bootstrap ==="
        bash "$SCRIPT_DIR/predeploy.sh" --skip-migrate
        ;;
    0|false|no|off|"")
        ;;
    *)
        echo "RUN_STARTUP_SEEDS must be true or false." >&2
        exit 64
        ;;
esac

workers="${WEB_CONCURRENCY:-${GUNICORN_WORKERS:-1}}"

echo "=== Starting Gunicorn ==="
exec gunicorn mysite.wsgi:application \
    --bind "0.0.0.0:${PORT:-8000}" \
    --workers "${workers}" \
    --timeout "${GUNICORN_TIMEOUT:-60}" \
    --no-control-socket \
    --access-logfile - \
    --error-logfile -
