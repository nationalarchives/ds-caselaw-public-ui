from ds_caselaw_utils import courts

from .template_view_with_context import TemplateViewWithContext


class AboutThisServiceView(TemplateViewWithContext):
    template_name = "pages/about_this_service.html"
    page_title = "About this service"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courts"] = courts.get_listable_groups()
        context["feedback_survey_type"] = "support"
        return context
