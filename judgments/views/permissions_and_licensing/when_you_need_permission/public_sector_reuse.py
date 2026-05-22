from django.urls import reverse

from config.views.template_view_with_context import TemplateViewWithContext


class PublicSectorReuseView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/permissions_and_licensing/when_you_need_permission/public_sector_reuse.jinja"
    page_title = "Public sector re-use"
    page_canonical_url_name = "public_sector_reuse"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "permissions_and_licensing"
        context["feedback_survey_type"] = "public_sector_reuse"
        context["page_description"] = (
            "Before you do anything else, you need to establish whether your organisation is a Crown body or a Non-Crown body."
        )
        context["breadcrumbs"] = [
            {"text": "Permissions and licensing", "url": reverse("permissions_and_licensing")},
            {"text": "When you need permission", "url": reverse("when_you_need_permission")},
            {"text": "Public sector re-use"},
        ]

        return context
