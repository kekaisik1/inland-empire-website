"""Phase 03 tests for privacy-aware tracking models and APIs."""

from __future__ import annotations

import importlib
import hashlib
import hmac
import json
import uuid
from datetime import timedelta
from io import StringIO
from unittest.mock import patch

from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.cache import cache
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import DatabaseError
from django.db import models
from django.test import RequestFactory, TestCase, override_settings
from django.utils import timezone

from tracking.models import TrackEvent, TrackSession


class TrackingModelContractTests(TestCase):
    """The target owns a privacy-safe, target-neutral tracking schema."""

    def test_tracking_models_use_uuid_sessions_and_never_store_raw_client_ip(self) -> None:
        self.assertTrue(apps.is_installed("tracking"))
        try:
            tracking_models = importlib.import_module("tracking.models")
        except Exception as exc:  # pragma: no cover - RED guard before app exists
            self.fail(f"tracking models are unavailable: {exc}")

        TrackSession = tracking_models.TrackSession
        TrackEvent = tracking_models.TrackEvent

        self.assertIsInstance(TrackSession._meta.get_field("session_id"), models.UUIDField)
        self.assertTrue(TrackSession._meta.get_field("session_id").unique)
        self.assertEqual(TrackSession._meta.get_field("ip_hash").max_length, 64)
        field_names = {field.name for field in TrackSession._meta.get_fields()}
        self.assertFalse({"ip", "ip_address", "remote_addr"} & field_names)

        session = TrackSession.objects.create(
            session_id=uuid.uuid4(),
            landing_url="https://inland.example/",
            ip_hash="a" * 64,
        )
        event = TrackEvent.objects.create(
            session=session,
            event_name="page_view",
            url="https://inland.example/",
            properties={"title": "Home"},
        )
        self.assertEqual(event.session, session)
        self.assertFalse(session.is_converted)
        self.assertNotIn("lowl", str(session).lower())


@override_settings(
    TRACKING_ENABLED=True,
    TRACKING_REQUIRE_CONSENT=True,
    TRACKING_REQUIRE_ORIGIN=True,
    TRACKING_ALLOWED_ORIGINS=(),
    TRACKING_COLLECT_RATE="30/m",
)
class TrackingCollectionTests(TestCase):
    URL = "/api/track/collect/"

    def _payload(self, **overrides: object) -> dict[str, object]:
        payload: dict[str, object] = {
            "session_id": str(uuid.uuid4()),
            "consent": True,
            "session_meta": {
                "landing_url": "http://testserver/?utm_source=private-query",
                "referrer": "https://search.example/results?q=private",
                "utm_source": "google",
                "screen_width": 390,
                "language": "en-US",
            },
            "events": [
                {
                    "name": "page_view",
                    "url": "http://testserver/?private=value",
                    "properties": {
                        "title": "Home",
                        "unknown_sensitive_field": "must not persist",
                    },
                    "ts": int(timezone.now().timestamp() * 1000),
                }
            ],
        }
        payload.update(overrides)
        return payload

    def _post(self, payload: object, **extra: str):
        headers = {"HTTP_ORIGIN": "http://testserver", "REMOTE_ADDR": "203.0.113.41"}
        headers.update(extra)
        return self.client.post(
            self.URL,
            data=json.dumps(payload),
            content_type="application/json",
            **headers,
        )

    def test_valid_collection_strips_url_queries_and_unknown_properties(self) -> None:
        response = self._post(self._payload())

        self.assertEqual(response.status_code, 202)
        self.assertFalse(response.cookies)
        session = TrackSession.objects.get()
        event = TrackEvent.objects.get()
        self.assertEqual(session.landing_url, "http://testserver/")
        self.assertEqual(session.referrer, "https://search.example/results")
        self.assertEqual(event.url, "http://testserver/")
        self.assertEqual(event.properties, {"title": "Home"})

    def test_collection_requires_json_content_type_and_object_shape(self) -> None:
        wrong_type = self.client.post(
            self.URL,
            data="{}",
            content_type="text/plain",
            HTTP_ORIGIN="http://testserver",
        )
        wrong_shape = self._post(["not", "an", "object"])

        self.assertEqual(wrong_type.status_code, 415)
        self.assertEqual(wrong_shape.status_code, 400)
        self.assertEqual(TrackSession.objects.count(), 0)

    def test_collection_rejects_cross_origin_and_oversized_payloads(self) -> None:
        cross_origin = self._post(
            self._payload(),
            HTTP_ORIGIN="https://attacker.example",
        )
        oversized = self.client.post(
            self.URL,
            data=b"{" + (b"x" * 65_536) + b"}",
            content_type="application/json",
            HTTP_ORIGIN="http://testserver",
        )

        self.assertEqual(cross_origin.status_code, 403)
        self.assertEqual(oversized.status_code, 413)
        self.assertEqual(TrackSession.objects.count(), 0)

    def test_database_failure_is_a_safe_noop(self) -> None:
        with patch.object(
            TrackSession.objects,
            "get_or_create",
            side_effect=DatabaseError("database unavailable"),
        ):
            response = self._post(self._payload())

        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.content, b"")


@override_settings(
    TRACKING_ENABLED=True,
    TRACKING_REQUIRE_CONSENT=True,
    TRACKING_REQUIRE_ORIGIN=True,
    TRACKING_ALLOWED_ORIGINS=(),
    TRACKING_COLLECT_RATE="30/m",
)
class TrackingPrivacyControlTests(TrackingCollectionTests):
    def setUp(self) -> None:
        cache.clear()

    def test_dnt_gpc_and_missing_consent_do_not_persist(self) -> None:
        dnt = self._post(self._payload(), HTTP_DNT="1")
        gpc = self._post(self._payload(), HTTP_SEC_GPC="1")
        no_consent = self._post(self._payload(consent=False))

        self.assertEqual([dnt.status_code, gpc.status_code, no_consent.status_code], [204, 204, 204])
        self.assertEqual(TrackSession.objects.count(), 0)

    @override_settings(TRACKING_ENABLED=False)
    def test_disabled_tracking_is_cookie_free_noop(self) -> None:
        response = self._post(self._payload())

        self.assertEqual(response.status_code, 204)
        self.assertFalse(response.cookies)
        self.assertEqual(TrackSession.objects.count(), 0)

    def test_client_ip_is_subnet_reduced_and_keyed_before_storage(self) -> None:
        from tracking.views import _privacy_ip_hash

        first = _privacy_ip_hash("203.0.113.41")
        same_subnet = _privacy_ip_hash("203.0.113.99")
        other_subnet = _privacy_ip_hash("203.0.114.41")

        self.assertEqual(len(first), 64)
        self.assertNotIn("203.0.113", first)
        self.assertEqual(first, same_subnet)
        self.assertNotEqual(first, other_subnet)

    @override_settings(TRACKING_COLLECT_RATE="2/m")
    def test_collection_rate_limit_fails_closed(self) -> None:
        responses = [self._post(self._payload()) for _ in range(3)]

        self.assertEqual([response.status_code for response in responses], [202, 202, 403])


@override_settings(
    TRACKING_WEBHOOK_ENABLED=True,
    TRACKING_SECRET="phase03-test-secret",
    TRACKING_WEBHOOK_RATE="10/m",
)
class TrackingWebhookTests(TestCase):
    URL = "/api/track/webhooks/booking-complete/"

    def setUp(self) -> None:
        cache.clear()
        self.session = TrackSession.objects.create(
            session_id=uuid.uuid4(),
            landing_url="http://testserver/",
        )

    def _body(self) -> bytes:
        return json.dumps(
            {
                "session_id": str(self.session.session_id),
                "booking_id": "BK-123",
                "service": "Refrigerator repair",
            },
            separators=(",", ":"),
        ).encode()

    def _post(self, body: bytes, signature: str | None = None):
        digest = signature
        if digest is None:
            digest = hmac.new(
                b"phase03-test-secret",
                body,
                hashlib.sha256,
            ).hexdigest()
        return self.client.post(
            self.URL,
            data=body,
            content_type="application/json",
            HTTP_X_TRACKING_SIGNATURE=f"sha256={digest}",
            REMOTE_ADDR="198.51.100.10",
        )

    def test_valid_hmac_marks_conversion_once_with_target_neutral_contract(self) -> None:
        body = self._body()
        first = self._post(body)
        second = self._post(body)

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.session.refresh_from_db()
        self.assertTrue(self.session.is_converted)
        self.assertEqual(
            TrackEvent.objects.filter(event_name="booking_completed").count(),
            1,
        )

    def test_invalid_hmac_and_missing_secret_fail_closed(self) -> None:
        invalid = self._post(self._body(), signature="0" * 64)
        with override_settings(TRACKING_SECRET=""):
            missing_secret = self._post(self._body())

        self.assertEqual(invalid.status_code, 403)
        self.assertEqual(missing_secret.status_code, 503)
        self.assertFalse(TrackSession.objects.get(pk=self.session.pk).is_converted)

    def test_webhook_validates_content_type_and_body_size(self) -> None:
        wrong_type = self.client.post(
            self.URL,
            data="{}",
            content_type="text/plain",
            HTTP_X_TRACKING_SIGNATURE="sha256=invalid",
        )
        oversized = self._post(b"x" * 65_537)

        self.assertEqual(wrong_type.status_code, 415)
        self.assertEqual(oversized.status_code, 413)

    @override_settings(TRACKING_WEBHOOK_RATE="1/m")
    def test_webhook_rate_limit_fails_closed(self) -> None:
        first = self._post(self._body())
        second = self._post(self._body())

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 403)


@override_settings(TRACKING_ENABLED=True)
class TrackServerEventTests(TestCase):
    def setUp(self) -> None:
        self.session = TrackSession.objects.create(
            session_id=uuid.uuid4(),
            landing_url="http://testserver/",
        )
        self.factory = RequestFactory()

    def test_server_event_uses_generic_session_field_and_property_allowlist(self) -> None:
        try:
            from tracking.utils import track_server_event
        except ModuleNotFoundError as exc:  # pragma: no cover - RED guard
            self.fail(f"server tracking utility is unavailable: {exc}")

        request = self.factory.post(
            "/contact/submit/",
            {"tracking_session_id": str(self.session.session_id)},
        )
        track_server_event(
            request,
            "contact_email_sent",
            {"utm_source": "google", "email": "must-not-persist@example.com"},
        )

        event = TrackEvent.objects.get()
        self.assertEqual(event.event_name, "contact_email_sent")
        self.assertEqual(event.properties, {"utm_source": "google"})
        self.assertNotIn("lowl", request.POST)

    @override_settings(TRACKING_ENABLED=False)
    def test_disabled_server_tracking_is_a_noop(self) -> None:
        from tracking.utils import track_server_event

        request = self.factory.post(
            "/contact/submit/",
            {"tracking_session_id": str(self.session.session_id)},
        )
        track_server_event(request, "contact_email_sent")

        self.assertEqual(TrackEvent.objects.count(), 0)

    def test_invalid_event_or_database_error_never_crashes_caller(self) -> None:
        from tracking.utils import track_server_event

        request = self.factory.post(
            "/contact/submit/",
            {"tracking_session_id": str(self.session.session_id)},
        )
        track_server_event(request, "arbitrary_event", {"secret": "value"})
        with patch.object(TrackEvent.objects, "create", side_effect=DatabaseError("offline")):
            track_server_event(request, "contact_email_sent")

        self.assertEqual(TrackEvent.objects.count(), 0)


class TrackingAdminTests(TestCase):
    def setUp(self) -> None:
        self.superuser = get_user_model().objects.create_superuser(
            username="tracking-admin",
            email="tracking-admin@example.com",
            password="test-password",
        )
        self.session = TrackSession.objects.create(
            session_id=uuid.uuid4(),
            landing_url="http://testserver/",
            utm_source="=unsafe-formula",
            ip_hash="f" * 64,
        )
        TrackEvent.objects.create(
            session=self.session,
            event_name="page_view",
            properties={"title": "Home"},
        )

    def test_tracking_dashboard_requires_model_permission(self) -> None:
        anonymous = self.client.get("/admin/tracking/")

        limited_user = get_user_model().objects.create_user(
            username="limited-admin",
            password="test-password",
            is_staff=True,
        )
        limited_user.user_permissions.add(
            Permission.objects.get(
                content_type__app_label="wagtailadmin",
                codename="access_admin",
            )
        )
        self.client.force_login(limited_user)
        forbidden = self.client.get("/admin/tracking/")

        self.assertEqual(anonymous.status_code, 302)
        self.assertIn(forbidden.status_code, {302, 403})
        self.assertNotEqual(forbidden.status_code, 200)

    def test_authorized_dashboard_and_detail_hide_ip_hash(self) -> None:
        self.client.force_login(self.superuser)
        dashboard = self.client.get("/admin/tracking/")
        detail = self.client.get(f"/admin/tracking/session/{self.session.pk}/")

        self.assertEqual(dashboard.status_code, 200)
        self.assertEqual(detail.status_code, 200)
        combined = dashboard.content + detail.content
        self.assertNotIn(("f" * 64).encode(), combined)
        self.assertNotIn(str(self.session.session_id).encode(), dashboard.content)

    def test_csv_export_is_permission_gated_and_formula_safe(self) -> None:
        self.client.force_login(self.superuser)
        response = self.client.get("/admin/tracking/export/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("text/csv", response["Content-Type"])
        content = response.content.decode()
        self.assertIn("'=unsafe-formula", content)
        self.assertNotIn(str(self.session.session_id), content)


@override_settings(
    TRACKING_RETENTION_DAYS=30,
    TRACKING_CONVERTED_RETENTION_DAYS=60,
)
class TrackingCleanupCommandTests(TestCase):
    def setUp(self) -> None:
        now = timezone.now()
        self.old_unconverted = TrackSession.objects.create(
            session_id=uuid.uuid4(),
            landing_url="http://testserver/old-unconverted",
        )
        self.old_converted = TrackSession.objects.create(
            session_id=uuid.uuid4(),
            landing_url="http://testserver/old-converted",
            is_converted=True,
            converted_at=now - timedelta(days=61),
        )
        self.recent = TrackSession.objects.create(
            session_id=uuid.uuid4(),
            landing_url="http://testserver/recent",
        )
        TrackSession.objects.filter(pk=self.old_unconverted.pk).update(
            created_at=now - timedelta(days=31)
        )
        TrackSession.objects.filter(pk=self.old_converted.pk).update(
            created_at=now - timedelta(days=61)
        )

    def test_cleanup_supports_dry_run_apply_and_idempotent_rerun(self) -> None:
        dry_output = StringIO()
        try:
            call_command("cleanup_tracking", "--dry-run", stdout=dry_output)
        except CommandError as exc:  # pragma: no cover - RED guard
            self.fail(f"tracking cleanup command is unavailable: {exc}")
        self.assertEqual(TrackSession.objects.count(), 3)
        self.assertIn("would delete", dry_output.getvalue().lower())

        apply_output = StringIO()
        call_command("cleanup_tracking", stdout=apply_output)
        self.assertEqual(
            set(TrackSession.objects.values_list("pk", flat=True)),
            {self.recent.pk},
        )
        self.assertIn("deleted 2", apply_output.getvalue().lower())

        rerun_output = StringIO()
        call_command("cleanup_tracking", stdout=rerun_output)
        self.assertIn("deleted 0", rerun_output.getvalue().lower())
