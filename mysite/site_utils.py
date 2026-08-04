"""Request-derived URL helpers for structured and machine-readable content."""

from __future__ import annotations

from django.http import HttpRequest


def absolute_site_url(request: HttpRequest, path: str) -> str:
    """Build a same-origin absolute URL; reject externally supplied URLs."""
    if not isinstance(path, str) or not path.startswith("/") or path.startswith("//"):
        return ""
    return request.build_absolute_uri(path)
