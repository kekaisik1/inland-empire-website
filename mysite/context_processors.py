"""Context processors providing global template data."""

from __future__ import annotations

import logging
import os
from typing import Any

from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest
from django.utils.translation import get_language, gettext as _
from wagtail.models import Locale, Page, Site

logger = logging.getLogger(__name__)

MAIN_NAV_DEFAULT_ORDER = "home,services,service_areas,brands,blog,about,contact"
FOOTER_COMPANY_DEFAULT_ORDER = (
    "about,contact,blog,service_areas,privacy_policy,terms_of_service"
)
MAIN_NAV_CONFIG = {
    "home": ("Home", "/", "link"),
    "services": ("Services", "/services/", "services_dropdown"),
    "service_areas": ("Service Areas", "/service-areas/", "areas_dropdown"),
    "brands": ("Brands", "", "brands_dropdown"),
    "blog": ("Blog", "/blog/", "link"),
    "about": ("About", "/about-us/", "link"),
    "contact": ("Contact", "/contact/", "link"),
}
FOOTER_COMPANY_CONFIG = {
    "about": ("About Us", "/about-us/"),
    "contact": ("Contact", "/contact/"),
    "blog": ("Blog", "/blog/"),
    "service_areas": ("Service Areas", "/service-areas/"),
    "privacy_policy": ("Privacy Policy", "/privacy-policy/"),
    "terms_of_service": ("Terms of Service", "/terms-of-service/"),
}


def _request_language(request: HttpRequest) -> str:
    """Resolve the public locale without trusting an unrelated active thread locale."""

    if request.path == "/es" or request.path.startswith("/es/"):
        return "es"
    request_language = getattr(request, "LANGUAGE_CODE", "")
    if request_language:
        return str(request_language).split("-", 1)[0]
    return str(get_language() or "en").split("-", 1)[0]


def _localized_path(path: str, language: str) -> str:
    if not path:
        return ""
    if language == "es":
        return "/es/" if path == "/" else f"/es{path}"
    return path


def _ordered_keys(raw_order: str, default_order: str, allowed: set[str]) -> list[str]:
    """Normalize editor ordering while dropping unknown and duplicate keys."""

    ordered: list[str] = []
    for key in (raw_order or default_order).split(","):
        normalized = key.strip()
        if normalized in allowed and normalized not in ordered:
            ordered.append(normalized)
    if ordered:
        return ordered
    return [key for key in default_order.split(",") if key in allowed]


def _build_main_nav_items(raw_order: str, language: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for key in _ordered_keys(
        raw_order,
        MAIN_NAV_DEFAULT_ORDER,
        set(MAIN_NAV_CONFIG),
    ):
        label, path, kind = MAIN_NAV_CONFIG[key]
        items.append(
            {
                "key": key,
                "label": _(label),
                "url": _localized_path(path, language),
                "kind": kind,
            }
        )
    return items


def _build_footer_company_links(
    raw_order: str,
    language: str,
) -> list[dict[str, str]]:
    links: list[dict[str, str]] = []
    for key in _ordered_keys(
        raw_order,
        FOOTER_COMPANY_DEFAULT_ORDER,
        set(FOOTER_COMPANY_CONFIG),
    ):
        label, path = FOOTER_COMPANY_CONFIG[key]
        links.append(
            {
                "key": key,
                "label": _(label),
                "url": _localized_path(path, language),
            }
        )
    return links


def _get_live_pages_for_locale(
    model: type[Page],
    lang: str,
    fields: tuple[str, ...] = ("id", "title", "slug", "url_path"),
    order_by: str = "path",
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
    language = _request_language(request)
    try:
        from home.models import SiteSettings

        site = Site.find_for_request(request)
        site_config = SiteSettings.for_site(site) if site is not None else None
    except (Site.DoesNotExist, AttributeError):
        site_config = None

    main_nav_items = _build_main_nav_items(
        getattr(site_config, "main_nav_order", MAIN_NAV_DEFAULT_ORDER),
        language,
    )
    footer_company_links = _build_footer_company_links(
        getattr(site_config, "footer_company_order", FOOTER_COMPANY_DEFAULT_ORDER),
        language,
    )

    # Admin, health, and API responses do not render the public menus. Keep the
    # cheap ordering contract available while avoiding service/city queries.
    if request.path.startswith(("/admin/", "/django-admin/", "/health", "/api/")):
        return {
            "global_services": [],
            "service_menu_items": [],
            "global_cities": [],
            "brand_menu_items": [],
            "service_zip_codes": [],
            "main_nav_items": main_nav_items,
            "footer_company_links": footer_company_links,
        }

    from home.brand_assets import get_brand_cards
    from home.service_seed_data import SEO_LANDING_SERVICE_SLUGS
    from locations.models import CityPage
    from services.models import ServicePage

    timeout: int = getattr(settings, "NAV_CACHE_TIMEOUT", 300)
    cache_key_services = f"inland:nav:services:{language}"
    cache_key_cities = f"inland:nav:cities:{language}"

    global_services = cache.get(cache_key_services)
    if global_services is None:
        global_services = _get_live_pages_for_locale(
            ServicePage,
            language,
            fields=("id", "title", "slug", "url_path", "is_regional_service_page"),
        )
        global_services = [
            service
            for service in global_services
            if not service.is_regional_service_page
        ]
        cache.set(cache_key_services, global_services, timeout)

    global_cities = cache.get(cache_key_cities)
    if global_cities is None:
        global_cities = _get_live_pages_for_locale(
            CityPage,
            language,
            fields=("id", "title", "slug", "url_path", "zip_codes"),
        )
        cache.set(cache_key_cities, global_cities, timeout)

    services_by_slug = {str(service.slug): service for service in global_services}
    service_menu_items = [
        service
        for service in global_services
        if str(service.slug) not in SEO_LANDING_SERVICE_SLUGS
    ]
    brand_menu_items = [
        card for card in get_brand_cards(services_by_slug) if card["page"] is not None
    ]
    service_zip_codes: list[str] = []
    for city in global_cities:
        for value in str(city.zip_codes or "").split(","):
            zip_code = value.strip()
            if len(zip_code) == 5 and zip_code.isdigit() and zip_code not in service_zip_codes:
                service_zip_codes.append(zip_code)
    settings_zip = str(getattr(site_config, "zip_code", "") or "").strip()
    if len(settings_zip) == 5 and settings_zip.isdigit() and settings_zip not in service_zip_codes:
        service_zip_codes.append(settings_zip)

    return {
        "global_services": global_services,
        "service_menu_items": service_menu_items,
        "global_cities": global_cities,
        "brand_menu_items": brand_menu_items,
        "service_zip_codes": service_zip_codes,
        "main_nav_items": main_nav_items,
        "footer_company_links": footer_company_links,
    }


def tracking_context(request: HttpRequest) -> dict[str, Any]:
    """Expose a cookie-free, consent-gated client tracking contract."""
    return {
        "tracking_enabled": bool(getattr(settings, "TRACKING_ENABLED", False)),
        "tracking_consent_required": bool(
            getattr(settings, "TRACKING_REQUIRE_CONSENT", True)
        ),
        "tracking_storage": "sessionStorage",
        "tracking_storage_key": getattr(
            settings, "TRACKING_STORAGE_KEY", "inland_tracking_sid"
        ),
        "tracking_endpoint": getattr(
            settings, "TRACKING_COLLECTION_PATH", "/api/track/collect/"
        ),
        "booking_domain": getattr(settings, "BOOKING_DOMAIN", ""),
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
