"""Development settings."""

from __future__ import annotations

from .base import *  # noqa: F401, F403

DEBUG = True
SECRET_KEY = "django-insecure-dev-only-change-in-production-xxxxxxxxxxxxxx"
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += ["debug_toolbar"]  # type: ignore[name-defined]  # noqa: F405
MIDDLEWARE.insert(  # type: ignore[name-defined]  # noqa: F405
    MIDDLEWARE.index("django.middleware.gzip.GZipMiddleware") + 1,  # type: ignore[name-defined]  # noqa: F405
    "debug_toolbar.middleware.DebugToolbarMiddleware",
)
INTERNAL_IPS = ["127.0.0.1"]
