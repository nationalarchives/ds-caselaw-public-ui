from django.urls import reverse
from ds_caselaw_utils import courts

from config.views.template_view_with_context import TemplateViewWithContext


class CourtsAndCoverageView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/about_this_service/courts_and_coverage.jinja"
    page_title = "Courts and coverage"
    page_canonical_url_name = "courts_and_coverage"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courts"] = courts.get_grouped_selectable_courts()
        context["active_navigation_endpoint"] = "about_this_service"
        context["feedback_survey_type"] = "courts_and_coverage"
        context["page_description"] = (
            "Find Case Law publishes judgments and decisions from courts and tribunals in England and Wales."
        )
        context["breadcrumbs"] = [
            {"url": reverse("about_this_service"), "text": "About this service"},
            {"text": "Courts and coverage"},
        ]
        return context
