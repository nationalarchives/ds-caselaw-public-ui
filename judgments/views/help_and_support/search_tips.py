from django.urls import reverse

from config.views.template_view_with_context import TemplateViewWithContext


class SearchTipsView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/help_and_support/search_tips.jinja"
    page_title = "Search tips"
    page_canonical_url_name = "search_tips"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "help_and_support"
        context["feedback_survey_type"] = "search_tips"
        context["page_description"] = (
            "Search court judgments and tribunal decisions in Find Case Law using the search box on the homepage of this website."
        )
        context["breadcrumbs"] = [
            {"text": "Help and support", "url": reverse("help_and_support")},
            {"text": "Search tips"},
        ]

        return context
