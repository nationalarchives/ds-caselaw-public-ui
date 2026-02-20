from django.urls import reverse
from ds_caselaw_utils import courts

from .template_view_with_context import TemplateViewWithContext


class AboutThisServiceView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/about_this_service.jinja"
    page_title = "About this service"
    page_canonical_url_name = "about_this_service"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courts"] = courts.get_listable_groups()
        context["active_navigation_endpoint"] = "about_this_service"
        context["feedback_survey_type"] = "about_this_service"
        context["page_description"] = (
            "The Find Case Law service provides free access to judgments and decisions made in England and Wales from 2001 onwards."
        )
        context["breadcrumbs"] = [
            {"text": self.page_title},
        ]
        return context


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
            {"text": self.page_title},
        ]
        context["breadcrumbs_postfix"] = "Last updated on 30 July 2025"
        return context


class ContactUsView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/contact_us.jinja"
    page_title = "Contact Us"
    page_canonical_url_name = "contact_us"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "help_and_support"
        context["feedback_survey_type"] = "contact_us"
        context["page_description"] = (
            "Find out how to get in touch with us to ask a question or report a problem to the Find Case Law service team."
        )
        context["breadcrumbs"] = [
            {"url": reverse("help_and_support"), "text": "Help and support"},
            {"text": "Contact us"},
        ]
        context["breadcrumbs_postfix"] = "Last updated on 21 January 2025"
        return context


class CourtsAndTribunalsInFclView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/courts_and_tribunals_in_fcl.jinja"
    page_title = "Courts and tribunals in Find Case Law"
    page_canonical_url_name = "courts_and_tribunals_in_fcl"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courts"] = courts.get_grouped_selectable_courts()
        context["active_navigation_endpoint"] = "about_this_service"
        context["feedback_survey_type"] = "courts_and_tribunals_in_fcl"
        context["page_description"] = (
            "Find out which courts and tribunals publish judgments and decisions on the Find Case Law service."
        )
        context["breadcrumbs"] = [
            {"url": reverse("about_this_service"), "text": "About this service"},
            {"text": "Courts and tribunals in Find Case Law"},
        ]
        context["breadcrumbs_postfix"] = "Last updated on 21 January 2025"
        return context


class HowToSearchFindCaseLawView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/how_to_search_find_case_law.jinja"
    page_title = "How to search Find Case Law"
    page_canonical_url_name = "how_to_search_find_case_law"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "help_and_support"
        context["feedback_survey_type"] = "how_to_search_find_case_law"
        context["page_description"] = (
            "Help and guidance on how to search judgments and decisions on the Find Case Law service using the search box and filters."
        )
        context["breadcrumbs"] = [
            {"url": reverse("help_and_support"), "text": "Help and support"},
            {"text": "How to search Find Case Law"},
        ]
        context["breadcrumbs_postfix"] = "Last updated on 21 January 2025"
        return context


class ReadingJudgmentsView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/reading_judgments.jinja"
    page_title = "Reading judgments"
    page_canonical_url_name = "reading_judgments"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "understanding_case_law"
        context["feedback_survey_type"] = "reading_judgments"
        context["page_description"] = (
            "Court judgments can seem complicated if you haven't read them before. We’ll help you understand how judgments are structured and how to find the information you need."
        )
        context["breadcrumbs"] = [
            {"url": reverse("understanding_case_law"), "text": "Understanding case law"},
            {"text": "Reading judgments"},
        ]
        context["breadcrumbs_postfix"] = "Last updated on 19 February 2026"
        return context


class OpenJusticeLicenceView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/open_justice_licence.jinja"

    page_title = "Open Justice Licence"
    page_canonical_url_name = "open_justice_licence"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "permissions_and_licencing"
        context["feedback_survey_type"] = "license"
        context["page_description"] = (
            "Open justice is a fundamental constitutional principle and necessary for the rule of law. The purpose of this licence is to support open justice."
        )
        context["breadcrumbs"] = [
            {"text": "Permissions and Licencing", "url": reverse("permissions_and_licencing")},
            {"text": "Legal framework", "url": reverse("legal_framework")},
            {"text": self.page_title},
        ]
        return context


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
        context["breadcrumbs_postfix"] = "Last updated on 20 August 2024"
        return context


class PublishingPolicyView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/publishing_policy.jinja"
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


class TermsOfUseView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/terms_of_use.jinja"
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
            {"text": "Terms of Use"},
        ]
        context["breadcrumbs_postfix"] = "Last updated on 20 August 2024"
        return context


class UnderstandingJudgmentsAndDecisionsView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/understanding_judgments_and_decisions.jinja"
    page_title = "Understanding judgments and decisions"
    page_canonical_url_name = "understanding_judgments_and_decisions"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "understanding_case_law"
        context["feedback_survey_type"] = "understanding_judgments_and_decisions"
        context["page_description"] = (
            "A basic overview of what a judgment is and how they are commonly structured to help people reading a judgment for the first time."
        )
        context["breadcrumbs"] = [
            {"url": reverse("help_and_support"), "text": "Help and support"},
            {"text": "Understanding judgments and decisions"},
        ]
        context["breadcrumbs_postfix"] = "Last updated on 21 January 2025"
        return context


class UnderstandingCaseLawView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/understanding_case_law.jinja"
    page_title = "Understanding case law"
    page_canonical_url_name = "understanding_case_law"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "understanding_case_law"
        context["feedback_survey_type"] = "understanding_case_law"
        context["page_description"] = (
            "If you're new to legal information, we’ll help you understand how case law works and how to read court judgments."
        )
        context["breadcrumbs"] = [
            {"text": "Understanding case law"},
        ]
        context["breadcrumbs_postfix"] = "Last updated 8 January 2026"
        return context


class SearchAndBrowseView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/search_and_browse.jinja"
    page_title = "Search and browse"
    page_canonical_url_name = "search_and_browse"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "search_and_browse"
        context["feedback_survey_type"] = "search_and_browse"
        context["page_description"] = (
            "Find the judgments and decisions you need using our search tools or browse by court and tribunal."
        )
        context["breadcrumbs"] = [
            {"text": "Search and browse"},
        ]
        context["breadcrumbs_postfix"] = "Last updated on 21 January 2026"
        return context


class BrowseCourtsAndTribunalsView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/browse_courts_and_tribunals.jinja"
    page_title = "Browse courts and tribunals"
    page_canonical_url_name = "browse_courts_and_tribunals"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "search_and_browse"
        context["feedback_survey_type"] = "browse_courts_and_tribunals"
        context["page_description"] = (
            "Explore judgments by court or tribunal type. This helps you understand what’s available and find cases from specific jurisdictions."
        )
        context["breadcrumbs"] = [
            {"text": "Search and browse", "url": reverse("search_and_browse")},
            {"text": "Browse courts and tribunals"},
        ]

        return context


class AboutFindCaseLawView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/about_find_case_law.jinja"
    page_title = "About Find Case Law"
    page_canonical_url_name = "about_find_case_law"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "about_this_service"
        context["feedback_survey_type"] = "about_find_case_law"
        context["page_description"] = (
            "Find Case Law is the official public source for judgments and decisions from courts and tribunals in England and Wales. We provide free access to judgments to support open justice, legal practice, research and public understanding."
        )
        context["breadcrumbs"] = [
            {"text": "About this service", "url": reverse("about_this_service")},
            {"text": "About Find Case Law"},
        ]

        return context


class WhatWeProvideView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/what_we_provide.jinja"
    page_title = "What we provide"
    page_canonical_url_name = "what_we_provide"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "about_this_service"
        context["feedback_survey_type"] = "what_we_provide"
        context["page_description"] = (
            "Find Case Law focuses on providing judgments and decisions from courts and tribunals in England and Wales. Understanding what we include – and what we don't – helps you know what to expect when searching."
        )
        context["breadcrumbs"] = [
            {"text": "About this service", "url": reverse("about_this_service")},
            {"text": "What we provide"},
        ]

        return context


class PermissionsAndLicencingView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/permissions_and_licencing.jinja"
    page_title = "Permissions and Licencing"
    page_canonical_url_name = "permissions_and_licencing"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "permissions_and_licencing"
        context["feedback_survey_type"] = "permissions_and_licencing"
        context["page_description"] = (
            "All judgments on Find Case Law are free to access, but different rules apply depending on how you want to use the records."
        )
        context["breadcrumbs"] = [
            {"text": "Permissions and Licencing"},
        ]

        return context


class WhatYouCanDoFreelyView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/what_you_can_do_freely.jinja"
    page_title = "What you can do freely"
    page_canonical_url_name = "what_you_can_do_freely"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "permissions_and_licencing"
        context["feedback_survey_type"] = "what_you_can_do_freely"
        context["page_description"] = (
            "Most uses of Find Case Law judgments don't require permission or a licence. You're free to use judgments under the Open Justice Licence in ways that support open justice, legal practice, research and commercial innovation."
        )
        context["breadcrumbs"] = [
            {"text": "Permissions and Licencing", "url": reverse("permissions_and_licencing")},
            {"text": "What you can do freely"},
        ]

        return context


class UsingFindCaseLawRecordsView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/using_find_case_law_records.jinja"
    page_title = "Using Find Case Law records"
    page_canonical_url_name = "using_find_case_law_records"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "permissions_and_licencing"
        context["feedback_survey_type"] = "using_find_case_law_records"
        context["page_description"] = (
            "You can freely use judgments from Find Case Law for most purposes without permission or payment. This page explains what you can do and gives practical examples."
        )
        context["breadcrumbs"] = [
            {"text": "Permissions and Licencing", "url": reverse("permissions_and_licencing")},
            {"text": "What you can do freely", "url": reverse("what_you_can_do_freely")},
            {"text": "Using Find Case Law records"},
        ]

        return context


class WhatYouNeedToApplyForALicenceView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/what_you_need_to_apply_for_a_licence.jinja"
    page_title = "What you need to apply for a licence"
    page_canonical_url_name = "what_you_need_to_apply_for_a_licence"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "permissions_and_licencing"
        context["feedback_survey_type"] = "what_you_need_to_apply_for_a_licence"
        context["page_description"] = (
            "If you want to perform computational analysis on Find Case Law records, you'll need to apply for a licence. Here's what the application involves and how to prepare."
        )
        context["breadcrumbs"] = [
            {"text": "Permissions and Licencing", "url": reverse("permissions_and_licencing")},
            {"text": "When you need permission", "url": reverse("when_you_need_permission")},
            {"text": "What you need to apply for a licence"},
        ]

        return context


class HowToGetPermissionView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/how_to_get_permission.jinja"
    page_title = "How to get permission"
    page_canonical_url_name = "how_to_get_permission"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "permissions_and_licencing"
        context["feedback_survey_type"] = "how_to_get_permission"
        context["page_description"] = (
            "If you need to perform computational analysis on Find Case Law records, you'll need to apply for a licence. Here's an overview of the process."
        )
        context["breadcrumbs"] = [
            {"text": "Permissions and Licencing", "url": reverse("permissions_and_licencing")},
            {"text": "How to get permission"},
        ]

        return context


class LicenceApplicationProcessView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/licence_application_process.jinja"
    page_title = "Licence application process"
    page_canonical_url_name = "licence_application_process"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "permissions_and_licencing"
        context["feedback_survey_type"] = "licence_application_process"
        context["page_description"] = (
            "If you want to perform computational analysis on Find Case Law records, you need to apply for a licence. Here's how applications are assessed and approved."
        )
        context["breadcrumbs"] = [
            {"text": "Permissions and Licencing", "url": reverse("permissions_and_licencing")},
            {"text": "How to get permission", "url": reverse("how_to_get_permission")},
            {"text": "Licence application process"},
        ]

        return context


class ApplyForALicenceView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/apply_for_a_licence.jinja"
    page_title = "Apply for a licence"
    page_canonical_url_name = "apply_for_a_licence"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "permissions_and_licencing"
        context["feedback_survey_type"] = "apply_for_a_licence"
        context["page_description"] = "Apply online to perform computational analysis on Find Case Law records."
        context["breadcrumbs"] = [
            {"text": "Permissions and Licencing", "url": reverse("permissions_and_licencing")},
            {"text": "How to get permission", "url": reverse("how_to_get_permission")},
            {"text": "Apply for a licence"},
        ]

        return context


class LegalFrameworkView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/legal_framework.jinja"
    page_title = "Legal framework"
    page_canonical_url_name = "legal_framework"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "permissions_and_licencing"
        context["feedback_survey_type"] = "legal_framework"
        context["page_description"] = (
            "Here are the legal and technical details of how Find Case Law judgments can be used and licensed."
        )
        context["breadcrumbs"] = [
            {"text": "Permissions and Licencing", "url": reverse("permissions_and_licencing")},
            {"text": "Legal framework"},
        ]

        return context


class WhenYouNeedPermissionView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/when_you_need_permission.jinja"
    page_title = "When you need permission"
    page_canonical_url_name = "when_you_need_permission"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "permissions_and_licencing"
        context["feedback_survey_type"] = "when_you_need_permission"
        context["page_description"] = (
            "Most uses of Find Case Law judgments are free under the Open Justice Licence, including commercial use. However, if you want to perform computational analysis, you need to apply for a licence."
        )
        context["breadcrumbs"] = [
            {"text": "Permissions and Licencing", "url": reverse("permissions_and_licencing")},
            {"text": "When you need permission"},
        ]

        return context


class SearchTipsView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/search_tips.jinja"
    page_title = "Search tips"
    page_canonical_url_name = "search_tips"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "help_and_support"
        context["feedback_survey_type"] = "search_tips"
        context["page_description"] = (
            "Search court judgments and tribunal decisions in Find Case Law using the search box on the homepage of this website."
        )
        context["breadcrumbs"] = [
            {"text": "Help and support", "url": reverse("help_and_support")},
            {"text": "Search tips"},
        ]

        return context


class HelpAndSupportView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/help_and_support.jinja"
    page_title = "Help and Support"
    page_canonical_url_name = "help_and_support"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "help_and_support"
        context["feedback_survey_type"] = "help_and_support"
        context["page_description"] = (
            "Get help using Find Case Law, report problems and share your feedback to help us improve the service."
        )
        context["breadcrumbs"] = [
            {"text": "Help and support"},
        ]

        return context


class CourtsAndDateCoverageView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/courts_and_date_coverage.jinja"
    page_title = "Courts and date coverage"
    page_canonical_url_name = "courts_and_date_coverage"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "about_this_service"
        context["feedback_survey_type"] = "courts_and_date_coverage"
        context["page_description"] = (
            "Different courts and tribunals have different coverage on Find Case Law. Some have comprehensive recent records, while others include selected historical judgments."
        )
        context["breadcrumbs"] = [
            {"text": "About this service", "url": reverse("about_this_service")},
            {"text": "Courts and date coverage"},
        ]

        return context


class FeedbackView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/feedback.jinja"
    page_title = "Feedback"
    page_canonical_url_name = "feedback"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "help_and_support"
        context["feedback_survey_type"] = "feedback"
        context["page_description"] = (
            "Your feedback and experiences help us improve Find Case Law for everyone. We want to hear from everyone, whether you use the service daily or are visiting for the first time."
        )
        context["breadcrumbs"] = [
            {"text": "Help and support", "url": reverse("help_and_support")},
            {"text": "Feedback"},
        ]

        return context


class UserResearchView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/user_research.jinja"
    page_title = "User research"
    page_canonical_url_name = "user_research"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_navigation_endpoint"] = "help_and_support"
        context["page_description"] = ""
        context["breadcrumbs"] = [
            {"text": "Help and support", "url": reverse("help_and_support")},
            {"text": "Feedback", "url": reverse("feedback")},
            {"text": "User research"},
        ]
        context["breadcrumbs_postfix"] = "Last updated on 3 July 2025"
        return context
