import urllib

from caselawclient.Client import RESULTS_PER_PAGE, MarklogicResourceNotFoundError
from django.http import Http404
from django.template.response import TemplateResponse
from ds_caselaw_utils import courts as all_courts

from judgments.forms.structured_search import StructuredSearchForm
from judgments.models import SearchResult

from judgments.utils import (
    MAX_RESULTS_PER_PAGE,
    as_integer,
    has_filters,
    paginator,
    parse_date_parameter,
    perform_advanced_search,
    preprocess_query,
)


def advanced_search(request):
    params = request.GET
    form = StructuredSearchForm(params)
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
        "court": params.getlist("court"),
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
        model = perform_advanced_search(
            query=query_without_stop_words,
            court=query_params["court"],
            judge=query_params["judge"],
            party=query_params["party"],
            neutral_citation=query_params["neutral_citation"],
            specific_keyword=query_params["specific_keyword"],
            page=page,
            order=order,
            date_from=query_params["from"],
            date_to=query_params["to"],
            per_page=per_page,
        )
        context["query"] = query_params["query"]
        context["search_results"] = [
            SearchResult.create_from_node(result) for result in model.results
        ]
        context["total"] = model.total
        context["paginator"] = paginator(page, model.total, per_page)
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
