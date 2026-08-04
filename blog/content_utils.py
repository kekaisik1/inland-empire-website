"""Utilities for CMS-managed blog StreamField content."""

from __future__ import annotations

import json
import re
from collections.abc import Iterable
from typing import Any

# Draftail's HTML-to-contentstate converter expects void tags such as <br /> to
# be XHTML-style self-closing. Raw <br> tags render on the public site but can
# crash the Wagtail edit form with "Unmatched tags: expected br, got p".
BR_TAG_RE = re.compile(r"<br(?P<attrs>[^>/]*?)>", re.IGNORECASE)


def normalize_rich_text_html(value: str) -> str:
    """Normalize rich-text HTML so Wagtail's Draftail editor can parse it."""

    return BR_TAG_RE.sub(lambda match: f"<br{match.group('attrs')} />", value)


def normalize_stream_data(value: Any) -> Any:
    """Recursively normalize rich-text strings inside StreamField raw data."""

    if isinstance(value, str):
        return normalize_rich_text_html(value)
    if isinstance(value, list):
        return [normalize_stream_data(item) for item in value]
    if isinstance(value, tuple):
        return tuple(normalize_stream_data(item) for item in value)
    if isinstance(value, dict):
        return {key: normalize_stream_data(item) for key, item in value.items()}
    return value


def stream_body(blocks: Iterable[tuple[str, str]]) -> str:
    """Convert (block_type, value) tuples to normalized StreamField JSON."""

    return json.dumps(
        [
            {"type": block_type, "value": normalize_rich_text_html(value)}
            for block_type, value in blocks
        ]
    )


def normalized_stream_json(raw_body: Any) -> tuple[str | None, bool]:
    """Return normalized StreamField JSON and whether the input changed.

    Accepts a Wagtail StreamValue, raw_data view, JSON string, or list/dict raw
    data. Returns ``(None, False)`` when the payload cannot be safely parsed.
    """

    if raw_body is None:
        return None, False

    raw_data = getattr(raw_body, "raw_data", raw_body)

    if isinstance(raw_data, str):
        try:
            data = json.loads(raw_data)
        except json.JSONDecodeError:
            normalized = normalize_rich_text_html(raw_data)
            return normalized, normalized != raw_data
    else:
        try:
            data = list(raw_data) if not isinstance(raw_data, dict) else dict(raw_data)
        except TypeError:
            return None, False

    normalized_data = normalize_stream_data(data)
    changed = normalized_data != data
    return json.dumps(normalized_data), changed
