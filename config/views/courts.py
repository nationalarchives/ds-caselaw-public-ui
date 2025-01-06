from caselawclient.client_helpers.search_helpers import (
    search_judgments_and_parse_response,
)
from caselawclient.search_parameters import RESULTS_PER_PAGE, SearchParameters
from ds_caselaw_utils import courts

from judgments.utils import api_client, clamp, paginator
from judgments.utils.utils import sanitise_input_to_integer

from .template_view_with_context import TemplateViewWithContext


class CourtsTribunalsListView(TemplateViewWithContext):
    """List view for all courts and tribunals in the Find Case Law database."""

    template_name = "pages/courts_and_tribunals.html"
    page_title = "Judgments and decisions by court or tribunal"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courts"] = courts.get_grouped_selectable_courts()
        context["tribunals"] = courts.get_grouped_selectable_tribunals()
        context["feedback_survey_type"] = "courts_and_tribunals"
        return context


class CourtOrTribunalView(TemplateViewWithContext):
    """Individual view for a specific court or tribunal."""

    template_name = "pages/court_or_tribunal.html"

    @property
    def page_title(self):
        return "Judgments for %s" % self.court.name

    @property
    def court(self):
        return courts.get_by_param(self.kwargs["param"])

    @property
    def page(self):
        return clamp(sanitise_input_to_integer(self.request.GET.get("page"), 1), minimum=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_response = search_judgments_and_parse_response(
            api_client,
            SearchParameters(court=self.court.canonical_param, order="-date", page=self.page),
        )

        context["feedback_survey_type"] = "court_or_tribunal_%s" % self.court.canonical_param
        context["request"] = self.request
        context["court"] = self.court
        context["judgments"] = search_response.results
        context["paginator"] = paginator(self.page, search_response.total, RESULTS_PER_PAGE)

        return context
