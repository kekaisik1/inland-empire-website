"""Responsive static hero-image metadata for service detail pages."""

from __future__ import annotations

from typing import TypedDict


class ServiceHeroImages(TypedDict):
    fallback: str
    webp_480: str
    webp_768: str
    webp_1200: str
    og: str


SERVICE_STATIC_HERO_SLUGS = frozenset(
    {
        "air-conditioning-repair-hvac",
        "dishwasher-repair",
        "dryer-repair",
        "freezer-repair",
        "ge-appliance-repair",
        "lg-appliance-repair",
        "maytag-appliance-repair",
        "microwave-repair",
        "oven-repair",
        "refrigerator-repair",
        "samsung-appliance-repair",
        "stove-repair",
        "washer-repair",
        "water-heater-repair",
        "whirlpool-appliance-repair",
    }
)


def get_static_service_hero_images(slug: str) -> ServiceHeroImages | None:
    """Return target-owned responsive static paths for a known service slug."""
    if slug not in SERVICE_STATIC_HERO_SLUGS:
        return None

    prefix = f"images/service-hero-{slug}"
    return {
        "fallback": f"{prefix}.png",
        "webp_480": f"{prefix}-480.webp",
        "webp_768": f"{prefix}-768.webp",
        "webp_1200": f"{prefix}-1200.webp",
        "og": f"{prefix}-1200.webp",
    }
