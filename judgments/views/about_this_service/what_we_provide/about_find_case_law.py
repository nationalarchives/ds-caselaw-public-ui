from django.urls import reverse

from config.views.template_view_with_context import TemplateViewWithContext


class AboutFindCaseLawView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/about_this_service/what_we_provide/about_find_case_law.jinja"
    page_title = "About Find Case Law"
    page_canonical_url_name = "about_find_case_law"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "about_this_service"
        context["feedback_survey_type"] = "about_find_case_law"
        context["page_description"] = (
            "Find Case Law is the official public source for judgments and decisions from courts and tribunals in England and Wales. We provide free access to judgments to support open justice, legal practice, research and public understanding."
        )
        context["breadcrumbs"] = [
            {"text": "About this service", "url": reverse("about_this_service")},
            {"text": "What we provide", "url": reverse("what_we_provide")},
            {"text": "About Find Case Law"},
        ]

        return context
