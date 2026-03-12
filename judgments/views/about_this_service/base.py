from config.views.template_view_with_context import TemplateViewWithContext


class AboutThisServiceView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/about_this_service.jinja"
    page_title = "About this service"
    page_canonical_url_name = "about_this_service"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "about_this_service"
        context["feedback_survey_type"] = "about_this_service"
        context["page_description"] = (
            "The Find Case Law service provides free access to judgments and decisions made in England and Wales from 2001 onwards."
        )
        context["breadcrumbs"] = [
            {"text": self.page_title},
        ]
        return context
