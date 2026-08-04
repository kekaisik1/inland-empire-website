"""Search view with rate limiting."""

from __future__ import annotations

from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest, HttpResponse
from django.db.models import Q
from django.template.response import TemplateResponse
from django_ratelimit.decorators import ratelimit

from wagtail.models import Locale, Page


@ratelimit(key="ip", rate="30/m", block=True)
def search(request: HttpRequest) -> HttpResponse:
    """Search live Wagtail pages in the request language."""
    per_page: int = getattr(settings, "SEARCH_RESULTS_PER_PAGE", 10)
    search_param = "q" if "q" in request.GET else "query"
    raw_search_query = request.GET.get(search_param) or ""
    search_query = str(raw_search_query).strip()
    results_page = None

    if search_query:
        language_code = getattr(request, "LANGUAGE_CODE", settings.LANGUAGE_CODE)
        locale_id = Locale.objects.filter(language_code=language_code).values_list(
            "id", flat=True
        ).first()
        unfiltered_results = Page.objects.live().search(search_query)
        search_results = [
            result
            for result in unfiltered_results
            if locale_id is not None and result.locale_id == locale_id
        ]
        if not search_results and locale_id is not None:
            search_results = list(
                Page.objects.live()
                .filter(locale_id=locale_id)
                .filter(
                    Q(title__icontains=search_query)
                    | Q(search_description__icontains=search_query)
                )
                .order_by("title")
            )
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
        {
            "search_param": search_param,
            "search_query": search_query,
            "search_results": results_page,
        },
    )
