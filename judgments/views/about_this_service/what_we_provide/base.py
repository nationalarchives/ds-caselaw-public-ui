from django.urls import reverse

from config.views.template_view_with_context import TemplateViewWithContext


class WhatWeProvideView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/about_this_service/what_we_provide.jinja"
    page_title = "What we provide"
    page_canonical_url_name = "what_we_provide"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "about_this_service"
        context["feedback_survey_type"] = "what_we_provide"
        context["page_description"] = (
            "Find Case Law focuses on providing judgments and decisions from courts and tribunals in England and Wales. Understanding what we include – and what we don't – helps you know what to expect when searching."
        )
        context["breadcrumbs"] = [
            {"text": "About this service", "url": reverse("about_this_service")},
            {"text": "What we provide"},
        ]

        return context
