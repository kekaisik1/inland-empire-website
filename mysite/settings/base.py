"""
Django settings for the Inland Empire website — shared base configuration.

All environment-specific settings live in dev.py and production.py.
Business info is managed via Wagtail SiteSettings + env vars.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ── Paths ──────────────────────────────────────────────────────
PROJECT_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = PROJECT_DIR.parent


def _env_bool(name: str, default: bool = False) -> bool:
    return os.environ.get(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


def _env_list(name: str) -> tuple[str, ...]:
    return tuple(value.strip() for value in os.environ.get(name, "").split(",") if value.strip())

# ── Named Constants (no magic numbers) ─────────────────────────
NAV_CACHE_TIMEOUT: int = 300  # 5 minutes
BLOG_POSTS_PER_PAGE: int = 9
SEARCH_RESULTS_PER_PAGE: int = 10

# ── Application definition ─────────────────────────────────────
INSTALLED_APPS: list[str] = [
    "home",
    "services",
    "locations",
    "pages",
    "blog",
    "search",
    "tracking.apps.TrackingConfig",
    # Wagtail
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.sitemaps",
    "wagtail.contrib.settings",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    # i18n (must come after wagtail apps)
    "wagtail_localize",
    "wagtail_localize.locales",
    # Third-party
    "modelcluster",
    "taggit",
    "django_filters",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
]

MIDDLEWARE: list[str] = [
    "mysite.middleware.RealIPMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "mysite.middleware.SEOHeadersMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "mysite.context_processors.navigation_data",
                "mysite.context_processors.site_settings_context",
                "mysite.context_processors.tracking_context",
            ],
        },
    },
]

WSGI_APPLICATION = "mysite.wsgi.application"

# ── Database ───────────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ── Auth ───────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ── i18n ───────────────────────────────────────────────────────
LANGUAGE_CODE = "en"
TIME_ZONE = "America/Los_Angeles"
USE_I18N = True
USE_L10N = True
USE_TZ = True

WAGTAIL_I18N_ENABLED = True

WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ("en", "English"),
    ("es", "Spanish"),
]

LOCALE_PATHS = [BASE_DIR / "locale"]

# ── Static files ───────────────────────────────────────────────
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
STATICFILES_DIRS = [PROJECT_DIR / "static"]
STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "/static/"
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

# ── Wagtail ────────────────────────────────────────────────────
WAGTAIL_SITE_NAME = os.environ.get(
    "BUSINESS_NAME", "Inland Empire Appliance Repair"
)
WAGTAILADMIN_BASE_URL = os.environ.get("WAGTAILADMIN_BASE_URL", "http://localhost:8000")
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10_000

WAGTAILSEARCH_BACKENDS = {
    "default": {"BACKEND": "wagtail.search.backends.database"},
}

WAGTAILDOCS_EXTENSIONS = [
    "csv",
    "docx",
    "key",
    "odt",
    "pdf",
    "pptx",
    "rtf",
    "txt",
    "xlsx",
    "zip",
]

# ── Cache ──────────────────────────────────────────────────────
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "inland-empire-cache",
    }
}

# Optional integrations are disabled by default and fail closed without secrets.
TRACKING_ENABLED = _env_bool("TRACKING_ENABLED")
TRACKING_WEBHOOK_ENABLED = _env_bool("TRACKING_WEBHOOK_ENABLED")
TRACKING_REQUIRE_CONSENT = _env_bool("TRACKING_REQUIRE_CONSENT", True)
TRACKING_REQUIRE_ORIGIN = _env_bool("TRACKING_REQUIRE_ORIGIN", True)
TRACKING_ALLOWED_ORIGINS = _env_list("TRACKING_ALLOWED_ORIGINS")
TRACKING_SECRET = os.environ.get("TRACKING_SECRET", "")
TRACKING_IP_HASH_KEY = os.environ.get("TRACKING_IP_HASH_KEY", "")
TRACKING_STORAGE_KEY = "inland_tracking_sid"
TRACKING_COLLECTION_PATH = "/api/track/collect/"
TRACKING_COLLECT_RATE = os.environ.get("TRACKING_COLLECT_RATE", "30/m")
TRACKING_WEBHOOK_RATE = os.environ.get("TRACKING_WEBHOOK_RATE", "10/m")
TRACKING_RETENTION_DAYS = int(os.environ.get("TRACKING_RETENTION_DAYS", "90"))
TRACKING_CONVERTED_RETENTION_DAYS = int(
    os.environ.get("TRACKING_CONVERTED_RETENTION_DAYS", "180")
)
TRACKING_ADMIN_ENABLED = _env_bool("TRACKING_ADMIN_ENABLED", True)
VAPI_ENABLED = _env_bool("VAPI_ENABLED")
VAPI_ALLOW_UNSIGNED = _env_bool("VAPI_ALLOW_UNSIGNED")
VAPI_SERVER_SECRET = os.environ.get("VAPI_SERVER_SECRET", "")
VAPI_RATE = os.environ.get("VAPI_RATE", "30/m")
BING_SITE_AUTH_TOKEN = os.environ.get("BING_SITE_AUTH_TOKEN", "")
BOOKING_DOMAIN = os.environ.get("BOOKING_DOMAIN", "")
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "")
TRUSTED_PROXY_CIDRS = _env_list("TRUSTED_PROXY_CIDRS")

# ── Default primary key ───────────────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ── Logging ────────────────────────────────────────────────────
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {"format": "{levelname} {message}", "style": "{"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "simple"},
    },
    "root": {"handlers": ["console"], "level": "WARNING"},
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "django.security": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "home": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "services": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "blog": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "locations": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "pages": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "mysite": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}

# ── Email (override in production.py for real SMTP) ───────────
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
