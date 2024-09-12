from datetime import date
from typing import Optional

from caselawclient.search_parameters import RESULTS_PER_PAGE, SearchParameters
from django.core.exceptions import BadRequest
from django.http import (
    HttpRequest,
)
from django.template.response import TemplateResponse

from judgments.forms import AdvancedSearchForm
from judgments.utils import (
    MAX_RESULTS_PER_PAGE,
    clamp,
    get_minimum_valid_year,
)
from judgments.utils.utils import sanitise_input_to_integer


def search_request_to_parameters(request: HttpRequest, return_page_if_invalid="pages/structured_search.html"):
    """
    The advanced search view handles any searches made in the application

    * Given a valid search form, query Marklogic and return the results
    * Given an invalid search form, render it again with the errors
    * Given GET request without form submission return an empty form
    * Given anything except an HTTP GET request raise an error
    """
    # We should only be handling GET requests here since we aren't changing anything on the server
    if request.method != "GET":
        # Raise an error if the user has tried any non GET HTTP requests.
        raise BadRequest("GET requests only to search_request_to_results")

    form: AdvancedSearchForm = AdvancedSearchForm(request.GET)
    params = request.GET
    """
    Form should be valid unless there is a critical issue
    with the submission (i.e. Month > 12)
    """
    if not form.is_valid():
        # If the form has errors, return it for rendering!
        return TemplateResponse(request, return_page_if_invalid, {"form": form})
    else:
        query_params: dict = {}
        query_text: str = form.cleaned_data.get("query", "")
        page: int = clamp(sanitise_input_to_integer(params.get("page"), 1), minimum=1)
        order = params.get("order", None)
        # If there is no query, order by -date, else order by relevance
        if not order and not query_text:
            order = "-date"
        elif not order:
            order = "relevance"

        from_date: date = form.cleaned_data.get("from_date", None)
        to_date: Optional[date] = form.cleaned_data.get("to_date")
        # If a from_date is not specified, set it to the current min year
        # This allows the users to choose if they'd like to go beyond that range
        if not from_date:
            from_date_for_search = date(get_minimum_valid_year(), 1, 1)
        else:
            from_date_for_search = from_date
            # Only provide the param back to the user if they set it
            query_params = query_params | {
                "from_date_0": from_date.day,
                "from_date_1": from_date.month,
                "from_date_2": from_date.year,
            }
        if to_date:
            query_params = query_params | {
                "to_date_0": to_date.day,
                "to_date_1": to_date.month,
                "to_date_2": to_date.year,
            }
        query_params = query_params | {
            "query": query_text,
            "court": form.cleaned_data.get("court", []),
            "tribunal": form.cleaned_data.get("tribunal", []),
            "judge": form.cleaned_data.get("judge", ""),
            "party": form.cleaned_data.get("party", ""),
            "order": order,
            "page": page,
        }
        # Merge the courts and tribunals as they are treated as the same in MarkLogic.
        courts_and_tribunals = form.cleaned_data.get("court", []) + form.cleaned_data.get("tribunal", [])
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
