from datetime import date
from typing import Optional
import urllib

from caselawclient.Client import MarklogicResourceNotFoundError
from caselawclient.client_helpers.search_helpers import (
    search_judgments_and_parse_response,
)
from caselawclient.search_parameters import RESULTS_PER_PAGE, SearchParameters
from caselawclient.responses.search_response import SearchResponse
from django.http import Http404
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext as _

from judgments.forms import AdvancedSearchForm
from judgments.models.court_dates import CourtDates
from judgments.utils import (
    MAX_RESULTS_PER_PAGE,
    api_client,
    as_integer,
    has_filters,
    paginator,
    preprocess_query,
    process_court_facets,
    process_year_facets,
    show_no_exact_ncn_warning,
)


def _do_dates_require_warnings(from_date, to_date):
    from_warning = False
    to_warning = False
    start_year = CourtDates.min_year()
    end_year = CourtDates.max_year()
    if from_date and to_date:
        if from_date.year < start_year:
            from_warning= True
        if to_date.year > end_year:
            to_warning = True
    return from_warning, to_warning


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
    if request.method == "GET":
        form: AdvancedSearchForm = AdvancedSearchForm(request.GET)
        params: dict = request.GET
        """
        Form should be valid unless there is a critical issue
        with the submission (i.e. Month > 12)
        """
        if form.is_valid():
            context: dict = {}
            court_facets: dict = {}
            year_facets: dict = {}
            query_params: dict = {}
            query_text: str = form.cleaned_data.get("query", "")
            per_page: str = str(
                as_integer(
                    params.get("per_page", "10"),
                    minimum=1,
                    maximum=MAX_RESULTS_PER_PAGE,
                    default=RESULTS_PER_PAGE,
                )
            )
            order: str = params.get("order", "-date")

            from_date: Optional[date] = form.cleaned_data.get("from_date")
            to_date: Optional[date] = form.cleaned_data.get("to_date", None)
            # If a from_date is not specified, set it to the current min year
            if not from_date:
                from_date = date(CourtDates.min_year(), 1, 1)
            else:
                # Only provide the param back to the user if they set it
                query_params = query_params | {
                    "from": from_date,
                    "from_day":  from_date.day,
                    "from_month": getattr(from_date, "month", None),
                    "from_year": getattr(from_date, "year", None)
                    }
            # If a to_date is not specified, set it to the current min year
            if not to_date:
                to_date = date(CourtDates.max_year(), 12, 31)
            else:
                # Only provide the param back to the user if they set it
                query_params = query_params | {
                    "to": to_date,
                    "to_day":  to_date.day,
                    "to_month": to_date.month,
                    "to_year": to_date.year
                    }
            
            query_params = query_params | {
                "query": query_text,
                "court": form.cleaned_data.get("court", []),
                "judge": form.cleaned_data.get("judge", ""),
                "party": form.cleaned_data.get("party", ""),
                "order": order,
            }
            page: str = str(as_integer("1", minimum=1))
            # Merge the courts and tribunals as they are treated as the same in MarkLogic.
            courts_and_tribunals = form.cleaned_data.get("courts") + form.cleaned_data.get("tribunals")
            # Construct the search parameter object required for Marklogic query
            search_parameters: SearchParameters = SearchParameters(
                # Should process query be moved to a clean method?
                query=preprocess_query(query_text),
                court=",".join(courts_and_tribunals),
                judge=form.cleaned_data.get("judge_name", ""),
                party=form.cleaned_data.get("party_name", ""),
                page=page,
                order=params.get("order", "-date"),
                date_from=from_date,
                date_to=to_date,
                page_size=int(params.get("per_page", "10"))
                )

            # Get the response from Marklogic
            try:
                search_response: SearchResponse = search_judgments_and_parse_response(
                    api_client, search_parameters
                    )
            except MarklogicResourceNotFoundError:
                raise Http404("Search failed")

            # If a query was provided, get relevant search facets to display to the user
            if search_parameters.query:
                unprocessed_facets, court_facets = process_court_facets(
                    search_response.facets, form.cleaned_data.get("court", [])
                )
                unprocessed_facets, year_facets = process_year_facets(
                    unprocessed_facets
                )
            
            if from_date and to_date:
                requires_from_warning, requires_to_warning = _do_dates_require_warnings(from_date, to_date)

            changed_queries = {
                key: value for key, value in params.items() if value is not None
            }
            # Populate context to provide feedback about filters etc. back to user
            # TODO: Maybe separate this dictionary into it's component parts?
            context = context | {
                "court_facets": court_facets,
                "year_facets": year_facets,
                "search_results": search_response.results,
                "total": search_response.total,
                "paginator": paginator(params.get("page", "1"), search_response.total, per_page),
                "query_string": urllib.parse.urlencode(changed_queries, doseq=True),
                "order": order,
                "per_page": per_page,
                "filtered": has_filters(params),
                "page_title": _("results.search.title"),
                "show_no_exact_ncn_warning": show_no_exact_ncn_warning(search_response.results, query_text, page),
                "query_params": query_params
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
                }
            )
        else:
            # If the form has errors, return it for rendering!
            return TemplateResponse(
                request, "pages/structured_search.html", {"form": form}
        )
    else:
        # Raise an error if the user has tried any not GET HTTP requests.
        raise Http404("GET requests only")
