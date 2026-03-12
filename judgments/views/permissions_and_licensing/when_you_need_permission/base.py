from django.urls import reverse

from config.views.template_view_with_context import TemplateViewWithContext


class WhenYouNeedPermissionView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/permissions_and_licensing/when_you_need_permission.jinja"
    page_title = "When you need permission"
    page_canonical_url_name = "when_you_need_permission"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "permissions_and_licensing"
        context["feedback_survey_type"] = "when_you_need_permission"
        context["page_description"] = (
            "Most uses of Find Case Law judgments are free under the Open Justice Licence, including commercial use. However, if you want to perform computational analysis, you need to apply for a licence."
        )
        context["breadcrumbs"] = [
            {"text": "Permissions and Licensing", "url": reverse("permissions_and_licensing")},
            {"text": "When you need permission"},
        ]

        return context
