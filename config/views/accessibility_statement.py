from .template_view_with_context import TemplateViewWithContext


class AccessibilityStatementView(TemplateViewWithContext):
    template_name = "pages/accessibility_statement.html"
    page_title = "accessibilitystatement.title"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "support"
        return context
