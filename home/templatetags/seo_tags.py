"""Custom template tags for SEO: JSON-LD structured data and breadcrumbs."""

from __future__ import annotations

import json
import logging
from typing import Any

from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

register = template.Library()
logger = logging.getLogger(__name__)


def _build_absolute_uri(context: dict[str, Any], path: str = "/") -> str:
    """Build an absolute URI from the request context."""
    request = context.get("request")
    if request and hasattr(request, "build_absolute_uri"):
        return request.build_absolute_uri(path)
    return ""


def _jsonld_script(data: dict[str, Any]) -> str:
    """Serialize a dict to a JSON-LD script tag.

    Escapes <, >, & to prevent script tag breakout (XSS)
    when CMS content contains sequences like ``</script>``.
    """
    json_str = json.dumps(data, separators=(",", ":"))
    json_str = (
        json_str.replace("<", "\\u003C").replace(">", "\\u003E").replace("&", "\\u0026")
    )
    return mark_safe(f'<script type="application/ld+json">{json_str}</script>')


_SOCIAL_ATTRS = ("google_business_url", "yelp_url", "facebook_url")


def _build_same_as(biz: Any) -> list[str]:
    """Extract social profile URLs from SiteSettings for sameAs field."""
    return [getattr(biz, attr, "") for attr in _SOCIAL_ATTRS if getattr(biz, attr, "")]


@register.simple_tag(takes_context=True)
def jsonld_local_business(context: dict[str, Any]) -> str:
    """Output JSON-LD LocalBusiness structured data with geo and reviews."""
    biz = context.get("biz")
    if not biz:
        return ""

    site_url = _build_absolute_uri(context, "/")

    data: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": ["LocalBusiness", "HomeAndConstructionBusiness"],
        "@id": f"{site_url}#business",
        "name": biz.business_name,
        "telephone": biz.phone,
        "email": biz.email,
        "url": site_url,
        "image": _build_absolute_uri(context, "/static/images/og-default.png"),
        "logo": _build_absolute_uri(context, "/static/images/icon.svg"),
        "description": (
            f"Professional appliance repair services in "
            f"{biz.city or 'Southern California'}, {biz.state or 'CA'}. "
            f"Same-day service, warranty included on all repairs."
        ),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": biz.address_line1,
            "addressLocality": biz.city,
            "addressRegion": biz.state,
            "postalCode": biz.zip_code,
            "addressCountry": "US",
        },
        "openingHours": biz.business_hours,
        "priceRange": "$$",
        "paymentAccepted": "Cash, Credit Card, Debit Card",
        "currenciesAccepted": "USD",
        "areaServed": {
            "@type": "State",
            "name": biz.state or "California",
        },
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Appliance Repair Services",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": "Appliance Diagnostic Service Call",
                        "description": "Professional on-site diagnosis of appliance issues",
                    },
                    "price": str(biz.service_call_fee),
                    "priceCurrency": "USD",
                    "priceSpecification": {
                        "@type": "UnitPriceSpecification",
                        "price": str(biz.service_call_fee),
                        "priceCurrency": "USD",
                        "unitText": "per visit",
                        "description": "Waived with repair",
                    },
                },
            ],
        },
    }

    # GeoCoordinates (helps Google Maps & local pack)
    if biz.latitude and biz.longitude:
        data["geo"] = {
            "@type": "GeoCoordinates",
            "latitude": str(biz.latitude),
            "longitude": str(biz.longitude),
        }

    # Structured opening hours from configurable fields
    opening = getattr(biz, "opening_time", None)
    closing = getattr(biz, "closing_time", None)
    # Handle both datetime.time objects and string defaults
    opens = (
        opening.strftime("%H:%M")
        if hasattr(opening, "strftime")
        else str(opening or "08:00")
    )
    closes = (
        closing.strftime("%H:%M")
        if hasattr(closing, "strftime")
        else str(closing or "20:00")
    )
    data["openingHoursSpecification"] = [
        {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ],
            "opens": opens,
            "closes": closes,
        },
    ]

    # Languages spoken
    data["knowsLanguage"] = ["en", "es"]

    # Aggregate rating from configurable fields
    if biz.google_review_count and biz.google_review_count > 0:
        data["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": str(biz.google_rating),
            "bestRating": "5",
            "reviewCount": str(biz.google_review_count),
        }

    # sameAs: social profiles for Google Knowledge Panel & local pack
    same_as = _build_same_as(biz)
    if same_as:
        data["sameAs"] = same_as

    return _jsonld_script(data)


@register.simple_tag(takes_context=True)
def jsonld_organization(context: dict[str, Any]) -> str:
    """Output JSON-LD Organization schema (separate from LocalBusiness)."""
    biz = context.get("biz")
    if not biz:
        return ""

    site_url = _build_absolute_uri(context, "/")

    data: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": f"{site_url}#organization",
        "name": biz.business_name,
        "url": site_url,
        "logo": _build_absolute_uri(context, "/static/images/icon.svg"),
        "image": _build_absolute_uri(context, "/static/images/og-default.png"),
        "telephone": biz.phone,
        "email": biz.email,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": biz.address_line1,
            "addressLocality": biz.city,
            "addressRegion": biz.state,
            "postalCode": biz.zip_code,
            "addressCountry": "US",
        },
        "contactPoint": [
            {
                "@type": "ContactPoint",
                "telephone": biz.phone,
                "contactType": "customer service",
                "areaServed": "US",
                "availableLanguage": ["English", "Spanish"],
            },
            {
                "@type": "ContactPoint",
                "telephone": biz.phone,
                "contactType": "sales",
                "areaServed": "US",
                "availableLanguage": ["English", "Spanish"],
            },
        ],
        "foundingLocation": {
            "@type": "Place",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": biz.city,
                "addressRegion": biz.state,
                "addressCountry": "US",
            },
        },
        "knowsLanguage": ["en", "es"],
    }

    # sameAs: social profiles for Google Knowledge Panel
    same_as = _build_same_as(biz)
    if same_as:
        data["sameAs"] = same_as

    return _jsonld_script(data)


@register.simple_tag(takes_context=True)
def jsonld_website(context: dict[str, Any]) -> str:
    """Output JSON-LD WebSite schema with SearchAction for sitelinks search box."""
    biz = context.get("biz")
    site_url = _build_absolute_uri(context, "/")
    if not site_url:
        return ""

    data: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": f"{site_url}#website",
        "url": site_url,
        "name": biz.business_name if biz else "LOWL Appliance Repair",
        "inLanguage": ["en-US", "es-MX"],
        "publisher": {
            "@type": "Organization",
            "@id": f"{site_url}#organization",
        },
        "potentialAction": {
            "@type": "SearchAction",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": f"{site_url}search/?query={{search_term_string}}",
            },
            "query-input": "required name=search_term_string",
        },
    }

    return _jsonld_script(data)


@register.simple_tag(takes_context=True)
def jsonld_service(context: dict[str, Any]) -> str:
    """Output JSON-LD Service structured data for a service page."""
    biz = context.get("biz")
    page = context.get("page") or context.get("self")
    if not biz or not page:
        return ""

    site_url = _build_absolute_uri(context, "/")
    title = getattr(page, "title", "")

    request = context.get("request")
    page_url = ""
    if request and hasattr(page, "get_url"):
        page_url = request.build_absolute_uri(page.get_url())

    data: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": title,
        "description": getattr(page, "intro", ""),
        "provider": {
            "@type": "LocalBusiness",
            "@id": f"{site_url}#business",
            "name": biz.business_name,
        },
        "areaServed": {
            "@type": "State",
            "name": biz.state or "California",
        },
        "serviceType": "Appliance Repair",
        "category": f"Appliance Repair > {title}",
        "offers": {
            "@type": "Offer",
            "price": str(biz.service_call_fee),
            "priceCurrency": "USD",
            "description": f"Diagnostic service call for {title.lower()} — waived with repair",
            "availability": "https://schema.org/InStock",
        },
        "termsOfService": f"Warranty included on all {title.lower()}",
        "serviceOutput": f"Fully repaired and functioning {title.lower().replace(' repair', '')}",
    }

    if page_url:
        data["url"] = page_url
        data["mainEntityOfPage"] = {"@type": "WebPage", "@id": page_url}

    # Booking channel (enables Google action buttons)
    booking_url = getattr(biz, "booking_url", "")
    if booking_url:
        data["availableChannel"] = {
            "@type": "ServiceChannel",
            "serviceUrl": booking_url,
            "servicePhone": biz.phone,
            "serviceSmsNumber": biz.phone,
        }

    # Aggregate rating at service level (inherits from business)
    if biz.google_review_count and biz.google_review_count > 0:
        data["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": str(biz.google_rating),
            "bestRating": "5",
            "reviewCount": str(biz.google_review_count),
        }

    return _jsonld_script(data)


@register.simple_tag(takes_context=True)
def jsonld_service_area(context: dict[str, Any]) -> str:
    """Output JSON-LD Service + areaServed for city/location pages."""
    biz = context.get("biz")
    page = context.get("page") or context.get("self")
    if not biz or not page:
        return ""

    city_name = getattr(page, "title", "")
    state = getattr(page, "state", biz.state or "CA")
    site_url = _build_absolute_uri(context, "/")
    zip_codes_str = getattr(page, "zip_codes", "")

    data: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": f"Appliance Repair in {city_name}, {state}",
        "description": getattr(page, "intro", ""),
        "provider": {
            "@type": "LocalBusiness",
            "@id": f"{site_url}#business",
            "name": biz.business_name,
        },
        "areaServed": {
            "@type": "City",
            "name": city_name,
            "containedInPlace": {
                "@type": "State",
                "name": state,
            },
        },
        "serviceType": "Appliance Repair",
        "offers": {
            "@type": "Offer",
            "price": str(biz.service_call_fee),
            "priceCurrency": "USD",
            "description": (
                f"Same-day appliance repair service call in {city_name}, {state}"
                " — diagnostic fee waived with repair"
            ),
            "availability": "https://schema.org/InStock",
        },
    }

    # Add aggregate rating
    if biz.google_review_count and biz.google_review_count > 0:
        data["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": str(biz.google_rating),
            "bestRating": "5",
            "reviewCount": str(biz.google_review_count),
        }

    # Add postal codes as additional area served detail
    if zip_codes_str:
        zips = [z.strip() for z in zip_codes_str.split(",") if z.strip()]
        if zips:
            data["areaServed"] = [
                data["areaServed"],
                *[
                    {
                        "@type": "PostalAddress",
                        "postalCode": z,
                        "addressRegion": state,
                        "addressCountry": "US",
                    }
                    for z in zips[:10]  # Limit to 10 for schema size
                ],
            ]

    request = context.get("request")
    if request and hasattr(page, "get_url"):
        data["url"] = request.build_absolute_uri(page.get_url())

    return _jsonld_script(data)


@register.simple_tag(takes_context=True)
def jsonld_faq(context: dict[str, Any]) -> str:
    """Output JSON-LD FAQPage structured data from a page's FAQ StreamField.

    Works with any page that has a ``faq`` StreamField containing
    ``faq_item`` blocks with ``question`` and ``answer`` fields.
    Also accepts a pre-built list of dicts via the ``faq_items`` context key
    (used by the home page where FAQ is hardcoded in template).
    """
    page = context.get("page") or context.get("self")

    qa_entries: list[dict[str, str]] = []

    # Try StreamField first (ServicePage)
    if page and hasattr(page, "faq"):
        for block in page.faq:
            qa_entries.append(
                {
                    "question": str(block.value.get("question", "")),
                    "answer": str(block.value.get("answer", "")),
                }
            )

    # Fallback to context-provided items (home page)
    if not qa_entries:
        items = context.get("faq_items", [])
        for item in items:
            qa_entries.append(
                {
                    "question": str(item.get("question", "")),
                    "answer": str(item.get("answer", "")),
                }
            )

    if not qa_entries:
        return ""

    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": entry["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": entry["answer"],
                },
            }
            for entry in qa_entries
        ],
    }

    return _jsonld_script(data)


@register.simple_tag(takes_context=True)
def jsonld_howto(context: dict[str, Any]) -> str:
    """Output JSON-LD HowTo schema for the booking process (Home page)."""
    biz = context.get("biz")
    site_url = _build_absolute_uri(context, "/")
    if not site_url:
        return ""

    business_name = biz.business_name if biz else "LOWL Appliance Repair"

    data: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": _("How to Book Appliance Repair with %(name)s")
        % {"name": business_name},
        "description": _(
            "Book same-day appliance repair in 3 easy steps: "
            "schedule online, get a diagnosis, and get it fixed on the spot."
        ),
        "totalTime": "PT5M",
        "step": [
            {
                "@type": "HowToStep",
                "position": 1,
                "name": _("Book Online"),
                "text": _("Select your appliance and preferred time slot."),
                "url": site_url,
            },
            {
                "@type": "HowToStep",
                "position": 2,
                "name": _("Diagnosis"),
                "text": _(
                    "A certified technician arrives, inspects the appliance, "
                    "and provides a transparent quote."
                ),
            },
            {
                "@type": "HowToStep",
                "position": 3,
                "name": _("Repair"),
                "text": _(
                    "We fix it on the spot with fully stocked parts. "
                    "Warranty included on all repairs."
                ),
            },
        ],
    }

    return _jsonld_script(data)


@register.simple_tag(takes_context=True)
def jsonld_article(context: dict[str, Any]) -> str:
    """Output JSON-LD Article structured data for a blog post."""
    biz = context.get("biz")
    page = context.get("page") or context.get("self")
    if not page:
        return ""

    request = context.get("request")
    page_url = ""
    if request and hasattr(request, "build_absolute_uri") and hasattr(page, "get_url"):
        page_url = request.build_absolute_uri(page.get_url())

    site_url = _build_absolute_uri(context, "/")

    data: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": getattr(page, "title", ""),
        "description": getattr(page, "intro", getattr(page, "search_description", "")),
        "url": page_url,
        "mainEntityOfPage": {"@type": "WebPage", "@id": page_url},
    }

    # Language signal for i18n sites
    locale = getattr(page, "locale", None)
    data["inLanguage"] = "es-MX" if locale and str(locale) != "en" else "en-US"

    # Date
    date = getattr(page, "date", None)
    if date:
        data["datePublished"] = date.isoformat()
    # Use last_published_at for dateModified (Wagtail tracks this automatically)
    last_published = getattr(page, "last_published_at", None)
    if last_published:
        data["dateModified"] = last_published.isoformat()
    elif date:
        data["dateModified"] = date.isoformat()

    # Image
    featured_image = getattr(page, "featured_image", None)
    if featured_image and request:
        try:
            rendition = featured_image.get_rendition("fill-1200x630")
            data["image"] = {
                "@type": "ImageObject",
                "url": request.build_absolute_uri(rendition.url),
                "width": 1200,
                "height": 630,
            }
        except (AttributeError, FileNotFoundError, ValueError) as exc:
            logger.warning("Failed to generate article image rendition: %s", exc)

    # Publisher (the business)
    if biz:
        data["publisher"] = {
            "@type": "Organization",
            "@id": f"{site_url}#organization",
            "name": biz.business_name,
            "url": site_url,
            "logo": {
                "@type": "ImageObject",
                "url": _build_absolute_uri(context, "/static/images/icon.svg"),
            },
        }
        # Prefer individual author (E-E-A-T), fall back to Organization
        author_name = getattr(page, "author_name", "")
        if author_name:
            data["author"] = {"@type": "Person", "name": author_name}
        else:
            data["author"] = {
                "@type": "Organization",
                "@id": f"{site_url}#organization",
                "name": biz.business_name,
            }

    return _jsonld_script(data)


@register.simple_tag(takes_context=True)
def jsonld_breadcrumbs(context: dict[str, Any]) -> str:
    """Output JSON-LD BreadcrumbList matching the visual breadcrumbs."""

    page = context.get("page") or context.get("self")
    if not page:
        return ""

    request = context.get("request")
    if not request or not hasattr(request, "build_absolute_uri"):
        return ""

    ancestors = list(page.get_ancestors(inclusive=False).filter(depth__gt=2))

    items: list[dict[str, Any]] = []

    # Home (localized for multilingual breadcrumb accuracy)
    items.append(
        {
            "@type": "ListItem",
            "position": 1,
            "name": _("Home"),
            "item": request.build_absolute_uri("/"),
        }
    )

    # Ancestors
    for i, ancestor in enumerate(ancestors, start=2):
        items.append(
            {
                "@type": "ListItem",
                "position": i,
                "name": ancestor.title,
                "item": request.build_absolute_uri(ancestor.url),
            }
        )

    # Current page
    items.append(
        {
            "@type": "ListItem",
            "position": len(items) + 1,
            "name": page.title,
            "item": request.build_absolute_uri(page.get_url()),
        }
    )

    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }

    return _jsonld_script(data)


@register.simple_tag(takes_context=True)
def jsonld_reviews(context: dict[str, Any]) -> str:
    """Output JSON-LD Review snippets from context-provided review items.

    Uses the ``review_items`` context key (list of dicts with
    ``author``, ``rating``, ``text``). Links reviews to the business
    entity via ``itemReviewed``.
    """
    biz = context.get("biz")
    items = context.get("review_items", [])
    if not items or not biz:
        return ""

    site_url = _build_absolute_uri(context, "/")

    reviews: list[dict[str, Any]] = []
    for item in items:
        reviews.append(
            {
                "@type": "Review",
                "author": {
                    "@type": "Person",
                    "name": item.get("author", ""),
                },
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": str(item.get("rating", 5)),
                    "bestRating": "5",
                },
                "reviewBody": item.get("text", ""),
                "itemReviewed": {
                    "@type": "LocalBusiness",
                    "@id": f"{site_url}#business",
                    "name": biz.business_name,
                },
            }
        )

    # Output as a single graph containing all reviews
    data: dict[str, Any] = {
        "@context": "https://schema.org",
        "@graph": reviews,
    }

    return _jsonld_script(data)


@register.simple_tag(takes_context=True)
def jsonld_itemlist(context: dict[str, Any]) -> str:
    """Output JSON-LD ItemList for index pages (services, locations).

    Generates a numbered list of child items which can appear as
    rich snippets in Google (carousel-style results).
    Looks for ``services`` or ``cities`` in the template context.
    """
    request = context.get("request")
    if not request or not hasattr(request, "build_absolute_uri"):
        return ""

    page = context.get("page") or context.get("self")
    page_url = ""
    if page and hasattr(page, "get_url"):
        page_url = request.build_absolute_uri(page.get_url())

    # Detect which list to render
    items_qs = context.get("services") or context.get("cities") or context.get("posts")
    if not items_qs:
        return ""

    list_items: list[dict[str, Any]] = []
    for i, item in enumerate(items_qs, start=1):
        item_data: dict[str, Any] = {
            "@type": "ListItem",
            "position": i,
            "name": getattr(item, "title", ""),
        }
        if hasattr(item, "get_url"):
            item_data["url"] = request.build_absolute_uri(item.get_url())
        list_items.append(item_data)

    if not list_items:
        return ""

    data: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": getattr(page, "title", ""),
        "numberOfItems": len(list_items),
        "itemListElement": list_items,
    }

    if page_url:
        data["url"] = page_url

    return _jsonld_script(data)


@register.simple_tag(takes_context=True)
def jsonld_webpage(context: dict[str, Any]) -> str:
    """Output JSON-LD WebPage schema for static pages (About, Contact, etc.).

    Provides Google with explicit page type signals, linking back to the
    parent WebSite and Organization entities for better entity resolution.
    """
    biz = context.get("biz")
    page = context.get("page") or context.get("self")
    if not page:
        return ""

    request = context.get("request")
    if not request or not hasattr(request, "build_absolute_uri"):
        return ""

    site_url = _build_absolute_uri(context, "/")
    page_url = (
        request.build_absolute_uri(page.get_url()) if hasattr(page, "get_url") else ""
    )
    slug = getattr(page, "slug", "")

    # Use ContactPage type for contact pages
    page_type = "ContactPage" if slug == "contact" else "WebPage"
    if slug == "about-us":
        page_type = "AboutPage"

    data: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": page_type,
        "name": getattr(page, "seo_title", "") or page.title,
        "url": page_url,
        "isPartOf": {"@type": "WebSite", "@id": f"{site_url}#website"},
        "about": {"@type": "Organization", "@id": f"{site_url}#organization"},
        "inLanguage": "es-MX"
        if getattr(page, "locale", None) and str(page.locale) != "en"
        else "en-US",
    }

    description = getattr(page, "search_description", "") or getattr(
        page, "hero_subtitle", ""
    )
    if description:
        data["description"] = description

    last_published = getattr(page, "last_published_at", None)
    if last_published:
        data["dateModified"] = last_published.isoformat()

    return _jsonld_script(data)


@register.filter
def split_comma(value: str) -> list[str]:
    """Split a string by comma and strip whitespace from each part."""
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


@register.inclusion_tag("home/tags/breadcrumbs.html", takes_context=True)
def site_breadcrumbs(context: dict[str, Any]) -> dict[str, Any]:
    """Render dynamic breadcrumbs from the Wagtail page tree."""
    page = context.get("page") or context.get("self")
    ancestors = []
    if page:
        ancestors = list(page.get_ancestors(inclusive=False).filter(depth__gt=2))
    return {"ancestors": ancestors, "current_page": page}


@register.simple_tag
def picture(
    image: Any,
    spec: str,
    alt: str = "",
    css_class: str = "",
    loading: str = "lazy",
    fetchpriority: str = "",
    decoding: str = "async",
) -> str:
    """Render <picture> with WebP <source> and fallback <img>.

    Outputs width/height attributes to prevent CLS, and uses
    WebP format for ~30% smaller file sizes on supported browsers.

    Usage::

        {% picture image "fill-400x225" css_class="w-full" loading="lazy" %}
    """
    from django.utils.html import escape as _esc

    if not image:
        return ""

    try:
        fallback = image.get_rendition(spec)
    except (AttributeError, FileNotFoundError, ValueError) as exc:
        logger.warning("Failed to render image %s with spec '%s': %s", image, spec, exc)
        return ""

    # Try WebP; fall back to plain <img> if Pillow lacks WebP support
    webp_source = ""
    try:
        webp = image.get_rendition(f"{spec}|format-webp")
        webp_source = f'<source srcset="{webp.url}" type="image/webp" />'
    except (AttributeError, FileNotFoundError, ValueError):
        pass  # WebP not available — fallback to original format

    alt_text = _esc(alt or getattr(image, "title", "") or "")

    attrs = [
        f'src="{fallback.url}"',
        f'alt="{alt_text}"',
        f'width="{fallback.width}"',
        f'height="{fallback.height}"',
    ]
    if css_class:
        attrs.append(f'class="{_esc(css_class)}"')
    if loading:
        attrs.append(f'loading="{_esc(loading)}"')
    if fetchpriority:
        attrs.append(f'fetchpriority="{_esc(fetchpriority)}"')
    if decoding:
        attrs.append(f'decoding="{_esc(decoding)}"')

    img_tag = f"<img {' '.join(attrs)} />"

    if webp_source:
        return mark_safe(f"<picture>{webp_source}{img_tag}</picture>")
    return mark_safe(img_tag)
