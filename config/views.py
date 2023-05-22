from django.utils.translation import gettext
from django.views.generic import TemplateView
from ds_caselaw_utils import courts


class TemplateViewWithContext(TemplateView):
    page_title = None

    def get_context_data(self, **kwargs):
        return {
            "context": {
                "page_title": gettext(self.page_title) if self.page_title else None
            }
        }


class TransactionalLicenceFormView(TemplateViewWithContext):
    template_name = "pages/transactional_licence.html"
    page_title = "transactionallicenceform.title"

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
        context["context"]["courts"] = courts.get_selectable()
        context["feedback_survey_type"] = "structured_search"
        return context


class CheckView(TemplateViewWithContext):
    template_name = "pages/check.html"


class WhatToExpectView(TemplateViewWithContext):
    template_name = "pages/what_to_expect.html"
    page_title = "whattoexpect.title"

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
