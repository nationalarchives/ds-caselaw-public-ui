import datetime
from urllib.parse import urlencode

from caselawclient.Client import MarklogicResourceNotFoundError
from caselawclient.client_helpers.search_helpers import (
    search_judgments_and_parse_response,
)
from caselawclient.search_parameters import RESULTS_PER_PAGE, SearchParameters
from django.http import Http404
from django.urls import reverse
from django.views.generic.base import TemplateView
from ds_caselaw_utils.courts import CourtNotFoundException
from ds_caselaw_utils.courts import courts as all_courts
from ds_caselaw_utils.types import CourtParam

from judgments.forms import AdvancedSearchForm
from judgments.forms.search_forms import TRIBUNAL_CHOICES
from judgments.utils import MAX_RESULTS_PER_PAGE, api_client, clamp, paginator
from judgments.utils.gtm_datalayer import GtmPageType, build_gtm_data_layer
from judgments.utils.utils import sanitise_input_to_integer


class BrowseView(TemplateView):
    template_engine = "jinja"
    template_name = "judgment/results.jinja"

    @staticmethod
    def _is_tribunal(court_query: str) -> bool:
        """Return True if court_query is a tribunal code in TRIBUNAL_CHOICES."""
        for key, value in TRIBUNAL_CHOICES.items():
            if isinstance(value, dict):
                if court_query in value:
                    return True
            elif key == court_query:
                return True
        return False

    def _build_atom_feed_url(self, court_query: str, year: int | None) -> str:
        """
        Build the Atom feed URL for browse results with court and year params.
        Browse pages can have court (which may include subdivision) and year.
        These map to feed params: court → court/tribunal, year → from_date_2/to_date_2.
        Year-only multipart date params are used so AdvancedSearchForm can default
        day/month (1 Jan / 31 Dec) when the Atom feed parses the URL.
        """
        params = {}
        if court_query:
            # TRIBUNAL_CHOICES nests some codes under group headings, so check nested
            # values as well as top-level keys.
            if self._is_tribunal(court_query):
                params["tribunal"] = court_query
            else:
                params["court"] = court_query
        if year:
            params["from_date_2"] = str(year)
            params["to_date_2"] = str(year)

        query_string = urlencode(params, doseq=True) if params else ""
        feed_path = reverse("search-feed")
        return f"{feed_path}?{query_string}" if query_string else feed_path

    def _build_alternates(self, atom_feed_url: str) -> list:
        """Build alternates list with single Atom feed entry."""
        return [
            {
                "type": "application/atom+xml",
                "href": atom_feed_url,
            }
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        court: str | None = self.kwargs.get("court")
        subdivision: str | None = self.kwargs.get("subdivision")
        year: int | None = self.kwargs.get("year")

        # All non-None values of court and subdivision should be truthy
        court_query = "/".join(filter(None, [court, subdivision]))
        page = clamp(sanitise_input_to_integer(self.request.GET.get("page"), 1), minimum=1)
        per_page = clamp(
            sanitise_input_to_integer(self.request.GET.get("per_page"), RESULTS_PER_PAGE),
            minimum=1,
            maximum=MAX_RESULTS_PER_PAGE,
        )

        context["form"] = AdvancedSearchForm(self.request.GET)

        try:
            search_parameters = SearchParameters(
                court=court_query if court_query else None,
                date_from=(datetime.date(year=year, month=1, day=1).strftime("%Y-%m-%d") if year else None),
                date_to=(datetime.date(year=year, month=12, day=31).strftime("%Y-%m-%d") if year else None),
                order="-date",
                page=page,
                page_size=per_page,
            )
            search_response = search_judgments_and_parse_response(api_client, search_parameters)

            context["query"] = self.request.GET.get("query", "")
            context["search_results"] = search_response.results
            context["total"] = search_response.total
            context["per_page"] = per_page
            context["paginator"] = paginator(page, search_response.total, per_page)
            context["courts"] = all_courts.get_grouped_selectable_courts()
            context["tribunals"] = all_courts.get_grouped_selectable_tribunals()
            context["page_title"] = "Search results"

            # Build feed URL and alternates for this browse view
            atom_feed_url = self._build_atom_feed_url(court_query, year)
            context["atom_feed_url"] = atom_feed_url
            context["alternates"] = self._build_alternates(atom_feed_url)

        except MarklogicResourceNotFoundError:
            raise Http404("Search failed")  # TODO: This should be something else!

        context["feedback_survey_tribunal"] = self.kwargs.get("tribunal")
        context["feedback_survey_type"] = "browse"
        context["feedback_survey_court"] = court_query

        court_for_analytics = None
        if court_query:
            try:
                court_for_analytics = all_courts.get_by_param(CourtParam(court_query))
            except CourtNotFoundException:
                pass

        context["gtm_data_layer"] = build_gtm_data_layer(
            page_type=GtmPageType.BROWSE,
            court=court_for_analytics,
        )

        return context
