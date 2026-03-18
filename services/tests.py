"""Tests for service pages and related functionality."""

from __future__ import annotations

from django.test import TestCase

from home.tests import create_test_home
from services.models import ServicePage, ServiceRelatedService, ServicesIndexPage


class ServicesPageTest(TestCase):
    """Test service page creation, rendering, and relationships."""

    def setUp(self) -> None:
        self.home, self.site = create_test_home()

        self.services_index = ServicesIndexPage(
            title="Services",
            slug="services",
            hero_title="Our Services",
        )
        self.home.add_child(instance=self.services_index)
        self.services_index.save_revision().publish()

        self.service = ServicePage(
            title="Refrigerator Repair",
            slug="refrigerator-repair",
            intro="Fix your fridge fast.",
            short_description="Cooling issues and leaks.",
        )
        self.services_index.add_child(instance=self.service)
        self.service.save_revision().publish()

    def test_services_index_renders_200(self) -> None:
        response = self.client.get(self.services_index.url)
        self.assertEqual(response.status_code, 200)

    def test_services_index_lists_services(self) -> None:
        response = self.client.get(self.services_index.url)
        self.assertIn("services", response.context)
        titles = [s.title for s in response.context["services"]]
        self.assertIn("Refrigerator Repair", titles)

    def test_service_page_renders_200(self) -> None:
        response = self.client.get(self.service.url)
        self.assertEqual(response.status_code, 200)

    def test_service_page_contains_title(self) -> None:
        response = self.client.get(self.service.url)
        self.assertContains(response, "Refrigerator Repair")

    def test_related_services(self) -> None:
        svc2 = ServicePage(
            title="Freezer Repair",
            slug="freezer-repair",
            intro="Fix your freezer.",
        )
        self.services_index.add_child(instance=svc2)
        svc2.save_revision().publish()

        ServiceRelatedService.objects.create(page=self.service, related_service=svc2)

        response = self.client.get(self.service.url)
        self.assertIn("related_services_optimized", response.context)
        self.assertEqual(len(response.context["related_services_optimized"]), 1)
