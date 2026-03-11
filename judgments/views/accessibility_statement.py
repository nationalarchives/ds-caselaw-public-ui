from config.views.template_view_with_context import TemplateViewWithContext


class AccessibilityStatementView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/accessibility_statement.jinja"
    page_title = "Accessibility statement for Find Case Law"
    page_canonical_url_name = "accessibility_statement"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "accessibility_statement"
        context["page_description"] = (
            "Find out how accessible the Find Case Law service is by reading our accessibility statement. It is important that everyone can use this service."
        )
        context["breadcrumbs"] = [
            {"text": self.page_title},
        ]
        context["breadcrumbs_postfix"] = "Last updated on 30 July 2025"
        return context
