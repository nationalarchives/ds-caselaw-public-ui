import urllib
from typing import Any, Dict

from caselawclient.Client import MarklogicAPIError
from caselawclient.client_helpers.search_helpers import (
    search_judgments_and_parse_response,
)
from caselawclient.search_parameters import RESULTS_PER_PAGE, SearchParameters
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils.translation import gettext
from ds_caselaw_utils import courts as all_courts

from judgments.utils import (
    MAX_RESULTS_PER_PAGE,
    api_client,
    as_integer,
    has_filters,
    paginator,
    preprocess_query,
)


def results(request):
    context: Dict[str, Any] = {"page_title": gettext("results.search.title")}
    try:
        params = request.GET
        query = preprocess_query(params.get("query", ""))
        page = str(as_integer(params.get("page"), minimum=1))
        per_page = str(
            as_integer(
                params.get("per_page"),
                minimum=1,
                maximum=MAX_RESULTS_PER_PAGE,
                default=RESULTS_PER_PAGE,
            )
        )

        if query:
            order = params.get("order", default="-relevance")
            search_parameters = SearchParameters(
                query=query, page=int(page), order=order, page_size=int(per_page)
            )
            search_response = search_judgments_and_parse_response(
                api_client, search_parameters
            )

            context["search_results"] = search_response.results
            context["total"] = search_response.total
            context["paginator"] = paginator(page, search_response.total, per_page)
            context["query"] = query
            context["order"] = order
            context["per_page"] = per_page

            context["query_string"] = urllib.parse.urlencode(
                {"query": query, "order": order, "per_page": per_page}
            )
            context["query_params"] = {"query": query, "order": order}
            context["filtered"] = has_filters(context["query_params"])
        else:
            order = params.get("order", default="-date")
            search_parameters = SearchParameters(
                order=order, page=int(page), page_size=int(per_page)
            )
            search_response = search_judgments_and_parse_response(
                api_client, search_parameters
            )
            search_results = search_response.results
            context["recent_judgments"] = search_results
            context["per_page"] = per_page
            context["total"] = search_response.total
            context["search_results"] = search_results
            context["order"] = order
            context["query_params"] = {"order": order}
            context["query_string"] = urllib.parse.urlencode(
                {"order": order, "per_page": per_page}
            )
            context["filtered"] = has_filters(context["query_params"])
            context["paginator"] = paginator(page, search_response.total, per_page)

            context["page_title"] = gettext("results.search.title")

        context["courts"] = all_courts.get_selectable()
    except MarklogicAPIError:
        raise Http404("Search error")  # TODO: This should be something else!
    return TemplateResponse(
        request,
        "judgment/results.html",
        context={
            "context": context,
            "feedback_survey_type": "search",
        },
    )
