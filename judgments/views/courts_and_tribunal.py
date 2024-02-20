from caselawclient.Client import MarklogicResourceNotFoundError
from caselawclient.client_helpers.search_helpers import (
    search_judgments_and_parse_response,
)
from caselawclient.search_parameters import SearchParameters
from django.http import Http404
from django.template.response import TemplateResponse
from ds_caselaw_utils import courts as all_courts

from judgments.utils import api_client


def CourtsTribunals(request):
    context = {}
    try:
        search_response = search_judgments_and_parse_response(
            api_client, SearchParameters(order="-date")
        )
        search_results = search_response.results
        context["courts_and_tribunals"] = search_results

    except MarklogicResourceNotFoundError:
        raise Http404(
            "Search results not found"
        )  # TODO: This should be something else!
    return TemplateResponse(
        request,
        "pages/courts_and_tribunals.html",
        context={
            "context": context,
            "courts": all_courts.get_listable_courts(),
            "tribunals": all_courts.get_listable_tribunals(),
            "feedback_survey_type": "home",
        },
    )
