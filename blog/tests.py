"""Tests for blog CMS model behavior."""

from __future__ import annotations

from datetime import date

from django.test import TestCase
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

from blog.models import BlogPage


class BlogPagePhase02MetadataTest(TestCase):
    """Portable LOWL blog model helpers needed by later templates."""

    def test_phase02_blog_reading_time_uses_streamfield_words_minimum_one(self) -> None:
        page = BlogPage(
            title="Repair Guide",
            slug="repair-guide",
            date=date(2026, 7, 31),
            intro="Short intro",
            body=[
                ("heading", "Washer repair checklist"),
                ("paragraph", "<p>" + "word " * 240 + "</p>"),
                ("quote", "quoted advice " * 10),
            ],
        )

        self.assertEqual(page.reading_time, 2)

    def test_phase02_blog_headings_extracts_heading_blocks_in_order(self) -> None:
        page = BlogPage(
            title="Repair Guide",
            slug="repair-guide",
            date=date(2026, 7, 31),
            intro="Short intro",
            body=[
                ("paragraph", "<p>Intro</p>"),
                ("heading", "First heading"),
                ("quote", "Quoted text"),
                ("heading", "Second heading"),
            ],
        )

        self.assertEqual(page.headings, ["First heading", "Second heading"])

    def test_phase02_blog_tags_and_author_are_editor_editable(self) -> None:
        field_names: set[str] = set()
        has_post_information_group = False

        for panel in BlogPage.content_panels:
            field_name = getattr(panel, "field_name", None)
            if field_name:
                field_names.add(field_name)
            if isinstance(panel, MultiFieldPanel):
                if panel.heading == "Post Information":
                    has_post_information_group = True
                for child in panel.children:
                    child_field_name = getattr(child, "field_name", None)
                    if child_field_name:
                        field_names.add(child_field_name)

        self.assertTrue(has_post_information_group)
        self.assertIn("author_name", field_names)
        self.assertIn("tags", field_names)
        self.assertTrue(any(
            isinstance(panel, FieldPanel) and panel.field_name == "tags"
            for panel in BlogPage.content_panels
        ))
