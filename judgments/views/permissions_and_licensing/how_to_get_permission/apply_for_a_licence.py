from django.urls import reverse

from config.views.template_view_with_context import TemplateViewWithContext


class ApplyForALicenceView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/permissions_and_licensing/how_to_get_permission/apply_for_a_licence.jinja"
    page_title = "Apply for a licence"
    page_canonical_url_name = "apply_for_a_licence"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "permissions_and_licensing"
        context["feedback_survey_type"] = "apply_for_a_licence"
        context["page_description"] = "Apply online to perform computational analysis on Find Case Law records."
        context["breadcrumbs"] = [
            {"text": "Permissions and Licensing", "url": reverse("permissions_and_licensing")},
            {"text": "How to get permission", "url": reverse("how_to_get_permission")},
            {"text": "Apply for a licence"},
        ]

        return context
