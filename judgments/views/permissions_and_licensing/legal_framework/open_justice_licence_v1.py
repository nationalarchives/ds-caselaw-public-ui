from django.urls import reverse

from config.views.template_view_with_context import TemplateViewWithContext


class OpenJusticeLicenceV1View(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/permissions_and_licensing/legal_framework/open_justice_licence_v1.jinja"

    page_title = "Open Justice Licence"
    page_canonical_url_name = "open_justice_licence_v1"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "permissions_and_licensing"
        context["feedback_survey_type"] = "license"
        context["page_description"] = (
            "Open justice is a fundamental constitutional principle and necessary for the rule of law. The purpose of this licence is to support open justice."
        )
        context["breadcrumbs"] = [
            {"text": "Permissions and licensing", "url": reverse("permissions_and_licensing")},
            {"text": "Legal framework", "url": reverse("legal_framework")},
            {"text": f"{self.page_title} v1.0"},
        ]
        return context
