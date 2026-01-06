import urllib
from datetime import date
from typing import Any, Optional

from caselawclient.Client import MarklogicResourceNotFoundError
from caselawclient.client_helpers.search_helpers import (
    search_judgments_and_parse_response,
)
from caselawclient.search_parameters import SearchParameters
from django.conf import settings
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from requests.exceptions import RequestException

from config.views.template_view_with_context import TemplateViewWithContext
from judgments.forms import AdvancedSearchForm
from judgments.utils import (
    api_client,
    get_minimum_warning_year,
    has_filters,
    paginator,
    process_court_facets,
    process_year_facets,
    show_no_exact_ncn_warning,
)
from judgments.utils.search_request_to_parameters import search_request_to_parameters


@method_decorator(csrf_exempt, name="dispatch")
class SearchResultsView(TemplateViewWithContext):
    """
    Handles any searches made in the application

    * Given a valid search form, query Marklogic and return the results
    * Given an invalid search form, render it again with the errors
    * Given GET request without form submission return an empty form
    * Given anything except an HTTP GET request raise an error
    """

    template_engine = "jinja"
    template_name = "judgment/results.jinja"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form: AdvancedSearchForm = AdvancedSearchForm(request.GET)
        if not form.is_valid():
            return TemplateResponse(
                request,
                "pages/advanced_search.jinja",
                {"form": form, "query": request.GET.get("query", "")},
                using="jinja",
            )

        search_parameters: SearchParameters = search_request_to_parameters(request)
        context = self._initialize_context(form)

        search_response = self._get_search_response(request, search_parameters, context)
        if isinstance(search_response, TemplateResponse):
            return search_response

        query_params = self._build_query_params(form, search_parameters)

        (
            court_facets,
            tribunal_facets,
            year_facets,
            requires_warning,
            warning,
            changed_queries,
        ) = self._process_facets_and_warnings(request, form, search_parameters, search_response)

        context.update(
            {
                "query": request.GET.get("query", ""),
                "requires_from_warning": requires_warning,
                "date_warning": warning,
                "earliest_record": get_minimum_warning_year(),
                "court_facets": court_facets,
                "tribunal_facets": tribunal_facets,
                "year_facets": year_facets,
                "search_results": search_response.results,
                "total": int(search_response.total),
                "paginator": paginator(search_parameters.page, search_response.total, search_parameters.page_size),
                "query_string": urllib.parse.urlencode(changed_queries, doseq=True),
                "order": search_parameters.order,
                "per_page": search_parameters.page_size,
                "page": search_parameters.page,
                "filtered": has_filters(self.request.GET),
                "page_title": "Search Results",
                "show_no_exact_ncn_warning": show_no_exact_ncn_warning(
                    search_response.results, search_parameters.query or "", search_parameters.page
                ),
                "query_params": query_params,
                "query_param_string": urllib.parse.urlencode(form.cleaned_data, doseq=True),
                "breadcrumbs": self._build_breadcrumbs(search_parameters),
            }
        )

        return self.render_to_response(context)

    def _initialize_context(self, form):
        context = {}
        context["form"] = form
        context["feedback_survey_type"] = "advanced_search_filters_applied"
        return context

    def _get_search_response(self, request, search_parameters, context):
        try:
            return search_judgments_and_parse_response(api_client, search_parameters)
        except (MarklogicResourceNotFoundError, RequestException):
            context["breadcrumbs"] = self._build_breadcrumbs(search_parameters)
            return TemplateResponse(request, "judgment/results_error.html", context)

    def _build_query_params(self, form, search_parameters):
        from_date: Optional[date] = form.cleaned_data.get("from_date")
        to_date: Optional[date] = form.cleaned_data.get("to_date")
        query_params: dict[str, Any] = {}
        if from_date:
            query_params |= {
                "from_date_0": from_date.day,
                "from_date_1": from_date.month,
                "from_date_2": from_date.year,
            }
        if to_date:
            query_params |= {
                "to_date_0": to_date.day,
                "to_date_1": to_date.month,
                "to_date_2": to_date.year,
            }
        query_params |= {
            "query": search_parameters.query,
            "court": form.cleaned_data.get("court", []),
            "tribunal": form.cleaned_data.get("tribunal", []),
            "judge": form.cleaned_data.get("judge", ""),
            "party": form.cleaned_data.get("party", ""),
            "order": search_parameters.order,
            "page": search_parameters.page,
        }
        return query_params

    def _process_facets_and_warnings(self, request, form, search_parameters, search_response):
        courts_and_tribunals = form.cleaned_data.get("court", []) + form.cleaned_data.get("tribunal", [])
        if search_parameters.query:
            (
                unprocessed_facets,
                court_facets,
                tribunal_facets,
            ) = process_court_facets(search_response.facets, courts_and_tribunals)
            unprocessed_facets, year_facets = process_year_facets(unprocessed_facets)
        else:
            unprocessed_facets, court_facets, tribunal_facets, year_facets = ({}, {}, {}, {})

        params = request.GET
        changed_queries = {}
        for key in params:
            values = params.getlist(key)
            if values and key != "page":
                changed_queries[key] = values

        min_actual_year = min([int(x) for x in year_facets.keys()]) if year_facets else None
        requires_warning, warning = self._do_dates_require_warnings(
            search_parameters.date_from, int(search_response.total), min_actual_year
        )

        return (court_facets, tribunal_facets, year_facets, requires_warning, warning, changed_queries)

    def _build_breadcrumbs(self, search_parameters):
        if search_parameters.query:
            return [{"text": f'Search results for "{search_parameters.query}"'}]
        else:
            return [{"text": "Search results"}]

    def _do_dates_require_warnings(
        self, iso_date: Optional[str], total_results: int, min_actual_year: Optional[int]
    ) -> tuple[bool, Optional[str]]:
        """
        Check if users have requested a year before what we have available,
        if it is, then we provide a warning letting them know.
        """
        min_year = get_minimum_warning_year()

        if not iso_date:
            return False, None
        from_date = date.fromisoformat(iso_date)
        # If the date is 1085, then that's the default, the user hasn't typed in
        # a non-sensical answer, don't warn about it.
        if from_date.year == settings.MINIMUM_ALLOWED_YEAR:
            return False, None
        if not from_date.year or total_results == 0 or from_date.year >= min_year:
            return False, None

        from_warning = True
        warning = f"""
                {from_date.year} is before {min_year},
                the date of the oldest record on the Find Case Law service.
                """

        if min_actual_year:
            warning += f"Showing matching results from {min_actual_year}. "

        return from_warning, warning
