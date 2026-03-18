"""Search view with rate limiting."""

from __future__ import annotations

from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse
from django_ratelimit.decorators import ratelimit

from wagtail.models import Page


@ratelimit(key="ip", rate="30/m", block=True)
def search(request: HttpRequest) -> HttpResponse:
    """Search across all live Wagtail pages."""
    per_page: int = getattr(settings, "SEARCH_RESULTS_PER_PAGE", 10)
    search_query = request.GET.get("query", "").strip()
    results_page = None

    if search_query:
        search_results = Page.objects.live().search(search_query)
        paginator = Paginator(search_results, per_page)
        raw_page = request.GET.get("page")

        try:
            page_num = max(1, int(raw_page)) if raw_page else 1
            results_page = paginator.page(page_num)
        except (PageNotAnInteger, ValueError, TypeError):
            results_page = paginator.page(1)
        except EmptyPage:
            results_page = paginator.page(paginator.num_pages)

    return TemplateResponse(
        request,
        "search/search.html",
        {"search_query": search_query, "search_results": results_page},
    )
