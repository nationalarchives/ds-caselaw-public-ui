from .template_view_with_context import TemplateViewWithContext


class TermsAndPoliciesView(TemplateViewWithContext):
    template_name = "pages/terms_and_policies.html"
    page_title = "Terms and policies"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "terms_and_policies"
        return context
