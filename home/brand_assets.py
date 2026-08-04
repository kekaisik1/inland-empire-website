"""Shared brand card/logo metadata for target templates."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

BRAND_LOGOS: tuple[dict[str, str | None], ...] = (
    {
        "name": "Whirlpool",
        "slug": "whirlpool-appliance-repair",
        "logo_static": "images/brand-logos/whirlpool.png",
        "logo_source": "Whirlpool Corporation official brand logo asset",
        "logo_kind": "wordmark",
    },
    {
        "name": "Samsung",
        "slug": "samsung-appliance-repair",
        "logo_static": "images/brand-logos/samsung.svg",
        "logo_source": "Simple Icons Samsung SVG",
        "logo_kind": "icon",
    },
    {
        "name": "LG",
        "slug": "lg-appliance-repair",
        "logo_static": "images/brand-logos/lg.svg",
        "logo_source": "Simple Icons LG SVG",
        "logo_kind": "icon",
    },
    {
        "name": "GE",
        "slug": "ge-appliance-repair",
        "logo_static": "images/brand-logos/ge.svg",
        "logo_source": "Simple Icons General Electric SVG",
        "logo_kind": "icon",
    },
    {
        "name": "Maytag",
        "slug": "maytag-appliance-repair",
        "logo_static": "images/brand-logos/maytag.svg",
        "logo_source": "Simple Icons Maytag SVG",
        "logo_kind": "icon",
    },
    {
        "name": "Bosch",
        "slug": "bosch-appliance-repair",
        "logo_static": "images/brand-logos/bosch.svg",
        "logo_source": "Simple Icons Bosch SVG",
        "logo_kind": "icon",
    },
    {
        "name": "KitchenAid",
        "slug": "kitchenaid-appliance-repair",
        "logo_static": "images/brand-logos/kitchenaid.svg",
        "logo_source": "Wikimedia Commons KitchenAid SVG",
        "logo_kind": "wordmark",
    },
    {
        "name": "Sub-Zero",
        "slug": "sub-zero-appliance-repair",
        "logo_static": "images/brand-logos/sub-zero.svg",
        "logo_source": "Wikimedia Commons Sub-Zero SVG",
        "logo_kind": "wordmark",
    },
    {
        "name": "Viking",
        "slug": "viking-appliance-repair",
        "logo_static": "images/brand-logos/viking.svg",
        "logo_source": "generated non-official wordmark fallback",
        "logo_kind": "wordmark",
    },
    {
        "name": "Thermador",
        "slug": "thermador-appliance-repair",
        "logo_static": "images/brand-logos/thermador.jpg",
        "logo_source": "Wikimedia Commons Thermador JPG",
        "logo_kind": "wordmark",
    },
    {
        "name": "Miele",
        "slug": "miele-appliance-repair",
        "logo_static": "images/brand-logos/miele.svg",
        "logo_source": "generated non-official wordmark fallback",
        "logo_kind": "wordmark",
    },
    {
        "name": "Kenmore",
        "slug": "kenmore-appliance-repair",
        "logo_static": "images/brand-logos/kenmore.svg",
        "logo_source": "generated non-official wordmark fallback",
        "logo_kind": "wordmark",
    },
    {
        "name": "Frigidaire",
        "slug": "frigidaire-appliance-repair",
        "logo_static": "images/brand-logos/frigidaire.svg",
        "logo_source": "generated non-official wordmark fallback",
        "logo_kind": "wordmark",
    },
    {
        "name": "Amana",
        "slug": "amana-appliance-repair",
        "logo_static": "images/brand-logos/amana.svg",
        "logo_source": "generated non-official wordmark fallback",
        "logo_kind": "wordmark",
    },
    {
        "name": "Electrolux",
        "slug": "electrolux-appliance-repair",
        "logo_static": "images/brand-logos/electrolux.svg",
        "logo_source": "generated non-official wordmark fallback",
        "logo_kind": "wordmark",
    },
    {
        "name": "Speed Queen",
        "slug": "speed-queen-appliance-repair",
        "logo_static": "images/brand-logos/speed-queen.svg",
        "logo_source": "generated non-official wordmark fallback",
        "logo_kind": "wordmark",
    },
    {
        "name": "Fisher & Paykel",
        "slug": "fisher-paykel-appliance-repair",
        "logo_static": "images/brand-logos/fisher-paykel.svg",
        "logo_source": "generated non-official wordmark fallback",
        "logo_kind": "wordmark",
    },
    {
        "name": "Monogram",
        "slug": "monogram-appliance-repair",
        "logo_static": "images/brand-logos/monogram.svg",
        "logo_source": "generated non-official wordmark fallback",
        "logo_kind": "wordmark",
    },
    {
        "name": "Wolf",
        "slug": "wolf-appliance-repair",
        "logo_static": "images/brand-logos/wolf.svg",
        "logo_source": "generated non-official wordmark fallback",
        "logo_kind": "wordmark",
    },
)


def get_brand_cards(
    service_pages_by_slug: Mapping[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Return template-ready brand cards with optional linked service pages."""
    pages = service_pages_by_slug or {}
    return [
        {
            "name": brand["name"],
            "slug": brand["slug"],
            "page": pages.get(str(brand["slug"])),
            "logo_static": brand["logo_static"],
            "logo_source": brand["logo_source"],
            "logo_kind": brand["logo_kind"],
        }
        for brand in BRAND_LOGOS
    ]
