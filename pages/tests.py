"""Phase 03 tests for contact tracking and the VAPI ZIP contract."""

from __future__ import annotations

import json
import uuid
from unittest.mock import patch

from django.core import mail
from django.core.cache import cache
from django.test import TestCase, override_settings

from home.tests import create_test_home
from locations.models import CityPage, LocationsIndexPage
from tracking.models import TrackEvent, TrackSession


@override_settings(
    VAPI_ENABLED=True,
    VAPI_SERVER_SECRET="phase03-vapi-secret",
    VAPI_ALLOW_UNSIGNED=False,
    VAPI_RATE="30/m",
)
class VapiZipEndpointTests(TestCase):
    URL = "/api/vapi/check-zip/"

    def setUp(self) -> None:
        cache.clear()
        home, _site = create_test_home()
        locations_index = LocationsIndexPage(
            title="Service Areas",
            slug="service-areas",
            intro="Target service areas",
        )
        home.add_child(instance=locations_index)
        locations_index.save_revision().publish()
        city = CityPage(
            title="Corona",
            slug="corona",
            intro="Corona service area",
            zip_codes="92879, 92880",
        )
        locations_index.add_child(instance=city)
        city.save_revision().publish()

    def _payload(self, zip_code: str = "92879") -> dict[str, object]:
        return {
            "message": {
                "toolCallList": [
                    {
                        "id": "call-123",
                        "function": {
                            "name": "check_zip_code",
                            "arguments": {"zip_code": zip_code},
                        },
                    }
                ]
            }
        }

    def _post(self, payload: object, **extra: str):
        headers = {
            "HTTP_X_VAPI_SECRET": "phase03-vapi-secret",
            "REMOTE_ADDR": "198.51.100.20",
        }
        headers.update(extra)
        return self.client.post(
            self.URL,
            data=json.dumps(payload),
            content_type="application/json",
            **headers,
        )

    def test_known_zip_uses_live_city_data_without_unsupported_claims(self) -> None:
        response = self._post(self._payload())

        self.assertEqual(response.status_code, 200)
        result = response.json()["results"][0]
        self.assertEqual(result["toolCallId"], "call-123")
        self.assertIn("Corona", result["result"])
        for forbidden in ("LOWL", "same-day", "$70", "no overtime", "certified"):
            self.assertNotIn(forbidden.lower(), result["result"].lower())

    def test_vapi_validates_auth_content_type_size_and_shape(self) -> None:
        wrong_secret = self._post(
            self._payload(),
            HTTP_X_VAPI_SECRET="wrong-secret",
        )
        wrong_type = self.client.post(
            self.URL,
            data="{}",
            content_type="text/plain",
            HTTP_X_VAPI_SECRET="phase03-vapi-secret",
        )
        oversized = self.client.post(
            self.URL,
            data=b"x" * 32_769,
            content_type="application/json",
            HTTP_X_VAPI_SECRET="phase03-vapi-secret",
        )
        wrong_shape = self._post(["not", "an", "object"])

        self.assertEqual(wrong_secret.status_code, 401)
        self.assertEqual(wrong_type.status_code, 415)
        self.assertEqual(oversized.status_code, 413)
        self.assertEqual(wrong_shape.status_code, 400)

    def test_vapi_missing_secret_fails_closed_unless_unsigned_mode_is_explicit(self) -> None:
        with override_settings(VAPI_SERVER_SECRET=""):
            closed = self._post(self._payload(), HTTP_X_VAPI_SECRET="")
        with override_settings(VAPI_SERVER_SECRET="", VAPI_ALLOW_UNSIGNED=True):
            explicit_unsigned = self._post(self._payload(), HTTP_X_VAPI_SECRET="")

        self.assertEqual(closed.status_code, 503)
        self.assertEqual(explicit_unsigned.status_code, 200)

    @override_settings(VAPI_ENABLED=False)
    def test_vapi_is_disabled_by_default_contract(self) -> None:
        response = self._post(self._payload())
        self.assertEqual(response.status_code, 404)

    @override_settings(VAPI_RATE="2/m")
    def test_vapi_rate_limit_fails_closed(self) -> None:
        responses = [self._post(self._payload()) for _ in range(3)]
        self.assertEqual([response.status_code for response in responses], [200, 200, 403])

    def test_get_is_not_allowed(self) -> None:
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 405)


@override_settings(
    TRACKING_ENABLED=True,
    CONTACT_EMAIL="business@example.com",
    DEFAULT_FROM_EMAIL="noreply@example.com",
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
class ContactTrackingTests(TestCase):
    URL = "/contact/submit/"

    def setUp(self) -> None:
        create_test_home()
        self.session = TrackSession.objects.create(
            session_id=uuid.uuid4(),
            landing_url="http://testserver/contact/",
        )

    def _post(self):
        return self.client.post(
            self.URL,
            {
                "name": "Target Customer",
                "email": "customer@example.com",
                "phone": "555-555-0100",
                "message": "Please contact me about my refrigerator.",
                "utm_source": "google\nInjected: value",
                "tracking_session_id": str(self.session.session_id),
            },
        )

    def test_successful_contact_email_records_allowlisted_server_event(self) -> None:
        response = self._post()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        try:
            event = TrackEvent.objects.get(event_name="contact_email_sent")
        except TrackEvent.DoesNotExist as exc:  # pragma: no cover - RED guard
            self.fail(f"contact tracking event is missing: {exc}")
        self.assertEqual(event.properties, {"utm_source": "googleInjected: value"})

    @override_settings(TRACKING_ENABLED=False)
    def test_disabled_tracking_does_not_change_contact_delivery(self) -> None:
        response = self._post()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(TrackEvent.objects.count(), 0)

    def test_email_failure_does_not_create_a_false_conversion_event(self) -> None:
        with patch("pages.views.send_mail", side_effect=RuntimeError("mail offline")):
            response = self._post()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(TrackEvent.objects.count(), 0)
