from ds_caselaw_utils import courts

from config.views.template_view_with_context import TemplateViewWithContext
from judgments.forms import AdvancedSearchForm


class AdvancedSearchView(TemplateViewWithContext):
    template_name = "pages/advanced_search.html"
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
        context["feedback_survey_type"] = "advanced_search"
        context["form"] = AdvancedSearchForm(self.request.GET)
        context["breadcrumbs"] = [
            {"text": self.page_title},
        ]

        return context


class AdvancedSearchViewJinja(AdvancedSearchView):
    template_engine = "jinja"
    template_name = "pages/advanced_search.jinja"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = context["form"]
        context["query"] = form.data.get("query", "")

        return context
