# Railway deployment guide

This repository is prepared for Railway Git deployments using the root `Dockerfile` and `railway.json`. During planning the local Railway CLI reported that this directory was not linked to a project. Phase 07 did not log in, link a project, set variables, create services, deploy, or otherwise mutate Railway.

## Deployment contract

Railway builds the multi-stage Docker image. The image installs pinned Python and Node inputs, builds Tailwind CSS, compiles the Spanish gettext catalog with `polib`, and runs `collectstatic` with WhiteNoise's manifest storage. Railway then runs `/app/predeploy.sh` once in a separate pre-deploy container. That script applies migrations and runs the approved idempotent Wagtail content sequence:

1. `setup_pages`
2. `create_brand_pages`
3. `populate_blog_posts`
4. `update_service_content`
5. `setup_regional_service_pages` (creates only missing city/service drafts)
6. `setup_spanish_pages`
7. `populate_spanish_content`

Any migration or seed failure aborts the deployment. Seeds are not launched as an unobserved background process. `/app/start.sh` performs a final idempotent migration safety check and starts Gunicorn on Railway's `PORT`; it does not repeat content reconciliation by default. This keeps the healthcheck cold start short while ensuring content is ready before serving. For direct Docker use without Railway's pre-deploy hook, set `RUN_STARTUP_SEEDS=true` for the first start.

The final image runs as the unprivileged `app` user. Application source and collected static artifacts are readable but not writable at runtime; only `/app/media` is writable for the explicitly documented local-media fallback. Gunicorn's default source-tree control socket is disabled so normal operation does not need to modify `/app`.

## 1. Connect the target GitHub repository

1. Create or select the intended Railway project and environment in the Railway dashboard.
2. Add a web service from the target GitHub repository `kekaisik1/inland-empire-website`.
3. Confirm the service root is the repository root and the detected builder is `DOCKERFILE` with `Dockerfile` at the root.
4. Do not connect the LOWL repository or copy a LOWL service/project configuration.
5. Add PostgreSQL before the first deployment so Railway can supply a `DATABASE_URL` reference to the web service.

Config-as-code overrides dashboard values for each deployment. Review the deployment details to confirm `railway.json` supplied the Dockerfile builder, pre-deploy command, start command, `/health/` path, and 300-second health timeout.

## 2. Required variables

Use Railway references and generated values; never paste values from another project.

- `SECRET_KEY`: required, unique, random, and at least 50 characters. Generate it locally with `python -c "import secrets; print(secrets.token_urlsafe(64))"`, then store only the result in Railway.
- `DATABASE_URL`: required. Reference the attached Railway PostgreSQL service rather than inventing a connection string.
- Host configuration: Railway supplies `RAILWAY_PUBLIC_DOMAIN`. For a custom domain, also set `ALLOWED_HOSTS` to a comma-separated hostname list and `CSRF_TRUSTED_ORIGINS` to comma-separated full `https://` origins.
- `TRUST_PROXY_HEADERS=true`: appropriate on Railway when the application is reachable only through Railway's proxy, which overwrites `X-Forwarded-Proto`. Leave it false for an origin that can be reached directly.

The production settings automatically allow `RAILWAY_PUBLIC_DOMAIN` and Railway's deployment probe host `healthcheck.railway.app`. The health endpoint is exempt from HTTPS redirect for Railway's internal HTTP probe. Railway's healthcheck proves startup readiness only; it is not continuous monitoring.

## 3. Recommended and optional services

### Redis

`REDIS_URL` is not required for the verified single-worker deployment. Keep `GUNICORN_WORKERS=1` (the repository default) while using the local-memory cache. Do not set `REDIS_URL` in this revision: enabling Django's Redis backend also requires adding the separately reviewed Python Redis client to `requirements.txt`. After that dependency is approved and verified, attach Redis, reference its URL, and then opt into multiple workers for shared rate-limit and cache behavior.

### Durable media with Cloudinary

`CLOUDINARY_URL` enables `django-cloudinary-storage` for Wagtail uploads. Without it, uploaded media uses the container filesystem and is ephemeral across rebuilds/restarts. Static files are not media: WhiteNoise serves immutable collected assets from the image. Configure Cloudinary, or another reviewed durable storage implementation, before relying on editor-uploaded production media. A Railway volume is not configured by this repository.

### Email

Set `CONTACT_EMAIL`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, and `DEFAULT_FROM_EMAIL` to enable contact delivery. The default SMTP hostname alone is not a working email configuration. Test delivery after deployment; the contact flow does not report success when sending fails.

### Booking and identity

Optional target-owned values are `BUSINESS_NAME`, `WAGTAILADMIN_BASE_URL`, `BOOKING_URL`, and `BOOKING_DOMAIN`. Keep these specific to Inland Empire. An explicit `WAGTAILADMIN_BASE_URL` is preserved when Railway also supplies its generated domain.

### Tracking, VAPI, discovery, and Sentry

All external/collection integrations are optional and disabled or fail closed by default. See `docs/configuration/phase-03-platform-contracts.md` and `.env.example` for names only. In particular:

- Tracking: `TRACKING_ENABLED`, `TRACKING_WEBHOOK_ENABLED`, consent/origin controls, rates/retention, `TRACKING_SECRET`, and `TRACKING_IP_HASH_KEY`.
- VAPI: `VAPI_ENABLED`, `VAPI_SERVER_SECRET`, `VAPI_ALLOW_UNSIGNED`, and `VAPI_RATE`. Never enable unsigned requests in production.
- Discovery: `BING_SITE_AUTH_TOKEN` is optional and the endpoint stays unavailable when unconfigured.
- Monitoring: `SENTRY_DSN`, environment, and sample-rate variables are optional.

## 4. Optional bootstrap superuser

For the first deployment only, set all three variables together:

- `DJANGO_SUPERUSER_USERNAME`
- `DJANGO_SUPERUSER_EMAIL`
- `DJANGO_SUPERUSER_PASSWORD`

The pre-deploy script creates the user only when the username does not already exist. Existing users are left unchanged. Remove all three variables after the first successful deployment. A partial set fails pre-deploy instead of silently creating an unintended account.

Alternatively, use a one-off Railway shell after deployment and run Django's normal superuser command interactively.

## 5. First deployment

1. Confirm PostgreSQL and the required variables are configured.
2. Generate a Railway domain or add the custom domain and CSRF values.
3. Trigger the first deployment from the target GitHub branch.
4. Inspect build logs for successful dependency installation, Tailwind build, translation compilation, and `collectstatic`.
5. Inspect pre-deploy logs for migrations and all seven seed commands. A nonzero command correctly blocks the release.
6. Inspect runtime logs for the final migration check and Gunicorn binding to the injected `PORT`.
7. Wait for Railway to record the deployment as `SUCCESS`; a queued/building deployment is not a success.

## 6. Deployment verification

After a successful Railway deployment, verify with the actual public/custom domain:

- `GET /health/` returns HTTP 200 and `{"status":"ok"}`.
- `/static/css/output.css` returns HTTP 200 with a long-lived immutable asset URL from the rendered page.
- `/`, `/services/`, one service detail, `/service-areas/`, one city, `/blog/`, and `/es/` render without 5xx responses.
- The admin login loads at `/admin/` and uses the expected external HTTPS URL.
- Migrations and seed logs have no warning that was converted into a hidden success.
- If enabled, test contact email, Cloudinary upload/readback, tracking consent/origin behavior, Redis-backed rate limits, and Sentry in that environment.

A Git push, Docker build, or local SQLite smoke is not proof of a Railway/PostgreSQL production deployment. Record the Railway deployment ID/commit and live checks only after they actually exist.

## 7. Rollback and recovery

- For an application regression, select the last known-good Railway deployment and redeploy/rollback it from the dashboard. Verify `/health/` and representative routes again.
- Application rollback does not reverse database migrations. All current migrations are forward-compatible for this release; if a future migration is destructive, take a PostgreSQL backup and write an explicit data rollback before deploying it.
- The content commands are idempotent and editor-preserving for their accepted seed contracts, but they are not a general database restore mechanism.
- If pre-deploy fails, fix the failing migration/seed in a new commit or correct a missing required variable; do not bypass it by masking the exit code.
- Restore uploaded media from the configured durable media provider. Container-local media cannot be recovered after replacement.

## 8. Local and CI verification

The GitHub Actions workflow runs on pushes and pull requests without secrets. It installs Python 3.12 and Node 20 inputs, runs `npm ci`, compiles translations, performs Django checks and migration drift detection, runs the full test suite, verifies a byte-stable Tailwind build, and validates this deployment contract.

Before publishing, run the same commands locally plus the production check and Docker smoke documented in the Phase 07 report. `.dockerignore` controls Docker build context. `.railwayignore` is specifically used by `railway up` CLI uploads, which also respect `.gitignore`; GitHub-backed deployments use the tracked repository and Docker build context. Required runtime PNG/WebP assets are intentionally included.

## Limitations

- This guide and Phase 07 provide deployment readiness, not a production deployment result.
- Local/container verification uses disposable SQLite for isolation and does not prove PostgreSQL data, extensions, latency, backups, or connection limits.
- Railway's healthcheck is a deployment readiness gate, not ongoing uptime monitoring.
- Local-memory cache is process-local; configure Redis for shared behavior.
- Container-local uploaded media is ephemeral; configure Cloudinary or another durable backend.
- SMTP, booking, tracking, VAPI, Bing verification, Sentry, custom DNS, and TLS behavior require environment-specific verification after they are enabled.
- The local Railway CLI remained unlinked and no Railway state was mutated in Phase 07.
