from config.views.template_view_with_context import TemplateViewWithContext


class SearchAndBrowseView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/search_and_browse.jinja"
    page_title = "Search and browse"
    page_canonical_url_name = "search_and_browse"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "search_and_browse"
        context["feedback_survey_type"] = "search_and_browse"
        context["page_description"] = (
            "Find the judgments and decisions you need using our search tools or browse by court and tribunal."
        )
        context["breadcrumbs"] = [
            {"text": "Search and browse"},
        ]
        context["breadcrumbs_postfix"] = "Last updated on 21 January 2026"
        return context
