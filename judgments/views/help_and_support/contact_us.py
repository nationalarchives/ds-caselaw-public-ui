from django.urls import reverse

from config.views.template_view_with_context import TemplateViewWithContext


class ContactUsView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/help_and_support/contact_us.jinja"
    page_title = "Contact Us"
    page_canonical_url_name = "contact_us"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "help_and_support"
        context["feedback_survey_type"] = "contact_us"
        context["page_description"] = (
            "Find out how to get in touch with us to ask a question or report a problem to the Find Case Law service team."
        )
        context["breadcrumbs"] = [
            {"url": reverse("help_and_support"), "text": "Help and support"},
            {"text": "Contact us"},
        ]
        context["breadcrumbs_postfix"] = "Last updated on 21 January 2025"
        return context
