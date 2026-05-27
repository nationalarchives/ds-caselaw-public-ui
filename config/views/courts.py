import logging

from caselawclient.Client import MarklogicResourceNotFoundError
from caselawclient.client_helpers.search_helpers import (
    search_judgments_and_parse_response,
)
from caselawclient.search_parameters import SearchParameters
from django.http import Http404
from django.urls import reverse
from django.utils.functional import cached_property
from ds_caselaw_utils import courts
from ds_caselaw_utils.courts import CourtNotFoundException
from requests.exceptions import RequestException

from judgments.models.court_dates import CourtDates
from judgments.utils import (
    api_client,
)

from .template_view_with_context import TemplateViewWithContext


class CourtsTribunalsListView(TemplateViewWithContext):
    """List view for all courts and tribunals in the Find Case Law database."""

    template_engine = "jinja"
    template_name = "pages/courts_and_tribunals.jinja"
    page_title = "Types of courts in England and Wales"
    page_allow_index = True

    def decorate_court_group(self, group):
        """
        Updates the start_year and end_year with data from CourtDates if available.
        """

        date_map = {
            date.pk: date
            for date in CourtDates.objects.filter(pk__in=[court.canonical_param for court in group.courts])
        }

        for court in group.courts:
            dates = date_map.get(court.canonical_param)

            if dates:
                court.start_year = dates.start_year
                court.end_year = dates.end_year

        return group

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        grouped_courts = [self.decorate_court_group(group) for group in courts.get_grouped_selectable_courts()]
        grouped_tribunals = [self.decorate_court_group(group) for group in courts.get_grouped_selectable_tribunals()]

        context["courts"] = grouped_courts
        context["tribunals"] = grouped_tribunals
        context["feedback_survey_type"] = "courts_and_tribunals"
        context["active_navigation_endpoint"] = "search_and_browse"
        context["breadcrumbs"] = [
            {"text": "Search and browse", "url": reverse("search_and_browse")},
            {"text": self.page_title},
        ]

        return context


class CourtOrTribunalView(TemplateViewWithContext):
    """Individual view for a specific court or tribunal landing page."""

    template_engine = "jinja"
    template_name = "pages/court_or_tribunal.jinja"
    page_allow_index = True

    @property
    def page_title(self):
        return self.court.name

    @cached_property
    def court(self):
        try:
            return courts.get_by_param(self.kwargs["param"])
        except CourtNotFoundException:
            raise Http404("Court not found")

    def _get_search_response(self, search_parameters):
        try:
            return search_judgments_and_parse_response(api_client, search_parameters)
        except (MarklogicResourceNotFoundError, RequestException) as error:
            logging.warn(f"Error fetching judgments for {self.court.name}: {error}")

            return []

    def get_context_data(self, **kwargs):

        court = self.court

        context = super().get_context_data(**kwargs)

        search_parameters: SearchParameters = SearchParameters(
            court=court.canonical_param, page=1, order="-date", page_size=5
        )

        search_response = self._get_search_response(search_parameters)

        context["documents"] = search_response.results
        context["feedback_survey_type"] = "court_or_tribunal_%s" % court.canonical_param
        context["court"] = court
        context["active_navigation_endpoint"] = "search_and_browse"
        context["breadcrumbs"] = [
            {"url": reverse("search_and_browse"), "text": "Search and browse"},
            {"url": reverse("courts_and_tribunals"), "text": "Types of courts in England and Wales"},
            {"text": self.page_title},
        ]

        return context
