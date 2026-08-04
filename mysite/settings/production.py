"""Production settings — security hardened."""

from __future__ import annotations

import os

import dj_database_url
import sentry_sdk

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F401, F403

# ── Core ───────────────────────────────────────────────────────
DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY", "").strip()
if len(SECRET_KEY) < 50:
    raise ImproperlyConfigured(
        "SECRET_KEY is required in production and must contain at least 50 characters."
    )

# Enforce required production infrastructure
if not os.environ.get("DATABASE_URL"):
    raise ImproperlyConfigured(
        "DATABASE_URL is required in production. "
        "Set it to a PostgreSQL connection string (e.g. postgres://user:pass@host:5432/db)."
    )
if not os.environ.get("REDIS_URL"):
    import warnings

    warnings.warn(
        "REDIS_URL not set — using local memory cache. "
        "This is not suitable for multi-worker Gunicorn deployments.",
        RuntimeWarning,
        stacklevel=1,
    )
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("ALLOWED_HOSTS", "").split(",")
    if host.strip()
]

# Railway auto-detection: RAILWAY_PUBLIC_DOMAIN is set automatically
railway_domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "").strip()
railway_environment = os.environ.get("RAILWAY_ENVIRONMENT", "").strip()
if railway_domain:
    ALLOWED_HOSTS.append(railway_domain)
if railway_domain or railway_environment:
    ALLOWED_HOSTS.append("healthcheck.railway.app")
ALLOWED_HOSTS = list(dict.fromkeys(ALLOWED_HOSTS))
if not ALLOWED_HOSTS:
    raise ImproperlyConfigured(
        "ALLOWED_HOSTS or RAILWAY_PUBLIC_DOMAIN is required in production."
    )

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]
if railway_domain:
    CSRF_TRUSTED_ORIGINS.append(f"https://{railway_domain}")
CSRF_TRUSTED_ORIGINS = list(dict.fromkeys(CSRF_TRUSTED_ORIGINS))

# ── Database ───────────────────────────────────────────────────
DATABASES["default"] = dj_database_url.config(  # type: ignore[name-defined]  # noqa: F405
    conn_max_age=600,
    conn_health_checks=True,
)

# ── Security ───────────────────────────────────────────────────
SECURE_PROXY_SSL_HEADER = (
    ("HTTP_X_FORWARDED_PROTO", "https")
    if os.environ.get("TRUST_PROXY_HEADERS", "false").strip().lower()
    in {"1", "true", "yes", "on"}
    else None
)
SECURE_SSL_REDIRECT = True
SECURE_REDIRECT_EXEMPT = [r"^health/$"]  # Railway healthcheck uses HTTP internally
SECURE_HSTS_SECONDS = 31_536_000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_AGE = 3600  # 1-hour admin sessions (not default 2 weeks)
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Lax"
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_BROWSER_XSS_FILTER = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# ── Static files ───────────────────────────────────────────────
STORAGES["staticfiles"] = {  # type: ignore[name-defined]  # noqa: F405
    "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
}

# ── Cache ──────────────────────────────────────────────────────
redis_url = os.environ.get("REDIS_URL")
if redis_url:
    CACHES = {  # noqa: F811
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": redis_url,
            "KEY_PREFIX": "inland",
        }
    }

# ── Media storage (Cloudinary) ─────────────────────────────────
cloudinary_url = os.environ.get("CLOUDINARY_URL")
if cloudinary_url:
    INSTALLED_APPS += ["cloudinary_storage", "cloudinary"]  # type: ignore[name-defined]  # noqa: F405
    STORAGES["default"] = {  # type: ignore[name-defined]  # noqa: F405
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    }

# ── Email (production SMTP) ───────────────────────────────────
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "noreply@example.com")

# ── Wagtail ────────────────────────────────────────────────────
# Auto-detect Railway domain unless an explicit custom/admin domain was supplied.
if railway_domain and not os.environ.get("WAGTAILADMIN_BASE_URL"):
    WAGTAILADMIN_BASE_URL = f"https://{railway_domain}"  # noqa: F405

# ── Sentry ─────────────────────────────────────────────────────
sentry_dsn = os.environ.get("SENTRY_DSN")
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        environment=os.environ.get("SENTRY_ENVIRONMENT", "production"),
        traces_sample_rate=float(os.environ.get("SENTRY_TRACES_SAMPLE_RATE", "0.1")),
        profiles_sample_rate=float(
            os.environ.get("SENTRY_PROFILES_SAMPLE_RATE", "0.1")
        ),
    )
