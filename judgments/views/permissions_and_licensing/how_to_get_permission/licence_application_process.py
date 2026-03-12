from django.urls import reverse

from config.views.template_view_with_context import TemplateViewWithContext


class LicenceApplicationProcessView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/permissions_and_licensing/how_to_get_permission/licence_application_process.jinja"
    page_title = "Licence application process"
    page_canonical_url_name = "licence_application_process"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "permissions_and_licensing"
        context["feedback_survey_type"] = "licence_application_process"
        context["page_description"] = (
            "If you want to perform computational analysis on Find Case Law records, you need to apply for a licence. Here's how applications are assessed and approved."
        )
        context["breadcrumbs"] = [
            {"text": "Permissions and Licensing", "url": reverse("permissions_and_licensing")},
            {"text": "How to get permission", "url": reverse("how_to_get_permission")},
            {"text": "Licence application process"},
        ]

        return context
