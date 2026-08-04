"""
Management command to assign featured images to blog posts.

Looks for real image files in the project's ``img/`` directory whose filenames
match blog post titles.  Falls back to generating a simple gradient placeholder
with PIL if no matching file is found.

Usage:
    python manage.py generate_blog_images              # Assign missing images
    python manage.py generate_blog_images --force      # Reassign all images
    python manage.py generate_blog_images --dry-run    # Preview without saving
"""

from __future__ import annotations

import logging
import re
import textwrap
from io import BytesIO
from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand, CommandParser
from PIL import Image as PILImage
from PIL import ImageDraw, ImageFont

from blog.models import BlogPage
from wagtail.images.models import Image as WagtailImage

logger = logging.getLogger(__name__)

# ── Image directory (project root / img) ─────────────────────────────────

IMG_DIR = Path(settings.BASE_DIR) / "img"

# ── PIL fallback dimensions ──────────────────────────────────────────────

WIDTH = 1200
HEIGHT = 630

# ── Topic-to-gradient color mapping (PIL fallback) ───────────────────────

TOPIC_GRADIENTS: list[tuple[list[str], tuple[str, str]]] = [
    (["refrigerator", "freezer", "cooling", "fridge"], ("#25262c", "#1a1b20")),
    (["washer", "washing", "laundry"], ("#1a6b3c", "#0f4d2a")),
    (["dryer", "heating", "heat"], ("#b84520", "#8c3418")),
    (["dishwasher", "cleaning", "drainage", "drain"], ("#2563eb", "#1d4ed8")),
    (["oven", "stove", "gas", "electric", "range", "burner"], ("#dc2626", "#991b1b")),
    (["samsung", "error-code", "error code", "fault code"], ("#1e293b", "#0f172a")),
    (
        ["maintenance", "tips", "cost", "price", "budget", "save"],
        ("#7c3aed", "#5b21b6"),
    ),
    (
        ["water-heater", "hot-water", "water heater", "hot water"],
        ("#0891b2", "#0e7490"),
    ),
]

DEFAULT_GRADIENT = ("#25262c", "#1a1b20")


# ── Helpers ──────────────────────────────────────────────────────────────


def _normalize(text: str) -> str:
    """Normalize a string for fuzzy filename matching.

    Strips quotes, punctuation, collapses whitespace, and lowercases.
    """
    text = text.strip().strip('"').strip("'")
    text = re.sub(r"[^\w\s]", "", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def _find_image_file(title: str) -> Path | None:
    """Find an image file in IMG_DIR matching the given blog post title.

    Tries exact stem match first, then falls back to normalized fuzzy match.
    Returns the Path if found, None otherwise.
    """
    if not IMG_DIR.is_dir():
        return None

    normalized_title = _normalize(title)

    for img_path in IMG_DIR.iterdir():
        if img_path.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
            continue
        # Strip surrounding quotes from filename stem
        stem = img_path.stem.strip('"').strip("'")
        if stem == title:
            return img_path
        if _normalize(stem) == normalized_title:
            return img_path

    return None


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert a six-digit hex color string to an RGB tuple."""
    hex_color = hex_color.lstrip("#")
    return (
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16),
    )


def _determine_gradient(post: BlogPage) -> tuple[str, str]:
    """Pick gradient colors based on the post's tags and title keywords."""
    tag_names: list[str] = []
    try:
        tag_names = [tag.name.lower() for tag in post.tags.all()]
    except Exception:
        pass

    search_text = " ".join(tag_names) + " " + post.title.lower()
    for keywords, gradient in TOPIC_GRADIENTS:
        for keyword in keywords:
            if keyword in search_text:
                return gradient
    return DEFAULT_GRADIENT


def _generate_placeholder(post: BlogPage) -> bytes:
    """Generate a simple gradient placeholder image as PNG bytes."""
    hex_top, hex_bottom = _determine_gradient(post)
    color_top = _hex_to_rgb(hex_top)
    color_bottom = _hex_to_rgb(hex_bottom)

    img = PILImage.new("RGB", (WIDTH, HEIGHT), color_top)
    draw = ImageDraw.Draw(img)

    # Vertical gradient
    for y in range(HEIGHT):
        ratio = y / max(HEIGHT - 1, 1)
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * ratio)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * ratio)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Title text
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42
        )
    except OSError:
        font = ImageFont.load_default()

    lines = textwrap.wrap(post.title, width=35)
    line_height = 56
    total_h = len(lines) * line_height
    y_start = (HEIGHT - total_h) // 2

    for i, line in enumerate(lines):
        w = font.getlength(line) if hasattr(font, "getlength") else len(line) * 20
        x = (WIDTH - w) / 2
        y = y_start + i * line_height
        draw.text((x + 2, y + 2), line, font=font, fill=(0, 0, 0, 80))
        draw.text((x, y), line, font=font, fill=(255, 255, 255))

    buf = BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


class Command(BaseCommand):
    """Assign featured images to blog posts from img/ directory or PIL fallback."""

    help = (
        "Assign featured images to BlogPage entries from the img/ directory. "
        "Falls back to a generated gradient placeholder if no file matches."
    )

    def add_arguments(self, parser: CommandParser) -> None:
        """Register --force and --dry-run flags."""
        parser.add_argument(
            "--force",
            action="store_true",
            default=False,
            help="Reassign images even for posts that already have one.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            default=False,
            help="Preview which posts would get images, without saving.",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Find eligible blog posts and assign featured images."""
        force: bool = options["force"]
        dry_run: bool = options["dry_run"]

        if dry_run:
            self.stdout.write(
                self.style.WARNING("DRY RUN — no images will be saved.\n")
            )

        posts = BlogPage.objects.live()
        if not force:
            posts = posts.filter(featured_image__isnull=True)
        posts = posts.order_by("first_published_at")
        total = posts.count()

        if total == 0:
            self.stdout.write(
                self.style.SUCCESS("All blog posts have featured images.")
            )
            return

        self.stdout.write(
            f"Found {total} post{'s' if total != 1 else ''} to process.\n"
        )

        if IMG_DIR.is_dir():
            self.stdout.write(f"Image directory: {IMG_DIR}\n")
        else:
            self.stdout.write(
                self.style.WARNING(f"Image directory not found: {IMG_DIR}\n")
            )
            self.stdout.write("Will use generated placeholders for all posts.\n")

        assigned = 0
        errors = 0

        for post in posts:
            label = f'"{post.title}"'
            img_path = _find_image_file(post.title)

            if dry_run:
                source = (
                    f"file: {img_path.name}" if img_path else "generated placeholder"
                )
                self.stdout.write(f"  [{source}] {label}")
                assigned += 1
                continue

            try:
                if img_path:
                    # Use real image file
                    image_bytes = img_path.read_bytes()
                    filename = f"blog-{post.slug}{img_path.suffix}"
                    self.stdout.write(f"  [FILE] {label} <- {img_path.name}")
                else:
                    # Fall back to PIL placeholder
                    image_bytes = _generate_placeholder(post)
                    filename = f"blog-{post.slug}.png"
                    self.stdout.write(
                        self.style.WARNING(f"  [GENERATED] {label} (no matching file)")
                    )

                img_file = ImageFile(BytesIO(image_bytes), name=filename)
                wagtail_image = WagtailImage(
                    title=f"Featured: {post.title}",
                    file=img_file,
                )
                wagtail_image.save()

                post.featured_image = wagtail_image
                post.save()

                assigned += 1
                logger.info(
                    "Assigned featured image for '%s' (pk=%d, wagtail_image=%d)",
                    post.title,
                    post.pk,
                    wagtail_image.pk,
                )

            except Exception:
                errors += 1
                logger.exception(
                    "Failed to assign image for '%s' (pk=%d)", post.title, post.pk
                )
                self.stderr.write(self.style.ERROR(f"  [FAIL] {label}"))

        self.stdout.write("")
        action = "Would assign" if dry_run else "Assigned"
        parts = [f"{action}: {assigned}"]
        if errors:
            parts.append(f"Errors: {errors}")
        summary = " | ".join(parts)

        if errors:
            self.stdout.write(self.style.WARNING(f"Done. {summary}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Done. {summary}"))
