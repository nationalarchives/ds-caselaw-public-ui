from django.urls import reverse
from ds_caselaw_utils import courts

from judgments.models.court_dates import CourtDates

from .template_view_with_context import TemplateViewWithContext


class CourtsTribunalsListView(TemplateViewWithContext):
    """List view for all courts and tribunals in the Find Case Law database."""

    template_name = "pages/courts_and_tribunals.html"
    page_title = "Types of courts in England and Wales"
    page_allow_index = True

    def decorate_court_group(self, group):
        """
        Updates the start_year and end_year with data from CourtDates if available.
        Updates the description_text_as_html with the updated dates if they are available..
        """

        date_map = {
            date.pk: date
            for date in CourtDates.objects.filter(pk__in=[court.canonical_param for court in group.courts])
        }

        for court in group.courts:
            dates = date_map.get(court.canonical_param)

            if dates:
                court.description_text_as_html = court.render_markdown_text(
                    "description", {"start_year": dates.start_year, "end_year": dates.end_year}
                )
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
        context["breadcrumbs"] = [
            {"text": self.page_title},
        ]

        return context


class CourtsTribunalsListJinjaView(CourtsTribunalsListView):
    template_engine = "jinja"
    template_name = "pages/courts_and_tribunals.jinja"


class CourtOrTribunalView(TemplateViewWithContext):
    """Individual view for a specific court or tribunal landing page."""

    template_name = "pages/court_or_tribunal.html"
    page_allow_index = True

    @property
    def page_title(self):
        return self.court.name

    @property
    def court(self):
        return courts.get_by_param(self.kwargs["param"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["feedback_survey_type"] = "court_or_tribunal_%s" % self.court.canonical_param
        context["court"] = self.court
        context["breadcrumbs"] = [
            {"url": reverse("courts_and_tribunals"), "text": "Types of courts in England and Wales"},
            {"text": self.page_title},
        ]

        return context


class CourtOrTribunalViewJinja(CourtOrTribunalView):
    template_engine = "jinja"
    template_name = "pages/court_or_tribunal.jinja"
