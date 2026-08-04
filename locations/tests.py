"""Tests for location pages and city page functionality."""

from __future__ import annotations

from django.test import TestCase

from home.tests import create_test_home
from locations.models import CityPage, LocationsIndexPage


def panel_field_names(panels: list[object]) -> set[str]:
    """Return field names from a nested Wagtail panel definition."""
    names: set[str] = set()
    for panel in panels:
        field_name = getattr(panel, "field_name", None)
        if field_name:
            names.add(field_name)
        children = getattr(panel, "children", None)
        if children:
            names.update(panel_field_names(list(children)))
    return names


class LocationsPageTest(TestCase):
    """Test location pages rendering and relationships."""

    def setUp(self) -> None:
        self.home, self.site = create_test_home()

        self.locations_index = LocationsIndexPage(
            title="Service Areas", slug="service-areas"
        )
        self.home.add_child(instance=self.locations_index)
        self.locations_index.save_revision().publish()

        self.city = CityPage(
            title="Corona",
            slug="appliance-repair-corona-ca",
            intro="Same-day repair in Corona.",
            state="CA",
            zip_codes="92879, 92880, 92881",
        )
        self.locations_index.add_child(instance=self.city)
        self.city.save_revision().publish()

    def test_locations_index_renders_200(self) -> None:
        response = self.client.get(self.locations_index.url)
        self.assertEqual(response.status_code, 200)

    def test_locations_index_lists_cities(self) -> None:
        response = self.client.get(self.locations_index.url)
        self.assertIn("cities", response.context)

    def test_city_page_renders_200(self) -> None:
        response = self.client.get(self.city.url)
        self.assertEqual(response.status_code, 200)

    def test_city_page_contains_state(self) -> None:
        response = self.client.get(self.city.url)
        self.assertContains(response, "CA")

    def test_city_page_contains_zip_codes(self) -> None:
        response = self.client.get(self.city.url)
        self.assertContains(response, "92879")

    def test_phase02_city_public_h1_field_exists(self) -> None:
        field = CityPage._meta.get_field("public_h1")

        self.assertTrue(field.blank)
        self.assertEqual(field.max_length, 255)

    def test_phase02_city_public_h1_is_editable(self) -> None:
        self.assertIn("public_h1", panel_field_names(CityPage.content_panels))
