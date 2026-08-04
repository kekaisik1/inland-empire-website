"""Phase 07 deployment contract tests."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import polib
from django.test import SimpleTestCase

ROOT = Path(__file__).resolve().parent.parent
STRONG_TEST_SECRET = "phase07-test-secret-" + ("x" * 64)


class ProductionSettingsPhase07Tests(SimpleTestCase):
    def _import_production(self, **overrides: str) -> subprocess.CompletedProcess[str]:
        env = {
            "PATH": os.environ.get("PATH", ""),
            "PYTHONPATH": str(ROOT),
            "DJANGO_SETTINGS_MODULE": "mysite.settings.production",
            "SECRET_KEY": STRONG_TEST_SECRET,
            "DATABASE_URL": "sqlite:////tmp/inland-phase07-settings-test.sqlite3",
            "REDIS_URL": "redis://127.0.0.1:6379/0",
            **overrides,
        }
        code = (
            "import json; "
            "from django.conf import settings; "
            "print(json.dumps({"
            "'allowed_hosts': settings.ALLOWED_HOSTS, "
            "'csrf_origins': settings.CSRF_TRUSTED_ORIGINS, "
            "'admin_url': settings.WAGTAILADMIN_BASE_URL"
            "}))"
        )
        return subprocess.run(
            [sys.executable, "-c", code],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_production_requires_allowed_host_or_railway_domain(self) -> None:
        result = self._import_production()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ALLOWED_HOSTS", result.stderr)

    def test_railway_healthcheck_host_is_allowed(self) -> None:
        result = self._import_production(
            RAILWAY_ENVIRONMENT="production",
            RAILWAY_PUBLIC_DOMAIN="inland.example",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertIn("inland.example", payload["allowed_hosts"])
        self.assertIn("healthcheck.railway.app", payload["allowed_hosts"])
        self.assertIn("https://inland.example", payload["csrf_origins"])

    def test_explicit_wagtail_admin_url_is_not_overwritten_by_railway_domain(self) -> None:
        result = self._import_production(
            RAILWAY_ENVIRONMENT="production",
            RAILWAY_PUBLIC_DOMAIN="inland-production.up.railway.app",
            WAGTAILADMIN_BASE_URL="https://www.inland.example",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["admin_url"], "https://www.inland.example")


class DockerfilePhase07Tests(SimpleTestCase):
    def test_non_root_runtime_user_can_read_application_source(self) -> None:
        dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")

        self.assertIn("chmod -R a+rX /app", dockerfile)
        self.assertIn("chown -R app:app /app/media", dockerfile)
        self.assertNotIn("chown -R app:app /app\n", dockerfile)
        self.assertIn("USER app", dockerfile)


class DeploymentShellPhase07Tests(SimpleTestCase):
    def _fake_command_environment(self, directory: Path) -> tuple[dict[str, str], Path]:
        log_path = directory / "calls.log"
        python_path = directory / "python"
        python_path.write_text(
            "#!/usr/bin/env bash\n"
            "printf 'python %s\\n' \"$*\" >> \"$CALL_LOG\"\n"
            "if [ -n \"${FAIL_ON:-}\" ] && [ \"${2:-}\" = \"$FAIL_ON\" ]; then exit 23; fi\n"
            "exit 0\n",
            encoding="utf-8",
        )
        gunicorn_path = directory / "gunicorn"
        gunicorn_path.write_text(
            "#!/usr/bin/env bash\n"
            "printf 'gunicorn %s\\n' \"$*\" >> \"$CALL_LOG\"\n"
            "exit 0\n",
            encoding="utf-8",
        )
        python_path.chmod(0o755)
        gunicorn_path.chmod(0o755)
        env = {
            "PATH": f"{directory}:{os.environ.get('PATH', '')}",
            "CALL_LOG": str(log_path),
            "DJANGO_SETTINGS_MODULE": "mysite.settings.production",
        }
        return env, log_path

    def _run_script(
        self,
        script_name: str,
        *,
        extra_env: dict[str, str] | None = None,
    ) -> tuple[subprocess.CompletedProcess[str], list[str]]:
        with TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            env, log_path = self._fake_command_environment(directory)
            if extra_env:
                env.update(extra_env)
            result = subprocess.run(
                ["bash", str(ROOT / script_name)],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
            calls = log_path.read_text(encoding="utf-8").splitlines() if log_path.exists() else []
            return result, calls

    def test_predeploy_runs_approved_seed_sequence_in_order(self) -> None:
        result, calls = self._run_script("predeploy.sh")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            calls,
            [
                "python manage.py migrate --noinput",
                "python manage.py setup_pages",
                "python manage.py create_brand_pages",
                "python manage.py populate_blog_posts",
                "python manage.py update_service_content",
                "python manage.py setup_regional_service_pages",
                "python manage.py setup_spanish_pages",
                "python manage.py populate_spanish_content",
            ],
        )

    def test_predeploy_stops_on_seed_failure(self) -> None:
        result, calls = self._run_script(
            "predeploy.sh",
            extra_env={"FAIL_ON": "create_brand_pages"},
        )

        self.assertEqual(result.returncode, 23)
        self.assertEqual(
            calls,
            [
                "python manage.py migrate --noinput",
                "python manage.py setup_pages",
                "python manage.py create_brand_pages",
            ],
        )

    def test_start_runs_migration_then_gunicorn_without_default_seeding(self) -> None:
        result, calls = self._run_script("start.sh")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls[0], "python manage.py migrate --noinput")
        self.assertEqual(len([call for call in calls if "setup_pages" in call]), 0)
        self.assertTrue(calls[-1].startswith("gunicorn mysite.wsgi:application "))
        self.assertIn("--bind 0.0.0.0:8000", calls[-1])
        self.assertIn("--workers 1", calls[-1])
        self.assertIn("--no-control-socket", calls[-1])

    def test_start_honors_explicit_web_concurrency(self) -> None:
        result, calls = self._run_script(
            "start.sh",
            extra_env={"WEB_CONCURRENCY": "4"},
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--workers 4", calls[-1])

    def test_start_can_opt_into_seed_sequence_for_direct_container_bootstrap(self) -> None:
        result, calls = self._run_script(
            "start.sh",
            extra_env={"RUN_STARTUP_SEEDS": "true"},
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls.count("python manage.py migrate --noinput"), 1)
        self.assertEqual(
            [call for call in calls if call.startswith("python manage.py")][1:],
            [
                "python manage.py setup_pages",
                "python manage.py create_brand_pages",
                "python manage.py populate_blog_posts",
                "python manage.py update_service_content",
                "python manage.py setup_regional_service_pages",
                "python manage.py setup_spanish_pages",
                "python manage.py populate_spanish_content",
            ],
        )
        self.assertTrue(calls[-1].startswith("gunicorn mysite.wsgi:application "))


class TranslationCompilerPhase07Tests(SimpleTestCase):
    def test_translation_compiler_creates_mo_catalog(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            locale_root = Path(temporary_directory) / "locale"
            catalog_directory = locale_root / "es" / "LC_MESSAGES"
            catalog_directory.mkdir(parents=True)
            po_path = catalog_directory / "django.po"
            po = polib.POFile()
            po.metadata = {
                "Content-Type": "text/plain; charset=UTF-8",
                "Language": "es",
            }
            po.append(polib.POEntry(msgid="Deployment ready", msgstr="Despliegue listo"))
            po.save(str(po_path))

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "compile_translations.py"),
                    "--locale-root",
                    str(locale_root),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            mo_path = po_path.with_suffix(".mo")
            self.assertTrue(mo_path.is_file())
            compiled = polib.mofile(str(mo_path))
            entry = compiled.find("Deployment ready")
            self.assertIsNotNone(entry)
            assert entry is not None
            self.assertEqual(entry.msgstr, "Despliegue listo")
