from django.urls import reverse

from config.views.template_view_with_context import TemplateViewWithContext


class UserResearchView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/help_and_support/feedback/user_research.jinja"
    page_title = "User research"
    page_canonical_url_name = "user_research"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "help_and_support"
        context["page_description"] = ""
        context["breadcrumbs"] = [
            {"text": "Help and support", "url": reverse("help_and_support")},
            {"text": "Feedback", "url": reverse("feedback")},
            {"text": "User research"},
        ]
        context["breadcrumbs_postfix"] = "Last updated on 3 July 2025"
        return context
