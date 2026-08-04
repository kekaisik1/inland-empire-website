# syntax=docker/dockerfile:1

# Python dependency stage
FROM python:3.12-slim AS deps

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

# Node stage for deterministic Tailwind output
FROM node:20-slim AS tailwind

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY tailwind.config.js ./
COPY mysite/static/src/ mysite/static/src/
COPY mysite/templates/ mysite/templates/
COPY home/templates/ home/templates/
COPY services/templates/ services/templates/
COPY locations/templates/ locations/templates/
COPY blog/templates/ blog/templates/
COPY pages/templates/ pages/templates/
COPY search/templates/ search/templates/
COPY tracking/templates/ tracking/templates/
RUN npm run build:css

# Final runtime stage (no compiler or Node toolchain)
FROM python:3.12-slim AS final

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=mysite.settings.production

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 curl && \
    rm -rf /var/lib/apt/lists/*

COPY --from=deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

COPY . .
COPY --from=tailwind /app/mysite/static/css/output.css mysite/static/css/output.css
COPY --chmod=755 start.sh predeploy.sh ./

RUN python scripts/compile_translations.py && \
    SECRET_KEY=build-only-not-a-runtime-secret-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx \
    DATABASE_URL=sqlite:////tmp/inland-build.db \
    ALLOWED_HOSTS=localhost \
    REDIS_URL=redis://127.0.0.1:6379/0 \
    python manage.py collectstatic --noinput && \
    rm -f /tmp/inland-build.db

RUN useradd --create-home --uid 10001 app && \
    mkdir -p /app/media /app/static && \
    chmod -R a+rX /app && \
    chown -R app:app /app/media

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -fsS "http://127.0.0.1:${PORT:-8000}/health/" >/dev/null

ENTRYPOINT ["/app/start.sh"]
