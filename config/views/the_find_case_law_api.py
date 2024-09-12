from .template_view_with_context import TemplateViewWithContext


class TheFindCaseLawApiView(TemplateViewWithContext):
    template_name = "pages/the_find_case_law_api.html"
    page_title = "The Find Case Law API"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "the_find_case_law_api"
        return context
