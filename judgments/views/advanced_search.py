import urllib
from datetime import date
from typing import Optional

from caselawclient.Client import MarklogicResourceNotFoundError
from caselawclient.client_helpers.search_helpers import (
    search_judgments_and_parse_response,
)
from caselawclient.responses.search_response import SearchResponse
from caselawclient.search_parameters import RESULTS_PER_PAGE, SearchParameters
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseServerError
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt

from judgments.forms import AdvancedSearchForm
from judgments.utils import (
    MAX_RESULTS_PER_PAGE,
    api_client,
    as_integer,
    get_minimum_valid_year,
    has_filters,
    paginator,
    process_court_facets,
    process_year_facets,
    show_no_exact_ncn_warning,
)


def _do_dates_require_warnings(from_date, total_results):
    """
    Check if users have requested a year before what we technically handle,
    if it is, then we provide a warning letting them know.
    """
    from_warning = False
    if from_date:
        if from_date.year < settings.MINIMUM_WARNING_YEAR or total_results < 1:
            from_warning = True
    return from_warning


@csrf_exempt
def advanced_search(request):
    """
    The advanced search view handles any searches made in the application

    * Given a valid search form, query Marklogic and return the results
    * Given an invalid search form, render it again with the errors
    * Given GET request without form submission return an empty form
    * Given anything except an HTTP GET request raise an error
    """
    # We should only be handling GET requests here since we aren't changing anything on the server
    if not request.method == "GET":
        # Raise an error if the user has tried any non GET HTTP requests.
        return HttpResponseBadRequest("GET requests only")
    else:
        form: AdvancedSearchForm = AdvancedSearchForm(request.GET)
        params: dict = request.GET
        """
        Form should be valid unless there is a critical issue
        with the submission (i.e. Month > 12)
        """
        if not form.is_valid():
            # If the form has errors, return it for rendering!
            return TemplateResponse(
                request, "pages/structured_search.html", {"form": form}
            )
        else:
            context: dict = {}
            court_facets: dict = {}
            tribunal_facets: dict = {}
            year_facets: dict = {}
            query_params: dict = {}
            query_text: str = form.cleaned_data.get("query", "")
            page: str = str(as_integer(params.get("page"), minimum=1))
            per_page: str = str(
                as_integer(
                    params.get("per_page", "10"),
                    minimum=1,
                    maximum=MAX_RESULTS_PER_PAGE,
                    default=RESULTS_PER_PAGE,
                )
            )
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
            courts_and_tribunals = form.cleaned_data.get(
                "court", []
            ) + form.cleaned_data.get("tribunal", [])
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
                page_size=as_integer(
                    params.get("per_page", "10"),
                    minimum=1,
                    maximum=MAX_RESULTS_PER_PAGE,
                    default=RESULTS_PER_PAGE,
                ),
            )

            # Get the response from Marklogic
            try:
                search_response: SearchResponse = search_judgments_and_parse_response(
                    api_client, search_parameters
                )
            except MarklogicResourceNotFoundError:
                return HttpResponseServerError("Search failed")

            # If a query was provided, get relevant search facets to display to the user
            if search_parameters.query:
                unprocessed_facets, court_facets, tribunal_facets = (
                    process_court_facets(search_response.facets, courts_and_tribunals)
                )
                unprocessed_facets, year_facets = process_year_facets(
                    unprocessed_facets
                )

            changed_queries = {
                key: value
                for key, value in params.items()
                if value is not None and not key == "page"
            }
            # Populate context to provide feedback about filters etc. back to user
            context = context | {
                "query": query_text,
                "requires_from_warning": _do_dates_require_warnings(
                    from_date, search_response.total
                ),
                "earliest_record": get_minimum_valid_year(),
                "court_facets": court_facets,
                "tribunal_facets": tribunal_facets,
                "year_facets": year_facets,
                "search_results": search_response.results,
                "total": search_response.total,
                "paginator": paginator(page, search_response.total, per_page),
                "query_string": urllib.parse.urlencode(changed_queries, doseq=True),
                "order": order,
                "per_page": per_page,
                "page": page,
                "filtered": has_filters(params),
                "page_title": _("results.search.title"),
                "show_no_exact_ncn_warning": show_no_exact_ncn_warning(
                    search_response.results, query_text, page
                ),
                "query_params": query_params,
            }

            # If we have a search query, stick it in the breadcrumbs. Otherwise, don't bother.
            if query_text:
                breadcrumbs = [{"text": f'Search results for "{query_text}"'}]
            else:
                breadcrumbs = [{"text": "Search results"}]
            return TemplateResponse(
                request,
                "judgment/results.html",
                context={
                    "form": form,
                    "context": context,
                    "breadcrumbs": breadcrumbs,
                    "feedback_survey_type": "structured_search",
                },
            )
