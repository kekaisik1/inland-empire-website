"""Source-grounded content helpers for regional service landing pages."""

from __future__ import annotations

import html
import re
from functools import lru_cache
from pathlib import Path
from textwrap import shorten


SOURCE_PATH = Path(__file__).with_name("data") / "regional_service_pages.md"

REGIONAL_AREAS = (
    {"name": "Lake Elsinore, CA", "slug": "lake-elsinore-ca"},
    {"name": "Riverside, CA", "slug": "riverside-ca"},
)

REGIONAL_SERVICE_SPECS = (
    {
        "source_title": "Freezer Repair",
        "base_slug": "freezer-repair",
        "regional_slug": "freezer-repair",
    },
    {
        "source_title": "AC Repair (HVAC)",
        "base_slug": "air-conditioning-repair-hvac",
        "regional_slug": "ac-repair",
    },
    {
        "source_title": "Refrigerator Repair",
        "base_slug": "refrigerator-repair",
        "regional_slug": "refrigerator-repair",
    },
    {
        "source_title": "Washer Repair",
        "base_slug": "washer-repair",
        "regional_slug": "washer-repair",
    },
    {
        "source_title": "Dryer Repair",
        "base_slug": "dryer-repair",
        "regional_slug": "dryer-repair",
    },
    {
        "source_title": "Dishwasher Repair",
        "base_slug": "dishwasher-repair",
        "regional_slug": "dishwasher-repair",
    },
    {
        "source_title": "Oven Repair",
        "base_slug": "oven-repair",
        "regional_slug": "oven-repair",
    },
    {
        "source_title": "Stove Repair",
        "base_slug": "stove-repair",
        "regional_slug": "stove-repair",
    },
    {
        "source_title": "Water Heater Repair",
        "base_slug": "water-heater-repair",
        "regional_slug": "water-heater-repair",
    },
    {
        "source_title": "Microwave Repair",
        "base_slug": "microwave-repair",
        "regional_slug": "microwave-repair",
    },
)


def _clean_source(value: str) -> str:
    return (
        value.replace(r"\[GEO\]", "[GEO]")
        .replace("\u00a0", " ")
        .replace("\r\n", "\n")
    )


@lru_cache(maxsize=1)
def regional_source_sections() -> dict[str, str]:
    """Return the ten H1-delimited source sections keyed by service title."""

    source = _clean_source(SOURCE_PATH.read_text(encoding="utf-8"))
    matches = list(re.finditer(r"(?m)^# (.+?)\s*$", source))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        raw_title = match.group(1).strip()
        title = re.sub(r"\s+in \[GEO\]$", "", raw_title)
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        sections[title] = source[match.end() : end].strip()

    expected = {spec["source_title"] for spec in REGIONAL_SERVICE_SPECS}
    if set(sections) != expected:
        missing = sorted(expected - set(sections))
        unexpected = sorted(set(sections) - expected)
        raise ValueError(
            f"Regional source headings changed; missing={missing}, unexpected={unexpected}"
        )
    return sections


def _escaped_text(value: str) -> str:
    return html.escape(value.strip(), quote=False)


def _is_table_separator(cells: list[str]) -> bool:
    return bool(cells) and all(
        not cell or re.fullmatch(r":?-{3,}:?", cell) for cell in cells
    )


def _render_table(lines: list[str]) -> str:
    rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines]
    rows = [row for row in rows if any(row) and not _is_table_separator(row)]
    if not rows:
        return ""
    header, *body = rows
    head_html = "".join(f"<th>{_escaped_text(cell)}</th>" for cell in header)
    body_html = "".join(
        "<tr>" + "".join(f"<td>{_escaped_text(cell)}</td>" for cell in row) + "</tr>"
        for row in body
    )
    return f"<table><thead><tr>{head_html}</tr></thead><tbody>{body_html}</tbody></table>"


def markdown_to_rich_text(source: str) -> str:
    """Convert the limited, trusted source Markdown into Wagtail RichText HTML."""

    lines = source.splitlines()
    output: list[str] = []
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            output.append(f"<p>{_escaped_text(' '.join(paragraph))}</p>")
            paragraph.clear()

    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            flush_paragraph()
            index += 1
            continue
        if line == "* * *":
            flush_paragraph()
            index += 1
            continue
        if line.startswith("## "):
            flush_paragraph()
            output.append(f"<h2>{_escaped_text(line[3:])}</h2>")
            index += 1
            continue
        if line.startswith("|"):
            flush_paragraph()
            table_lines: list[str] = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index].strip())
                index += 1
            rendered_table = _render_table(table_lines)
            if rendered_table:
                output.append(rendered_table)
            continue
        if line.startswith("- "):
            flush_paragraph()
            items: list[str] = []
            while index < len(lines) and lines[index].strip().startswith("- "):
                items.append(lines[index].strip()[2:])
                index += 1
            output.append(
                "<ul>" + "".join(f"<li>{_escaped_text(item)}</li>" for item in items) + "</ul>"
            )
            continue
        if re.match(r"^\d+\.\s+", line):
            flush_paragraph()
            items = []
            while index < len(lines):
                numbered = re.match(r"^\d+\.\s+(.+)$", lines[index].strip())
                if not numbered:
                    break
                items.append(numbered.group(1))
                index += 1
            output.append(
                "<ol>" + "".join(f"<li>{_escaped_text(item)}</li>" for item in items) + "</ol>"
            )
            continue
        paragraph.append(line)
        index += 1

    flush_paragraph()
    return "\n".join(output)


def _first_paragraph(source: str) -> str:
    for block in re.split(r"\n\s*\n", source):
        block = block.strip()
        if block and not block.startswith(("#", "-", "|")):
            return shorten(" ".join(block.split()), width=245, placeholder="...")
    raise ValueError("Regional service section does not contain an introductory paragraph")


def regional_service_records() -> list[dict[str, str]]:
    """Build the 20 page records (ten services across two requested cities)."""

    sections = regional_source_sections()
    records: list[dict[str, str]] = []
    for area in REGIONAL_AREAS:
        for spec in REGIONAL_SERVICE_SPECS:
            source = sections[spec["source_title"]].replace("[GEO]", area["name"])
            title = f"{spec['source_title']} in {area['name']}"
            records.append(
                {
                    "title": title,
                    "slug": f"{spec['regional_slug']}-{area['slug']}",
                    "base_slug": spec["base_slug"],
                    "area": area["name"],
                    "intro": _first_paragraph(source),
                    "body": markdown_to_rich_text(source),
                }
            )
    return records


def get_regional_base_service_slug(slug: str) -> str | None:
    """Resolve a generated regional slug to its ordinary service hero slug."""

    for area in REGIONAL_AREAS:
        suffix = f"-{area['slug']}"
        if not slug.endswith(suffix):
            continue
        regional_slug = slug[: -len(suffix)]
        for spec in REGIONAL_SERVICE_SPECS:
            if spec["regional_slug"] == regional_slug:
                return spec["base_slug"]
    return None
