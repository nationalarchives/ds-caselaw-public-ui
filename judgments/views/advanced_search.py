import urllib

from caselawclient.Client import RESULTS_PER_PAGE, MarklogicResourceNotFoundError
from django.http import Http404
from django.template import loader
from django.template.response import TemplateResponse
from ds_caselaw_utils import courts as all_courts

from judgments.models import SearchResult
from judgments.utils import (
    MAX_RESULTS_PER_PAGE,
    as_integer,
    has_filters,
    paginator,
    perform_advanced_search,
    preprocess_query,
)


def advanced_search(request):
    params = request.GET
    query_params = {
        "query": params.get("query"),
        "court": params.getlist("court"),
        "judge": params.get("judge"),
        "party": params.get("party"),
        "neutral_citation": params.get("neutral_citation"),
        "specific_keyword": params.get("specific_keyword"),
        "order": params.get("order", ""),
        "from": params.get("from"),
        "to": params.get("to"),
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
    template = loader.get_template("judgment/results.html")
    return TemplateResponse(
        request,
        template,
        context={
            "context": context,
            "feedback_survey_type": "structured_search",
        },
    )
