"""Static image fallbacks for service-area CityPage templates."""

from __future__ import annotations

from typing import TypedDict


class CityHeroImages(TypedDict):
    """Template-ready static image paths for one city hero image set."""

    fallback: str
    webp_480: str
    webp_768: str
    webp_1200: str
    og: str


CITY_STATIC_HERO_BASES: dict[str, str] = {
    "appliance-repair-beaumont-ca": "appliance-repair-beaumont-ca-hero",
    "appliance-repair-canyon-lake-ca": "appliance-repair-canyon-lake-ca-hero",
    "appliance-repair-corona-ca": "appliance-repair-corona-ca-hero",
    "appliance-repair-lake-elsinore-ca": "appliance-repair-lake-elsinore-ca-hero",
    "appliance-repair-menifee-ca": "appliance-repair-menifee-ca-hero",
    "appliance-repair-murrieta-ca": "appliance-repair-murrieta-ca-hero",
    "appliance-repair-norco-ca": "appliance-repair-norco-ca-hero",
    "appliance-repair-perris-ca": "appliance-repair-perris-ca-hero",
    "appliance-repair-riverside-ca": "appliance-repair-riverside-ca-hero",
    "appliance-repair-temecula-ca": "appliance-repair-temecula-ca-hero",
}


def get_static_city_hero_images(slug: str) -> CityHeroImages | None:
    """Return responsive static image paths for a known service-area slug."""
    base = CITY_STATIC_HERO_BASES.get(slug)
    if not base:
        return None

    prefix = f"images/service-areas/{base}"
    return {
        "fallback": f"{prefix}.png",
        "webp_480": f"{prefix}-480.webp",
        "webp_768": f"{prefix}-768.webp",
        "webp_1200": f"{prefix}-1200.webp",
        "og": f"{prefix}-1200.webp",
    }
