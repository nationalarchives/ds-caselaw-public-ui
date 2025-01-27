from django.urls import reverse
from ds_caselaw_utils import courts

from .template_view_with_context import TemplateViewWithContext


class CourtsTribunalsListView(TemplateViewWithContext):
    """List view for all courts and tribunals in the Find Case Law database."""

    template_name = "pages/courts_and_tribunals.html"
    page_title = "Types of courts in England and Wales"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courts"] = courts.get_grouped_selectable_courts()
        context["tribunals"] = courts.get_grouped_selectable_tribunals()
        context["feedback_survey_type"] = "courts_and_tribunals"
        context["breadcrumbs"] = [
            {"text": self.page_title},
        ]

        return context


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
