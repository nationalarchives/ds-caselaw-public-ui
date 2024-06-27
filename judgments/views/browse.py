import datetime
from typing import Union

from caselawclient.Client import MarklogicResourceNotFoundError
from caselawclient.client_helpers.search_helpers import (
    search_judgments_and_parse_response,
)
from caselawclient.search_parameters import RESULTS_PER_PAGE, SearchParameters
from django.http import Http404
from django.utils.translation import gettext
from django.views.generic.base import TemplateView
from ds_caselaw_utils import courts as all_courts

from judgments.utils import MAX_RESULTS_PER_PAGE, api_client, as_integer, paginator
from judgments.utils.utils import sanitise_input_to_integer


class BrowseView(TemplateView):
    template_name = "judgment/results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        court: Union[str, None] = self.kwargs.get("court")
        subdivision: Union[str, None] = self.kwargs.get("subdivision")
        year: Union[int, None] = self.kwargs.get("year")

        # All non-None values of court and subdivision should be truthy
        court_query = "/".join(filter(None, [court, subdivision]))
        page = as_integer(
            sanitise_input_to_integer(self.request.GET.get("page"), 1), minimum=1
        )
        per_page = as_integer(
            sanitise_input_to_integer(
                self.request.GET.get("per_page"), RESULTS_PER_PAGE
            ),
            minimum=1,
            maximum=MAX_RESULTS_PER_PAGE,
        )

        try:
            search_parameters = SearchParameters(
                court=court_query if court_query else None,
                date_from=(
                    datetime.date(year=year, month=1, day=1).strftime("%Y-%m-%d")
                    if year
                    else None
                ),
                date_to=(
                    datetime.date(year=year, month=12, day=31).strftime("%Y-%m-%d")
                    if year
                    else None
                ),
                order="-date",
                page=page,
                page_size=per_page,
            )
            search_response = search_judgments_and_parse_response(
                api_client, search_parameters
            )

            context["search_results"] = search_response.results
            context["total"] = search_response.total
            context["per_page"] = per_page
            context["paginator"] = paginator(page, search_response.total, per_page)
            context["courts"] = all_courts.get_grouped_selectable_courts()
            context["tribunals"] = all_courts.get_grouped_selectable_tribunals()
            context["page_title"] = gettext("results.search.title")

        except MarklogicResourceNotFoundError:
            raise Http404("Search failed")  # TODO: This should be something else!

        context["feedback_survey_type"] = "browse"
        context["feedback_survey_court"] = court_query

        return context
