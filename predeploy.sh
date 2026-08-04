#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-mysite.settings.production}"

if [ "${1:-}" = "--skip-migrate" ]; then
    shift
elif [ "$#" -ne 0 ]; then
    echo "Usage: $0 [--skip-migrate]" >&2
    exit 64
else
    echo "=== Applying database migrations ==="
    python manage.py migrate --noinput
fi

if [ "$#" -ne 0 ]; then
    echo "Usage: $0 [--skip-migrate]" >&2
    exit 64
fi

echo "=== Reconciling idempotent Wagtail content ==="
seed_commands=(
    setup_pages
    create_brand_pages
    populate_blog_posts
    update_service_content
    setup_regional_service_pages
    setup_spanish_pages
    populate_spanish_content
)
for command in "${seed_commands[@]}"; do
    echo "--- python manage.py $command"
    python manage.py "$command"
done

superuser_variables=(
    DJANGO_SUPERUSER_USERNAME
    DJANGO_SUPERUSER_EMAIL
    DJANGO_SUPERUSER_PASSWORD
)
superuser_values_set=0
for variable in "${superuser_variables[@]}"; do
    if [ -n "${!variable:-}" ]; then
        superuser_values_set=$((superuser_values_set + 1))
    fi
done

if [ "$superuser_values_set" -ne 0 ] && [ "$superuser_values_set" -ne 3 ]; then
    echo "DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, and DJANGO_SUPERUSER_PASSWORD must be set together." >&2
    exit 64
fi

if [ "$superuser_values_set" -eq 3 ]; then
    echo "=== Ensuring bootstrap superuser exists ==="
    if python manage.py shell -c 'import os; from django.contrib.auth import get_user_model; raise SystemExit(0 if get_user_model().objects.filter(username=os.environ["DJANGO_SUPERUSER_USERNAME"]).exists() else 1)'; then
        echo "Bootstrap superuser already exists; leaving it unchanged."
    else
        python manage.py createsuperuser --noinput
    fi
fi

echo "=== Pre-deploy database preparation complete ==="
