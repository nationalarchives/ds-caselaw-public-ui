from django.urls import reverse

from config.views.template_view_with_context import TemplateViewWithContext


class BrowseCourtsAndTribunalsView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/search_and_browse/browse_courts_and_tribunals.jinja"
    page_title = "Browse courts and tribunals"
    page_canonical_url_name = "browse_courts_and_tribunals"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "search_and_browse"
        context["feedback_survey_type"] = "browse_courts_and_tribunals"
        context["page_description"] = (
            "Explore judgments by court or tribunal type. This helps you understand what’s available and find cases from specific jurisdictions."
        )
        context["breadcrumbs"] = [
            {"text": "Search and browse", "url": reverse("search_and_browse")},
            {"text": "Browse courts and tribunals"},
        ]

        return context
