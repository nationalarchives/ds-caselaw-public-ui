from django.urls import reverse

from config.views.template_view_with_context import TemplateViewWithContext


class ReadingJudgmentsView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/understanding_case_law/reading_judgments.jinja"
    page_title = "Reading judgments"
    page_canonical_url_name = "reading_judgments"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "understanding_case_law"
        context["feedback_survey_type"] = "reading_judgments"
        context["page_description"] = (
            "Court judgments can seem complicated if you haven't read them before. We’ll help you understand how judgments are structured and how to find the information you need."
        )
        context["breadcrumbs"] = [
            {"url": reverse("understanding_case_law"), "text": "Understanding case law"},
            {"text": "Reading judgments"},
        ]
        context["breadcrumbs_postfix"] = "Last updated on 19 February 2026"
        return context
