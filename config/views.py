import requests
from django.http import Http404, HttpResponse
from django.utils.translation import gettext
from django.views.generic import TemplateView
from ds_caselaw_utils import courts

# where the schemas can be downloaded from. Slash-terminated.
SCHEMA_ROOT = "https://raw.githubusercontent.com/nationalarchives/ds-caselaw-marklogic/main/src/main/ml-schemas/"


class TemplateViewWithContext(TemplateView):
    page_title = None

    def get_context_data(self, **kwargs):
        return {
            "context": {
                "page_title": gettext(self.page_title) if self.page_title else None
            }
        }


class CourtsTribunalsView(TemplateViewWithContext):
    template_name = "pages/courts_and_tribunals.html"
    page_title = "Judgments and decisions by court or tribunal"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["context"]["courts"] = courts.get_grouped_selectable_courts()
        context["context"]["tribunals"] = courts.get_grouped_selectable_tribunals()
        context["feedback_survey_type"] = "structured_search"
        return context


class ComputationalLicenceFormView(TemplateViewWithContext):
    template_name = "pages/computational_licence.html"
    page_title = "Apply to do computational analysis"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "license"
        return context


class AccessibilityStatement(TemplateViewWithContext):
    template_name = "pages/accessibility_statement.html"
    page_title = "accessibilitystatement.title"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "support"
        return context


class OpenJusticeLicenceView(TemplateViewWithContext):
    template_name = "pages/open_justice_licence.html"
    page_title = "openjusticelicence.title"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "license"
        return context


class TermsOfUseView(TemplateViewWithContext):
    template_name = "pages/terms_of_use.html"
    page_title = "terms.title"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "support"
        return context


class PublishingPolicyView(TemplateViewWithContext):
    template_name = "pages/publishing_policy.html"
    page_title = "publishing_policy.title"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "publishing_policy"
        return context


class StructuredSearchView(TemplateViewWithContext):
    template_name = "pages/structured_search.html"
    page_title = "structured_search.title"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["context"]["courts"] = courts.get_grouped_selectable_courts()
        context["context"]["tribunals"] = courts.get_grouped_selectable_tribunals()
        context["feedback_survey_type"] = "structured_search"
        return context


class CheckView(TemplateViewWithContext):
    template_name = "pages/check.html"


class AboutThisServiceView(TemplateViewWithContext):
    template_name = "pages/about_this_service.html"
    page_title = "aboutthisservice.titleshort"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["context"]["courts"] = courts.get_listable_groups()
        context["feedback_survey_type"] = "support"
        return context


class HowToUseThisService(TemplateViewWithContext):
    template_name = "pages/how_to_use_this_service.html"
    page_title = "howtousethisservice.title"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "support"
        return context


class PrivacyNotice(TemplateViewWithContext):
    template_name = "pages/privacy_notice.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "privacy_notice"
        return context


def schema(request, schemafile: str):
    response = requests.get(f"{SCHEMA_ROOT}{schemafile}")
    if response.status_code != 200:
        raise Http404("Could not get schema")

    return HttpResponse(response.content, content_type="application/xml")
