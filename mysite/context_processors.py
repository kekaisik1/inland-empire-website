"""Context processors providing global template data."""

from __future__ import annotations

import logging
import os
from typing import Any

from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest
from django.utils.translation import get_language
from wagtail.models import Locale, Page

logger = logging.getLogger(__name__)


def _get_live_pages_for_locale(
    model: type[Page],
    lang: str,
    fields: tuple[str, ...] = ("id", "title", "slug", "url_path"),
    order_by: str = "title",
) -> list[Page]:
    """Fetch live pages filtered by locale, falling back to all locales."""
    try:
        locale = Locale.objects.get(language_code=lang)
        return list(
            model.objects.live().filter(locale=locale).order_by(order_by).only(*fields)
        )
    except Locale.DoesNotExist:
        return list(model.objects.live().order_by(order_by).only(*fields))


def navigation_data(request: HttpRequest) -> dict[str, Any]:
    """Provide cached navigation data (services + cities) to all templates.

    Filters pages by the current locale so that Spanish pages show in /es/
    and English pages show on the default site.
    """
    # Skip DB queries for non-page requests (admin, health check, API)
    if request.path.startswith(("/admin/", "/django-admin/", "/health")):
        return {"global_services": [], "global_cities": []}

    from locations.models import CityPage
    from services.models import ServicePage

    timeout: int = getattr(settings, "NAV_CACHE_TIMEOUT", 300)
    lang = get_language() or "en"
    cache_key_services = f"lowl:nav:services:{lang}"
    cache_key_cities = f"lowl:nav:cities:{lang}"

    global_services = cache.get(cache_key_services)
    if global_services is None:
        global_services = _get_live_pages_for_locale(
            ServicePage, lang, fields=("id", "title", "slug", "url_path")
        )
        cache.set(cache_key_services, global_services, timeout)

    global_cities = cache.get(cache_key_cities)
    if global_cities is None:
        global_cities = _get_live_pages_for_locale(
            CityPage, lang, fields=("id", "title", "slug", "url_path")
        )
        cache.set(cache_key_cities, global_cities, timeout)

    return {
        "global_services": global_services,
        "global_cities": global_cities,
    }


def site_settings_context(request: HttpRequest) -> dict[str, Any]:
    """Provide business settings to all templates from SiteSettings or env vars."""
    try:
        from home.models import SiteSettings
        from wagtail.models import Site

        site = Site.find_for_request(request)
        site_settings = SiteSettings.for_site(site)
        return {
            "biz": site_settings,
            "booking_url": site_settings.booking_url
            or os.environ.get("BOOKING_URL", "#"),
        }
    except (Site.DoesNotExist, AttributeError) as exc:
        logger.warning("SiteSettings lookup failed: %s", exc)
        return {
            "biz": None,
            "booking_url": os.environ.get("BOOKING_URL", "#"),
        }
