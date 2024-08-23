from .template_view_with_context import TemplateViewWithContext
from ds_caselaw_utils import courts


class CourtsAndTribunalsInFclView(TemplateViewWithContext):
    template_name = "pages/courts_and_tribunals_in_fcl.html"
    page_title = "Courts and tribunals in Find Case Law"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courts"] = courts.get_listable_groups()
        context["feedback_survey_type"] = "courts_and_tribunals_in_fcl"
        return context
