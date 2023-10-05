import datetime
from typing import Any, Dict

from caselawclient.Client import MarklogicResourceNotFoundError
from caselawclient.client_helpers.search_helpers import (
    search_judgments_and_parse_response,
)
from caselawclient.search_parameters import RESULTS_PER_PAGE, SearchParameters
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils.translation import gettext
from ds_caselaw_utils import courts as all_courts

from judgments.utils import MAX_RESULTS_PER_PAGE, api_client, as_integer, paginator


def browse(request, court=None, subdivision=None, year=None):
    court_query = "/".join(filter(lambda x: x is not None, [court, subdivision]))
    page = str(as_integer(request.GET.get("page"), minimum=1))
    per_page = str(
        as_integer(
            request.GET.get("per_page"),
            minimum=1,
            maximum=MAX_RESULTS_PER_PAGE,
            default=RESULTS_PER_PAGE,
        )
    )

    context: Dict[str, Any] = {}

    try:
        search_parameters = SearchParameters(
            court=court_query if court_query else None,
            date_from=datetime.date(year=year, month=1, day=1).strftime("%Y-%m-%d")
            if year
            else None,
            date_to=datetime.date(year=year, month=12, day=31).strftime("%Y-%m-%d")
            if year
            else None,
            order="-date",
            page=as_integer(page, minimum=1),
            page_size=as_integer(per_page, minimum=1),
        )
        search_response = search_judgments_and_parse_response(
            api_client, search_parameters
        )

        context["search_results"] = search_response.results
        context["total"] = search_response.total
        context["per_page"] = per_page
        context["paginator"] = paginator(page, search_response.total, per_page)
        context["courts"] = all_courts.get_selectable_groups()

        context["page_title"] = gettext("results.search.title")

    except MarklogicResourceNotFoundError:
        raise Http404("Search failed")  # TODO: This should be something else!
    return TemplateResponse(
        request,
        "judgment/results.html",
        context={
            "context": context,
            "feedback_survey_type": "browse",
            "feedback_survey_court": court_query,
        },
    )
