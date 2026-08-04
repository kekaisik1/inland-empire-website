"""SEO and performance middleware."""

from __future__ import annotations

import ipaddress

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.http import http_date


class RealIPMiddleware:
    """Trust forwarding headers only when the immediate peer is configured."""

    def __init__(self, get_response: object) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        peer_text = request.META.get("REMOTE_ADDR", "")
        try:
            peer = ipaddress.ip_address(peer_text)
        except ValueError:
            return self.get_response(request)
        networks = []
        for value in getattr(settings, "TRUSTED_PROXY_CIDRS", ()):
            try:
                networks.append(ipaddress.ip_network(value, strict=False))
            except ValueError:
                continue
        if not any(peer in network for network in networks):
            return self.get_response(request)

        forwarded = request.headers.get("X-Forwarded-For", "")
        if forwarded:
            try:
                chain = [ipaddress.ip_address(item.strip()) for item in forwarded.split(",")]
            except ValueError:
                chain = []
            if chain:
                candidate = peer
                for address in reversed(chain):
                    candidate = address
                    if not any(address in network for network in networks):
                        break
                request.META["REMOTE_ADDR"] = str(candidate)
                return self.get_response(request)

        try:
            request.META["REMOTE_ADDR"] = str(
                ipaddress.ip_address(request.headers.get("X-Real-IP", ""))
            )
        except ValueError:
            pass
        return self.get_response(request)


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
        if is_html and "X-Robots-Tag" not in response:
            if response.status_code >= 400 or request.path.startswith(
                ("/admin/", "/django-admin/", "/api/")
            ):
                response["X-Robots-Tag"] = "noindex, nofollow"
            elif request.path.startswith(("/search/", "/es/search/")):
                response["X-Robots-Tag"] = "noindex, follow"
            else:
                response["X-Robots-Tag"] = "index, follow"

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
        varies_on_cookie = "cookie" in response.get("Vary", "").lower()
        sets_cookie = bool(response.cookies)
        if is_cacheable and is_anonymous and not varies_on_cookie and not sets_cookie:
            response["Cache-Control"] = (
                f"public, max-age={self.CACHE_MAX_AGE}, stale-while-revalidate=60"
            )
        elif is_html and not is_anonymous:
            response["Cache-Control"] = "private, no-store"

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
                "<https://fonts.googleapis.com>; rel=preconnect; crossorigin, "
                "<https://fonts.gstatic.com>; rel=preconnect; crossorigin, "
                "<https://cdn.jsdelivr.net>; rel=preconnect; crossorigin"
            )

        # Content-Security-Policy (security trust signal for search engines)
        if "Content-Security-Policy" not in response:
            response["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://www.googletagmanager.com "
                "https://www.google-analytics.com https://cdn.jsdelivr.net https://cdn.callrail.com; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
                "img-src 'self' data: blob: https://res.cloudinary.com "
                "https://www.googletagmanager.com https://www.google-analytics.com; "
                "font-src 'self' https://fonts.gstatic.com; "
                "connect-src 'self' https://www.google-analytics.com https://analytics.google.com "
                "https://region1.google-analytics.com https://www.googletagmanager.com "
                "https://cdn.callrail.com; "
                "frame-src 'self' https://www.googletagmanager.com; "
                "media-src 'self' blob: https://res.cloudinary.com; "
                "object-src 'none'; "
                "base-uri 'self'; "
                "form-action 'self'; "
                "frame-ancestors 'self'"
            )

        return response
