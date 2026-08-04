# Inland Empire visual and identity invariants worksheet

Task: `t_372a84d5`
Run: `inland-lowl-parity-20260731`
Created: `2026-07-31T08:32:48+05:00`
Target repo: `/home/kaisar/Desktop/work/Kabi/inland-empire-website`
Read-only source repo: `/home/kaisar/Desktop/work/Kabi/lowl-website`
Captured source baseline: `.hermes/sources/lowl-parity-20260731/`

This worksheet is evidence-only. It defines what later phases must preserve while porting portable LOWL behavior. It does not implement product code, copy runtime assets, mutate LOWL, start Phase 02, deploy, commit, or push.

## 1. Evidence read and authority order

Authoritative target/design evidence:

1. `.project.context.md` establishes the current goal: port LOWL functionality while preserving the Inland Empire dark/yellow design and target-specific identity (`.project.context.md:16-33`).
2. `docs/parity/evidence/immutable-baseline-report.md` locks the source/target baseline and says downstream workers must use the captured source artifacts and target design contract rather than range-merging or bulk-copying same-path files (`docs/parity/evidence/immutable-baseline-report.md:151-157`).
3. `docs/design/inland-empire-design-contract.md` defines the existing Phase 01 design contract and forbidden changes (`docs/design/inland-empire-design-contract.md:20-39`, `docs/design/inland-empire-design-contract.md:82-97`).
4. `.hermes/sources/lowl-parity-20260731/target-design-sha256.txt` hashes the immutable target design surfaces: the ignored design reference, `tailwind.config.js`, source CSS, base shell, home template, and built CSS (`.hermes/sources/lowl-parity-20260731/target-design-sha256.txt:1-6`).
5. `design-bc900e36-8ca8-4ef6-9d17-63f980a08d2a.html` and its captured copy `.hermes/sources/lowl-parity-20260731/design-reference.html` are visual references only, not product-code copy sources. They carry the dark/yellow presentation tokens and also contain prototype LOWL labels/booking strings that must not become target production identity (`design-bc900e36-8ca8-4ef6-9d17-63f980a08d2a.html:7-27`, `design-bc900e36-8ca8-4ef6-9d17-63f980a08d2a.html:741`, `design-bc900e36-8ca8-4ef6-9d17-63f980a08d2a.html:956-1006`).
6. Target templates/assets read in this worksheet: `mysite/templates/base.html`, `home/templates/home/home_page.html`, service/city/blog/static/search templates, `tailwind.config.js`, `mysite/static/src/input.css`, `mysite/static/js/alpine-components.js`, `home/models.py`, `home/migrations/0009_update_contact_info_corona.py`, and `home/templatetags/seo_tags.py`.
7. Captured-source behavior/styling evidence read by path from the read-only LOWL repo, cross-checked against the captured manifest rows in `docs/parity/lowl-feature-parity.md`: `tailwind.config.js`, `mysite/static/src/input.css`, `mysite/templates/base.html`, `home/templates/home/home_page.html`, `home/models.py`, and source template searches.

Unavailable evidence / do not invent:

- No browser screenshots were available or generated for this evidence-only task; screenshot requirements below are contracts for later browser QA, not observed screenshots.
- No live production Inland Empire or LOWL deployment was inspected; identity claims are from repository files only.
- No source design screenshots beyond the captured/reference HTML were available; LOWL blue/white/Satoshi assertions are from source code paths, not visual captures.
- No review provenance, Google Business Profile, Yelp page, or exact public rating source was inspected here. Later content phases must not treat existing review/rating defaults as verified facts.
- No analytics, verification, booking, Railway, or CallRail IDs were inspected as secrets; concrete values remain prohibited unless explicitly target-owned and configured through settings/env.

## 2. Core product boundary

Later workers may port portable LOWL functionality but must not port LOWL production identity or public visual style.

Portable behavior examples:

- CMS fields, admin panels, model capability, migrations replayed target-natively, nav ordering, static-page/contact behavior, VAPI ZIP endpoint, booking/UTM mechanics, SEO endpoints, sitemap/robots/llms endpoints, structured-data generation, tracking collection/admin behavior, localization/hreflang, content seeding commands, page-family interactions, carousels, FAQ accordions, pagination, and tests. These are assigned across P03-P50 in `docs/parity/lowl-feature-parity.md`.

Source styling/identity that is not portable as-is:

- LOWL blue primary palette `#1545ad`, pale/white backgrounds, gray text system, Satoshi global typography, 8px cards/4px buttons, white nav/header/footer/card treatments, LOWL production defaults, LOWL source remote/domain/deployment values, CallRail source URLs, source analytics/verification values, source review claims, and source booking-source defaults. Evidence: LOWL source Tailwind tokens (`/home/kaisar/Desktop/work/Kabi/lowl-website/tailwind.config.js:16-42`), LOWL source CSS Satoshi/font and white card treatments (`/home/kaisar/Desktop/work/Kabi/lowl-website/mysite/static/src/input.css:5-40`, `/home/kaisar/Desktop/work/Kabi/lowl-website/mysite/static/src/input.css:56-97`), LOWL source base white header and Satoshi preloads (`/home/kaisar/Desktop/work/Kabi/lowl-website/mysite/templates/base.html:124-130`, `/home/kaisar/Desktop/work/Kabi/lowl-website/mysite/templates/base.html:193-220`), and LOWL source home blue hero/white booking bar (`/home/kaisar/Desktop/work/Kabi/lowl-website/home/templates/home/home_page.html:41-43`, `/home/kaisar/Desktop/work/Kabi/lowl-website/home/templates/home/home_page.html:114-138`).

## 3. Target visual tokens to preserve

| Invariant | Target evidence | Acceptable changes | Prohibited changes |
|---|---|---|---|
| Background and surfaces remain dark. Use `#1A1B20` background, `#25262C` surface, `#2d2e35` hover surface, `#15161A` footer. | `tailwind.config.js:28-31`; `mysite/static/src/input.css:5-8`; design reference variables in `design-bc900e36-8ca8-4ef6-9d17-63f980a08d2a.html:11-13`. | Add new semantic aliases that resolve to the dark palette; add component-specific dark variants when a new feature requires them. | Replacing target palette with LOWL `#1545ad`, `#f9fafb`, `#ffffff`, gray cards, or a white page shell from source `tailwind.config.js:16-29`. |
| Yellow remains the primary accent/CTA cue: `#FFD504`, hover `#e6c003`, light `#ffe34d`, pale `rgba(255,213,4,0.08)`. | `tailwind.config.js:16-20`; `mysite/static/src/input.css:17-20`, `55-60`, `198-224`. | New components can use yellow accents, rings, chips, lines, and focus states if contrast is maintained. | Blue primary CTA or blue gradients from source `tailwind.config.js:16-21` and source blog gradients using `#1545ad/#3b76e8` in LOWL templates. |
| Text hierarchy: white primary, muted `#A0A0A5`, dark `#121212` on yellow/light CTAs. | `tailwind.config.js:22-25`; base/body and component applications in `mysite/static/src/input.css:5-8`, `31-60`, `125-147`. | Add specific semantic text tokens if they preserve contrast and are backed by browser/a11y checks. | Global gray-on-white source text system from LOWL source `tailwind.config.js:22-29` or source CSS gray card text (`/home/kaisar/Desktop/work/Kabi/lowl-website/mysite/static/src/input.css:117-139`). |
| Typography: Montserrat display, Inter body, Sacramento decorative only where intended. | `tailwind.config.js:37-40`; Google font preload in `mysite/templates/base.html:120-124`; design reference font variables `design-bc900e36-8ca8-4ef6-9d17-63f980a08d2a.html:25-27`. | Add weights/styles for these families if necessary. | Importing LOWL Satoshi as global sans or copying source Satoshi font files into the global design (`/home/kaisar/Desktop/work/Kabi/lowl-website/mysite/static/src/input.css:5-40`; `docs/parity/lowl-feature-parity.md:79-88`). |
| Geometry: 24px cards, 50px pill buttons, 8px inputs, 1280px container. | `tailwind.config.js:42-49`; button/card/input definitions in `mysite/static/src/input.css:24-66`, `74-105`, `184-196`. | New components should map to `rounded-card`, `rounded-button`, `rounded-input`, and `container-site`. | Reverting to LOWL 8px cards and 4px buttons from source `tailwind.config.js:37-42`. |
| Motion/effects: dark glass nav, diagonal yellow stripe motif, dark scrollbars, reduced-motion support. | `mysite/templates/base.html:184-187`; `mysite/static/src/input.css:198-224`, `252-280`; design reference stripe/nav/footer evidence `design-bc900e36-8ca8-4ef6-9d17-63f980a08d2a.html:63-89`, `165-180`, `995-1001`. | Improve motion if it still obeys reduced-motion and does not create horizontal overflow. | Replacing stripes/glass/dark scrollbars with source white header, blue arc decorations, or blue blog/editorial treatments (`/home/kaisar/Desktop/work/Kabi/lowl-website/mysite/templates/base.html:193-220`; `/home/kaisar/Desktop/work/Kabi/lowl-website/home/templates/home/home_page.html:41-45`). |

## 4. Shell, navigation, footer, and mobile quick actions

Must preserve:

- Fixed dark glass navigation at 80px height, dark border, `rgba(26,27,32,0.85)` blur, and desktop dropdowns using dark `bg-surface` panels with white/yellow hover/focus treatments (`mysite/templates/base.html:184-224`, `227-253`).
- Logo/wordmark treatment: yellow business short-name segment plus white `INLAND REPAIR` / `INLAND` suffix in the target shell (`mysite/templates/base.html:190-193`, `381-384`). Existing fallback text still contains LOWL and must be treated as identity debt, not a desired default (`mysite/templates/base.html:191`, `382`, `451`).
- Desktop links: Home, Services, Service Areas, Blog, About, Contact; service and city dropdowns are dark, scrollable, and no wider than viewport (`mysite/templates/base.html:196-258`).
- Language switcher EN/ES with active yellow pill and hreflang links (`mysite/templates/base.html:260-279`, `90-106`).
- Desktop CTA and phone remain high-contrast and keyboard-visible; booking links use `data-booking` behavior and target-owned `booking_url` (`mysite/templates/base.html:281-294`).
- Mobile menu uses a 44px toggle, `aria-expanded`, dark full-height sheet, language switcher, Book/Call buttons, and closes on item click (`mysite/templates/base.html:297-364`).
- Footer remains dark `bg-footer`, four-column on desktop with services/company/contact/address, yellow contact link, and dark bottom divider (`mysite/templates/base.html:375-454`).
- Mobile bottom bar remains fixed bottom, dark/glass, 64px high, with at least 44px touch targets for Call/Book (`mysite/templates/base.html:456-475`).

Interaction/accessibility checks later phases must run when touching shell/navigation:

- Desktop keyboard focus opens dropdowns or otherwise exposes menu links without mouse-only trapping.
- Mobile toggle changes `aria-expanded`, menu is reachable in tab order, and content is not covered by the quick bar.
- EN/ES switch preserves localized intent via `translation_url` and generated hreflang.
- Skip link remains first-focusable and visible on focus (`mysite/templates/base.html:178-182`).
- No horizontal overflow at 360, 390, 768, 1280, and 1440 widths.

Prohibited:

- Source white sticky header, gray desktop links, white dropdown panels, and source `site-header` style takeover (`/home/kaisar/Desktop/work/Kabi/lowl-website/mysite/templates/base.html:193-220`).
- Removing the mobile quick-action bar without an equivalent reviewed replacement.
- Replacing target nav/footer with LOWL's source loop structure without translating classes and identity.

## 5. Component and page-family treatment invariants

Homepage:

- Hero remains dark `bg-background`, uppercase Montserrat display, yellow-highlight city, diagonal stripe background, and two-column layout with dark booking widget (`home/templates/home/home_page.html:24-42`, `73-99`).
- Trust chips remain dark translucent pills with yellow circular icons (`home/templates/home/home_page.html:52-70`).
- Commercial/residential split remains dark/surface section with rounded imagery (`home/templates/home/home_page.html:104-155`).
- Services grid uses dark service cards, yellow hover/icon transitions, and empty state copy on dark background (`home/templates/home/home_page.html:157-180`).
- Process/pricing/brand/areas/reviews/FAQ/CTA sections must keep alternating dark/surface backgrounds, yellow accents, and high-contrast focus/hover states (`home/templates/home/home_page.html:182-448`).

Services pages:

- Service detail hero remains dark surface with stripe background, breadcrumbs, white H1, muted intro, and pill Book/Call CTAs (`services/templates/services/service_page.html:46-67`).
- Body/FAQ/brand chips/problem lists must stay dark/yellow: `.service-body`, dark cards, `bg-primary/10`, white section headers, 44px FAQ buttons (`services/templates/services/service_page.html:69-180`; `mysite/static/src/input.css:107-149`).
- Source service carousel behavior may be ported under parity row P09, but carousel panels/buttons/images must be translated away from source white/gray panels (source carousel evidence in `/home/kaisar/Desktop/work/Kabi/lowl-website/services/templates/services/service_page.html` matched white/gray carousel treatments in search output).

City/location pages:

- City detail hero remains dark surface with stripes, trust chips, city H1, Book Now in city CTA, and phone CTA (`locations/templates/locations/city_page.html:46-85`).
- Featured service cards, zip-code chips, localized process, FAQ accordions, and sidebar/CTA treatments must stay in target dark/yellow palette (`locations/templates/locations/city_page.html:87-180`).
- Location index page keeps dark hero stripe/arc accents, dark trust/value cards, and bottom CTA (`locations/templates/locations/locations_index_page.html` evidence from matched lines in search output).

Blog/static/search pages:

- Blog index retains dark hero, dark background, `article` cards with `bg-surface`, white headings, muted body, yellow empty/placeholder states, and dark/yellow pagination (`blog/templates/blog/blog_index_page.html:42-146`).
- Blog detail/static/contact/search templates must not import LOWL source's white editorial card system wholesale. Source blog evidence shows white headers/cards and blue gradients (`/home/kaisar/Desktop/work/Kabi/lowl-website/blog/templates/blog/blog_page.html` matched lines with `bg-white`, `text-gray`, `#1545ad/#3b76e8`).
- Static/contact forms should use dark `input-dark` or equivalent high-contrast field styling, target phone/address/email, and accessible error/success states; target static template currently already has dark sidebar/contact evidence in matched lines from `pages/templates/pages/static_page.html`.

Shared components:

- `.btn`, `.btn-primary`, `.btn-outline`, `.btn-accent`, `.container-site`, `.section-header`, `.service-card`, `.price-box`, `.booking-widget`, `.glow-dot`, `.trust-chip`, `.input-dark`, `.stripe-bg`, `.prose`, reduced-motion, and scrollbars in `mysite/static/src/input.css:24-280` are target component contracts.
- FAQ components use CSP-compatible Alpine `faqItem`, one-open-per-section coordination, `aria-expanded`, and `x-collapse` (`mysite/static/js/alpine-components.js:36-99`).
- Mobile navigation uses CSP-compatible `mobileNav` with `expandedStr` for ARIA (`mysite/static/js/alpine-components.js:13-34`).

## 6. Target-owned identity and brand-sensitive values

Identity values that later phases must preserve or make target-configurable:

| Value class | Target evidence | Rule |
|---|---|---|
| Business name | Current model default still says `LOWL Appliance Repair` (`home/models.py:200-205`), but project context and target migration require Inland Empire identity preservation (`.project.context.md:29-33`). | Later phases must remove LOWL fallback/default leakage or route it through target settings without importing LOWL production identity. Do not hardcode source LOWL identity into new templates/tests. |
| Contact phone | Target 0009 sets `+190****2506` / `(909) 975-2506` (`home/migrations/0009_update_contact_info_corona.py:37-55`); model currently matches (`home/models.py:213-225`). | Treat this as target-owned unless human supplies a replacement. Do not restore LOWL source phone or source tests' Lake Elsinore defaults. |
| Email | Target 0009 sets `inlandrepair.ca@gmail.com` (`home/migrations/0009_update_contact_info_corona.py:30-35`); model currently matches (`home/models.py:226`). | Preserve or parameterize as target setting. Do not copy `info@lowl.net` from source (`/home/kaisar/Desktop/work/Kabi/lowl-website/home/models.py:357`) or earlier target migration debt (`home/migrations/0002_update_defaults_real_business_info.py:22-27`). |
| Address/city/zip | Target 0009 sets `632 Shadybrook Ln`, Corona, CA, 92879 (`home/migrations/0009_update_contact_info_corona.py:13-28`, `57-60`); model currently matches (`home/models.py:228-235`). | Preserve target address/city/zip and target migration 0009. Source `409 N Langstaff St`, `Ste A`, Lake Elsinore, 92530 is not portable identity (`/home/kaisar/Desktop/work/Kabi/lowl-website/home/models.py:359-366`). |
| Booking URL/source | Model currently has LOWL booking URL/source defaults (`home/models.py:237-248`); context says booking URL/defaults are target-owned (`docs/design/inland-empire-design-contract.md:82-89`). | Treat current LOWL booking default as identity debt requiring Phase 03/05 cleanup. Preserve booking behavior (`data-booking`, UTM forwarding) but replace/default through target settings/env, not source production URL/source. |
| Analytics/GTM/verification | Template only emits GA/GTM/search verification when fields exist (`mysite/templates/base.html:26-32`, `149-158`, `503-510`); fields are blank-capable (`home/models.py:320-338`). | Port field/endpoint behavior only. Never copy source concrete tokens/IDs. Final QA should verify absence of LOWL IDs unless target-provided. |
| Metadata/structured data | JSON-LD uses `biz` settings for LocalBusiness/Organization/WebSite names, phone, email, address, logo/image, rating, sameAs (`home/templatetags/seo_tags.py:46-167`, `170-230`, `233-262`). | Structured data must reflect target business/settings. Review/rating schema requires provenance; suppress or relabel when evidence is unavailable. |
| Wagtail/site/cache names | Target still has LOWL strings in `WAGTAIL_SITE_NAME`, cache keys/prefixes, comments, fallback template copy (`mysite/settings/base.py` and `mysite/context_processors.py` matched search output). | Treat these as identity-sensitive debt for later phases. Behavior may remain, but public/admin-facing target identity should not say LOWL after final migration. |
| Logos/icons | Target static assets currently include `icon.svg`, `apple-touch-icon.png`, `og-default.png`, and home hero variants (`mysite/static/images/` listing). Design reference wordmark uses prototype LOWL/Inland labels (`design-bc900e36-8ca8-4ef6-9d17-63f980a08d2a.html:741`, `928`). | Do not copy LOWL logos/brand logos into runtime without provenance. Manufacturer logos may be used only as service capability/trademark references with asset provenance. |
| Locations/service areas | Target content emphasizes Inland Empire/Riverside County/Corona plus listed cities in home and location pages (`home/templates/home/home_page.html:269-290`; `locations/templates/locations/city_page.html:27-35`, `53-80`). | City/service content from LOWL may be behavior/content-seed input only after changing identity/copy to target truth and preserving target route structure. |

## 7. Content voice invariants

Tone to preserve:

- Direct, local-service, premium but practical: "same-day appliance repair", "certified technicians", "warranty included", "diagnostic waived with repair", "pay after work", "Riverside County", "Inland Empire", "Corona" where target settings say so. Evidence: home hero and process copy (`home/templates/home/home_page.html:33-50`, `182-238`), city/service metadata (`services/templates/services/service_page.html:27-35`; `locations/templates/locations/city_page.html:27-35`).
- CTA verbs: Book Now, Book a Repair, Check Availability, Call, Book Same-Day Repair, Book This Service. Evidence: base/home/service/city templates (`mysite/templates/base.html:291-294`, `456-470`; `home/templates/home/home_page.html:73-99`; `services/templates/services/service_page.html:58-64`; `locations/templates/locations/city_page.html:76-80`).
- Content should remain bilingual-ready using Django translation tags and existing EN/ES language switcher/hreflang (`mysite/templates/base.html:90-106`, `260-279`).

Claims requiring evidence or safe parameterization before final:

- `4.9 Rating`, `150+ reviews`, EPA/factory/OEM certification/training claims, same-day availability, 140 ZIP codes, no overtime, waived diagnostic, warranty terms, review cards, manufacturer-specific claims, and commercial capability. These appear in target templates but were not externally verified in this worksheet (`home/templates/home/home_page.html:52-70`, `120-150`, `241-331`, `333-443`). Later phases must either source-ground them, keep them as editable settings/copy under target approval, or suppress schema/claims that imply verified public facts.

Prohibited voice/copy changes:

- Public headings like "Contact LOWL Appliance Repair" from source static pages (`/home/kaisar/Desktop/work/Kabi/lowl-website/pages/templates/pages/static_page.html` matched line 52) must not enter target public templates.
- Do not relabel source LOWL reviews as Inland Empire reviews without direct evidence.
- Do not claim Railway deployment or production service status from repository changes alone.

## 8. Representative routes, page families, viewports, and evidence matrix

Final Phase 08 minimum matrix. Earlier UI phases must cover the affected subset.

| Family | English route | Spanish route expectation | Viewports | Required screenshots/evidence | Interaction checks |
|---|---|---|---|---|---|
| Home/global shell | `/` | `/es/` when translation exists | 1440x900, 1280x720, 768x1024, 390x844, 360x740 | Full-page screenshot plus above-the-fold crop showing dark/yellow hero, glass nav, dark booking widget, trust chips, footer, mobile bottom bar. | Nav dropdown keyboard/mouse, mobile menu toggle/close, language switcher, booking form submit URL, phone link, no horizontal overflow, console clean. |
| Services index | `/services/` | `/es/services/` when translation exists | 1440x900, 768x1024, 390x844, 360x740 | Dark service index hero/cards and CTAs; no source white/blue card takeover. | Service links reachable, CTA focus states, mobile quick bar not covering content. |
| Service detail | `/services/refrigerator-repair/` or first seeded service route | `/es/services/refrigerator-repair/` equivalent when seeded | 1440x900, 768x1024, 390x844, 360x740 | Dark service hero, service body, problem list, FAQ, related/brand/carousel states where present. | FAQ aria-expanded, carousel empty/one/many image keyboard/touch states, Book/Call links, JSON-LD service/FAQ target identity. |
| Service areas index | `/service-areas/` | `/es/service-areas/` when translation exists | 1440x900, 768x1024, 390x844, 360x740 | Dark service-area hub, city chips/cards, target Inland/Corona identity. | City links, CTA focus, no overflow. |
| City detail | `/service-areas/corona-ca/` or first seeded city route | `/es/service-areas/corona-ca/` equivalent when seeded | 1440x900, 768x1024, 390x844, 360x740 | Dark city hero, trust chips, zip chips, service cards, FAQ, sidebar/CTA. | FAQ toggle, city-specific Book/Call, structured data uses target business and city. |
| Blog index | `/blog/` | `/es/blog/` when translated posts exist | 1440x900, 768x1024, 390x844, 360x740 | Dark blog hero, dark cards, pagination states, empty state if no posts. | Pagination, article links, no source white editorial page takeover. |
| Blog detail | first seeded article route | localized article route when exists | 1440x900, 768x1024, 390x844, 360x740 | Dark article shell/card/prose treatments; target author/business metadata. | TOC/share/related/CTA if ported, schema Article identity, keyboard focus. |
| Static/contact | `/contact/`, `/about-us/` | `/es/contact/`, `/es/about-us/` when exists | 1440x900, 768x1024, 390x844, 360x740 | Dark static hero/form/contact cards with target phone/email/address. | Form empty/error/success, focus order, labels, target email/phone, no LOWL public copy. |
| Search | `/search/?q=washer`, `/search/?q=`, `/search/?q=unlikely-no-results-term` | `/es/search/?q=lavadora` if localized search route exists | 1440x900, 768x1024, 390x844, 360x740 | Dark search input/results/no-results states. | Search submit, keyboard focus, result links, no layout shift/overflow. |
| SEO machine endpoints | `/robots.txt`, `/sitemap.xml`, `/image-sitemap.xml`, `/llms.txt`, `/llms-full.txt`, optional `/BingSiteAuth.xml` only when configured | Non-localized unless implementation intentionally localizes | n/a | Raw response captures and schema/URL assertions. | No concrete LOWL domain/token; correct target host; safe empty/disabled states. |
| Tracking/admin (when Phase 03 ports) | Wagtail admin tracking dashboard paths from manifest | Admin locale as supported | 1440x900, 1280x720, 768x1024 | Admin-only dashboard/session/detail/partials screenshots or render evidence. | Permission checks, no public leakage, privacy-safe fields, CSV export if ported. |

Viewport contract:

- Desktop: 1440x900 and 1280x720.
- Tablet portrait: 768x1024.
- Modern mobile: 390x844.
- Small mobile: 360x740.
- Every visual screenshot must include evidence that dark background/surfaces dominate, yellow is accent/CTA, no LOWL blue/white global takeover, no horizontal overflow, no hidden primary content behind fixed nav/bottom bar, and no console/network errors for local static assets.

## 9. Phase-specific invariant handoffs

Phase 04 content/localization/assets:

- Use source seed commands, blog assets, service/city assets, brand logos, and Spanish catalogs only as behavior/source-material inputs. Do not bulk-copy or publish assets without provenance.
- Brand/logo assets require `SOURCES.md` or equivalent provenance; manufacturer names/logos are allowed only as service capability/trademark references, not as owned brand identity.
- Reviews/rating cards require direct source evidence before schema output. If evidence is unavailable, visible testimonial-like content must be relabeled or schema suppressed.
- Spanish content must say target/Inland/Corona identity, not LOWL production identity; route-language behavior must preserve `hreflang` and localized page intent.

Phase 05 shell/home/shared interactions:

- Merge nav/footer/home/booking/ZIP/tracking-client hooks into existing dark shell and home geometry. Do not wholesale replace `mysite/templates/base.html`, `home/templates/home/home_page.html`, `tailwind.config.js`, or `mysite/static/src/input.css` with source versions.
- Target global shell must retain dark glass nav, dropdowns, footer, mobile menu, mobile quick bar, skip link, EN/ES switcher, pill CTAs, dark booking widget, trust chips, and diagonal stripes.
- Booking/UTM behavior must use target-owned URL/source defaults and must not leak `lowl` or `lowl-booking-production` in final public JS/defaults.

Phase 06 secondary page families:

- Service/city/blog/static/search template behavior can be ported, but every source white/blue/Satoshi class must be translated to target dark/yellow tokens.
- Any carousel, FAQ, pagination, search, contact form, sidebar, callout, review, or related-card treatment must pass desktop/mobile a11y and overflow checks.
- Page-specific SEO/metadata/schema must use target business/settings and not LOWL fallback strings.

Phase 08 final verification:

- Re-run the complete route/viewport matrix above after all implementation phases.
- Explicitly search final target runtime/code for forbidden visual tokens and identity strings: `#1545ad`, `#3b76e8`, `Satoshi`, `info@lowl.net`, `409 N Langstaff`, `Lake Elsinore` as default identity, `lowl-booking-production`, `booking_source default='lowl'`, source analytics IDs/tokens/domains, and public `LOWL Appliance Repair` fallbacks.
- Fail the gate if LOWL blue/white/Satoshi has become global public UI or if LOWL production identity appears in public metadata/schema/defaults without a documented target-owned reason.

## 10. Acceptable versus prohibited changes summary

Acceptable:

- Add fields/models/migrations/tests in target-native sequence.
- Add or adapt templates/components that map to target tokens and accessibility conventions.
- Add source-derived behavior behind target settings/env with safe defaults.
- Add assets only with provenance and target-appropriate use.
- Update copy to target truth; parameterize claims that lack source evidence.
- Update generated CSS only after intentional source CSS/Tailwind/template changes and proof of dark/yellow contract.

Prohibited:

- LOWL blue/white/Satoshi visual takeover.
- Wholesale overwrites of target design merge surfaces from LOWL.
- Concrete LOWL production identity: business name, address, phone, email, booking URL, booking source, analytics/GTM/search verification tokens, CallRail swap URL, domains, remote/Railway identifiers, admin passwords, database/media/log/runtime artifacts.
- Importing source `.git`, `.hermes`, QA archives, Trello/Google exports, credentials, local DB/media/logs, or deployment artifacts.
- Claiming source reviews, ratings, certifications, review counts, or business facts as target facts without evidence.
- Starting Phase 02 or writing product code from this evidence task.

## 11. Quick checklist for downstream reviewers

A downstream UI/content change is acceptable only if reviewers can answer yes to all:

1. Does it still look like the Inland Empire dark/yellow site at required desktop/tablet/mobile widths?
2. Are Montserrat/Inter/Sacramento still the global typography and Satoshi absent from global public UI?
3. Are cards/buttons/forms/nav/footer/mobile bar still dark/yellow/pill/rounded according to target tokens?
4. Are public names, contact details, booking URLs, metadata, schema, analytics, and verification values target-owned or blank/configured, not source LOWL production values?
5. Are claims/reviews/source-sensitive copy either verified, editable target-owned content, or suppressed from schema?
6. Are English and Spanish routes preserving localized intent and hreflang?
7. Are interaction states keyboard-accessible with 44px touch targets on mobile and no overflow?
8. Are source/captured paths cited for every behavior imported and target paths cited for every design/identity invariant preserved?
