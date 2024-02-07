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


class CheckAnswersView(TemplateViewWithContext):
    template_name = "form/check_answers.html"
    page_title = "Check Answers"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "license"
        return context


class AnyCommentsView(TemplateViewWithContext):
    template_name = "form/any_comments.html"
    page_title = "Any Comments"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "license"
        return context


class AccurateDataRepresentationView(TemplateViewWithContext):
    template_name = "form/accurate_data_representation.html"
    page_title = "Accurate Data Representation"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "license"
        return context


class AlgorithmicTransparencyView(TemplateViewWithContext):
    template_name = "form/algorithmic_transparency.html"
    page_title = "Algorithmic Transparency"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "license"
        return context


class DiscoverabilityView(TemplateViewWithContext):
    template_name = "form/discoverability.html"
    page_title = "Discoverability"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "license"
        return context


class PersonalPrivacyView(TemplateViewWithContext):
    template_name = "form/personal_privacy.html"
    page_title = "Personal Privacy"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "license"
        return context


class AntiBiasView(TemplateViewWithContext):
    template_name = "form/anti_bias.html"
    page_title = "Anti-bias"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "license"
        return context


class AntiDiscriminatoryHarmView(TemplateViewWithContext):
    template_name = "form/anti_discriminatory_harm.html"
    page_title = "Anti-Discriminatory Harm"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "license"
        return context


class AppropriateScrutinyView(TemplateViewWithContext):
    template_name = "form/appropriate_scrutiny.html"
    page_title = "Appropriate scrutiny"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "license"
        return context


class IndependenceCourtView(TemplateViewWithContext):
    template_name = "form/independence_of_the_court.html"
    page_title = "Independence of the court"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "license"
        return context


class DignityCourtsView(TemplateViewWithContext):
    template_name = "form/dignity_of_the_courts.html"
    page_title = "Dignity of the courts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "license"
        return context


class StatementsPrinciplestView(TemplateViewWithContext):
    template_name = "form/statements_and_principles.html"
    page_title = "Statements and Principles"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "license"
        return context


class PublicStatementView(TemplateViewWithContext):
    template_name = "form/public_statement.html"
    page_title = "Public Statement"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "license"
        return context


class PurposeActivitiesView(TemplateViewWithContext):
    template_name = "form/purpose_and_activities.html"
    page_title = "Purpose and Activities"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "license"
        return context


class YourOrganisationView(TemplateViewWithContext):
    template_name = "form/your_organisation.html"
    page_title = "About your organisation"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "license"
        return context


class SubmitDetailsView(TemplateViewWithContext):
    template_name = "form/submit_details.html"
    page_title = "Submission form to do computational analysis"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "license"
        return context


class ComputationalLicenceSubmitView(TemplateViewWithContext):
    template_name = "form/computational_licence_application.html"
    page_title = "Check you need to apply"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_survey_type"] = "license"
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
