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

from judgments.models import SearchFormErrors
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
    errors = SearchFormErrors()
    try:
        from_date = parse_date_parameter(params, "from")
    except ValueError as error:
        from_date = None
        errors.add_error(
            gettext("search.errors.from_date_headline"), "from_date", str(error)
        )
    try:
        to_date = parse_date_parameter(params, "to", default_to_last=True)
    except ValueError as error:
        to_date = None
        errors.add_error(
            gettext("search.errors.to_date_headline"), "to_date", str(error)
        )

    if to_date is not None and from_date is not None and to_date < from_date:
        errors.add_error(
            gettext("search.errors.to_before_from_headline"),
            "to_date",
            gettext("search.errors.to_before_from_detail"),
        )

    query_params = {
        "query": params.get("query", ""),
        "court": ",".join(params.getlist("court")),
        "judge": params.get("judge"),
        "party": params.get("party"),
        "neutral_citation": params.get("neutral_citation"),
        "specific_keyword": params.get("specific_keyword"),
        "order": params.get("order", ""),
        "from": from_date,
        "from_day": params.get("from_day"),
        "from_month": params.get("from_month"),
        "from_year": params.get("from_year"),
        "to": to_date,
        "to_day": params.get("to_day"),
        "to_month": params.get("to_month"),
        "to_year": params.get("to_year"),
        "per_page": params.get("per_page"),
        "text_date_input": params.get("text_date_input"),
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

    context = {
        "errors": errors,
        "query": query_params["query"],
        "courts": all_courts.get_selectable(),
        "query_params": query_params,
    }

    for key in query_params:
        context[key] = query_params[key] or ""

    if errors.has_errors():
        return TemplateResponse(
            request, "pages/structured_search.html", context={"context": context}
        )
    else:
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

            context["search_results"] = search_response.results
            context["total"] = search_response.total
            context["paginator"] = paginator(page, search_response.total, per_page)
            changed_queries = {
                key: value for key, value in query_params.items() if value is not None
            }
            context["query_string"] = urllib.parse.urlencode(
                changed_queries, doseq=True
            )
            context["order"] = order
            context["per_page"] = per_page
            context["filtered"] = has_filters(context["query_params"])
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
