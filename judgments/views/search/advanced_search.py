from django.urls import reverse
from ds_caselaw_utils import courts

from config.views.template_view_with_context import TemplateViewWithContext
from judgments.forms import AdvancedSearchForm


class AdvancedSearchView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/advanced_search.jinja"

    page_canonical_url_name = "advanced_search"
    page_title = "Advanced search"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_description"] = (
            "Search the Find Case Law service using filters such as date ranges, courts and names of parties and judges."
        )
        context["courts"] = courts.get_grouped_selectable_courts()
        context["tribunals"] = courts.get_grouped_selectable_tribunals()
        context["active_navigation_endpoint"] = "search_and_browse"
        context["feedback_survey_type"] = "advanced_search"
        context["form"] = AdvancedSearchForm(self.request.GET)
        context["query"] = self.request.GET.get("query", "")
        context["breadcrumbs_variant"] = "accent"
        context["breadcrumbs"] = [
            {"text": "Search and browse", "url": reverse("search_and_browse")},
            {"text": self.page_title},
        ]

        return context
