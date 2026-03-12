from config.views.template_view_with_context import TemplateViewWithContext


class PrivacyNoticeView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/privacy_notice.jinja"
    page_title = "Privacy Notice"
    page_canonical_url_name = "privacy_notice"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "privacy_notice"
        context["page_description"] = (
            "Read our privacy notice to understand more about personal data in judgments and decisions on the Find Case Law service."
        )
        context["breadcrumbs"] = [
            {"text": self.page_title},
        ]
        context["breadcrumbs_postfix"] = "Last updated on 20 August 2024"
        return context
