# Schema and migration sequencing conflict audit

Task: `t_75808fac`
Run: `inland-lowl-parity-20260731`
Target repo: `/home/kaisar/Desktop/work/Kabi/inland-empire-website`
Read-only source repo: `/home/kaisar/Desktop/work/Kabi/lowl-website`
Captured source baseline: `.hermes/sources/lowl-parity-20260731/`

This is evidence-only. I did not create migrations, run Django commands, install dependencies, edit product code, or mutate LOWL. The only new artifact is this report under `docs/parity/evidence/`.

## Inputs inspected

Governance and phase inputs:

- `.project.context.md`
- `.hermes/plans/master-plan.md`
- `.hermes/plans/phase-status.md`
- `.hermes/prompts/phase-02.md`
- `.hermes/sources/lowl-parity-20260731/README.md`
- `docs/parity/lowl-feature-parity.md`
- `docs/design/inland-empire-design-contract.md`
- `docs/parity/evidence/immutable-baseline-report.md`

Code/evidence inspected read-only:

- Target and source migrations under `home/migrations/`, `services/migrations/`, `locations/migrations/`, `blog/migrations/`, `pages/migrations/`, and source `tracking/migrations/`.
- Target and source `home/models.py`, `services/models.py`, `locations/models.py`, `blog/models.py`, `mysite/settings/base.py`.
- Source tracking model/admin hook files: `tracking/models.py`, `tracking/migrations/0001_initial.py`, `tracking/wagtail_hooks.py`.
- Source and target management-command inventories under `home/management/commands/`, `services/management/commands/`, and `blog/management/commands/`.
- Source/target tests searched for schema/admin assertions around `public_h1`, `photo_carousel`, `callrail`, `main_nav_order`, `footer_company_order`, `reading_time`, `headings`, `TrackSession`, and `TrackEvent`.

Confirmed with a read-only file comparison command that these common migrations are byte-identical in source and target: home `0001` through `0008`, services `0001` through `0002`, locations `0001` through `0003`, blog `0001` through `0003`, and pages `0001`.

## Hard constraints that drive sequencing

1. Target `home/migrations/0009_update_contact_info_corona.py` is authoritative target history and target identity. It depends on target/source-common `home.0008_add_opening_closing_time` and changes target `SiteSettings` defaults for address, city, email, phone, display phone, and ZIP.
2. Source `home/migrations/0009_add_callrail_swap_url.py` also depends on `home.0008_add_opening_closing_time`, but it adds `SiteSettings.callrail_swap_url`. Directly copying it to the target would create two `home.0009` leaves from `0008` or overwrite target history.
3. Source `home.0010` through `home.0014` depend linearly on the source `home.0009`. Their semantics must be replayed after target `home.0009`, not copied by filename.
4. Phase 02 may add schema/model/admin foundations, but must not implement request/platform APIs, tracking ingestion, middleware/context processors, templates/CSS/JS, content seeding, runtime assets, Docker/Railway, commits, or LOWL writes.
5. Defaults are identity-bearing. Source phone/address/email/booking defaults must not replace target Corona/Inland values. Source model behavior can be ported only with target-owned defaults or empty/configurable values.

## Dependency-aware migration map

### Home app

| Source migration | Source dependency and semantics | Target state | Disposition | Phase 02-safe target strategy |
|---|---|---|---|---|
| `home.0001_initial` | Initial `HomePage` and `SiteSettings`; common baseline. | Byte-identical target migration exists. | `already_equivalent` | No action. Treat as shared base. |
| `home.0002_update_defaults_real_business_info` | Alters target/source-common business/contact defaults. | Byte-identical target migration exists. | `already_equivalent` | No action. Existing defaults are then intentionally overridden later by target `0009`. |
| `home.0003_warranty_text_and_address` | Adds/adjusts warranty/address fields. | Byte-identical target migration exists. | `already_equivalent` | No action. |
| `home.0004_change_booking_source_default` | Alters booking source default. | Byte-identical target migration exists. | `already_equivalent` | No action; later phases must keep target-owned booking behavior. |
| `home.0005_add_seo_fields_to_sitesettings` | Adds SEO/analytics/config fields. | Byte-identical target migration exists. | `already_equivalent` | No action. |
| `home.0006_add_search_verification_fields` | Adds search verification fields. | Byte-identical target migration exists. | `already_equivalent` | No action; concrete verification values are forbidden. |
| `home.0007_add_social_profile_urls` | Adds social profile URL fields. | Byte-identical target migration exists. | `already_equivalent` | No action. |
| `home.0008_add_opening_closing_time` | Adds opening/closing time fields. | Byte-identical target migration exists. | `already_equivalent` | No action. This is the semantic join point. |
| Source `home.0009_add_callrail_swap_url` | Depends on `home.0008`; adds `SiteSettings.callrail_swap_url` URLField with blank allowed. | Target already has a different `home.0009_update_contact_info_corona` from the same dependency. | `adapt_to_target_identity` | Replay as target `home.0010_add_callrail_swap_url`, dependency `("home", "0009_update_contact_info_corona")`. Keep blank default and env/config-only semantics; do not copy any CallRail URL value. |
| Target-only `home.0009_update_contact_info_corona` | Depends on `home.0008`; alters `address_line1`, `address_line2`, `city`, `email`, `phone`, `phone_display`, `zip_code` to Corona/Inland defaults. | No source counterpart. | `target_supersedes` | Preserve immutable. All later target home migrations depend on this file. Do not rename, squash, delete, or replace it. |
| Source `home.0010_alter_sitesettings_phone_and_more` | Depends on source `home.0009`; changes `phone` and `phone_display` defaults to blank and help text for auto-generation. | Target `home.0009` intentionally set nonblank Inland phone/display defaults. Source model also adds `_format_phone_for_display()` and `save()` auto-sync behavior. | `adapt_to_target_identity` | Do not replay source blank defaults verbatim. If Phase 02 ports auto-format behavior, use a target-native migration only when model field definitions actually change, and preserve existing target values/defaults unless a test proves empty defaults are required for fresh deploy safety. Add upgrade tests ensuring customized target phone/display values are not blanked. |
| Source `home.0011_homepage_areas_heading_homepage_areas_subheading_and_more` | Depends on source `home.0010`; adds editable `HomePage` section fields (`hero_title`, `hero_subtitle`, `commercial_*`, `services_heading`, `process_*`, `pricing_*`, `brands_*`, `areas_*`, `testimonials_heading`, `faq_heading`) and runs `seed_spanish_homepage_fields` for Spanish pages with `noop_reverse`. | Target `HomePage` lacks these editable fields; source RunPython is content seeding and only has a noop reverse. | `adapt_to_target_identity` | Replay schema as target `home.0011_homepage_section_fields`, dependency `home.0010_add_callrail_swap_url`. Use target-safe defaults or blank fields plus template fallbacks; do not execute Spanish/content seeding in Phase 02. Move source `seed_spanish_homepage_fields` semantics to Phase 04 localization commands. Record the data migration as intentionally not copied because it is content/identity work and partly irreversible. |
| Source `home.0012_configurable_navigation_order` | Depends on source `home.0011`; adds `SiteSettings.main_nav_order` and `footer_company_order` with comma-separated defaults. | Target lacks these fields; target context processor lacks source nav-order behavior. | `adapt_to_target_design` | Replay schema as target `home.0012_sitesettings_navigation_order`, dependency `home.0011_homepage_section_fields`. Keep values target-owned. The context-processor/menu behavior belongs to Phase 03/05, but fields/panels can be Phase 02 foundations. |
| Source `home.0013_alter_sitesettings_main_nav_order` | Depends on source `home.0012`; changes `main_nav_order` default to include `brands`. | Target has no field yet. | `adapt_to_target_design` | Prefer squashing into target `home.0012_sitesettings_navigation_order` with the final target-approved default if `brands` is a Phase 04/05 capability. If reviewers want one-source-migration-per-target-migration traceability, create target `home.0013_alter_sitesettings_main_nav_order`, but it is not semantically required when the field is first introduced with the final default. |
| Source `home.0014_repair_legacy_main_nav_order` | Depends on source `home.0013`; reversible `RunPython` updates rows exactly equal to old default to include `brands`. | Target cannot have legacy values for a field that does not exist before Phase 02. | `adapt_to_target_design` | Do not create this data migration if target `0012` adds the field with the final default. If a staged strategy creates old default first, then replay as a reversible target `0014_repair_legacy_main_nav_order` after target `0013`; it must only update rows equal to the old default and must be proven reversible. |

Recommended home numbering is therefore:

1. Keep target `home.0009_update_contact_info_corona` unchanged.
2. Add target `home.0010_add_callrail_swap_url`, depending on target `0009`.
3. Add target `home.0011_homepage_section_fields`, depending on target `0010`; schema only, no Spanish RunPython seed.
4. Add target `home.0012_sitesettings_navigation_order`, depending on target `0011`; include the final target-approved nav/footer field defaults and admin panels.
5. Do not create target `0013`/`0014` unless Phase 02 intentionally stages the old nav default first. If created, they must follow target `0012` and be reversible/row-constrained.

### Services app

| Source migration | Source dependency and semantics | Target state | Disposition | Phase 02-safe target strategy |
|---|---|---|---|---|
| `services.0001_initial` | Initial service index/detail/orderable related services. | Byte-identical target migration exists. | `already_equivalent` | No action. |
| `services.0002_add_service_featured_image` | Adds `ServicePage.featured_image`. | Byte-identical target migration exists. | `already_equivalent` | No action. |
| `services.0003_servicepage_public_h1` | Depends on `services.0002`; adds blank `ServicePage.public_h1`. Source tests assert custom public H1, blank fallback, and admin panel exposure. | Target lacks `public_h1`. | `adapt_to_target_design` | Copy/replay as target `services.0003_servicepage_public_h1` because target has no numbering collision. Preserve blank field and fallback behavior. |
| `services.0004_service_photo_carousel_foundation` | Depends on `services.0003` and `wagtailimages.0027_image_description`; adds `ServicePage.photo_carousel_title` and creates `ServicePhotoCarouselImage` orderable with `ParentalKey(... related_name="photo_carousel_images")`, `image` FK, `ordering=["sort_order"]`. Captured untracked copy is identical to live source file. Source tests assert panels, image relation, empty/single/multiple behavior, and ordering. | Target lacks these fields/model. | `adapt_to_target_design` | Replay as target `services.0004_service_photo_carousel_foundation` after target `0003`; preserve `wagtailimages.0027` dependency. Template/carousel UI rendering belongs later, but schema and admin panels are Phase 02. |

### Locations app

| Source migration | Source dependency and semantics | Target state | Disposition | Phase 02-safe target strategy |
|---|---|---|---|---|
| `locations.0001_initial` | Initial locations index/city/orderables. | Byte-identical target migration exists. | `already_equivalent` | No action. |
| `locations.0002_initial` | Common Wagtail locale/page dependency continuation. | Byte-identical target migration exists. | `already_equivalent` | No action. |
| `locations.0003_add_city_featured_image` | Adds `CityPage.featured_image`. | Byte-identical target migration exists. | `already_equivalent` | No action. |
| `locations.0004_citypage_public_h1` | Depends on `locations.0003`; adds blank `CityPage.public_h1`. Source tests assert custom H1, blank fallback, and admin panel exposure. | Target lacks `public_h1`. | `adapt_to_target_design` | Replay as target `locations.0004_citypage_public_h1`; no numbering collision. Static city image mapping from `locations/city_assets.py` is not migration work and belongs to Phase 04/06. |

### Blog app

| Source migration | Source dependency and semantics | Target state | Disposition | Phase 02-safe target strategy |
|---|---|---|---|---|
| `blog.0001_initial` | Initial blog index/page with StreamField and image relation. | Byte-identical target migration exists. | `already_equivalent` | No action. |
| `blog.0002_add_blog_tags` | Depends on `blog.0001` and `taggit.0006...`; creates `BlogPageTag` and adds `ClusterTaggableManager`. | Byte-identical target migration exists and target model already has tags/panel. | `already_equivalent` | No action. |
| `blog.0003_add_blog_author_name` | Depends on `blog.0002`; adds `BlogPage.author_name`. | Byte-identical target migration exists and target model already has author panel. | `already_equivalent` | No action. |

Source `blog/models.py` adds non-schema `BlogPage.reading_time` and `BlogPage.headings` properties beyond target. Those need no migration; they can be copied as portable model behavior in Phase 02 or later page rendering work, with tests. Source `blog/content_utils.py` and blog seeding/repair commands are `copy_portable`/`adapt_to_target_identity` but are not migration sequencing blockers; command behavior belongs Phase 04.

### Pages app

| Source migration | Source dependency and semantics | Target state | Disposition | Phase 02-safe target strategy |
|---|---|---|---|---|
| `pages.0001_initial` | Initial `StaticPage`. | Byte-identical target migration exists. | `already_equivalent` | No action for Phase 02. Contact/VAPI/rate-limit behavior in source `pages` belongs Phase 03. |

### Tracking app

| Source migration | Source dependency and semantics | Target state | Disposition | Phase strategy |
|---|---|---|---|---|
| `tracking.0001_initial` | New app with `TrackSession` and `TrackEvent`; indexes on session, conversion/time, UTM source, event/time; no dependencies. Source settings install `tracking` and add tracking config/context processor. Source Wagtail hook registers tracking dashboard URLs/menu. | Target has no `tracking` app, no installed-app entry, no migration path. | `adapt_to_target_identity` | Not Phase 02. Phase 03 should add target `tracking.0001_initial` with privacy-safe defaults, app registration, tests for models/collection/HMAC/rate limits/admin routes/retention, and no source analytics IDs/secrets. |

## Model/admin registration audit

- There are no `admin.py` registrations in either source or target app trees inspected. Admin/editability is expressed through Wagtail `content_panels`, `edit_handler`, `@register_setting`, and source `tracking/wagtail_hooks.py`.
- `HomePage`: target has no editable section fields/panels. Source adds `hero_*`, commercial, services/process/pricing/brand/area/testimonials/FAQ fields and grouped Wagtail panels. Phase 02 should port fields/panels but not source content claims or Spanish seeding.
- `SiteSettings`: both target and source are registered with `@register_setting`. Source adds `callrail_swap_url`, nav/footer order fields, `HelpPanel` guidance, phone auto-formatting, and a Navigation tab. Target has Corona/Inland contact defaults from target `0009`; Phase 02 must preserve them.
- `ServicePage`: source adds `public_h1`, `photo_carousel_title`, `ServicePhotoCarouselImage`, and corresponding FieldPanel/InlinePanel. Target lacks them. These are Phase 02 schema/admin foundations.
- `CityPage`: source adds `public_h1` and a panel. Target lacks it. Static city hero image lookup is non-schema and belongs later.
- `BlogPage`: target already has source schema for tags and `author_name`; source-only `reading_time`/`headings` are non-schema methods. No admin registration collision.
- `Tracking`: source Wagtail hook registers admin URLs/menu (`tracking_dashboard`, `tracking_session_detail`, `tracking_export_csv`). Target has no tracking app. This is Phase 03 platform/admin-dashboard work, not a Phase 02 dependency.

## Startup/seeding and data-migration risks

- Source `home.0011` contains `RunPython(seed_spanish_homepage_fields, noop_reverse)`. It writes Spanish page content and has a no-op reverse. Treat this as content/localization seeding, not Phase 02 schema. Replaying it in Phase 02 would mix schema with identity-bearing content and would not be cleanly reversible.
- Source `home.0014` is reversible and only repairs old `main_nav_order` rows. In the target, that field does not yet exist, so the safest strategy is to add it once with the final target-approved default and avoid a redundant data migration. If staged for traceability, constrain updates to rows equal to the old default and prove reverse behavior.
- Source management commands are richer than target (`create_brand_pages.py`, `repair_card8_menu_routes.py`, SEO fix commands, blog populate/repair/spanish commands, `add_brand_faqs.py`, tracking cleanup). These commands assume fields/routes/content families not all present in target. They belong mostly to Phase 04, with Phase 03 owning tracking cleanup/platform and Phase 05/06 owning UI/template integration.
- Source and target `setup_pages.py` are both content-heavy and include brand/OEM/same-day/service claims. Phase 02 must not run or port command content. Later phases must adapt claims to target evidence and preserve Inland identity.
- Target existing rows/customized settings can be damaged by source `home.0010` blank phone defaults or by unguarded nav repair. Phase 02 needs explicit upgrade tests for customized `SiteSettings` values, especially phone/display phone, address, email, booking URL/source, and nav order.

## Conflict classification by parity family

| Family | Disposition | Reason and owner |
|---|---|---|
| P02 Django/Wagtail shared scaffold | `exclude_runtime_or_audit` | Shared filenames are not equivalence; preserve target settings/module identity and migration graph. Phase 02 should touch only schema/admin foundations. |
| P03/P04 HomePage and SiteSettings fields | `adapt_to_target_design` / `adapt_to_target_identity` | Source adds portable fields, while source defaults/content include LOWL identity. Phase 02 must port schema with target-owned defaults and value-preservation tests. |
| P05 Home migration-number collision | `adapt_to_target_identity` | Target `home.0009_update_contact_info_corona` remains immutable; source `home.0009` and successors replay as target `0010+`. |
| P08/P09 Service public H1/carousel | `adapt_to_target_design` | Schema/orderable fields are portable, but public template/carousel styling must stay target dark/yellow in later phases. |
| P11 Location/city public H1/images | `adapt_to_target_design` | `public_h1` is Phase 02 schema; city asset mapping/provenance and templates belong Phase 04/06. |
| P06 Blog admin/content utilities | `copy_portable` | Target already has tag/author migrations; source non-schema helpers can be copied with tests. Templates stay target design. |
| P12/P13 Static pages/contact/VAPI | `adapt_to_target_identity` | No migration conflict; VAPI/contact/rate-limit behavior is Phase 03. |
| P39-P46 startup/content commands | `adapt_to_target_identity` | Commands depend on schema and are content/seed work; Phase 04. |
| P20 navigation/context processor ordering | `adapt_to_target_design` | SiteSettings nav/footer fields can be Phase 02; context processor and UI shell behavior belong Phase 03/05. |
| P15-P18 tracking models/APIs/admin/cleanup | `adapt_to_target_identity` for models/APIs/admin, `copy_portable` for cleanup mechanics | New source-only app; target `tracking.0001` belongs Phase 03, with privacy/identity gates. |
| P48 source tests as specs | `copy_portable` with adaptations | Use source tests for behavior shape, but replace source identity/default assertions and keep RED/GREEN evidence. |

## Phase 02 validation guidance

Minimum checks Phase 02 should run after implementation, in addition to the phase prompt's full list:

1. Capture target migration leaves before and after implementation. Expected target app leaves after the recommended schema work: `home.0012_sitesettings_navigation_order` (or `home.0014_repair_legacy_main_nav_order` if staged), `services.0004_service_photo_carousel_foundation`, `locations.0004_citypage_public_h1`, existing `blog.0003_add_blog_author_name`, existing `pages.0001_initial`.
2. `python manage.py makemigrations --check --dry-run` must report no drift after model edits.
3. Fresh database migration test must traverse the target graph with exactly one `home.0009`: target `home.0009_update_contact_info_corona`.
4. Baseline-upgrade migration test must prove target `SiteSettings` rows keep Corona/Inland/custom values through source-derived field additions. Explicitly assert no blanking of target phone/display phone, address, email, booking URL/source, or business name.
5. Wagtail panel tests should assert: HomePage section panels; SiteSettings CallRail and Navigation panels; ServicePage `public_h1`, `photo_carousel_title`, `photo_carousel_images` InlinePanel; CityPage `public_h1`; BlogPage tags/author still editable; optional BlogPage `reading_time`/`headings` behavior if ported.
6. Source-derived data migrations must be classified in evidence: Spanish homepage seeding deferred to Phase 04; nav repair either omitted as not applicable or added as a reversible constrained migration.
7. Run focused app tests for home/services/locations/blog and full suite as required by Phase 02, but do not run any Django command in LOWL.
8. Source-read-only verification should use the captured baseline artifacts and read-only status/checksum comparison; any external source drift must be explained before Phase 02 proceeds.

## Blockers and handoff

No blocker prevents Phase 02 sequencing if the target strategy above is followed. The main review-sensitive decision is whether to compress source `home.0012` through `home.0014` into one target nav-order schema migration with the final default, or preserve one-source-migration-per-target-migration traceability. I recommend the compressed target-native strategy because the target has no pre-existing nav-order field and does not need a legacy repair data migration.

Non-schema dependencies intentionally mapped out of Phase 02:

- Tracking app settings, collection APIs, HMAC booking webhook, admin dashboard, retention cleanup: Phase 03.
- Context processors/navigation rendering, booking/UTM/VAPI/SEO endpoints/security headers: Phase 03 and Phase 05 as assigned by the parity matrix.
- Spanish content, management-command seed/repair behavior, brand/service/city/blog assets and claims: Phase 04.
- Public templates/CSS/JS/browser evidence for homepage/service/city/blog/search/contact: Phases 05 and 06.
- Deployment/Railway/CI: Phase 07.

## Verification performed for this audit

- `git status --short --branch` in target: branch `main...origin/main`, modified `.gitignore`, untracked `.hermes/`, `.project.context.md`, and `docs/`.
- Read-only common-migration comparison: home `0001`-`0008`, services `0001`-`0002`, locations `0001`-`0003`, blog `0001`-`0003`, and pages `0001` are byte-identical between source and target.
- Source `services/migrations/0004_service_photo_carousel_foundation.py` and captured untracked baseline copy under `.hermes/sources/lowl-parity-20260731/untracked-product/` were inspected and are semantically the same file content for this audit.
- No Django commands, migrations, installs, LOWL Git mutation, target product-code edits, commits, pushes, or deployments were performed.
