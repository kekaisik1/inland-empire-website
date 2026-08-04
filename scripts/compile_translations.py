#!/usr/bin/env python3
"""Compile gettext PO catalogs with polib, without requiring system msgfmt."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import polib


def compile_catalogs(locale_root: Path) -> list[Path]:
    """Compile every django.po below locale_root atomically and return MO paths."""
    compiled: list[Path] = []
    for po_path in sorted(locale_root.rglob("*.po")):
        mo_path = po_path.with_suffix(".mo")
        temporary_path = mo_path.with_suffix(".mo.tmp")
        catalog = polib.pofile(str(po_path))
        try:
            catalog.save_as_mofile(str(temporary_path))
            os.replace(temporary_path, mo_path)
        finally:
            temporary_path.unlink(missing_ok=True)
        compiled.append(mo_path)
    return compiled


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--locale-root",
        type=Path,
        default=Path("locale"),
        help="Locale directory to scan (default: ./locale)",
    )
    args = parser.parse_args()
    compiled = compile_catalogs(args.locale_root)
    for path in compiled:
        print(f"compiled {path}")
    print(f"compiled_catalogs={len(compiled)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
