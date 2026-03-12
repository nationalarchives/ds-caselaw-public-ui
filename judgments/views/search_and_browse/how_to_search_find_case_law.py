from django.urls import reverse

from config.views.template_view_with_context import TemplateViewWithContext


class HowToSearchFindCaseLawView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/search_and_browse/how_to_search_find_case_law.jinja"
    page_title = "How to search Find Case Law"
    page_canonical_url_name = "how_to_search_find_case_law"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "help_and_support"
        context["feedback_survey_type"] = "how_to_search_find_case_law"
        context["page_description"] = (
            "Help and guidance on how to search judgments and decisions on the Find Case Law service using the search box and filters."
        )
        context["breadcrumbs"] = [
            {"url": reverse("search_and_browse"), "text": "Search and Browse"},
            {"text": "How to search Find Case Law"},
        ]
        context["breadcrumbs_postfix"] = "Last updated on 21 January 2025"
        return context
