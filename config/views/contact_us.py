from .template_view_with_context import TemplateViewWithContext


class ContactUsView(TemplateViewWithContext):
    template_name = "pages/contact_us.html"
    page_title = "Contact Us"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "contact_us"
        return context
