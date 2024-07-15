from .template_view_with_context import TemplateViewWithContext


class HowToUseThisService(TemplateViewWithContext):
    template_name = "pages/how_to_use_this_service.html"
    page_title = "howtousethisservice.title"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "support"
        return context
