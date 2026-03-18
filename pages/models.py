"""Pages app models: StaticPage for About, Contact, etc."""

from __future__ import annotations

from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class StaticPage(Page):
    """Flexible static page for About Us, Contact, etc.

    CTA booking URL comes from SiteSettings (not hardcoded).
    """

    hero_title = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional hero title. If empty, page title is used.",
    )
    hero_subtitle = models.TextField(
        blank=True,
        help_text="Short subtitle or tagline for the hero section.",
    )
    body = RichTextField(blank=True)

    # CTA section (booking URL comes from SiteSettings)
    cta_title = models.CharField(
        max_length=255, blank=True, default="Ready to Get Started?"
    )
    cta_text = models.TextField(
        blank=True, default="Book your appliance repair service today."
    )
    cta_button_text = models.CharField(max_length=50, blank=True, default="Book Now")

    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
        FieldPanel("body"),
        MultiFieldPanel(
            [
                FieldPanel("cta_title"),
                FieldPanel("cta_text"),
                FieldPanel("cta_button_text"),
            ],
            heading="Call to Action",
        ),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types: list[str] = []
