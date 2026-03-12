from django.urls import reverse
from ds_caselaw_utils import courts

from config.views.template_view_with_context import TemplateViewWithContext


class CourtsAndTribunalsInFclView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/about_this_service/courts_and_date_coverage/courts_and_tribunals_in_fcl.jinja"
    page_title = "Courts and tribunals in Find Case Law"
    page_canonical_url_name = "courts_and_tribunals_in_fcl"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courts"] = courts.get_grouped_selectable_courts()
        context["active_navigation_endpoint"] = "about_this_service"
        context["feedback_survey_type"] = "courts_and_tribunals_in_fcl"
        context["page_description"] = (
            "Find out which courts and tribunals publish judgments and decisions on the Find Case Law service."
        )
        context["breadcrumbs"] = [
            {"url": reverse("about_this_service"), "text": "About this service"},
            {"url": reverse("courts_and_date_coverage"), "text": "Courts and date coverage"},
            {"text": "Courts and tribunals in Find Case Law"},
        ]
        context["breadcrumbs_postfix"] = "Last updated on 21 January 2025"
        return context
