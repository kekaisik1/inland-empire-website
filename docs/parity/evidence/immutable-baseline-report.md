# Immutable source and target baseline evidence

Task: `t_a9af4b60`
Run: `inland-lowl-parity-20260731`
Target repo: `/home/kaisar/Desktop/work/Kabi/inland-empire-website`
Read-only source repo: `/home/kaisar/Desktop/work/Kabi/lowl-website`
Captured source baseline: `.hermes/sources/lowl-parity-20260731/`

This report is evidence-only. It does not implement product code and does not mutate LOWL.

## Context read

Read before writing this report:

- `.project.context.md`
- `.hermes/plans/master-plan.md`
- `.hermes/plans/phase-status.md`
- `.hermes/sources/lowl-parity-20260731/README.md`
- `.hermes/sources/lowl-parity-20260731/source-head.txt`
- `.hermes/sources/lowl-parity-20260731/source-product-status.txt`
- `.hermes/sources/lowl-parity-20260731/source-product-files.txt`
- `.hermes/sources/lowl-parity-20260731/source-product-sha256.txt`
- `.hermes/sources/lowl-parity-20260731/source-product-working-tree.patch.sha256`
- `.hermes/sources/lowl-parity-20260731/target-design-sha256.txt`
- `docs/parity/lowl-feature-parity.md`
- `docs/design/inland-empire-design-contract.md`
- prior excluded recovery evidence at `.hermes/runs/inland-lowl-parity-20260731/recovery/goal-autodecompose-20260731T073630/moved-target/docs/parity/evidence/source-target-inventory.md`

Checked and not present in the target root: `AGENTS.md`, `CLAUDE.md`, `CODEX.md`, `GEMINI.md`, `.cursorrules`.

## Target Git baseline

Read-only commands used:

- `git status --short --branch`
- `git remote -v`
- `git rev-parse HEAD`
- `git branch --show-current`
- `git log --oneline --decorate --max-count=5 --all`

Observed target state:

- Branch: `main`
- Remote: `origin git@github.com:kekaisik1/inland-empire-website.git` for fetch and push
- HEAD: `f97ebeb835925b66659fa57f8a9d19759ee83341`
- Recent history: `f97ebeb (HEAD -> main, origin/main) feat: initial commit — Wagtail CMS site for Inland Empire services`
- Status: `## main...origin/main`, with modified `.gitignore` and untracked `.hermes/`, `.project.context.md`, and `docs/`
- Tracked target product tree count from `git ls-files | wc -l`: 106

## Source Git baseline and drift

Read-only commands used in LOWL:

- `git status --short --branch`
- `git remote -v`
- `git rev-parse HEAD`
- `git branch --show-current`
- `git log --oneline --decorate --max-count=5 --all`
- `git show --no-patch --format='%H %s' 4bdb0a342c47da223588897f56ab7d11c50c44f4`
- `sha256sum --check /home/kaisar/Desktop/work/Kabi/inland-empire-website/.hermes/sources/lowl-parity-20260731/source-product-sha256.txt`

Observed source state:

- Branch: `main`
- Remote: `origin https://github.com/kekaisik1/lowl-website.git` for fetch and push
- HEAD: `4bdb0a342c47da223588897f56ab7d11c50c44f4`
- Captured commit resolves in source as `4bdb0a342c47da223588897f56ab7d11c50c44f4 fix: clean LOWL service JSON-LD for GSC`
- Recent history starts with `4bdb0a3 (HEAD -> main, origin/main) fix: clean LOWL service JSON-LD for GSC`
- Full live source status includes workflow/audit drift under `.hermes/**`, `.project.context.md`, `.claude/**`, archived prompts/reports/QA docs, plus the captured product dirtiness.
- Product drift against the immutable capture is absent: `sha256sum --check .../source-product-sha256.txt` exited 0 and reported 356 OK lines with 0 stderr lines.
- Filtered live product status exactly matches `.hermes/sources/lowl-parity-20260731/source-product-status.txt`; the status diff exited 0.

Drift conclusion: live LOWL has non-product workflow/audit drift outside the captured product baseline. The live source product paths, product status, and product checksums still match the capture. If source product drift appears later, downstream workers must treat the captured artifacts plus read-only `git show` for `4bdb0a342c47da223588897f56ab7d11c50c44f4` as authoritative, not the live dirty working tree.

## Captured baseline artifacts

Checksum/count commands used in the target:

- `wc -l .hermes/sources/lowl-parity-20260731/source-product-files.txt .hermes/sources/lowl-parity-20260731/source-product-sha256.txt .hermes/sources/lowl-parity-20260731/source-product-status.txt`
- `sha256sum .hermes/sources/lowl-parity-20260731/source-product-working-tree.patch .hermes/sources/lowl-parity-20260731/source-product-status.txt`

Observed artifact facts:

- `source-product-files.txt`: 356 lines
- `source-product-sha256.txt`: 356 lines
- `source-product-status.txt`: 20 lines
- `source-product-working-tree.patch` SHA-256: `d55202656bb6217798b20ab9ebc8ff0626c9ee36370aaf00be0bf85545d1b2c2`
- `source-product-status.txt` SHA-256: `652e053af0983fc81a613cd76bfdba58f9e783638a50e24acc2278c014926690`
- Patch checksum matches `.hermes/sources/lowl-parity-20260731/source-product-working-tree.patch.sha256` and the README.
- Status checksum matches the README.

Captured working-tree patch accounting:

- 17 modified tracked product files are represented in `source-product-status.txt`: `home/brand_assets.py`, `home/high_end_brand_seed_data.py`, `home/management/commands/setup_spanish_pages.py`, `home/service_seed_data.py`, `home/tests.py`, `locale/es/LC_MESSAGES/django.mo`, `locale/es/LC_MESSAGES/django.po`, `locations/templates/locations/city_page.html`, `locations/tests.py`, `mysite/static/css/output.css`, `mysite/static/images/brand-logos/SOURCES.md`, `mysite/static/js/alpine-components.js`, `mysite/templates/base.html`, `mysite/urls.py`, `services/models.py`, `services/templates/services/service_page.html`, `services/tests.py`.
- 3 untracked product files are represented both in `source-product-status.txt` and copied under `untracked-product/`: `mysite/static/images/brand-logos/monogram.svg`, `mysite/static/images/brand-logos/wolf.svg`, `services/migrations/0004_service_photo_carousel_foundation.py`.

## Source manifest vs target tracked tree

Read-only/diff commands used:

- `git ls-files | wc -l`
- `git ls-files | sort > /tmp/inland-target-files.txt`
- `sort .hermes/sources/lowl-parity-20260731/source-product-files.txt > /tmp/lowl-source-files.txt`
- `comm -12 /tmp/lowl-source-files.txt /tmp/inland-target-files.txt | wc -l`
- `comm -23 /tmp/lowl-source-files.txt /tmp/inland-target-files.txt | wc -l`
- `comm -13 /tmp/lowl-source-files.txt /tmp/inland-target-files.txt | wc -l`

Observed reconciliation:

- Captured source product paths: 356
- Target tracked product paths: 106
- Common paths by exact manifest string: 105
- Source-only captured product paths: 251
- Target-only tracked product paths: 1
- Target-only tracked product path: `home/migrations/0009_update_contact_info_corona.py`

Manifest-level coverage of all 356 captured paths is already locked in `docs/parity/lowl-feature-parity.md` and the Phase 01 inventory evidence:

- 13 repository/deploy/build/runtime contract paths: P01, P02, P33, P49, P50, P51.
- 16 `blog/**` paths: P06, P31, P43, P48.
- 38 `home/**` paths: P03, P04, P05, P10, P20, P23, P28, P38-P40, P42, P45, P47, P48.
- 40 `img/**` paths: P35, P36, P43.
- 2 `locale/es/LC_MESSAGES/**` paths: P41.
- 14 `locations/**` paths: P11, P30, P36, P44, P48.
- 186 `mysite/**` paths: P19-P28, P33-P38, P49.
- 9 `pages/**` paths: P12, P13, P32, P48.
- 5 `search/**` paths: P14, P32.
- 14 `services/**` paths: P07-P10, P29, P46, P48.
- 19 `tracking/**` paths: P15-P18, P48.

Coverage arithmetic: 13 + 16 + 38 + 40 + 2 + 14 + 186 + 9 + 5 + 14 + 19 = 356. The captured 20-line working-tree status/patch is accounted for separately above. Virtualenv, vendor, cache, generated/runtime private material, source `.git`, source `.hermes`, Trello/Google exports, QA archives, databases, media, logs, credentials, concrete verification tokens, and source deployment identifiers are excluded by the capture README and Phase 01 contracts; no excluded material is needed to account for the 356 captured product paths.

## Common ancestry test

Read-only commands used:

- In target: `git merge-base HEAD 4bdb0a342c47da223588897f56ab7d11c50c44f4`
- In target: `git rev-list --all | wc -l`
- In source: `git rev-list --all | wc -l`
- Cross-repo object-set comparison using sorted `git rev-list --all` outputs and `comm -12`

Observed ancestry evidence:

- `git merge-base HEAD 4bdb0a342c47da223588897f56ab7d11c50c44f4` in the target failed with `fatal: Not a valid commit name 4bdb0a342c47da223588897f56ab7d11c50c44f4`; exit code 128.
- Target repository has 1 reachable commit.
- LOWL source repository has 63 reachable commits.
- Cross-repo reachable commit ID intersection count: 0.

Conclusion: there is no usable common Git ancestry for a simple source-to-target commit-range merge, merge-base, or cherry-pick workflow. Downstream phases must port behavior semantically from the immutable captured artifacts and read-only source evidence.

## Authoritative baseline decision for downstream workers

1. Use `.hermes/sources/lowl-parity-20260731/README.md`, `source-head.txt`, `source-product-files.txt`, `source-product-sha256.txt`, `source-product-status.txt`, `source-product-working-tree.patch`, `source-product-working-tree.patch.sha256`, copied `untracked-product/**`, and read-only `git show` at `4bdb0a342c47da223588897f56ab7d11c50c44f4` as the source authority.
2. Treat live LOWL as read-only and currently product-equivalent to the capture, despite non-product workflow/audit drift.
3. Treat target `main` at `f97ebeb835925b66659fa57f8a9d19759ee83341`, the target tracked tree, `docs/parity/lowl-feature-parity.md`, and `docs/design/inland-empire-design-contract.md` as the target baseline/contract.
4. Do not bulk-copy same-path files or use Git range merging. The 105 common paths include semantic merge surfaces; the single target-only migration `home/migrations/0009_update_contact_info_corona.py` is authoritative and prevents copying source `home/0009` directly.
5. Do not start Phase 02 from this task. This report is only the immutable baseline/evidence handoff.
