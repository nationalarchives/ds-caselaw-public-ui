import requests
from caselawclient.client_helpers.search_helpers import (
    search_judgments_and_parse_response,
)
from caselawclient.search_parameters import RESULTS_PER_PAGE, SearchParameters
from django.http import Http404, HttpResponse
from django.utils.translation import gettext
from django.views.generic import TemplateView
from ds_caselaw_utils import courts

from judgments.forms import AdvancedSearchForm
from judgments.utils import api_client, clamp, paginator
from judgments.utils.utils import sanitise_input_to_integer

# where the schemas can be downloaded from. Slash-terminated.
SCHEMA_ROOT = "https://raw.githubusercontent.com/nationalarchives/ds-caselaw-marklogic/main/src/main/ml-schemas/"


class TemplateViewWithContext(TemplateView):
    page_title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = gettext(self.page_title) if self.page_title else None
        return context


class CourtsTribunalsListView(TemplateViewWithContext):
    """List view for all courts and tribunals in the Find Case Law database."""

    template_name = "pages/courts_and_tribunals.html"
    page_title = "Judgments and decisions by court or tribunal"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courts"] = courts.get_grouped_selectable_courts()
        context["tribunals"] = courts.get_grouped_selectable_tribunals()
        context["feedback_survey_type"] = "courts_and_tribunals"
        return context


class CourtOrTribunalView(TemplateViewWithContext):
    """Individual view for a specific court or tribunal."""

    template_name = "pages/court_or_tribunal.html"

    @property
    def page_title(self):
        return "Judgments for %s" % self.court.name

    @property
    def court(self):
        return courts.get_by_param(self.kwargs["param"])

    @property
    def page(self):
        return clamp(sanitise_input_to_integer(self.request.GET.get("page"), 1), minimum=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_response = search_judgments_and_parse_response(
            api_client,
            SearchParameters(court=self.court.canonical_param, order="-date", page=self.page),
        )

        context["feedback_survey_type"] = "court_or_tribunal_%s" % self.court.canonical_param
        context["request"] = self.request
        context["court"] = self.court
        context["judgments"] = search_response.results
        context["paginator"] = paginator(self.page, search_response.total, RESULTS_PER_PAGE)

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


class StyleGuide(TemplateViewWithContext):
    template_name = "pages/style_guide.html"
    page_title = "Style Guide"

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
        context["courts"] = courts.get_grouped_selectable_courts()
        context["tribunals"] = courts.get_grouped_selectable_tribunals()
        context["feedback_survey_type"] = "structured_search"
        context["form"] = AdvancedSearchForm()
        return context


class CheckView(TemplateViewWithContext):
    template_name = "pages/check.html"


class AboutThisServiceView(TemplateViewWithContext):
    template_name = "pages/about_this_service.html"
    page_title = "aboutthisservice.titleshort"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courts"] = courts.get_listable_groups()
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
