from .template_view_with_context import TemplateViewWithContext


class PrivacyNotice(TemplateViewWithContext):
    template_name = "pages/privacy_notice.html"
    page_title = "Privacy Notice"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "privacy_notice"
        return context
