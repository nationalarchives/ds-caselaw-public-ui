from django.urls import reverse

from config.views.template_view_with_context import TemplateViewWithContext


class WhatYouNeedToApplyForALicenceView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = (
        "pages/permissions_and_licensing/when_you_need_permission/what_you_need_to_apply_for_a_licence.jinja"
    )
    page_title = "What you need to apply for a licence"
    page_canonical_url_name = "what_you_need_to_apply_for_a_licence"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "permissions_and_licensing"
        context["feedback_survey_type"] = "what_you_need_to_apply_for_a_licence"
        context["page_description"] = (
            "If you want to perform computational analysis on Find Case Law records, you'll need to apply for a licence. Here's what the application involves and how to prepare."
        )
        context["breadcrumbs"] = [
            {"text": "Permissions and Licensing", "url": reverse("permissions_and_licensing")},
            {"text": "When you need permission", "url": reverse("when_you_need_permission")},
            {"text": "What you need to apply for a licence"},
        ]

        return context
