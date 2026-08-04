# Inland Empire Design and Identity Contract — Phase 01

Run: `inland-lowl-parity-20260731`
Root Kanban task: `t_3fa6c191`
Purpose: preserve the Inland Empire dark/yellow visual system and target-owned identity while portable LOWL functionality is ported behavior-by-behavior.

This is the authoritative design and identity contract for Phases 02-09. It converts the Phase 01 design worksheet and baseline browser QA evidence into enforceable invariants. It does not implement product functionality, modify LOWL, commit, push, deploy, or begin Phase 02.

## Evidence authority

1. `.project.context.md`: port LOWL functionality while preserving Inland Empire design and target-specific identity.
2. `.hermes/sources/lowl-parity-20260731/target-design-sha256.txt`: baseline hashes for target design surfaces.
3. `design-bc900e36-8ca8-4ef6-9d17-63f980a08d2a.html` and `.hermes/sources/lowl-parity-20260731/design-reference.html`: visual reference only; do not copy prototype LOWL labels/booking strings as production identity.
4. Target merge surfaces: `tailwind.config.js`, `mysite/static/src/input.css`, `mysite/static/css/output.css`, `mysite/templates/base.html`, `home/templates/home/home_page.html`.
5. `docs/design/evidence/inland-empire-visual-identity-invariants.md`: source-cited design worksheet.
6. `docs/design/evidence/t_9079c74f/baseline-manifest.md` and `browser-observations-summary.txt`: local browser baseline evidence.
7. `docs/parity/lowl-feature-parity.md`: behavior-family ownership and identity/design disposition matrix.

Baseline design hashes captured at Phase 01 start:

| Surface | SHA-256 |
|---|---|
| `design-bc900e36-8ca8-4ef6-9d17-63f980a08d2a.html` | `d2d33e5463806b4da1b6677b2b50a6e3a2442a8393e417f10ff313b7e4f6b7a9` |
| `tailwind.config.js` | `fd4f2c2b52895c09a1865d3cb8f750a8285ae3b4a09febc92df25ad1d307a86d` |
| `mysite/static/src/input.css` | `a1b04690c626bcb03bba56057e7d2e54faa012c8c7b0ff424222e6f5347f7d51` |
| `mysite/templates/base.html` | `18c1858346aef7488d60237017b8a419166486b2d8176fe38a758a4dda3286cb` |
| `home/templates/home/home_page.html` | `862358b8c66b16997a052e6e7db13c0b65ed1af8d109dca1d09800c4a484c1e6` |
| `mysite/static/css/output.css` | `9cd453159b40972d1fd3c89114ecfc1ce4e3895adb8437e1e89ca69c49b3ccab` |

Later phases may intentionally change these files, but every change must cite affected parity rows, preserve the invariants below, rebuild CSS when needed, and provide browser evidence.

## Core rule

Portable LOWL behavior may be ported; LOWL production identity and LOWL public visual style may not.

Portable behavior examples: CMS fields, admin panels, target-native migrations, navigation ordering, static/contact behavior, VAPI ZIP endpoint, booking/UTM mechanics, SEO endpoints, sitemap/robots/llms endpoints, structured data generation, tracking collection/admin behavior, localization/hreflang, seeding commands, carousels, FAQ accordions, pagination, accessibility behaviors, and tests.

Non-portable as-is: LOWL blue palette, white page shell, Satoshi global typography, LOWL production business name/address/phone/email/domain/booking URL/booking source/analytics IDs/verification tokens/review claims/Railway identifiers/source remote, and source runtime/audit material.

## Visual tokens and component invariants

| Invariant | Required behavior | Prohibited behavior |
|---|---|---|
| Background and surfaces | Dark background `#1A1B20`, surface `#25262C`, hover surface `#2d2e35`, footer `#15161A` remain dominant across public routes. | Replacing the site shell/cards with LOWL white, pale gray, or blue-heavy surfaces. |
| Accent color | Yellow `#FFD504` is the primary CTA/accent/focus cue; hover `#e6c003`, light `#ffe34d`, pale yellow overlays allowed. | Global blue CTA/gradient takeover using LOWL `#1545ad`/`#3b76e8`. |
| Text | White primary text, muted gray `#A0A0A5`, dark `#121212` text on yellow/light CTAs. | LOWL gray-on-white text hierarchy as the global public style. |
| Typography | Montserrat display, Inter body, Sacramento only where intentionally decorative. | Importing or applying LOWL Satoshi as the global public font. |
| Geometry | 24px cards, 50px pill buttons, 8px inputs, 1280px site container. | Reverting public components to LOWL 8px cards and square/4px buttons. |
| Motion/effects | Dark/glass nav, diagonal yellow stripe motif, dark scrollbars, reduced-motion support. | White sticky header, blue arcs, or blue editorial treatments replacing target effects. |
| Accessibility | Visible focus states, 44px touch targets for primary mobile controls, semantic landmarks, no horizontal overflow. | Mouse-only dropdowns/modals, hidden labels for new inputs, or fixed bars covering primary actions. |

Component contracts: `.btn`, `.btn-primary`, `.btn-outline`, `.btn-accent`, `.container-site`, `.section-header`, `.service-card`, `.price-box`, `.booking-widget`, `.glow-dot`, `.trust-chip`, `.input-dark`, `.stripe-bg`, `.prose`, FAQ Alpine components, mobile navigation Alpine components, skip link, dark footer, and bottom mobile quick-action bar remain the target primitives unless a reviewed target-native replacement is documented.

## Shell, navigation, footer, and mobile quick actions

Must preserve:

- Fixed dark glass navigation around 80px high, dark border, blur, and dark dropdown panels.
- Target-style wordmark treatment: yellow short-name segment plus white Inland wording. Existing public LOWL fallback strings are baseline debt to fix, not acceptable future defaults.
- Desktop links for Home, Services, Service Areas, Blog, About, Contact, with service/city dropdowns that remain readable and constrained to viewport.
- EN/ES switcher, active yellow pill, and hreflang/translation-url behavior.
- Desktop booking/phone CTAs with `data-booking` mechanics and target-owned booking URL/source.
- Mobile menu with 44px toggle, `aria-expanded`, dark full-height sheet, language switcher, Book/Call buttons, predictable close behavior.
- Dark footer with services/company/contact/address columns and yellow contact links.
- Bottom mobile quick-action bar, dark/glass, at least 44px touch targets, without hiding required content.
- Skip link remains first-focusable and visible on focus.

Prohibited:

- Source white sticky header, gray links, white dropdown panels, or wholesale source `base.html` takeover.
- Removing the mobile quick-action bar without a reviewed equivalent.
- Copying source loop structures or fallback strings unless they are translated to target design and target identity.

## Page-family invariants

| Family | Required design behavior | Identity/content cautions |
|---|---|---|
| Home | Dark hero, Montserrat display, yellow-highlighted locality, diagonal stripes, two-column booking widget, trust chips, dark/surface section rhythm, yellow CTAs, dark FAQ/reviews/areas/process/pricing treatments. | Existing LOWL name/booking leakage is baseline debt; service/review/pricing claims require evidence or target approval. |
| Services index/detail | Dark service hero/cards/body/FAQ, yellow icons/buttons, target service cards, accessible FAQ and future carousel controls. | Carousel behavior may port, but not source white/gray carousel styling; service claims must be target-safe. |
| Service areas/city | Dark city hero, trust chips, ZIP chips, featured-service cards, sidebar/CTA, FAQ accordions, target locality names. | City/service-area copy must use Inland/Corona/Riverside County truth and reviewed ZIP coverage. |
| Blog | Dark blog hero/cards/pagination/detail/prose; article cards should remain readable on dark surfaces. | Do not import source white editorial card system or blue gradients; article facts/prices require source grounding. |
| Static/contact | Dark hero, dark form fields/cards, accessible labels/error/success states, target phone/email/address. | No public `Contact LOWL Appliance Repair`; contact values from settings/env/SiteSettings only. |
| Search | Dark search input/results/no-results cards, keyboard/focus-visible result links. | Localized search routes must preserve language intent when present. |
| SEO machine endpoints | Raw response checks for robots/sitemaps/llms/Bing when configured. | No concrete LOWL domain/token; host and verification values target-owned/env-driven. |
| Tracking/admin | Wagtail admin dashboard/session/detail/partials only after Phase 03; privacy-safe admin display. | No public tracking dashboard leakage; no source analytics IDs/secrets. |

## Target-owned identity contract

The following values are target-owned and must be preserved or made configurable through target settings/SiteSettings/env. They must not be replaced with LOWL production defaults:

Target migration continuity is part of identity preservation: keep `home/migrations/0009_update_contact_info_corona.py` unchanged and replay source-only home behavior as target-native `0010+` migrations.

- Business name and public/admin/site metadata.
- Phone and display phone.
- Email.
- Street address, city, ZIP, service-area defaults.
- Booking URL and booking source.
- Analytics, GTM, search verification, Bing verification, tracking secrets, CallRail swap URL.
- Railway/GitHub remote/project values.
- Structured data name, phone, email, address, logo/image, rating/reviews, sameAs links.
- Logos/icons and manufacturer/brand labels.
- English and Spanish public copy.

Known baseline identity debt from browser evidence:

- Public pages included `LOWL` strings in body/title/logo, including titles ending `| LOWL` and copy such as `LOWL Appliance Repair`.
- Booking URLs used `https://lowl-booking-production.up.railway.app/?source=lowl`.
- Existing model/template fallbacks include LOWL strings. These are not allowed final behavior; later phases must remove or parameterize them as target-owned values.

Claims requiring evidence or safe parameterization before final public/schema use:

- Ratings and review counts.
- Customer review cards and exact review text.
- Same-day availability and scheduling guarantees.
- Warranty/no-overtime/diagnostic-fee statements.
- OEM/factory/EPA/certification/authorization claims.
- Manufacturer-specific repair capabilities beyond generic service offerings.
- ZIP/service-area counts and city coverage.
- Commercial capability statements.
- Blog/service/city/Spanish facts that imply public truth.

If direct source evidence is not available, use editable target-owned copy, suppress schema fields, or mark `blocked_needs_evidence`.

## English/Spanish expectations

- EN/ES routes must preserve localized page intent and emit correct hreflang where implemented.
- Spanish pages must use target/Inland/Corona identity, not LOWL production identity.
- Language switcher behavior must keep users on equivalent page families where translations exist.
- Translation catalogs and seed commands must be compiled/run only in the target and verified with rendered route evidence.
- When translations do not exist yet, fallback behavior must be explicit and must not silently introduce LOWL copy.

## Representative routes and viewports

Phase 08 owns final full browser QA. Earlier UI phases must capture the subset they touch.

| Family | English route | Spanish expectation | Viewports | Required evidence | Interaction checks |
|---|---|---|---|---|---|
| Home/global shell | `/` | `/es/` when translation exists | 1440x900, 1280x720, 768x1024, 390x844, 360x740 | Screenshots showing dark/yellow hero, glass nav, dark booking widget, trust chips, footer, mobile bottom bar. | Dropdown keyboard/mouse, mobile menu toggle/close, language switcher, booking URL, phone link, overflow, console. |
| Services index | `/services/` | `/es/services/` when translation exists | 1440x900, 768x1024, 390x844, 360x740 | Dark service index hero/cards/CTAs. | Service links, CTA focus states, mobile quick bar overlap. |
| Service detail | `/services/refrigerator-repair/` or first seeded service | `/es/services/refrigerator-repair/` equivalent when seeded | 1440x900, 768x1024, 390x844, 360x740 | Dark service hero/body/problem list/FAQ/related/brand/carousel states. | FAQ aria-expanded, carousel empty/one/many keyboard/touch, Book/Call, JSON-LD target identity. |
| Service areas index | `/service-areas/` | `/es/service-areas/` when translation exists | 1440x900, 768x1024, 390x844, 360x740 | Dark service-area hub/city cards. | City links, CTA focus, no overflow. |
| City detail | `/service-areas/corona-ca/` or first seeded city route | `/es/service-areas/corona-ca/` equivalent when seeded | 1440x900, 768x1024, 390x844, 360x740 | Dark city hero/trust chips/ZIP chips/service cards/FAQ/sidebar. | FAQ, city Book/Call, structured data target business/city. |
| Blog index/detail | `/blog/` and first seeded article | `/es/blog/` and localized article when present | 1440x900, 768x1024, 390x844, 360x740 | Dark blog cards/pagination/article/prose. | Pagination, article links, Article schema identity, keyboard focus. |
| Static/contact | `/contact/`, `/about-us/` | `/es/contact/`, `/es/about-us/` when present | 1440x900, 768x1024, 390x844, 360x740 | Dark static hero/forms/contact cards. | Form empty/error/success, labels, target phone/email, no LOWL copy. |
| Search | `/search/?q=washer`, empty query, no-results query | `/es/search/?q=lavadora` if localized route exists | 1440x900, 768x1024, 390x844, 360x740 | Dark search input/results/no-results. | Search submit, keyboard focus, result links, no layout shift/overflow. |
| SEO machine endpoints | `/robots.txt`, `/sitemap.xml`, `/image-sitemap.xml` or target equivalent, `/llms.txt`, `/llms-full.txt`, optional `/BingSiteAuth.xml` | Non-localized unless intentionally localized | n/a | Raw response captures and schema/URL assertions. | No concrete LOWL domain/token; safe disabled states. |
| Tracking/admin | Wagtail tracking routes from `tracking/admin_views.py` and `tracking/wagtail_hooks.py`; templates `tracking/templates/tracking/dashboard.html`, `tracking/templates/tracking/session_detail.html`, `tracking/templates/tracking/partials/conversion_table.html`, `tracking/templates/tracking/partials/funnel_chart.html`, and `tracking/templates/tracking/partials/sessions_table.html` | Admin locale as supported | 1440x900, 1280x720, 768x1024 | Admin dashboard/session-detail/partial screenshots or render evidence. | Hook/menu/route registration, authenticated/unauthorized permission checks, privacy-safe fields, and CSV export. |

## Baseline QA issues that must remain visible

Phase 01 browser evidence captured 65 route/viewport observations and 17 screenshots. Baseline evidence passed startup/routes/screenshots with issues:

- PASS: no horizontal overflow across 65 observations.
- PASS: no missing/broken images detected by DOM image checks.
- PASS: global shell had `main`, `nav`, and `footer` landmarks.
- PASS: mobile menu toggled `aria-expanded="true"` and made `#mobile-menu` visible on sampled tablet/mobile/small-mobile home pages.
- PASS: visual screenshots preserved dark Inland structure: dark background/surfaces, large white headings, yellow accent text/buttons/trust chips, dark/glass nav, mobile quick bar.
- FAIL baseline identity leakage: public page families included LOWL strings and LOWL booking URLs.
- WARN console: Google Fonts preload credentials mismatch warning on observed pages.
- WARN accessibility/touch spot: sub-44px focusable links and 1x1 skip link in raw spot checks; refine with better focus-state checks in Phase 08.
- WARN accessibility spot: sampled home hero ZIP input lacked explicit accessible name beyond placeholder.
- WARN mobile visual: home booking widget begins below fold and bottom quick-action bar overlays bottom edge of content; no horizontal overflow observed.

Later workers must not erase these findings from evidence. They must fix or explicitly carry them into Phase 08 with status and proof.

## Explicit prohibitions

- Do not replace public visual system with LOWL blue/white/Satoshi styling.
- Do not wholesale overwrite `tailwind.config.js`, `mysite/static/src/input.css`, `mysite/static/css/output.css`, `mysite/templates/base.html`, or `home/templates/home/home_page.html` from LOWL.
- Do not copy concrete LOWL production identity: business name, address, phone, email, booking URL, booking source, analytics/GTM/search verification tokens, CallRail URL, domains, remote, Railway identifiers, admin credentials, source DB/media/logs, or source runtime/audit folders.
- Do not import source `.git`, `.hermes`, QA archives, Trello/Google exports, credentials, local DB/media/logs, or deployment artifacts.
- Do not claim source reviews, ratings, certifications, review counts, or business facts as Inland Empire facts without direct evidence.
- Do not output review JSON-LD without source-grounded review provenance.
- Do not claim Railway deployment or production service status from a Git push or config file alone.
- Do not use Phase 01 worker self-report alone as readiness for Phase 02; this document and the final review gate are the contract.

## Handoff gates for later phases

- Phase 02: schema/admin workers must preserve target migration `home/migrations/0009_update_contact_info_corona.py`, add source-derived migrations target-natively as `0010+`, and prove no target identity blanking. No UI/content/deploy work.
- Phase 03: platform/API workers must use target env/settings for secrets and identifiers. Tracking and SEO endpoints must be privacy-safe and disabled safely when not configured.
- Phase 04: content/assets workers must produce provenance manifests and source-grounding for sensitive claims. Spanish content must be target-safe.
- Phase 05: shell/home workers must merge behavior into existing dark/yellow shell and home geometry, then capture desktop/mobile interaction evidence.
- Phase 06: page-family workers must translate all source markup to target design primitives and prove service/city/blog/static/contact/search route behavior.
- Phase 07: deployment workers may prove readiness only; no Railway mutation.
- Phase 08: independent QA must run the full route/viewport matrix, inspect console/network/accessibility/overflow/schema, and scan for forbidden LOWL tokens and identity strings (`#1545ad`, `#3b76e8`, `Satoshi`, `info@lowl.net`, `409 N Langstaff`, `Lake Elsinore` as default identity, `lowl-booking-production`, `booking_source default='lowl'`, concrete source IDs/tokens/domains, public `LOWL Appliance Repair` fallbacks).
- Phase 09: release worker must perform final diff/secret/source-read-only checks and may commit/push only target paths to the target GitHub remote.
