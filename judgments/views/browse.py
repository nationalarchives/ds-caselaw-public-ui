import datetime

from caselawclient.Client import RESULTS_PER_PAGE, MarklogicResourceNotFoundError
from django.http import Http404
from django.template import loader
from django.template.response import TemplateResponse
from ds_caselaw_utils import courts as all_courts

from judgments.models import SearchResult
from judgments.utils import (
    MAX_RESULTS_PER_PAGE,
    as_integer,
    paginator,
    perform_advanced_search,
)


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

    context = {}

    try:
        model = perform_advanced_search(
            court=court_query if court_query else None,
            date_from=datetime.date(year=year, month=1, day=1).strftime("%Y-%m-%d")
            if year
            else None,
            date_to=datetime.date(year=year, month=12, day=31).strftime("%Y-%m-%d")
            if year
            else None,
            order="-date",
            page=as_integer(page, minimum=1),
            per_page=as_integer(per_page, minimum=1),
        )
        context["search_results"] = [
            SearchResult.create_from_node(result) for result in model.results
        ]
        context["total"] = model.total
        context["per_page"] = per_page
        context["paginator"] = paginator(page, model.total, per_page)
        context["courts"] = all_courts.get_selectable()
    except MarklogicResourceNotFoundError:
        raise Http404("Search failed")  # TODO: This should be something else!
    template = loader.get_template("judgment/results.html")
    return TemplateResponse(
        request,
        template,
        context={
            "context": context,
            "feedback_survey_type": "browse",
            "feedback_survey_court": court_query,
        },
    )
