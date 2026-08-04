"""Tests for service pages and related functionality."""

from __future__ import annotations

from django.test import TestCase

from home.tests import create_test_home
from services.models import ServicePage, ServiceRelatedService, ServicesIndexPage


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


def panel_relation_names(panels: list[object]) -> set[str]:
    """Return InlinePanel relation names from a nested Wagtail panel definition."""
    names: set[str] = set()
    for panel in panels:
        relation_name = getattr(panel, "relation_name", None)
        if relation_name:
            names.add(relation_name)
        children = getattr(panel, "children", None)
        if children:
            names.update(panel_relation_names(list(children)))
    return names


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

    def test_phase02_service_index_model_and_admin_foundation_is_owned_here(self) -> None:
        names = panel_field_names(ServicesIndexPage.content_panels)

        self.assertIn("hero_title", names)
        self.assertIn("hero_subtitle", names)
        self.assertIn("intro", names)
        self.assertEqual(ServicesIndexPage.subpage_types, ["services.ServicePage"])
        self.assertEqual(ServicesIndexPage.parent_page_types, ["home.HomePage"])

    def test_service_page_renders_200(self) -> None:
        response = self.client.get(self.service.url)
        self.assertEqual(response.status_code, 200)

    def test_service_page_contains_title(self) -> None:
        response = self.client.get(self.service.url)
        self.assertContains(response, "Refrigerator Repair")

    def test_phase02_service_public_h1_and_carousel_fields_exist(self) -> None:
        public_h1 = ServicePage._meta.get_field("public_h1")
        carousel_title = ServicePage._meta.get_field("photo_carousel_title")

        self.assertTrue(public_h1.blank)
        self.assertTrue(carousel_title.blank)
        self.assertEqual(public_h1.max_length, 255)
        self.assertEqual(carousel_title.max_length, 255)

    def test_phase02_service_public_h1_and_carousel_are_editable(self) -> None:
        names = panel_field_names(ServicePage.content_panels)

        self.assertIn("public_h1", names)
        self.assertIn("photo_carousel_title", names)
        self.assertIn("photo_carousel_images", panel_relation_names(ServicePage.content_panels))

    def test_phase02_service_photo_carousel_orderable_contract(self) -> None:
        from services.models import ServicePhotoCarouselImage

        page_field = ServicePhotoCarouselImage._meta.get_field("page")
        image_field = ServicePhotoCarouselImage._meta.get_field("image")

        self.assertEqual(page_field.remote_field.model, ServicePage)
        self.assertEqual(page_field.remote_field.related_name, "photo_carousel_images")
        self.assertEqual(image_field.remote_field.model._meta.label, "wagtailimages.Image")
        self.assertEqual(ServicePhotoCarouselImage._meta.ordering, ["sort_order"])

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
