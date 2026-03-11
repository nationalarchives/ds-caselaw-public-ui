from config.views.template_view_with_context import TemplateViewWithContext


class PermissionsAndLicensingView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/permissions_and_licensing.jinja"
    page_title = "Permissions and Licensing"
    page_canonical_url_name = "permissions_and_licensing"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "permissions_and_licensing"
        context["feedback_survey_type"] = "permissions_and_licensing"
        context["page_description"] = (
            "All judgments on Find Case Law are free to access, but different rules apply depending on how you want to use the records."
        )
        context["breadcrumbs"] = [
            {"text": "Permissions and Licensing"},
        ]

        return context
