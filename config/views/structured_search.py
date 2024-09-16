from ds_caselaw_utils import courts

from judgments.forms import AdvancedSearchForm

from .template_view_with_context import TemplateViewWithContext


class StructuredSearchView(TemplateViewWithContext):
    template_name = "pages/structured_search.html"
    page_title = "structured_search.title"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courts"] = courts.get_grouped_selectable_courts()
        context["tribunals"] = courts.get_grouped_selectable_tribunals()
        context["feedback_survey_type"] = "structured_search"
        context["form"] = AdvancedSearchForm()
        return context
