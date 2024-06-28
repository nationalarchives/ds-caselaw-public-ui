from caselawclient.Client import MarklogicResourceNotFoundError
from caselawclient.client_helpers.search_helpers import (
    search_judgments_and_parse_response,
)
from caselawclient.search_parameters import SearchParameters
from django.http import Http404
from django.views.generic import TemplateView
from ds_caselaw_utils import courts as all_courts

from judgments.forms import AdvancedSearchForm
from judgments.utils import api_client


class IndexView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            search_response = search_judgments_and_parse_response(
                api_client, SearchParameters(order="-date")
            )
            search_results = search_response.results
            context["recent_judgments"] = search_results

        except MarklogicResourceNotFoundError:
            raise Http404(
                "Search results not found"
            )  # TODO: This should be something else!

        context["courts"] = all_courts.get_listable_courts()
        context["tribunals"] = all_courts.get_listable_tribunals()
        context["feedback_survey_type"] = "home"
        context["form"] = AdvancedSearchForm()

        return context
