from config.views.template_view_with_context import TemplateViewWithContext


class TermsOfUseView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/terms_of_use.jinja"
    page_title = "Terms of use"
    page_canonical_url_name = "terms_of_use"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "terms_of_use"
        context["page_description"] = (
            "The terms of use page and pages it links to explains how you can use information from the Find Case Law service."
        )
        context["breadcrumbs"] = [
            {"text": "Terms of Use"},
        ]
        context["breadcrumbs_postfix"] = "Last updated on 20 August 2024"
        return context
