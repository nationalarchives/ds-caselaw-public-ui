from django.urls import reverse

from config.views.template_view_with_context import TemplateViewWithContext


class UnderstandingJudgmentsAndDecisionsView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/understanding_case_law/reading_judgments/understanding_judgments_and_decisions.jinja"
    page_title = "Understanding judgments and decisions"
    page_canonical_url_name = "understanding_judgments_and_decisions"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "understanding_case_law"
        context["feedback_survey_type"] = "understanding_judgments_and_decisions"
        context["page_description"] = (
            "A basic overview of what a judgment is and how they are commonly structured to help people reading a judgment for the first time."
        )
        context["breadcrumbs"] = [
            {"url": reverse("understanding_case_law"), "text": "Understanding Case Law"},
            {"url": reverse("reading_judgments"), "text": "Reading judgments"},
            {"text": "Understanding judgments and decisions"},
        ]
        context["breadcrumbs_postfix"] = "Last updated on 21 January 2025"
        return context
