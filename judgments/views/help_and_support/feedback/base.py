from django.urls import reverse

from config.views.template_view_with_context import TemplateViewWithContext


class FeedbackView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/help_and_support/feedback.jinja"
    page_title = "Feedback"
    page_canonical_url_name = "feedback"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "help_and_support"
        context["feedback_survey_type"] = "feedback"
        context["page_description"] = (
            "Your feedback and experiences help us improve Find Case Law for everyone. We want to hear from everyone, whether you use the service daily or are visiting for the first time."
        )
        context["breadcrumbs"] = [
            {"text": "Help and support", "url": reverse("help_and_support")},
            {"text": "Feedback"},
        ]

        return context
