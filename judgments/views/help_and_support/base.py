from config.views.template_view_with_context import TemplateViewWithContext


class HelpAndSupportView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/help_and_support.jinja"
    page_title = "Help and Support"
    page_canonical_url_name = "help_and_support"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "help_and_support"
        context["feedback_survey_type"] = "help_and_support"
        context["page_description"] = (
            "Get help using Find Case Law, report problems and share your feedback to help us improve the service."
        )
        context["breadcrumbs"] = [
            {"text": "Help and support"},
        ]

        return context
