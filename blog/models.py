"""Blog app models: BlogIndexPage, BlogPage, and BlogPageTag."""

from __future__ import annotations

import math
import re

from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.search import index


WORDS_PER_MINUTE = 200


class BlogPageTag(TaggedItemBase):
    """Through model for BlogPage tags — required by ClusterTaggableManager."""

    content_object = ParentalKey(
        "blog.BlogPage",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )


class BlogIndexPage(Page):
    """Main blog listing page with pagination."""

    intro = models.TextField(blank=True)
    hero_title = models.CharField(
        max_length=255,
        blank=True,
        default="Our Blog",
        help_text="Main heading for the blog page",
    )
    hero_subtitle = models.TextField(
        blank=True,
        default="Tips, guides, and insights about appliance care and repair.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
        FieldPanel("intro"),
    ]

    subpage_types = ["blog.BlogPage"]
    parent_page_types = ["home.HomePage"]

    def get_context(self, request: object) -> dict:
        """Fetch paginated child posts with optimized queries.

        Filters posts by the current page's locale so each language
        only shows its own posts.
        """
        context = super().get_context(request)
        per_page: int = getattr(settings, "BLOG_POSTS_PER_PAGE", 9)

        all_posts = (
            BlogPage.objects.child_of(self)
            .live()
            .filter(locale=self.locale)
            .order_by("-date")
            .select_related("featured_image")
        )

        paginator = Paginator(all_posts, per_page)
        raw_page = request.GET.get("page")  # type: ignore[union-attr]

        try:
            page_num = max(1, int(raw_page)) if raw_page else 1
            posts = paginator.page(page_num)
        except (PageNotAnInteger, ValueError, TypeError):
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context["posts"] = posts
        context["featured_post"] = all_posts.first()
        return context


class BlogPage(Page):
    """Individual blog post with rich content, featured image, and tags."""

    date = models.DateField("Post date")
    intro = models.CharField(max_length=250, help_text="Brief summary for listings")

    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Featured image for the blog post",
    )

    author_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Author name (uses business name if blank). Improves E-E-A-T signals.",
    )

    tags = ClusterTaggableManager(
        through=BlogPageTag,
        blank=True,
        help_text="Tags for content clustering (e.g. refrigerator, washer, maintenance)",
    )

    body = StreamField(
        [
            ("heading", blocks.CharBlock(form_classname="full title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("quote", blocks.BlockQuoteBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("date"),
                FieldPanel("intro"),
                FieldPanel("featured_image"),
                FieldPanel("author_name"),
            ],
            heading="Post Information",
        ),
        FieldPanel("tags"),
        FieldPanel("body"),
    ]

    parent_page_types = ["blog.BlogIndexPage"]

    class Meta:
        indexes = [models.Index(fields=["-date"])]

    @property
    def reading_time(self) -> int:
        """Estimated reading time in minutes based on body word count."""
        word_count = 0
        for block in self.body:
            if block.block_type in ("paragraph", "quote"):
                text = re.sub(r"<[^>]+>", "", str(block.value))
                word_count += len(text.split())
            elif block.block_type == "heading":
                word_count += len(str(block.value).split())
        return max(1, math.ceil(word_count / WORDS_PER_MINUTE))

    @property
    def headings(self) -> list[str]:
        """Extract heading texts from the body StreamField for later TOC UI."""
        return [
            str(block.value) for block in self.body if block.block_type == "heading"
        ]

    def get_context(self, request: object) -> dict:
        """Add recent posts and tag-based related posts to the context."""
        context = super().get_context(request)

        # Related posts: find posts sharing the same tags for internal linking
        tag_ids = self.tags.values_list("id", flat=True)
        if tag_ids:
            related = (
                BlogPage.objects.live()
                .filter(locale=self.locale, tags__in=tag_ids)
                .exclude(pk=self.pk)
                .distinct()
                .order_by("-date")
                .only("id", "title", "slug", "url_path", "date", "intro")[:4]
            )
            context["related_posts"] = related
            related_ids = list(related.values_list("pk", flat=True))
        else:
            context["related_posts"] = BlogPage.objects.none()
            related_ids = []

        # Keep the recent sidebar additive rather than repeating related cards.
        context["recent_posts"] = (
            BlogPage.objects.live()
            .filter(locale=self.locale)
            .exclude(pk=self.pk)
            .exclude(pk__in=related_ids)
            .order_by("-date")
            .only("id", "title", "slug", "url_path", "date", "intro")[:5]
        )

        return context
