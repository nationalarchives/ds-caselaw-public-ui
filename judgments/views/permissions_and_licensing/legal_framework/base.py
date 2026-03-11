from django.urls import reverse

from config.views.template_view_with_context import TemplateViewWithContext


class LegalFrameworkView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/permissions_and_licensing/legal_framework.jinja"
    page_title = "Legal framework"
    page_canonical_url_name = "legal_framework"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "permissions_and_licensing"
        context["feedback_survey_type"] = "legal_framework"
        context["page_description"] = (
            "Here are the legal and technical details of how Find Case Law judgments can be used and licensed."
        )
        context["breadcrumbs"] = [
            {"text": "Permissions and Licensing", "url": reverse("permissions_and_licensing")},
            {"text": "Legal framework"},
        ]

        return context
