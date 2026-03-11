from config.views.template_view_with_context import TemplateViewWithContext


class UnderstandingCaseLawView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/understanding_case_law.jinja"
    page_title = "Understanding case law"
    page_canonical_url_name = "understanding_case_law"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "understanding_case_law"
        context["feedback_survey_type"] = "understanding_case_law"
        context["page_description"] = (
            "If you're new to legal information, we’ll help you understand how case law works and how to read court judgments."
        )
        context["breadcrumbs"] = [
            {"text": "Understanding case law"},
        ]
        context["breadcrumbs_postfix"] = "Last updated 8 January 2026"
        return context
