# ── Build dependencies stage ──
FROM python:3.12-slim AS deps

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Node stage for Tailwind build ──
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
RUN npx tailwindcss -i ./mysite/static/src/input.css -o ./mysite/static/css/output.css --minify

# ── Final runtime stage (no gcc, no dev headers) ──
FROM python:3.12-slim AS final

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Runtime-only deps: libpq for psycopg2, curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 curl && \
    rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from deps stage
COPY --from=deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

COPY . .
COPY --from=tailwind /app/mysite/static/css/output.css mysite/static/css/output.css

RUN DJANGO_SETTINGS_MODULE=mysite.settings.production \
    SECRET_KEY=build-placeholder \
    DATABASE_URL=sqlite:///tmp/build.db \
    python manage.py collectstatic --noinput 2>/dev/null || true

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health/ || exit 1

ENTRYPOINT ["/app/start.sh"]
