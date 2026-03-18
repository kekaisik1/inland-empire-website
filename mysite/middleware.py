"""SEO and performance middleware."""

from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.utils.http import http_date


class SEOHeadersMiddleware:
    """Add SEO-relevant HTTP headers to responses.

    - Permissions-Policy: restricts browser features for security signals.
    - Cache-Control: sets browser caching for anonymous HTML pages.
    - Last-Modified: helps crawlers optimize crawl budget.
    - X-Robots-Tag: reinforces indexing directives at HTTP level.
    - Link: preconnect hints for faster resource loading.
    """

    CACHE_MAX_AGE: int = 300  # 5 minutes for HTML pages
    STATIC_CACHE_MAX_AGE: int = 31_536_000  # 1 year for static assets

    def __init__(self, get_response: object) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)

        is_html = "text/html" in response.get("Content-Type", "")
        is_admin = request.path.startswith(("/admin/", "/django-admin/"))

        # Permissions-Policy (restricts unused browser APIs — trust signal)
        if "Permissions-Policy" not in response:
            response["Permissions-Policy"] = (
                "camera=(), microphone=(), geolocation=(self), payment=()"
            )

        # X-Robots-Tag header reinforces meta robots for search engines
        if is_html and not is_admin and "X-Robots-Tag" not in response:
            response["X-Robots-Tag"] = (
                "index, follow, max-snippet:-1, max-image-preview:large,"
                " max-video-preview:-1"
            )

        # Last-Modified from Wagtail page's last_published_at (crawl budget)
        if is_html and not is_admin and "Last-Modified" not in response:
            page = getattr(request, "wagtailpage", None)
            if page is None:
                # Wagtail stores the served page on the request via serve()
                page = getattr(request, "_wagtail_page", None)
            last_published = getattr(page, "last_published_at", None) if page else None
            if last_published:
                response["Last-Modified"] = http_date(last_published.timestamp())

        # Cache-Control for anonymous, non-admin HTML responses
        is_cacheable = (
            "Cache-Control" not in response
            and request.method == "GET"
            and response.status_code == 200
            and is_html
            and not is_admin
        )
        is_anonymous = not hasattr(request, "user") or not request.user.is_authenticated
        if is_cacheable and is_anonymous:
            response["Cache-Control"] = (
                f"public, max-age={self.CACHE_MAX_AGE}, stale-while-revalidate=60"
            )

        # Vary: Accept-Language so CDNs/proxies cache i18n pages separately
        if is_html and not is_admin:
            vary = response.get("Vary", "")
            if "Accept-Language" not in vary:
                response["Vary"] = (
                    f"{vary}, Accept-Language" if vary else "Accept-Language"
                )

        # Link header: preconnect hints for critical third-party origins
        # Browsers can start DNS+TCP+TLS before parsing HTML
        if is_html and not is_admin and "Link" not in response:
            response["Link"] = (
                "<https://api.fontshare.com>; rel=preconnect; crossorigin, "
                "<https://cdn.fontshare.com>; rel=preconnect; crossorigin, "
                "<https://cdn.jsdelivr.net>; rel=preconnect; crossorigin"
            )

        # Content-Security-Policy (security trust signal for search engines)
        if "Content-Security-Policy" not in response:
            response["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://www.googletagmanager.com "
                "https://www.google-analytics.com https://cdn.jsdelivr.net "
                "https://googleads.g.doubleclick.net https://www.googleadservices.com "
                "https://www.gstatic.com https://mc.yandex.ru; "
                "style-src 'self' 'unsafe-inline' https://api.fontshare.com; "
                "img-src 'self' data: https://res.cloudinary.com https://www.googletagmanager.com "
                "https://www.google.com https://*.google.com https://*.google.co.* "
                "https://googleads.g.doubleclick.net https://www.google-analytics.com "
                "https://www.googleadservices.com https://mc.yandex.ru; "
                "font-src 'self' https://api.fontshare.com https://cdn.fontshare.com; "
                "connect-src 'self' https://www.google-analytics.com https://analytics.google.com "
                "https://www.googletagmanager.com https://www.google.com "
                "https://googleads.g.doubleclick.net https://mc.yandex.ru; "
                "frame-src https://www.googletagmanager.com https://googleads.g.doubleclick.net; "
                "base-uri 'self'; "
                "form-action 'self'; "
                "frame-ancestors 'none'"
            )

        return response
