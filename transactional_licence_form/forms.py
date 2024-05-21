from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Field, Layout
from django import forms

from . import choices, fields
from .utils import countries_and_territories_choices, list_to_choices


class FCLForm(forms.Form):

    display_in_review = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = self.layout()

    def layout(self):
        pass


class ContactForm(FCLForm):
    title = "Contact Details"

    contact_lastname = fields.FCLCharField(
        label="The full name of the person we can discuss your licence application with",
        max_length=50,
    )
    contact_email = fields.FCLEmailField(
        label="The email address of the person we can discuss your licence application with",
        max_length=50,
    )
    # NOTE: please see comment in transactional_lcence_form.js if changing the wording / order of the options here.
    alternative_contact = fields.FCLChoiceField(
        label=(
            "We need to ensure we have contact details of the person in your "
            "organisation who will be responsible for licence compliance. This "
            "should be someone senior who has overall responsibility for "
            "ensuring your organisation complies with all terms and conditions "
            "of the licence."
        ),
        choices=list_to_choices(choices.ALTERNATIVE_CONTACT_CHOICES),
        label_class="as_para",
    )
    licence_holder_lastname = fields.FCLCharField(
        label="The full name of the person in your organisation who will be responsible for licence compliance",
        max_length=50,
        show_hidden_initial=True,
        required=False,
    )
    licence_holder_email = fields.FCLEmailField(
        label="The email address of the person in your organisation who will be responsible for licence compliance",
        max_length=50,
        show_hidden_initial=True,
        required=False,
    )


class OrganizationForm(FCLForm):

    title = "About your organisastion"

    agent_companyname = fields.FCLCharField(
        label="What is the full legal name of your organisation?", max_length=50
    )
    agent_companyname_other = fields.FCLCharField(
        label="Please enter any other names your organisation is known by",
        max_length=50,
        help_text="If your organisation is not known by any other names, please type <strong>none</strong>.",
    )
    agent_country = fields.FCLChoiceField(
        label="Where is your organisation registered?",
        choices=countries_and_territories_choices,
        widget=forms.Select(attrs={"class": "location-autocomplete"}),
    )

    tna_contacttype = fields.FCLMultipleChoiceFieldWithOthers(
        label="What type of organisation is it?",
        help_text="Select all that apply.",
        choices=list_to_choices(choices.TNA_CONTACTTYPE_CHOICES),
        other_fields={9: "other"},
    )

    agent_companyid = fields.FCLCharField(
        max_length=100,
        label="Please provide your organisation identifier (e.g. company number or charity registration number)",
        help_text="If your organisation does not have an identifier, please type <strong>none</strong>.",
    )
    partners = fields.FCLCharField(
        max_length=100,
        label="Please provide the name of any partners or organisations you are working with",
        help_text="If you are not working with any partners or organisations, please type <strong>none</strong>.",
    )


class ProjectPurposeForm(FCLForm):
    title = "Purpose and Activities"

    project_name = fields.FCLCharField(
        label="Please give any project or product name associated with this work",
        max_length=250,
    )
    project_url = fields.FCLCharField(
        label="Please share a link to the project or product site",
        help_text="If you cannot share a link, please type <strong>none</strong>.",
        max_length=250,
    )

    project_purpose = fields.FCLMultipleChoiceFieldWithOthers(
        label="What is the main purpose of your project or product?",
        help_text="Select all that apply.",
        choices=list_to_choices(choices.PROJECT_PURPOSE_CHOICES),
        other_fields={5: "other"},
    )

    user = fields.FCLChoiceField(
        label="Which one best describes who will be able to access the outcomes of your computational analysis?",
        help_text="Please select one.",
        choices=list_to_choices(choices.USER_CHOICES),
    )

    benefit = fields.FCLMultipleChoiceFieldWithOthers(
        label="Which Individuals or communities will benefit from your computational analysis?",
        help_text="Select all that apply.",
        choices=list_to_choices(choices.BENEFIT_CHOICES),
        other_fields={6: "community_other", 7: "profession_other", 8: "benefit_other"},
    )


class PublicStatementForm(FCLForm):

    title = "Public Statement"

    def layout(self):
        return Layout(Field.textarea("public_statement", max_words=150))

    public_statement = fields.FCLCharField(
        label="Please provide a public statement",
        help_text="Please aim for no more than around 150 words.",
        widget=forms.Textarea(attrs={"data-maxwords": 150}),
    )


class WorkingPractices1Form(FCLForm):

    title = "Working Practices"

    focus_on_specific = fields.FCLChoiceField(
        label=" Will the computational analysis focus on specific individuals or specific groups of people?",
        choices=list_to_choices(choices.YES_NO_CHOICES),
    )
    anonymise_individuals = fields.FCLChoiceField(
        label="Will you anonymise individuals before you analyse records?",
        choices=list_to_choices(choices.YES_NO_CHOICES),
    )
    algorithm_review = fields.FCLChoiceField(
        label="Will you regularly review algorithms for bias?",
        choices=list_to_choices(choices.YES_NO_CHOICES),
    )
    code_of_ethics = fields.FCLChoiceField(
        label="Will you abide by a code of ethics?",
        choices=list_to_choices(choices.YES_NO_CHOICES),
    )
    third_party_ethics_review = fields.FCLChoiceField(
        label="Will an impartial party review your work against an ethical framework?",
        help_text="For example, an Ethics Advisory Board (EAB) or Research Ethics Committee (REC).",
        choices=list_to_choices(choices.YES_NO_CHOICES),
    )


class WorkingPractices2Form(FCLForm):

    title = "Working Practices"

    entire_record_available = fields.FCLChoiceField(
        label="Will you make the entire record available online?",
        help_text=(
            "For example, you may choose to signpost a full judgment "
            "to users, where you have published or highlighted parts "
            "of a judgment."
        ),
        choices=list_to_choices(choices.YES_NO_CHOICES),
    )
    data_extracted_available = fields.FCLChoiceField(
        label="Will data extracted from these records be published online?",
        help_text="Any statistical analysis, for example: lists of citations or entities from within the records",
        choices=list_to_choices(choices.YES_NO_CHOICES),
    )
    methodology_available = fields.FCLChoiceField(
        label="For transparency, will you make your methodology available to others for scrutiny?",
        choices=list_to_choices(choices.YES_NO_CHOICES),
    )
    publish_findings = fields.FCLChoiceField(
        label="Will you analyse and publish findings online?",
        choices=list_to_choices(choices.YES_NO_CHOICES),
    )
    computational_analysis_type = fields.FCLMultipleChoiceField(
        label="Do you intend to use computational analysis to do any of the following?",
        help_text="Select all that apply.",
        choices=list_to_choices(choices.COMPUTATIONAL_ANALYSIS_TYPE_CHOICES),
    )
    generative_ai_use = fields.FCLChoiceField(
        label="Will you notify people when they are using generative AI services or content?",
        choices=list_to_choices(choices.GENERATIVE_AI_USE_CHOICES),
    )
    explain_limitations = fields.FCLChoiceField(
        label=(
            "Will you explain how the limits of the find case law "
            "collection impacts your computational analysis to users?"
        ),
        choices=list_to_choices(choices.YES_NO_CHOICES),
    )


class NinePrinciplesAgreementForm(FCLForm):
    title = "Statements and Principles"

    accept_principles = fields.FCLChoiceField(
        label="Licence holders must acknowledge and abide by all the 9 principles. Do you accept this licence term?",
        choices=list_to_choices(choices.YES_NO_CHOICES),
    )


class NinePrinciplesStatementForm(FCLForm):
    title = "Statements and Principles"

    def layout(self):
        return Layout(
            Field.textarea("principles_statement", max_words=150),
        )

    principles_statement = fields.FCLCharField(
        label="Please describe how you will meet the 9 principles",
        help_text="You should identify any risks and how you will address these risks for each of the 9 principles.",
        widget=forms.Textarea(attrs={"data-maxwords": 150}),
    )


class AdditionalCommentsForm(FCLForm):
    title = "Additional Comments"

    def layout(self):
        return Layout(
            Field.textarea("additional_comments", max_words=250),
        )

    additional_comments = fields.FCLCharField(
        label="Are there any additional comments you would like to make in relation to your application?",
        help_text="This question is optional.",
        widget=forms.Textarea(attrs={"data-maxwords": 250}),
    )


class ReviewForm(FCLForm):
    title = "Review your Answers"
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
