from django.urls import reverse

from config.views.template_view_with_context import TemplateViewWithContext


class HowToGetPermissionView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/permissions_and_licensing/how_to_get_permission.jinja"
    page_title = "How to get permission"
    page_canonical_url_name = "how_to_get_permission"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "permissions_and_licensing"
        context["feedback_survey_type"] = "how_to_get_permission"
        context["page_description"] = (
            "If you need to perform computational analysis on Find Case Law records, you'll need to apply for a licence. Here's an overview of the process."
        )
        context["breadcrumbs"] = [
            {"text": "Permissions and Licensing", "url": reverse("permissions_and_licensing")},
            {"text": "How to get permission"},
        ]

        return context
