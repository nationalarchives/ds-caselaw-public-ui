from datetime import date

from caselawclient.search_parameters import RESULTS_PER_PAGE, SearchParameters
from django.conf import settings
from django.core.exceptions import BadRequest
from django.http import (
    HttpRequest,
)

from judgments.forms import AdvancedSearchForm
from judgments.search_scopes import get_higher_court_params, get_other_courts
from judgments.utils import (
    MAX_RESULTS_PER_PAGE,
    clamp,
)
from judgments.utils.utils import sanitise_input_to_integer


def search_request_to_parameters(request: HttpRequest) -> SearchParameters:
    """
    The advanced search view handles any searches made in the application

    * Given a valid search form, query Marklogic and return the results
    * Given an invalid search form, render it again with the errors
    * Given GET request without form submission return an empty form
    """

    form: AdvancedSearchForm = AdvancedSearchForm(request.GET)
    params = request.GET
    """
    Form should be valid unless there is a critical issue
    with the submission (i.e. Month > 12)
    """
    if not form.is_valid():
        raise BadRequest(form.errors.as_json())

    query_text: str = form.cleaned_data.get("query", "")
    page: int = clamp(sanitise_input_to_integer(params.get("page"), 1), minimum=1)
    order = form.cleaned_data.get("order")
    # If there is no query, order by -date, else order by relevance
    if not order and not query_text:
        order = "-date"
    elif not order:
        order = "relevance"

    from_date: date | None = form.cleaned_data.get("from_date")
    to_date: date | None = form.cleaned_data.get("to_date")
    # If a from_date is not specified, ensure it is set to a year
    # which encompasses all possible records
    if not from_date:
        from_date_for_search = date(settings.MINIMUM_ALLOWED_YEAR, 1, 1)
    else:
        from_date_for_search = from_date
    courts_and_tribunals = form.cleaned_data.get("court", [])
    scopes = form.cleaned_data.get("scope", [])
    if scopes:
        courts_and_tribunals = []
        if "all_courts" not in scopes:
            if "higher_courts" in scopes:
                courts_and_tribunals.extend(get_higher_court_params())
            if "other_courts" in scopes:
                courts_and_tribunals.extend(str(court.canonical_param) for court in get_other_courts())
    # `SearchParameters` takes an optional string for dates
    if not to_date:
        to_date_as_search_param = None
    else:
        to_date_as_search_param = to_date.strftime("%Y-%m-%d")

    # Construct the search parameter object required for Marklogic query
    search_parameters: SearchParameters = SearchParameters(
        query=query_text,
        court=",".join(courts_and_tribunals),
        judge=form.cleaned_data.get("judge"),
        party=form.cleaned_data.get("party"),
        page=int(page),
        order=order,
        date_from=from_date_for_search.strftime("%Y-%m-%d"),
        date_to=to_date_as_search_param,
        page_size=clamp(
            sanitise_input_to_integer(params.get("per_page"), RESULTS_PER_PAGE),
            minimum=1,
            maximum=MAX_RESULTS_PER_PAGE,
        ),
    )

    return search_parameters
