# Phase 03 Platform Integration Contracts

This document describes the runtime contracts introduced by Phase 03. It contains no credentials. All optional integrations are disabled by default and must be enabled explicitly through environment settings.

## First-party tracking

- `TRACKING_ENABLED` (default `false`): enables browser collection and server-side event recording.
- `TRACKING_WEBHOOK_ENABLED` (default `false`): enables the booking-completion webhook independently.
- `TRACKING_REQUIRE_CONSENT` (default `true`): collection requests without `consent: true` are accepted as no-ops and are not persisted.
- `TRACKING_REQUIRE_ORIGIN` (default `true`): browser collection requires a same-origin `Origin` header or an exact origin listed in `TRACKING_ALLOWED_ORIGINS`.
- `TRACKING_ALLOWED_ORIGINS`: comma-separated exact origins. Wildcards are not supported.
- `TRACKING_SECRET`: HMAC-SHA256 secret for `POST /api/track/webhooks/booking-complete/`. The endpoint fails closed when this is missing.
- `TRACKING_IP_HASH_KEY`: optional separate HMAC key for privacy-preserving network-prefix hashes. Django's application secret is the fallback; raw IP addresses are never stored.
- `TRACKING_COLLECT_RATE` / `TRACKING_WEBHOOK_RATE`: `django-ratelimit` rates (defaults `30/m` and `10/m`).
- `TRACKING_RETENTION_DAYS` / `TRACKING_CONVERTED_RETENTION_DAYS`: retention windows (defaults 90 and 180 days).
- `TRACKING_ADMIN_ENABLED` (default `true`): controls Wagtail menu visibility; model permission checks still protect every view/export.

The client contract uses `sessionStorage`, not cookies, with key `inland_tracking_sid`. Do-not-track (`DNT: 1`) and Global Privacy Control (`Sec-GPC: 1`) make browser collection a no-op. URLs are reduced to scheme/host/path, event properties are allowlisted, client timestamps are bounded, and the collection response never sets a cookie.

The retention command supports preview and idempotent application:

```text
python manage.py cleanup_tracking --dry-run
python manage.py cleanup_tracking
```

## VAPI ZIP tool

- `VAPI_ENABLED` (default `false`): enables `POST /api/vapi/check-zip/`.
- `VAPI_SERVER_SECRET`: compared in constant time with the `X-Vapi-Secret` header.
- `VAPI_ALLOW_UNSIGNED` (default `false`): explicit development escape hatch; never enable in production.
- `VAPI_RATE` (default `30/m`): per-client rate.

The endpoint accepts one `check_zip_code` tool call, caps JSON bodies at 32 KiB, and reads live `CityPage.zip_codes`. It performs no external call and makes no availability, pricing, certification, or warranty claim.

## Discovery and verification

- `BING_SITE_AUTH_TOKEN` (default empty): enables `/BingSiteAuth.xml` only when it contains a valid token-shaped value.
- `/llms.txt` and `/llms-full.txt` derive identity/content from the current Wagtail site and build links from the request host.
- `/robots.txt`, `/sitemap.xml`, and `/sitemap-images.xml` derive scheme/host from the request. Reverse-proxy scheme trust is controlled separately below.

## Contact and booking integration

- `CONTACT_EMAIL`: required destination for contact form delivery. Delivery failures are shown as failures and never create a success tracking event.
- `BOOKING_DOMAIN`: optional target booking host exposed to the template context.

## Proxy trust and response security

- `TRUSTED_PROXY_CIDRS`: comma-separated proxy networks whose forwarding headers may influence `REMOTE_ADDR`. An untrusted immediate peer cannot override the client IP. Invalid chains fall back safely.
- `TRUST_PROXY_HEADERS`: explicit production opt-in for Django's forwarded-protocol handling. It defaults off, including on Railway. Enable it only when the origin is reachable exclusively through a proxy that overwrites `X-Forwarded-Proto`.

The CSP uses explicit origins required by the target's current Google Fonts, jsDelivr, analytics, CallRail, Cloudinary, and Tag Manager integrations. No broad host wildcard or `unsafe-eval` is allowed. Existing inline target templates still require `unsafe-inline`; removing it requires the later public-template/JavaScript integration phase to introduce nonces or externalize scripts without regressions.
