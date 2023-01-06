import urllib

from caselawclient.Client import RESULTS_PER_PAGE, MarklogicAPIError
from django.http import Http404
from django.template import loader
from django.template.response import TemplateResponse
from django.utils.translation import gettext

from judgments.models import SearchResult
from judgments.models import courts as all_courts
from judgments.utils import (
    MAX_RESULTS_PER_PAGE,
    as_integer,
    has_filters,
    paginator,
    perform_advanced_search,
)


def results(request):
    context = {"page_title": gettext("results.search.title")}

    try:
        params = request.GET
        query = params.get("query")
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
            model = perform_advanced_search(
                query=query, page=page, order=order, per_page=per_page
            )

            context["search_results"] = [
                SearchResult.create_from_node(result) for result in model.results
            ]
            context["total"] = model.total
            context["paginator"] = paginator(page, model.total, per_page)
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
            model = perform_advanced_search(order=order, page=page, per_page=per_page)
            search_results = [
                SearchResult.create_from_node(result) for result in model.results
            ]
            context["recent_judgments"] = search_results
            context["per_page"] = per_page
            context["total"] = model.total
            context["search_results"] = search_results
            context["order"] = order
            context["query_params"] = {"order": order}
            context["query_string"] = urllib.parse.urlencode(
                {"order": order, "per_page": per_page}
            )
            context["filtered"] = has_filters(context["query_params"])
            context["paginator"] = paginator(page, model.total, per_page)
        context["courts"] = all_courts.get_selectable()
    except MarklogicAPIError:
        raise Http404("Search error")  # TODO: This should be something else!
    template = loader.get_template("judgment/results.html")
    return TemplateResponse(request, template, context={"context": context})
