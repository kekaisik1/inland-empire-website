"""Plain-text discovery endpoints for language-model consumers."""

from __future__ import annotations

import re

from django.http import HttpRequest, HttpResponse
from django.utils.html import strip_tags
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET
from wagtail.models import Site

from home.models import SiteSettings
from locations.models import CityPage
from services.models import ServicePage


def _plain(value: object, limit: int = 500) -> str:
    text = strip_tags(str(value or ""))
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text).strip()[:limit]


def _site_context(request: HttpRequest) -> tuple[SiteSettings, list, list]:
    site = Site.find_for_request(request)
    business = SiteSettings.for_site(site)
    services = list(ServicePage.objects.live().public().order_by("title"))
    cities = list(CityPage.objects.live().public().order_by("title"))
    return business, services, cities


def _url(request: HttpRequest, page: object) -> str:
    path = getattr(page, "url", "") or "/"
    return request.build_absolute_uri(path)


@require_GET
@cache_page(3600)
def llms_txt(request: HttpRequest) -> HttpResponse:
    business, services, cities = _site_context(request)
    lines = [
        f"# {_plain(business.business_name, 120)}",
        "",
        f"> {_plain(getattr(business, 'description', ''), 400)}",
        "",
        f"Website: {request.build_absolute_uri('/')}",
        f"Phone: {_plain(business.phone, 80)}",
        f"Email: {_plain(business.email, 120)}",
        f"Service area: {_plain(business.city, 80)}, {_plain(business.state, 20)}",
        "",
        "## Services",
    ]
    lines.extend(f"- {_plain(page.title, 120)}: {_url(request, page)}" for page in services)
    lines.extend(("", "## Service Areas"))
    lines.extend(f"- {_plain(page.title, 120)}: {_url(request, page)}" for page in cities)
    response = HttpResponse("\n".join(lines) + "\n", content_type="text/plain; charset=utf-8")
    response["Cache-Control"] = "public, max-age=3600"
    return response


@require_GET
@cache_page(3600)
def llms_full_txt(request: HttpRequest) -> HttpResponse:
    business, services, cities = _site_context(request)
    sections = [
        f"# {_plain(business.business_name, 120)} — Full Guide",
        "",
        f"Canonical website: {request.build_absolute_uri('/')}",
        f"Contact: {_plain(business.phone, 80)} | {_plain(business.email, 120)}",
        "",
        "## Services",
    ]
    for page in services:
        sections.extend(
            (f"### {_plain(page.title, 120)}", _url(request, page), _plain(getattr(page, "intro", "")), "")
        )
    sections.append("## Service Areas")
    for page in cities:
        sections.extend(
            (f"### {_plain(page.title, 120)}", _url(request, page), _plain(getattr(page, "intro", "")), "")
        )
    response = HttpResponse("\n".join(sections) + "\n", content_type="text/plain; charset=utf-8")
    response["Cache-Control"] = "public, max-age=3600"
    return response
