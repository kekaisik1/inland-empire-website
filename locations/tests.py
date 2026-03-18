"""Tests for location pages and city page functionality."""

from __future__ import annotations

from django.test import TestCase

from home.tests import create_test_home
from locations.models import CityPage, LocationsIndexPage


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
