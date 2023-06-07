import urllib

from caselawclient.Client import MarklogicResourceNotFoundError, api_client
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
    as_integer,
    has_filters,
    paginator,
    parse_date_parameter,
    preprocess_query,
)


def advanced_search(request):
    params = request.GET

    try:
        from_date = parse_date_parameter(params, "from")
    except ValueError:
        from_date = None  # TODO - we need to add a mechanism
        # for informing user of input validation errors
        # - see https://trello.com/c/vsN1NKLu

    try:
        to_date = parse_date_parameter(params, "to", default_to_last=True)
    except ValueError:
        to_date = None  # TODO - as above, see https://trello.com/c/vsN1NKLu

    query_params = {
        "query": params.get("query", ""),
        "court": ",".join(params.getlist("court")),
        "judge": params.get("judge"),
        "party": params.get("party"),
        "neutral_citation": params.get("neutral_citation"),
        "specific_keyword": params.get("specific_keyword"),
        "order": params.get("order", ""),
        "from": from_date,
        "to": to_date,
        "per_page": params.get("per_page"),
    }
    page = str(as_integer(params.get("page"), minimum=1))
    per_page = str(
        as_integer(
            params.get("per_page"),
            minimum=1,
            maximum=MAX_RESULTS_PER_PAGE,
            default=RESULTS_PER_PAGE,
        )
    )

    order = query_params["order"]
    # If there is no query, order by -date, else order by relevance
    if not order and not query_params["query"]:
        order = "-date"
    elif not order:
        order = "relevance"

    context = {}

    try:
        query_without_stop_words = preprocess_query(query_params["query"])
        search_parameters = SearchParameters(
            query=query_without_stop_words,
            court=query_params["court"],
            judge=query_params["judge"],
            party=query_params["party"],
            neutral_citation=query_params["neutral_citation"],
            specific_keyword=query_params["specific_keyword"],
            page=int(page),
            order=order,
            date_from=query_params["from"],
            date_to=query_params["to"],
            page_size=int(per_page),
        )
        search_response = search_judgments_and_parse_response(
            api_client, search_parameters
        )

        context["query"] = query_params["query"]
        context["search_results"] = search_response.results
        context["total"] = search_response.total
        context["paginator"] = paginator(page, search_response.total, per_page)
        changed_queries = {
            key: value for key, value in query_params.items() if value is not None
        }
        context["query_string"] = urllib.parse.urlencode(changed_queries, doseq=True)
        context["query_params"] = query_params
        for key in query_params:
            context[key] = query_params[key] or ""
        context["order"] = order
        context["per_page"] = per_page
        context["filtered"] = has_filters(context["query_params"])
        context["courts"] = all_courts.get_selectable()

        context["page_title"] = gettext("results.search.title")

    except MarklogicResourceNotFoundError:
        raise Http404("Search failed")  # TODO: This should be something else!
    return TemplateResponse(
        request,
        "judgment/results.html",
        context={
            "context": context,
            "feedback_survey_type": "structured_search",
        },
    )
