#!/usr/bin/env python3
"""Fail-closed structural verifier for the Phase 07 deployment contract."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import yaml

EXPECTED_RUNTIME_ENV = {
    "ALLOWED_HOSTS",
    "BING_SITE_AUTH_TOKEN",
    "BOOKING_DOMAIN",
    "BOOKING_URL",
    "BUSINESS_NAME",
    "CLOUDINARY_URL",
    "CONTACT_EMAIL",
    "CSRF_TRUSTED_ORIGINS",
    "DATABASE_URL",
    "DEFAULT_FROM_EMAIL",
    "DJANGO_LOG_LEVEL",
    "DJANGO_SETTINGS_MODULE",
    "DJANGO_SUPERUSER_EMAIL",
    "DJANGO_SUPERUSER_PASSWORD",
    "DJANGO_SUPERUSER_USERNAME",
    "EMAIL_HOST",
    "EMAIL_HOST_PASSWORD",
    "EMAIL_HOST_USER",
    "EMAIL_PORT",
    "GUNICORN_TIMEOUT",
    "GUNICORN_WORKERS",
    "PORT",
    "POSTGRES_DB",
    "POSTGRES_PASSWORD",
    "POSTGRES_USER",
    "RAILWAY_ENVIRONMENT",
    "RAILWAY_PUBLIC_DOMAIN",
    "REDIS_URL",
    "RUN_STARTUP_SEEDS",
    "SECRET_KEY",
    "SENTRY_DSN",
    "SENTRY_ENVIRONMENT",
    "SENTRY_PROFILES_SAMPLE_RATE",
    "SENTRY_TRACES_SAMPLE_RATE",
    "TRACKING_ADMIN_ENABLED",
    "TRACKING_ALLOWED_ORIGINS",
    "TRACKING_COLLECT_RATE",
    "TRACKING_CONVERTED_RETENTION_DAYS",
    "TRACKING_ENABLED",
    "TRACKING_IP_HASH_KEY",
    "TRACKING_REQUIRE_CONSENT",
    "TRACKING_REQUIRE_ORIGIN",
    "TRACKING_RETENTION_DAYS",
    "TRACKING_SECRET",
    "TRACKING_WEBHOOK_ENABLED",
    "TRACKING_WEBHOOK_RATE",
    "TRUSTED_PROXY_CIDRS",
    "TRUST_PROXY_HEADERS",
    "VAPI_ALLOW_UNSIGNED",
    "VAPI_ENABLED",
    "VAPI_RATE",
    "VAPI_SERVER_SECRET",
    "WAGTAILADMIN_BASE_URL",
    "WEB_CONCURRENCY",
}
INTERNAL_ENV = {
    "BASH_SOURCE",
    "CALL_LOG",
    "FAIL_ON",
    "HOME",
    "PATH",
    "PIP_DISABLE_PIP_VERSION_CHECK",
    "PYTHONDONTWRITEBYTECODE",
    "PYTHONPATH",
    "PYTHONUNBUFFERED",
}
SEED_SEQUENCE = (
    "setup_pages",
    "create_brand_pages",
    "populate_blog_posts",
    "update_service_content",
    "setup_regional_service_pages",
    "setup_spanish_pages",
    "populate_spanish_content",
)
REQUIRED_FILES = (
    ".dockerignore",
    ".env.example",
    ".github/workflows/ci.yml",
    ".railwayignore",
    "Dockerfile",
    "docs/deployment/railway.md",
    "home/data/regional_service_pages.md",
    "home/management/commands/setup_regional_service_pages.py",
    "home/regional_service_seed_data.py",
    "locale/es/LC_MESSAGES/django.po",
    "mysite/static/css/output.css",
    "package-lock.json",
    "package.json",
    "predeploy.sh",
    "railway.json",
    "requirements.txt",
    "scripts/compile_translations.py",
    "start.sh",
)


def read_text(root: Path, relative_path: str) -> str:
    return (root / relative_path).read_text(encoding="utf-8")


def collect_environment_names(root: Path) -> set[str]:
    names: set[str] = set()
    python_patterns = (
        re.compile(r"os\.environ\.get\(\s*['\"]([A-Z][A-Z0-9_]*)['\"]"),
        re.compile(r"os\.environ\[\s*['\"]([A-Z][A-Z0-9_]*)['\"]\s*\]"),
        re.compile(r"_env_(?:bool|list)\(\s*['\"]([A-Z][A-Z0-9_]*)['\"]"),
    )
    for path in sorted((root / "mysite").rglob("*.py")) + sorted((root / "pages").rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        for pattern in python_patterns:
            names.update(pattern.findall(text))
    shell_pattern = re.compile(r"\$\{([A-Z][A-Z0-9_]*)")
    for relative_path in ("start.sh", "predeploy.sh"):
        names.update(shell_pattern.findall(read_text(root, relative_path)))
    return names


def parse_env_example(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = re.fullmatch(r"([A-Z][A-Z0-9_]*)=(.*)", stripped)
        if match:
            values[match.group(1)] = match.group(2)
    return values


def check_order(text: str, values: tuple[str, ...]) -> bool:
    positions = [text.find(value) for value in values]
    return all(position >= 0 for position in positions) and positions == sorted(positions)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []
    checks: dict[str, Any] = {}

    missing_files = [path for path in REQUIRED_FILES if not (root / path).is_file()]
    if missing_files:
        errors.append(f"missing required files: {missing_files}")
    checks["required_files"] = len(REQUIRED_FILES) - len(missing_files)
    if missing_files:
        print(json.dumps({"passed": False, "errors": errors}, indent=2))
        return 1

    env_text = read_text(root, ".env.example")
    env_values = parse_env_example(env_text)
    referenced_env = collect_environment_names(root) | EXPECTED_RUNTIME_ENV
    undocumented_env = sorted(referenced_env - set(env_values) - INTERNAL_ENV)
    if undocumented_env:
        errors.append(f"environment names missing from .env.example: {undocumented_env}")
    suspicious_examples: list[str] = []
    placeholder_markers = ("change-me", "USER", "PASSWORD", "HOST", "DATABASE", "your-domain")
    for name, value in env_values.items():
        if not value:
            continue
        if any(marker in name for marker in ("SECRET", "PASSWORD", "TOKEN", "DSN", "KEY")):
            if not any(marker.lower() in value.lower() for marker in placeholder_markers):
                suspicious_examples.append(name)
    if suspicious_examples:
        errors.append(f"credential-like example values are not obvious placeholders: {suspicious_examples}")
    checks["documented_environment_names"] = sorted(set(env_values))
    checks["internal_environment_names"] = sorted(INTERNAL_ENV & referenced_env)

    start_text = read_text(root, "start.sh")
    predeploy_text = read_text(root, "predeploy.sh")
    if not check_order(predeploy_text, SEED_SEQUENCE):
        errors.append("predeploy.sh does not contain the approved seed sequence in order")
    if "set -Eeuo pipefail" not in predeploy_text or "||" in predeploy_text:
        errors.append("predeploy.sh must be fail-closed without masked command failures")
    if "RUN_STARTUP_SEEDS" not in start_text or "exec gunicorn" not in start_text:
        errors.append("start.sh is missing the direct-bootstrap gate or Gunicorn exec")
    if "set -Eeuo pipefail" not in start_text or "||" in start_text:
        errors.append("start.sh must be fail-closed without masked command failures")
    checks["seed_sequence"] = list(SEED_SEQUENCE)

    dockerfile = read_text(root, "Dockerfile")
    required_docker_markers = (
        "COPY . .",
        "npm run build:css",
        "python scripts/compile_translations.py",
        "python manage.py collectstatic --noinput",
        "chmod -R a+rX /app",
        "chown -R app:app /app/media",
        "USER app",
        "ENTRYPOINT [\"/app/start.sh\"]",
    )
    missing_docker_markers = [marker for marker in required_docker_markers if marker not in dockerfile]
    if missing_docker_markers:
        errors.append(f"Dockerfile missing deterministic build markers: {missing_docker_markers}")
    if "|| true" in dockerfile or "2>/dev/null" in dockerfile:
        errors.append("Dockerfile masks a build failure")
    if "chown -R app:app /app\n" in dockerfile:
        errors.append("Dockerfile makes the immutable application source writable by the runtime user")
    if "--no-control-socket" not in start_text:
        errors.append("start.sh must disable Gunicorn's source-tree control socket")
    checks["docker_markers"] = len(required_docker_markers) - len(missing_docker_markers)

    railway = json.loads(read_text(root, "railway.json"))
    if railway.get("build", {}).get("builder") != "DOCKERFILE":
        errors.append("railway.json must use the DOCKERFILE builder")
    if railway.get("build", {}).get("dockerfilePath") != "Dockerfile":
        errors.append("railway.json must reference the root Dockerfile")
    deploy = railway.get("deploy", {})
    if deploy.get("preDeployCommand") != ["/app/predeploy.sh"]:
        errors.append("railway.json must run /app/predeploy.sh as its only pre-deploy command")
    if deploy.get("startCommand") != "/app/start.sh":
        errors.append("railway.json must run /app/start.sh")
    if deploy.get("healthcheckPath") != "/health/" or deploy.get("healthcheckTimeout") != 300:
        errors.append("railway.json healthcheck contract is incomplete")
    checks["railway_config"] = "parsed"

    workflow = yaml.safe_load(read_text(root, ".github/workflows/ci.yml"))
    triggers = workflow.get("on", workflow.get(True, {}))
    if not isinstance(triggers, dict) or not {"push", "pull_request"}.issubset(triggers):
        errors.append("CI workflow must trigger on pushes and pull requests")
    workflow_text = read_text(root, ".github/workflows/ci.yml")
    workflow_markers = (
        'python-version: "3.12"',
        'node-version: "20"',
        "python -m pip install -r requirements.txt",
        "npm ci",
        "python scripts/compile_translations.py",
        "python manage.py check",
        "python manage.py makemigrations --check --dry-run",
        "python manage.py test --verbosity 1",
        "npm run build:css",
        "python scripts/verify_deployment_contract.py",
    )
    missing_workflow_markers = [marker for marker in workflow_markers if marker not in workflow_text]
    if missing_workflow_markers:
        errors.append(f"CI workflow is missing commands: {missing_workflow_markers}")
    checks["ci_markers"] = len(workflow_markers) - len(missing_workflow_markers)

    requirement_lines = [
        line.strip()
        for line in read_text(root, "requirements.txt").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    unpinned_python = [line for line in requirement_lines if "==" not in line]
    if unpinned_python:
        errors.append(f"unpinned direct Python requirements: {unpinned_python}")
    package = json.loads(read_text(root, "package.json"))
    package_lock = json.loads(read_text(root, "package-lock.json"))
    if package.get("name") != "inland-empire-website":
        errors.append("package.json retains a non-target package name")
    if package_lock.get("name") != "inland-empire-website":
        errors.append("package-lock.json retains a non-target package name")
    unpinned_node = {
        name: version
        for name, version in package.get("devDependencies", {}).items()
        if version.startswith(("^", "~", ">", "<", "*"))
    }
    if unpinned_node:
        errors.append(f"unpinned direct Node dependencies: {unpinned_node}")
    checks["python_requirements"] = len(requirement_lines)
    checks["node_dev_dependencies"] = len(package.get("devDependencies", {}))

    for ignore_name in (".dockerignore", ".railwayignore"):
        ignore_lines = {
            line.strip()
            for line in read_text(root, ignore_name).splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        forbidden_patterns = {"*.png", "**/*.png", "Dockerfile", "/Dockerfile", "start.sh", "/start.sh", "predeploy.sh", "/predeploy.sh", "railway.json", "/railway.json", "mysite/", "/mysite/"}
        bad_patterns = sorted(ignore_lines & forbidden_patterns)
        if bad_patterns:
            errors.append(f"{ignore_name} excludes required build/runtime material: {bad_patterns}")
    runtime_pngs = sorted((root / "mysite" / "static" / "images").rglob("*.png"))
    ignored_runtime_pngs: list[str] = []
    for path in runtime_pngs:
        relative_path = str(path.relative_to(root))
        result = subprocess.run(
            ["git", "check-ignore", "-q", "--", relative_path],
            cwd=root,
            check=False,
        )
        if result.returncode == 0:
            ignored_runtime_pngs.append(relative_path)
    if ignored_runtime_pngs:
        errors.append(f".gitignore still hides runtime PNG assets: {ignored_runtime_pngs}")
    env_example_ignored = subprocess.run(
        ["git", "check-ignore", "-q", "--", ".env.example"],
        cwd=root,
        check=False,
    )
    if env_example_ignored.returncode == 0:
        errors.append(".env.example is ignored by Git and cannot be committed")
    checks["runtime_png_assets_visible"] = len(runtime_pngs) - len(ignored_runtime_pngs)

    identity_files = (
        "Dockerfile",
        "docker-compose.yml",
        "mysite/settings/production.py",
        "mysite/wsgi.py",
        "package.json",
        "package-lock.json",
        "predeploy.sh",
        "railway.json",
        "start.sh",
    )
    leaked_identity = [path for path in identity_files if "lowl" in read_text(root, path).lower()]
    if leaked_identity:
        errors.append(f"deployment/runtime identity still references LOWL: {leaked_identity}")

    guide = read_text(root, "docs/deployment/railway.md").lower()
    guide_markers = (
        "postgresql",
        "redis",
        "cloudinary",
        "email",
        "tracking",
        "domain",
        "csrf",
        "superuser",
        "github",
        "first deployment",
        "deployment verification",
        "rollback",
        "limitations",
        "not linked",
        "did not",
        "media",
    )
    missing_guide_markers = [marker for marker in guide_markers if marker not in guide]
    if missing_guide_markers:
        errors.append(f"Railway guide is incomplete: {missing_guide_markers}")
    checks["deployment_guide_markers"] = len(guide_markers) - len(missing_guide_markers)

    payload = {
        "schema_version": 1,
        "passed": not errors,
        "checks": checks,
        "errors": errors,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
