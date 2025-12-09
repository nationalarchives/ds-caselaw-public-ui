from django.urls import reverse
from ds_caselaw_utils import courts

from .template_view_with_context import TemplateViewWithContext


class AboutThisServiceView(TemplateViewWithContext):
    template_name = "pages/about_this_service.html"
    page_title = "About Find Case Law"
    page_canonical_url_name = "about_this_service"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courts"] = courts.get_listable_groups()
        context["feedback_survey_type"] = "about_this_service"
        context["page_description"] = (
            "The Find Case Law service provides free access to judgments and decisions made in England and Wales from 2001 onwards."
        )
        context["breadcrumbs"] = [
            {"text": self.page_title},
        ]
        return context


class AboutThisServiceJinjaView(AboutThisServiceView):
    template_engine = "jinja"
    template_name = "pages/about_this_service.jinja"


class AccessibilityStatementView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/accessibility_statement.jinja"
    page_title = "Accessibility statement for Find Case Law"
    page_canonical_url_name = "accessibility_statement"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "accessibility_statement"
        context["page_description"] = (
            "Find out how accessible the Find Case Law service is by reading our accessibility statement. It is important that everyone can use this service."
        )
        context["breadcrumbs"] = [
            {"url": reverse("terms_and_policies"), "text": "Terms and policies"},
            {"text": self.page_title},
        ]
        return context


class ContactUsView(TemplateViewWithContext):
    template_name = "pages/contact_us.html"
    page_title = "Contact Us"
    page_canonical_url_name = "contact_us"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "contact_us"
        context["page_description"] = (
            "Find out how to get in touch with us to ask a question or report a problem to the Find Case Law service team."
        )
        context["breadcrumbs"] = [
            {"url": reverse("help_and_guidance"), "text": "Help and guidance"},
            {"text": "Contact us"},
        ]
        return context


class ContactUsJinjaView(ContactUsView):
    template_engine = "jinja"
    template_name = "pages/contact_us.jinja"


class CourtsAndTribunalsInFclView(TemplateViewWithContext):
    template_name = "pages/courts_and_tribunals_in_fcl.html"
    page_title = "Courts and tribunals in Find Case Law"
    page_canonical_url_name = "courts_and_tribunals_in_fcl"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courts"] = courts.get_grouped_selectable_courts()
        context["feedback_survey_type"] = "courts_and_tribunals_in_fcl"
        context["page_description"] = (
            "Find out which courts and tribunals publish judgments and decisions on the Find Case Law service."
        )
        context["breadcrumbs"] = [
            {"url": reverse("about_this_service"), "text": "About Find Case Law"},
            {"text": "Courts and tribunals in Find Case Law"},
        ]
        return context


class CourtsAndTribunalsInFclJinjaView(CourtsAndTribunalsInFclView):
    template_engine = "jinja"
    template_name = "pages/courts_and_tribunals_in_fcl.jinja"


class HelpAndGuidanceView(TemplateViewWithContext):
    template_name = "pages/help_and_guidance.html"
    page_title = "Help and guidance"
    page_canonical_url_name = "help_and_guidance"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "help_and_guidance"
        context["page_description"] = (
            "A list of help and guidance available on the Find Case Law service. We do not offer legal advice or research services."
        )
        context["breadcrumbs"] = [
            {"text": self.page_title},
        ]
        return context


class HelpAndGuidanceJinjaView(HelpAndGuidanceView):
    template_engine = "jinja"
    template_name = "pages/help_and_guidance.jinja"


class HowToSearchFindCaseLawView(TemplateViewWithContext):
    template_name = "pages/how_to_search_find_case_law.html"
    page_title = "How to search Find Case Law"
    page_canonical_url_name = "how_to_search_find_case_law"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "how_to_search_find_case_law"
        context["page_description"] = (
            "Help and guidance on how to search judgments and decisions on the Find Case Law service using the search box and filters."
        )
        context["breadcrumbs"] = [
            {"url": reverse("help_and_guidance"), "text": "Help and guidance"},
            {"text": "How to search Find Case Law"},
        ]
        return context


class HowToSearchFindCaseLawJinjaView(HowToSearchFindCaseLawView):
    template_engine = "jinja"
    template_name = "pages/how_to_search_find_case_law.jinja"


class OpenJusticeLicenceView(TemplateViewWithContext):
    template_name = "pages/open_justice_licence.html"
    page_title = "Open Justice Licence"
    page_canonical_url_name = "open_justice_licence"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "license"
        context["breadcrumbs"] = [
            {"text": self.page_title},
        ]
        return context


class OpenJusticeLicenceJinjaView(OpenJusticeLicenceView):
    template_engine = "jinja"
    template_name = "pages/open_justice_licence.jinja"


class PrivacyNotice(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/privacy_notice.jinja"
    page_title = "Privacy Notice"
    page_canonical_url_name = "privacy_notice"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "privacy_notice"
        context["page_description"] = (
            "Read our privacy notice to understand more about personal data in judgments and decisions on the Find Case Law service."
        )
        context["breadcrumbs"] = [
            {"text": self.page_title},
        ]
        return context


class PublishingPolicyView(TemplateViewWithContext):
    template_name = "pages/publishing_policy.html"
    page_title = "Publishing policy"
    page_canonical_url_name = "publishing_policy"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "publishing_policy"
        context["page_description"] = (
            "Read our policy to find out how we receive and publish judgments and decisions on the Find Case Law service."
        )
        context["breadcrumbs"] = [
            {"url": reverse("terms_and_policies"), "text": "Terms and policies"},
            {"text": "Publishing policy"},
        ]
        return context


class PublishingPolicyJinjaView(PublishingPolicyView):
    template_engine = "jinja"
    template_name = "pages/publishing_policy.jinja"


class TermsAndPoliciesView(TemplateViewWithContext):
    template_name = "pages/terms_and_policies.html"
    page_title = "Terms and policies"
    page_canonical_url_name = "terms_and_policies"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "terms_and_policies"
        context["page_description"] = (
            "A list of the Find Case Law service’s terms and policies including the accessibility statement, publishing policy and terms of use."
        )
        context["breadcrumbs"] = [
            {"text": self.page_title},
        ]
        return context


class TermsAndPoliciesJinjaView(TermsAndPoliciesView):
    template_engine = "jinja"
    template_name = "pages/terms_and_policies.jinja"


class TermsOfUseView(TemplateViewWithContext):
    template_name = "pages/terms_of_use.html"
    page_title = "Terms of use"
    page_canonical_url_name = "terms_of_use"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "terms_of_use"
        context["page_description"] = (
            "The terms of use page and pages it links to explains how you can use information from the Find Case Law service."
        )
        context["breadcrumbs"] = [
            {"url": reverse("terms_and_policies"), "text": "Terms and policies"},
            {"text": "Terms of Use"},
        ]
        return context


class TermsOfUseJinjaView(TermsOfUseView):
    template_engine = "jinja"
    template_name = "pages/terms_of_use.jinja"


class UnderstandingJudgmentsAndDecisionsView(TemplateViewWithContext):
    template_name = "pages/understanding_judgments_and_decisions.html"
    page_title = "Understanding judgments and decisions"
    page_canonical_url_name = "understanding_judgments_and_decisions"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "understanding_judgments_and_decisions"
        context["page_description"] = (
            "A basic overview of what a judgment is and how they are commonly structured to help people reading a judgment for the first time."
        )
        context["breadcrumbs"] = [
            {"url": reverse("help_and_guidance"), "text": "Help and guidance"},
            {"text": "Understanding judgments and decisions"},
        ]
        return context


class UnderstandingJudgmentsAndDecisionsJinjaView(UnderstandingJudgmentsAndDecisionsView):
    template_engine = "jinja"
    template_name = "pages/understanding_judgments_and_decisions.jinja"


class UserResearchView(TemplateViewWithContext):
    template_name = "pages/user_research.html"
    page_title = "User research"
    page_canonical_url_name = "user_research"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_description"] = ""
        context["breadcrumbs"] = [
            {"text": "User research"},
        ]
        return context


class UserResearchJinjaView(UserResearchView):
    template_engine = "jinja"
    template_name = "pages/user_research.jinja"
