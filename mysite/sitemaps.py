"""Custom XML sitemaps with per-type priorities, changefreq, lastmod, and hreflang.

Replaces Wagtail's flat default sitemap with granular control over
crawl priority signals. Each page type gets its own sitemap section
with appropriate priority and change frequency values.

Includes hreflang annotations so Google sees dual signals
(HTML <head> + sitemap) for multilingual pages.

Also provides an image sitemap view for blog and service featured images.
"""

from __future__ import annotations

import logging
from typing import Any

from django.contrib.sitemaps import Sitemap
from django.http import HttpRequest, HttpResponse
from wagtail.models import Page

from blog.models import BlogIndexPage, BlogPage
from home.models import HomePage
from locations.models import CityPage, LocationsIndexPage
from pages.models import StaticPage
from services.models import ServicePage, ServicesIndexPage

logger = logging.getLogger(__name__)


class _WagtailPageSitemap(Sitemap):
    """Base sitemap for Wagtail pages with lastmod and hreflang alternates."""

    # Let Django's sitemap view derive the scheme from the current request.
    protocol = None

    def items(self) -> list[Page]:
        return list(self.model.objects.live().public().order_by("-last_published_at"))

    def lastmod(self, obj: Page) -> Any:
        return obj.last_published_at

    def location(self, obj: Page) -> str:
        return obj.get_url() or "/"

    def get_urls(
        self, page: int = 1, site: Any = None, protocol: str | None = None
    ) -> list[dict[str, Any]]:
        """Add hreflang alternates to each URL entry for multilingual SEO."""
        urls = super().get_urls(page=page, site=site, protocol=protocol)
        proto = protocol or self.protocol
        domain = site.domain if site else ""

        for url_info in urls:
            item = url_info.get("item")
            if not item or not hasattr(item, "get_translations"):
                continue

            lang = str(item.locale.language_code) if hasattr(item, "locale") else "en"
            page_url = f"{proto}://{domain}{item.get_url()}"

            alternates: list[dict[str, str]] = [
                {"lang_code": lang, "location": page_url},
            ]

            for trans in item.get_translations().live():
                trans_lang = str(trans.locale.language_code)
                trans_url = f"{proto}://{domain}{trans.get_url()}"
                alternates.append({"lang_code": trans_lang, "location": trans_url})

            # x-default points to English version
            if lang == "en":
                alternates.append({"lang_code": "x-default", "location": page_url})
            else:
                for trans in item.get_translations().live():
                    if str(trans.locale.language_code) == "en":
                        alternates.append(
                            {
                                "lang_code": "x-default",
                                "location": f"{proto}://{domain}{trans.get_url()}",
                            }
                        )
                        break

            url_info["alternates"] = alternates

        return urls


class HomePageSitemap(_WagtailPageSitemap):
    """Homepage — highest priority, changes weekly (pricing, reviews)."""

    model = HomePage
    changefreq = "weekly"
    priority = 1.0


class ServicePageSitemap(_WagtailPageSitemap):
    """Individual service pages — high priority money pages."""

    model = ServicePage
    changefreq = "weekly"
    priority = 0.9


class ServicesIndexSitemap(_WagtailPageSitemap):
    """Services listing page."""

    model = ServicesIndexPage
    changefreq = "weekly"
    priority = 0.8


class CityPageSitemap(_WagtailPageSitemap):
    """City/location pages — high priority for local SEO."""

    model = CityPage
    changefreq = "weekly"
    priority = 0.9


class LocationsIndexSitemap(_WagtailPageSitemap):
    """Locations listing page."""

    model = LocationsIndexPage
    changefreq = "weekly"
    priority = 0.8


class BlogPageSitemap(_WagtailPageSitemap):
    """Individual blog posts — medium priority content pages."""

    model = BlogPage
    changefreq = "monthly"
    priority = 0.6


class BlogIndexSitemap(_WagtailPageSitemap):
    """Blog listing page."""

    model = BlogIndexPage
    changefreq = "weekly"
    priority = 0.5


class StaticPageSitemap(_WagtailPageSitemap):
    """Static pages (About, Contact) — medium priority."""

    model = StaticPage
    changefreq = "monthly"
    priority = 0.7


# Registry used in urls.py
SITEMAPS: dict[str, type[Sitemap]] = {
    "home": HomePageSitemap,
    "services": ServicePageSitemap,
    "services-index": ServicesIndexSitemap,
    "cities": CityPageSitemap,
    "locations-index": LocationsIndexSitemap,
    "blog-posts": BlogPageSitemap,
    "blog-index": BlogIndexSitemap,
    "static-pages": StaticPageSitemap,
}


def _append_image_entry(
    lines: list[str],
    request: HttpRequest,
    page: Page,
    caption: str = "",
) -> None:
    """Append a <url> with <image:image> for a page's featured_image."""
    from django.utils.html import escape as esc

    page_url = request.build_absolute_uri(page.get_url())
    try:
        image_url = request.build_absolute_uri(page.featured_image.file.url)
    except (AttributeError, ValueError) as exc:
        logger.warning("Skipping image sitemap entry for '%s': %s", page.title, exc)
        return

    lines.append("  <url>")
    lines.append(f"    <loc>{esc(page_url)}</loc>")
    lines.append("    <image:image>")
    lines.append(f"      <image:loc>{esc(image_url)}</image:loc>")
    lines.append(f"      <image:title>{esc(page.title)}</image:title>")
    alt_text = getattr(page.featured_image, "alt", "") or page.title
    if alt_text:
        lines.append(f"      <image:alt>{esc(alt_text)}</image:alt>")
    if caption:
        lines.append(f"      <image:caption>{esc(caption)}</image:caption>")
    lines.append("    </image:image>")

    # Include inline images from StreamField body (blog posts)
    if hasattr(page, "body") and hasattr(page.body, "__iter__"):
        for block in page.body:
            if block.block_type == "image" and block.value:
                try:
                    inline_url = request.build_absolute_uri(block.value.file.url)
                    lines.append("    <image:image>")
                    lines.append(f"      <image:loc>{esc(inline_url)}</image:loc>")
                    img_title = getattr(block.value, "title", "")
                    if img_title:
                        lines.append(
                            f"      <image:title>{esc(img_title)}</image:title>"
                        )
                    lines.append("    </image:image>")
                except (AttributeError, TypeError, ValueError) as exc:
                    logger.warning("Skipping inline image in '%s': %s", page.title, exc)

    lines.append("  </url>")


def image_sitemap_view(request: HttpRequest) -> HttpResponse:
    """Generate image sitemap XML for blog and service featured images.

    Google recommends including ``<image:image>`` elements so it can
    discover images that may be behind lazy-loading or JavaScript.
    Covers both blog posts (with inline images) and service pages.
    """
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
    ]

    # Blog posts — featured + inline images
    posts = (
        BlogPage.objects.live()
        .public()
        .filter(featured_image__isnull=False)
        .select_related("featured_image")
        .order_by("-last_published_at")
    )
    for post in posts.iterator(chunk_size=500):
        _append_image_entry(lines, request, post, caption=post.intro)

    # Service pages — featured images (money pages, priority 0.9)
    services = (
        ServicePage.objects.live()
        .public()
        .filter(featured_image__isnull=False)
        .select_related("featured_image")
        .order_by("-last_published_at")
    )
    for service in services.iterator(chunk_size=500):
        _append_image_entry(lines, request, service, caption=service.intro)

    lines.append("</urlset>")

    response = HttpResponse(
        "\n".join(lines),
        content_type="application/xml; charset=utf-8",
    )
    response["Cache-Control"] = "public, max-age=3600"
    return response
