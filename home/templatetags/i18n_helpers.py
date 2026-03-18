"""Template tags for language switching with proper fallbacks."""

from __future__ import annotations

from django import template
from wagtail.models import Locale

register = template.Library()


@register.simple_tag
def translation_url(page: object | None, language_code: str, fallback: str) -> str:
    """Return the URL for a page's translation, or fallback if none exists.

    Usage: {% translation_url page 'es' '/es/' %}
    """
    if page is None:
        return fallback
    try:
        locale = Locale.objects.get(language_code=language_code)
        translation = page.get_translation_or_none(locale)
        if translation is not None and translation.live:
            return translation.get_url()
    except (Locale.DoesNotExist, AttributeError):
        pass
    return fallback
