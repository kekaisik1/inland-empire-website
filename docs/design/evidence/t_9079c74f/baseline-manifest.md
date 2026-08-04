# Baseline browser QA evidence — t_9079c74f

Run target: `/home/kaisar/Desktop/work/Kabi/inland-empire-website`
Evidence directory: `docs/design/evidence/t_9079c74f/`
Local base URL: `http://127.0.0.1:8057`
Task scope: baseline-only checks and screenshots; no product fixes, commits, pushes, Railway mutations, or LOWL commands.

## Pre-existing target Git status

Recorded before baseline checks or evidence writes:

```text
M .gitignore
?? .hermes/
?? .project.context.md
?? docs/
```

Final Git status still preserves those pre-existing target changes and adds only this task's evidence under `docs/design/evidence/t_9079c74f/`.

## Environment and startup

- Python initially could not import Django from the ambient interpreter (`ModuleNotFoundError: No module named 'django'`).
- Created/used ignored local virtualenv `.venv/` with `uv venv .venv && . .venv/bin/activate && uv pip install -r requirements.txt`; no requirements or product dependency files were edited.
- Local DB `db.sqlite3` already existed/was ignored; `migrate --noinput` reported no migrations to apply.
- App started safely with `.venv/bin/python manage.py runserver 127.0.0.1:8057`.
- Local DB seed/content commands were run only in this target workspace against ignored local SQLite state to make live representative routes available.

## Commands and results

| Status | Command | Result |
|---|---|---|
| FAIL (env prerequisite) | `python manage.py check` before venv activation | Exit 1, Django import missing. |
| PASS | `uv venv .venv && . .venv/bin/activate && uv pip install -r requirements.txt` | Exit 0; installed runtime deps into ignored `.venv/`. |
| PASS with warning | `python manage.py check` | Exit 0; existing `debug_toolbar.W003` middleware ordering warning. |
| PASS with warning | `python manage.py makemigrations --check --dry-run` | Exit 0; no changes detected; same debug-toolbar warning. |
| PASS with warning | `python manage.py test --verbosity 1` | Exit 0; 69 tests OK; same debug-toolbar warning. |
| PASS | `npm run build:css` | Exit 0; Tailwind rebuilt; Browserslist stale notice; no tracked CSS diff. |
| PASS | `git diff --check` | Exit 0. |
| PASS with warning | `python manage.py migrate --noinput` | Exit 0; no migrations to apply; debug-toolbar warning. |
| PASS / local DB mutation only | `python manage.py setup_pages` | Exit 0; skipped because HomePage already existed. |
| PASS / local DB mutation only | `python manage.py setup_spanish_pages` | Exit 0; created 26 Spanish page translations in local DB. |
| PASS / local DB mutation only | `python manage.py populate_spanish_content` | Exit 0; skipped 10 pages already containing body content. |
| PASS / local DB mutation only | `python manage.py populate_city_seo --apply` | Exit 0; updated/published 20 local DB city pages. |
| PASS / local DB mutation only | `python manage.py expand_service_faq --apply` | Exit 0; updated/published 9 local DB service pages. |
| PASS | `python docs/design/evidence/t_9079c74f/route_probe.py http://127.0.0.1:8057` | 18 expected route probes returned 200; `/no-such-page/` returned expected 404. See `route-status.txt`. |
| PASS / substitute browser automation | `python docs/design/evidence/t_9079c74f/cdp_capture.py http://127.0.0.1:8057` | Captured 65 route/viewport observations to `browser-observations.json`. |
| PASS | `bash docs/design/evidence/t_9079c74f/capture_screenshots.sh http://127.0.0.1:8057` | Captured 17 PNG screenshots. |
| PASS | `python docs/design/evidence/t_9079c74f/summarize_observations.py` | Wrote spot-check summary to `browser-observations-summary.txt`. |

## Route status coverage

See `route-status.txt` for exact bytes/title/final URL. Summary:

- PASS: `/`, `/services/`, `/services/refrigerator-repair/`, `/service-areas/`, `/service-areas/appliance-repair-corona-ca/`, `/blog/`, `/contact/`, `/about-us/`, `/search/?q=washer` returned 200.
- PASS: Spanish `/es/`, `/es/services/`, `/es/services/refrigerator-repair/`, `/es/service-areas/appliance-repair-corona-ca/`, `/es/blog/` returned 200.
- PASS: `/robots.txt`, `/sitemap.xml`, `/sitemap-images.xml`, `/health/` returned 200.
- PASS: `/no-such-page/` returned expected 404.
- SKIPPED: Blog detail route; this local baseline DB exposes a blog index but no seeded blog article.
- SKIPPED: `/image-sitemap.xml`, `/llms.txt`, `/llms-full.txt`; this baseline target exposes `/sitemap-images.xml` but these Phase 08 endpoints are not present in the current route file.

## Viewports and screenshots

Observation matrix covered these viewports for every route listed in `cdp_capture.py`:

- `desktop-1440x900`
- `laptop-1280x720`
- `tablet-768x1024`
- `mobile-390x844`
- `small-mobile-360x740`

Screenshots captured:

- `desktop-1440x900__home-en.png`
- `mobile-390x844__home-en.png`
- `tablet-768x1024__home-en.png`
- `desktop-1440x900__services-en.png`
- `desktop-1440x900__service-refrigerator-en.png`
- `mobile-390x844__service-refrigerator-en.png`
- `desktop-1440x900__areas-en.png`
- `desktop-1440x900__city-corona-en.png`
- `mobile-390x844__city-corona-en.png`
- `desktop-1440x900__blog-en.png`
- `desktop-1440x900__contact-en.png`
- `desktop-1440x900__search-en.png`
- `desktop-1440x900__home-es.png`
- `mobile-390x844__home-es.png`
- `mobile-390x844__service-refrigerator-es.png`
- `desktop-1440x900__city-corona-es.png`
- `desktop-1440x900__blog-es.png`

## Browser, responsive, and interaction observations

PASS:

- No horizontal overflow detected in 65 route/viewport observations.
- No missing/broken images detected by DOM image completeness checks.
- Global shell rendered with `main`, `nav`, and `footer` landmarks on observed routes.
- Mobile menu button toggled to `aria-expanded="true"` and made `#mobile-menu` visible on tablet, mobile, and small-mobile home samples for both EN and ES.
- Visual screenshots preserve the dark Inland visual structure: dark background/surfaces, large white headings, yellow accent text/buttons/trust chips, dark/glass top nav, and bottom mobile quick-action bar.
- Desktop and mobile representative home/service/city screenshots fit the viewport without visible horizontal clipping.

WARN / FAIL baseline findings:

- FAIL identity leakage: all observed public page families include visible/body/title `LOWL` strings, e.g. logo `LOWL INLAND REPAIR`, titles ending `| LOWL`, copy `LOWL Appliance Repair`, and booking URLs `https://lowl-booking-production.up.railway.app/?source=lowl`. This violates the target-owned Inland identity contract but is recorded as pre-existing baseline state, not fixed here.
- WARN console/runtime: each observed page emitted a Chrome warning for Google Fonts preload credentials mismatch: `A preload for 'https://fonts.googleapis.com/...' is found, but is not used because the request credentials mode does not match.` No uncaught page exceptions were captured.
- WARN accessibility/touch spot: automated JS detected sub-44px focusable links on all pages, mostly desktop nav/menu/language/phone links and the 1x1 skip link before focus. Mobile primary CTAs are visually 44px+ in screenshots, but the raw spot check should be refined in Phase 08.
- WARN accessibility spot: 20 observations included unnamed visible controls, with the home hero ZIP input lacking an explicit accessible name in the sampled markup. It has a placeholder but no visible label/aria-label in the captured DOM sample.
- WARN mobile visual: mobile home screenshot shows the booking widget starts below the fold and bottom quick-action bar overlays the very bottom edge of content; no horizontal overflow observed, but long forms need deeper interaction testing.

## Accessibility and QA substitutions

- Automated axe was skipped: `@axe-core/playwright`/Playwright is not part of the current documented project dependencies, and this baseline task was constrained not to add product/dependency changes. Substitute evidence is the CDP/DOM spot check in `browser-observations.json` plus manual visual review of screenshots.
- Lighthouse was skipped for the same no-new-tooling baseline constraint. Substitute evidence: route status, DOM readiness, screenshot capture, broken image checks, and console warning capture.
- Browser tool access to `http://127.0.0.1:8057/` was blocked because the browser backend rejects private/internal URLs, so local Chrome headless/CDP was used instead.

## Final baseline verdict

Verdict: PASS-WITH-ISSUES for evidence capture.

The baseline target can be started and exercised locally, documented checks pass with the known debug-toolbar warning, and reproducible route/viewport/screenshot evidence is stored under this directory. The app is not a product pass: identity/booking leakage from LOWL and accessibility/console warnings are pre-existing baseline findings for later phases to fix and compare against.
