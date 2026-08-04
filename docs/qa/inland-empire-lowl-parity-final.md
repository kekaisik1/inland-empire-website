# Inland Empire LOWL parity — final QA

Date: 2026-08-04

## Verdict

The Inland Empire application is a release-ready functional adaptation of the current LOWL product behavior while retaining its own dark charcoal, white, and yellow design. LOWL was treated as a read-only reference. Public rendering, seed workflows, localization, draft handling, deployment contracts, and representative production-container routes pass locally.

## Functional reconciliation

- The target includes LOWL-equivalent CMS, tracking, consent, booking/UTM, ZIP/VAPI, contact, search, SEO/schema, sitemap, localization, service, city, blog, static-page, brand-hub, and deployment behavior.
- The current LOWL service delta is present: garbage disposal, cooktop, and ice maker pages seed in English and Spanish.
- Twenty regional city/service pages seed as editor-preserving drafts. They remain absent from navigation, public listings, Spanish cloning, and sitemaps until explicitly published.
- The public identity remains Inland Empire Appliance Repair. No LOWL booking URL, contact identity, remote, deployment identifier, blue visual token, or Satoshi font is used by the rendered application.

## Automated verification

The final gate includes:

- `python manage.py check`
- `python manage.py makemigrations --check --dry-run`
- full Django test suite
- Ruff over application and deployment-script Python
- Node interaction tests under `mysite/static/js/tests/`
- `npm ci` and deterministic `npm run build:css`
- gettext compilation
- production `check --deploy` with disposable settings
- `python scripts/verify_deployment_contract.py`
- `git diff --check`
- `docker compose config --quiet` with safe local variables
- a clean multi-stage `docker build`

## Production-container QA

A fresh image was started with production settings, a disposable SQLite database, idempotent startup seeds, Railway-style forwarded HTTPS, and no external integrations. Migrations and all seven seed commands completed before Gunicorn became healthy.

The following routes returned the expected result:

| Route | Result |
|---|---:|
| `/health/` | 200 |
| `/` | 200 |
| `/services/` | 200 |
| `/services/garbage-disposal-repair/` | 200 |
| `/services/cooktop-repair/` | 200 |
| `/services/ice-maker-repair/` | 200 |
| `/service-areas/` | 200 |
| `/blog/` | 200 |
| `/es/` | 200 |
| `/admin/login/` | 200 |
| `/static/css/output.css` | 200 |
| `/sitemap.xml` | 200 |
| `/services/ac-repair-riverside-ca/` | 404, expected draft behavior |

Headless Chrome inspected the English home, services index, all three restored service pages, Spanish home, and a 390px mobile home viewport. Every inspected page had zero broken images, no horizontal overflow, no LOWL public-identity text, and the expected `rgb(26, 27, 32)` dark background. The Spanish 1440px header intentionally uses the full accessible menu instead of allowing translated labels to collide. English keeps the full desktop navigation.

## Deployment notes

Railway should deploy from `kekaisik1/inland-empire-website` using the root `Dockerfile` and `railway.json`. PostgreSQL, a unique 50-plus-character `SECRET_KEY`, and `TRUST_PROXY_HEADERS=true` are required for the intended Railway setup. Redis, Cloudinary, SMTP, tracking, VAPI, Sentry, and custom domains remain environment-specific opt-ins documented in `docs/deployment/railway.md`.

Local-memory cache is sufficient for the verified basic deployment. Shared Redis behavior must not be enabled unless the Python Redis client is included in the production dependency set.

## Source boundary

The current LOWL product reference remained at commit `9565400e588890f816d81616b3b2ca05e74f238d`. Its pre-existing workflow-only working-tree changes were not touched, and its product tree had no live diff outside those excluded workflow/QA paths at final reconciliation.
