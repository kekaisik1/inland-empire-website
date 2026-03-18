"""URL configuration for the LOWL website."""

from __future__ import annotations

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import include, path

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from mysite.sitemaps import SITEMAPS


def health_check(request: HttpRequest) -> JsonResponse:
    """Health check endpoint for monitoring and container orchestration."""
    return JsonResponse({"status": "ok"})


def robots_txt(request: HttpRequest) -> HttpResponse:
    """Serve a dynamic robots.txt with sitemap reference and AI bot blocking."""
    base_url = f"https://{request.get_host()}"
    # AI training crawlers to block (comprehensive, updated 2026)
    ai_bots = [
        "GPTBot",
        "ChatGPT-User",
        "Google-Extended",
        "CCBot",
        "anthropic-ai",
        "ClaudeBot",
        "Claude-Web",
        "Bytespider",
        "FacebookBot",
        "Applebot-Extended",
        "PerplexityBot",
        "Amazonbot",
        "Diffbot",
        "Omgilibot",
        "Timpibot",
        "PetalBot",
        "YouBot",
        "AI2Bot",
        "Cohere-ai",
        "cohere-training",
        "Meta-ExternalAgent",
        "Meta-ExternalFetcher",
        "ImagesiftBot",
        "Kangaroo Bot",
        "ISSCyberRiskCrawler",
    ]
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        "# Block admin, internal paths, and duplicate content",
        "Disallow: /admin/",
        "Disallow: /django-admin/",
        "Disallow: /search/",
        "Disallow: /es/search/",
        "Disallow: /documents/",
        "Disallow: /health/",
        "",
        "# Block AI training crawlers",
    ]
    for bot in ai_bots:
        lines += [f"User-agent: {bot}", "Disallow: /", ""]
    # Crawl budget: slow down aggressive/unknown bots
    lines += [
        "# Crawl rate limits for aggressive bots",
        "User-agent: SemrushBot",
        "Crawl-delay: 10",
        "",
        "User-agent: AhrefsBot",
        "Crawl-delay: 10",
        "",
        "User-agent: DotBot",
        "Crawl-delay: 10",
        "",
        "User-agent: MJ12bot",
        "Crawl-delay: 10",
        "",
        f"Sitemap: {base_url}/sitemap.xml",
        f"Sitemap: {base_url}/sitemap-images.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


def _image_sitemap(request: HttpRequest) -> HttpResponse:
    """Serve an image sitemap for blog featured and inline images."""
    from mysite.sitemaps import image_sitemap_view

    return image_sitemap_view(request)


# Non-localised URLs (admin, docs, health check)
urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("health/", health_check, name="health_check"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": SITEMAPS},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("sitemap-images.xml", _image_sitemap, name="image_sitemap"),
]


# Localised URLs — English has no prefix, Spanish gets /es/
urlpatterns += i18n_patterns(
    path("search/", include("search.urls")),
    path("contact/", include("pages.urls")),
    path("", include(wagtail_urls)),
    prefix_default_language=False,
)

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    try:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
    except ImportError:
        pass
