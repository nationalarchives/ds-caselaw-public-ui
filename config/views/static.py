from ds_caselaw_utils import courts

from .template_view_with_context import TemplateViewWithContext


class AboutThisServiceView(TemplateViewWithContext):
    template_name = "pages/about_this_service.html"
    page_title = "About this service"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courts"] = courts.get_listable_groups()
        context["feedback_survey_type"] = "support"
        return context


class AccessibilityStatementView(TemplateViewWithContext):
    template_name = "pages/accessibility_statement.html"
    page_title = "Accessibility statement"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "support"
        return context


class ContactUsView(TemplateViewWithContext):
    template_name = "pages/contact_us.html"
    page_title = "Contact Us"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "contact_us"
        return context


class CourtsAndTribunalsInFclView(TemplateViewWithContext):
    template_name = "pages/courts_and_tribunals_in_fcl.html"
    page_title = "Courts and tribunals in Find Case Law"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courts"] = courts.get_listable_groups()
        context["feedback_survey_type"] = "courts_and_tribunals_in_fcl"
        return context


class FindCaseLawApiView(TemplateViewWithContext):
    template_name = "pages/the_find_case_law_api.html"
    page_title = "The Find Case Law API"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "the_find_case_law_api"
        return context


class HelpAndGuidanceView(TemplateViewWithContext):
    template_name = "pages/help_and_guidance.html"
    page_title = "Help and guidance"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "help_and_guidance"
        return context


class HowToSearchFindCaseLawView(TemplateViewWithContext):
    template_name = "pages/how_to_search_find_case_law.html"
    page_title = "How to search Find Case Law"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "how_to_search_find_case_law"
        return context


class HowToUseThisService(TemplateViewWithContext):
    template_name = "pages/how_to_use_this_service.html"
    page_title = "How to use the Find Case Law service"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "support"
        return context


class OpenJusticeLicenceView(TemplateViewWithContext):
    template_name = "pages/open_justice_licence.html"
    page_title = "Open Justice Licence"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "license"
        return context


class PrivacyNotice(TemplateViewWithContext):
    template_name = "pages/privacy_notice.html"
    page_title = "Privacy Notice"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "privacy_notice"
        return context


class PublishingPolicyView(TemplateViewWithContext):
    template_name = "pages/publishing_policy.html"
    page_title = "Publishing policy"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "publishing_policy"
        return context


class TermsAndPoliciesView(TemplateViewWithContext):
    template_name = "pages/terms_and_policies.html"
    page_title = "Terms and policies"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "terms_and_policies"
        return context


class TermsOfUseView(TemplateViewWithContext):
    template_name = "pages/terms_of_use.html"
    page_title = "Terms of Use"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "support"
        return context


class UnderstandingJudgmentsAndDecisionsView(TemplateViewWithContext):
    template_name = "pages/understanding_judgments_and_decisions.html"
    page_title = "Understanding judgments and decisions"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "understanding_judgments_and_decisions"
        return context
