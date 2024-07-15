from .template_view_with_context import TemplateViewWithContext


class PublishingPolicyView(TemplateViewWithContext):
    template_name = "pages/publishing_policy.html"
    page_title = "publishing_policy.title"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "publishing_policy"
        return context
