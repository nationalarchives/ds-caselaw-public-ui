from .template_view_with_context import TemplateViewWithContext


class OpenJusticeLicenceView(TemplateViewWithContext):
    template_name = "pages/open_justice_licence.html"
    page_title = "Open Justice Licence"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "license"
        return context
