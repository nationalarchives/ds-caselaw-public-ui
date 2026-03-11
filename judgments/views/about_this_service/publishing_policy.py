from django.urls import reverse

from config.views.template_view_with_context import TemplateViewWithContext


class PublishingPolicyView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/about_this_service/publishing_policy.jinja"
    page_title = "Publishing policy"
    page_canonical_url_name = "publishing_policy"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "about_this_service"
        context["feedback_survey_type"] = "publishing_policy"
        context["page_description"] = (
            "Read our policy to find out how we receive and publish judgments and decisions on the Find Case Law service."
        )
        context["breadcrumbs"] = [
            {"url": reverse("about_this_service"), "text": "About this service"},
            {"text": "Publishing policy"},
        ]
        context["breadcrumbs_postfix"] = "Last updated on 20 August 2024"
        return context
