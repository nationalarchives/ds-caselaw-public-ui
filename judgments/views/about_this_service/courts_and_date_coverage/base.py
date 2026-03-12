from django.urls import reverse

from config.views.template_view_with_context import TemplateViewWithContext


class CourtsAndDateCoverageView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/about_this_service/courts_and_date_coverage.jinja"
    page_title = "Courts and date coverage"
    page_canonical_url_name = "courts_and_date_coverage"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "about_this_service"
        context["feedback_survey_type"] = "courts_and_date_coverage"
        context["page_description"] = (
            "Different courts and tribunals have different coverage on Find Case Law. Some have comprehensive recent records, while others include selected historical judgments."
        )
        context["breadcrumbs"] = [
            {"text": "About this service", "url": reverse("about_this_service")},
            {"text": "Courts and date coverage"},
        ]

        return context
