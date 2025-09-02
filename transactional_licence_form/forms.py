from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Field, Fieldset, Layout
from django import forms

from . import choices, fields
from .utils import countries_and_territories_choices, list_to_choices, validate_max_words


class FCLForm(forms.Form):
    display_in_review = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = self.layout()

    def layout(self):
        pass


class LicenseApplicationForm(FCLForm):
    NAVIGATION_STEPS = [
        "1 – Are you ready to apply",
        "2 – Contact details",
        "3 – About your organisation",
        "4 – Purpose and activities",
        "5 – Public statement",
        "6 – Working practices",
        "7 – Working practices",
        "8 – Nine principles",
        "9 – Nine principles statement",
        "10 – Additional comments",
        "11 – Review your answers",
    ]

    @property
    def navigation_done(self):
        return tuple(self.NAVIGATION_STEPS[: self.step_index])

    @property
    def navigation_current(self):
        return self.NAVIGATION_STEPS[self.step_index]

    @property
    def navigation_todo(self):
        return tuple(self.NAVIGATION_STEPS[self.step_index + 1 :])


class ContactForm(LicenseApplicationForm):
    step_index = 1

    title = "Step 2 – Contact details"

    contact_lastname = fields.FCLCharField(
        label="1. Contact Full Name",
        max_length=50,
    )
    contact_email = fields.FCLEmailField(
        label="2. Contact Email address",
        max_length=50,
        # NOTE: this is a temporary workaround as there is a bug in crispy-forms-gds where they forgot to apply error styling to email inputs
        widget=forms.TextInput(attrs={"type": "email"}),
    )
    # NOTE: please see comment in transactional_lcence_form.js if changing the wording / order of the options here.
    alternative_contact = fields.FCLChoiceField(
        label=(
            "3. We need the contact details of the person who will be responsible "
            "for the licence. This should be someone senior who has overall responsibility "
            "for complaince with the terms and conditions of the licence."
        ),
        choices=choices.ALTERNATIVE_CONTACT_CHOICES,
    )
    licence_holder_lastname = fields.FCLCharField(
        label="1a. Licence holder Full Name",
        max_length=50,
        show_hidden_initial=True,
        required=False,
    )
    licence_holder_email = fields.FCLEmailField(
        label="2a. Licence holder Email",
        max_length=50,
        show_hidden_initial=True,
        required=False,
    )


class OrganizationForm(LicenseApplicationForm):
    def __init__(self, *args, **kwargs):
        super(OrganizationForm, self).__init__(*args, **kwargs)
        self.initial["agent_country"] = "country:GB"

    def layout(self):
        return Layout(
            Field("agent_companyname"),
            Field("agent_companyname_other"),
            Fieldset(
                Field("agent_address_line_1"),
                Field("agent_address_line_2"),
                Field("agent_town"),
                Field("agent_county"),
                Field("agent_postcode"),
                Field("agent_country"),
                legend="6. Please enter your organisation address",
            ),
            Field("tna_contacttype"),
            Field("agent_companyid"),
            Field("partners"),
        )

    step_index = 2

    title = "Step 3 – About your organisation"

    agent_companyname = fields.FCLCharField(
        label="4. What is the full legal name of your organisation?", max_length=100
    )
    agent_companyname_other = fields.FCLCharField(
        label="5. Please enter any other names your organisation is known by",
        max_length=50,
        help_text="If your organisation is not known by any other names, please type <strong>none</strong>.",
    )

    agent_address_line_1 = fields.FCLCharField(label="Address line 1")

    agent_address_line_2 = fields.FCLCharField(label="Address line 2 (optional)", required=False)

    agent_town = fields.FCLCharField(label="Town or city")

    agent_county = fields.FCLCharField(label="County (optional)", required=False)

    agent_postcode = fields.FCLCharField(label="Postcode")

    agent_country = fields.FCLChoiceField(
        label="Country",
        choices=countries_and_territories_choices,
        widget=forms.Select(attrs={"class": "location-autocomplete"}),
    )

    tna_contacttype = fields.FCLMultipleChoiceFieldWithOthers(
        label="7. What type of organisation is it?",
        help_text="Select all that apply.",
        choices=list_to_choices(choices.TNA_CONTACTTYPE_CHOICES),
        other_fields={9: "other"},
    )

    agent_companyid = fields.FCLCharField(
        max_length=100,
        label="8. Please provide your organisation identifier (e.g. company number or charity registration number)",
        help_text="If your organisation does not have an identifier, please type <strong>none</strong>.",
    )
    partners = fields.FCLCharField(
        max_length=100,
        label=(
            "9. Please provide the name of any partners or organisations "
            "you are working with to do the computational analysis"
        ),
        help_text="If you are not working with any partners or organisations, please type <strong>none</strong>.",
    )


class ProjectPurposeForm(LicenseApplicationForm):
    step_index = 3

    title = "Step 4 – Purpose and activities"

    project_name = fields.FCLCharField(
        label="10. Please give any project or product name associated with this work",
        max_length=250,
    )
    project_url = fields.FCLCharField(
        label="11. Please share a link to the project or product site",
        help_text="If you cannot share a link, please type <strong>none</strong>.",
        max_length=250,
    )

    project_purpose = fields.FCLMultipleChoiceFieldWithOthers(
        label="12. What is the main purpose of your project or product?",
        help_text="Select all that apply.",
        choices=list_to_choices(choices.PROJECT_PURPOSE_CHOICES),
        other_fields={5: "other"},
    )

    user = fields.FCLChoiceField(
        label="13. Which one best describes who will be able to access the outcomes of your computational analysis?",
        help_text="Please select one.",
        choices=list_to_choices(choices.USER_CHOICES),
    )

    benefit = fields.FCLMultipleChoiceFieldWithOthers(
        label="14. Which Individuals or communities will benefit from your computational analysis?",
        help_text="Select all that apply.",
        choices=list_to_choices(choices.BENEFIT_CHOICES),
        other_fields={6: "community_other", 7: "profession_other", 8: "other"},
    )


class PublicStatementForm(LicenseApplicationForm):
    step_index = 4

    title = "Step 5 – Public statement"

    def layout(self):
        return Layout(Field.textarea("public_statement", max_words=150))

    public_statement = fields.FCLCharField(
        label="15. Please provide a public statement",
        help_text="Please aim for 50-150 words",
        widget=forms.Textarea(),
        validators=[lambda v: validate_max_words(v, max_words=150)],
    )


class WorkingPractices1Form(LicenseApplicationForm):
    step_index = 5

    title = "Step 6 – Working practices"

    focus_on_specific = fields.FCLChoiceField(
        label="16. Will the computational analysis focus on specific individuals or specific groups of people?",
        choices=list_to_choices(choices.YES_NO_CHOICES),
    )
    anonymise_individuals = fields.FCLChoiceField(
        label="17. Will you anonymise individuals before you analyse records?",
        choices=list_to_choices(choices.YES_NO_CHOICES),
    )
    algorithm_review = fields.FCLChoiceField(
        label="18. Will you regularly review algorithms for bias?",
        choices=list_to_choices(choices.YES_NO_CHOICES),
    )
    code_of_ethics = fields.FCLChoiceField(
        label="19. Will you abide by a code of ethics?",
        choices=list_to_choices(choices.YES_NO_CHOICES),
    )
    third_party_ethics_review = fields.FCLChoiceField(
        label="20. Will an impartial party review your work against an ethical framework?",
        help_text="For example, an Ethics Advisory Board (EAB) or Research Ethics Committee (REC).",
        choices=list_to_choices(choices.YES_NO_CHOICES),
    )


class WorkingPractices2Form(LicenseApplicationForm):
    step_index = 6

    title = "Step 7 – Working practices"

    entire_record_available = fields.FCLChoiceField(
        label="21. Will you make the entire record available online?",
        help_text=(
            "For example, you may choose to signpost a full judgment "
            "to users, where you have published or highlighted parts "
            "of a judgment."
        ),
        choices=list_to_choices(choices.YES_NO_CHOICES),
    )
    data_extracted_available = fields.FCLChoiceField(
        label="22. Will data extracted from these records be published online?",
        help_text=(
            "For example, any statistical analysis, for example: lists of citations or entities from within the records"
        ),
        choices=list_to_choices(choices.YES_NO_CHOICES),
    )
    methodology_available = fields.FCLChoiceField(
        label="23. For transparency, will you make your methodology available to others for scrutiny?",
        choices=list_to_choices(choices.YES_NO_CHOICES),
    )
    publish_findings = fields.FCLChoiceField(
        label="24. Will you analyse and publish findings online?",
        choices=list_to_choices(choices.YES_NO_CHOICES),
    )
    computational_analysis_type = fields.FCLMultipleChoiceField(
        label="25. Do you intend to use computational analysis to do any of the following?",
        help_text="Select all that apply.",
        choices=list_to_choices(choices.COMPUTATIONAL_ANALYSIS_TYPE_CHOICES),
    )
    generative_ai_use = fields.FCLChoiceField(
        label="26. Will you notify people when they are using generative AI services or content?",
        choices=list_to_choices(choices.GENERATIVE_AI_USE_CHOICES),
    )
    explain_limitations = fields.FCLChoiceField(
        label=(
            "27. Will you explain how the limits of the Find Case Law "
            "collection impacts the outcomes of your computational analysis?"
        ),
        choices=list_to_choices(choices.YES_NO_CHOICES),
    )


class NinePrinciplesAgreementForm(LicenseApplicationForm):
    step_index = 7

    title = "Step 8 – Nine principles"

    accept_principles = fields.FCLChoiceField(
        label=(
            "28. Licence holders must acknowledge and abide by all the nine principles."
            "Do you accept all nine principles as licence terms?"
        ),
        choices=list_to_choices(choices.YES_NO_CHOICES),
    )


class NinePrinciplesStatementForm(LicenseApplicationForm):
    step_index = 8

    title = "Step 9 – Nine principles statement"

    def layout(self):
        return Layout(
            Field.textarea("principles_statement"),
        )

    principles_statement = fields.FCLCharField(
        label="29. Please describe how you will meet the nine principles as terms.",
        widget=forms.Textarea(attrs={"maxlength": 500000}),
    )


class AdditionalCommentsForm(LicenseApplicationForm):
    step_index = 9

    title = "Step 10 – Additional comments"

    def layout(self):
        return Layout(
            Field.textarea("additional_comments", max_words=250),
        )

    additional_comments = fields.FCLCharField(
        label="30. Are there any additional comments you would like us to consider as part of your application?",
        help_text="This question is optional.",
        widget=forms.Textarea(attrs={"data-maxwords": 250, "maxlength": 1500}),
        required=False,
    )


class ReviewForm(LicenseApplicationForm):
    step_index = 10

    title = "Step 11 – Review your Answers"
    display_in_review = False
    # The Review screen has to be a form 'step' with none of its own inputs
    # and a custom template, as once the `done` callback of the form-tools
    # wizard is called, the form data has been scrubbed from the session,
    # making amendments impossible.
    pass


FORMS = (
    ("contact", ContactForm),
    ("organization", OrganizationForm),
    ("project-purpose", ProjectPurposeForm),
    ("public-statement", PublicStatementForm),
    ("working-practices-1", WorkingPractices1Form),
    ("working-practices-2", WorkingPractices2Form),
    ("nine-principles-1", NinePrinciplesAgreementForm),
    ("nine-principles-2", NinePrinciplesStatementForm),
    ("additional-comments", AdditionalCommentsForm),
    ("review", ReviewForm),
)
