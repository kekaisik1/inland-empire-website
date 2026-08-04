"""Target-safe review provenance for public Inland Empire pages.

The captured LOWL source includes review excerpts tied to LOWL Google/Yelp
profiles. They are useful source-grounding evidence for the migration, but they
are not valid Inland Empire public claims. Public helpers therefore return no
renderable review cards until target-owned review evidence is supplied.
"""

from __future__ import annotations

from typing import Final, TypedDict


GOOGLE_REVIEW_SOURCE_URL: Final = "https://maps.app.goo.gl/3oVquXaKjxQR3XBn8"
YELP_REVIEW_SOURCE_URL: Final = "https://www.yelp.com/biz/lowl-lake-elsinore"
YELP_RUSS_REVIEW_URL: Final = (
    "https://www.yelp.com/biz/lowl-lake-elsinore?hrid=LJAahSfJ-m8RhPYWQObAQQ"
)
YELP_AMANDA_REVIEW_URL: Final = (
    "https://www.yelp.com/biz/lowl-lake-elsinore?hrid=Q5k-KcfNguM3dSoRQUKgIg"
)
YELP_ZELNE_REVIEW_URL: Final = (
    "https://www.yelp.com/biz/lowl-lake-elsinore?hrid=V0uIA2luANWXt_gP3VzrAA"
)


class ReviewItem(TypedDict):
    """Public review card data shared by homepage and service pages."""

    author: str
    date: str
    date_published: str
    rating: int
    source: str
    source_url: str
    text: str


class WithheldReviewItem(ReviewItem):
    """Review evidence retained but not rendered as target public content."""

    withheld_reason: str


_WITHHELD_REASON: Final = (
    "Captured source review belongs to LOWL, not Inland Empire Appliance Repair; "
    "withheld from public target review cards/schema until target-owned review "
    "evidence is supplied."
)

_SOURCE_REVIEW_EXCERPTS: Final[tuple[dict[str, str | int], ...]] = (
    {
        "author": "Maria G.",
        "date": "",
        "date_published": "",
        "rating": 5,
        "source": "Google",
        "source_url": GOOGLE_REVIEW_SOURCE_URL,
        "text": (
            "Called in the morning and they were here by noon. Fixed my refrigerator "
            "on the spot. Very professional and fair pricing."
        ),
    },
    {
        "author": "Russ L.",
        "date": "May 18, 2026",
        "date_published": "2026-05-18",
        "rating": 5,
        "source": "Yelp",
        "source_url": YELP_RUSS_REVIEW_URL,
        "text": (
            "The experience was very nice, the two techs showed up on time after calling me, "
            "the showed expertise beyond my expectation. They examined my frig and found the "
            "problem and resolved my issues. Gave me alternatives to fix the issues and made "
            "the repairs. All very professionally done."
        ),
    },
    {
        "author": "Amanda S.",
        "date": "Apr 1, 2026",
        "date_published": "2026-04-01",
        "rating": 5,
        "source": "Yelp",
        "source_url": YELP_AMANDA_REVIEW_URL,
        "text": (
            "Great experience! They fixed my refrigerator quickly and professionally. The "
            "technician was on time, explained everything clearly, and the repair was done "
            "right. Pricing was fair and worth every penny. Highly recommend!"
        ),
    },
    {
        "author": "Zelne Z.",
        "date": "Aug 18, 2025",
        "date_published": "2025-08-18",
        "rating": 5,
        "source": "Yelp",
        "source_url": YELP_ZELNE_REVIEW_URL,
        "text": (
            "My washing machine was acting funny, they were able to get me an appointment "
            "that day, find the leaking part and fix it that same day. I feel the price was "
            "fair for the work and appreciated the quick service I received. I would use "
            "this company again."
        ),
    },
)


def get_customer_review_items(
    google_source_url: str | None = None,
    yelp_source_url: str | None = None,
) -> list[ReviewItem]:
    """Return target-approved public reviews.

    Captured LOWL review excerpts are intentionally not returned for the Inland
    Empire target because that would relabel another business's public reviews.
    """

    return []


def get_withheld_review_items() -> list[WithheldReviewItem]:
    """Return retained source review evidence with explicit withholding reason."""

    withheld: list[WithheldReviewItem] = []
    for item in _SOURCE_REVIEW_EXCERPTS:
        withheld.append(
            {
                "author": str(item["author"]),
                "date": str(item["date"]),
                "date_published": str(item["date_published"]),
                "rating": int(item["rating"]),
                "source": str(item["source"]),
                "source_url": str(item["source_url"]),
                "text": str(item["text"]),
                "withheld_reason": _WITHHELD_REASON,
            }
        )
    return withheld
