from django.urls import reverse

from config.views.template_view_with_context import TemplateViewWithContext


class WhatYouCanDoFreelyView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/permissions_and_licensing/what_you_can_do_freely.jinja"
    page_title = "What you can do freely"
    page_canonical_url_name = "what_you_can_do_freely"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "permissions_and_licensing"
        context["feedback_survey_type"] = "what_you_can_do_freely"
        context["page_description"] = (
            "Most uses of Find Case Law judgments don't require permission or a licence. You're free to use judgments under the Open Justice Licence in ways that support open justice, legal practice, research and commercial innovation."
        )
        context["breadcrumbs"] = [
            {"text": "Permissions and Licensing", "url": reverse("permissions_and_licensing")},
            {"text": "What you can do freely"},
        ]

        return context
