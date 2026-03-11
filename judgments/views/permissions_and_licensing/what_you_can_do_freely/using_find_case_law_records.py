from django.urls import reverse

from config.views.template_view_with_context import TemplateViewWithContext


class UsingFindCaseLawRecordsView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/permissions_and_licensing/what_you_can_do_freely/using_find_case_law_records.jinja"
    page_title = "Using Find Case Law records"
    page_canonical_url_name = "using_find_case_law_records"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "permissions_and_licensing"
        context["feedback_survey_type"] = "using_find_case_law_records"
        context["page_description"] = (
            "You can freely use judgments from Find Case Law for most purposes without permission or payment. This page explains what you can do and gives practical examples."
        )
        context["breadcrumbs"] = [
            {"text": "Permissions and Licensing", "url": reverse("permissions_and_licensing")},
            {"text": "What you can do freely", "url": reverse("what_you_can_do_freely")},
            {"text": "Using Find Case Law records"},
        ]

        return context
