from django import forms

from .utils import countries_and_territories

YES_NO_CHOICES = ["Yes", "No"]


def with_label_class(class_name, field):
    field.label_class = class_name
    return field


def list_to_choices(values):
    return [(v, v) for v in values]


class FCLFormMixin(object):
    def __init__(self, **kwargs):
        self.send_to_dynamics = kwargs.pop("send_to_dynamics", True)
        self.label_class = kwargs.pop("label_class", None)
        super(FCLFormMixin, self).__init__(**kwargs)


class FCLCharField(FCLFormMixin, forms.CharField):
    pass


class FCLChoiceField(FCLFormMixin, forms.ChoiceField):
    pass


class FCLMultipleChoiceField(FCLFormMixin, forms.MultipleChoiceField):
    pass


class ContactForm(forms.Form):

    ALTERNATIVE_CONTACT_CHOICES = [
        "This is the same person as the main contact",
        "This is a different person (please enter their details below)",
    ]

    contact_lastname = FCLCharField(
        label="The full name of the person we can discuss your licence application with",
        max_length=50,
    )
    contact_email = FCLCharField(
        label="The email address of the person we can discuss your licence application with",
        max_length=50,
    )
    alternative_contact = FCLChoiceField(
        label=(
            "We need to ensure we have contact details of the person in your "
            "organisation who will be responsible for licence compliance. This "
            "should be someone senior who has overall responsibility for "
            "ensuring your organisation complies with all terms and conditions "
            "of the licence."
        ),
        widget=forms.RadioSelect,
        choices=list_to_choices(ALTERNATIVE_CONTACT_CHOICES),
        label_class="as_para",
    )
    licence_holder_lastname = FCLCharField(
        label="The full name of the person in your organisation who will be responsible for licence compliance",
        max_length=50,
        show_hidden_initial=True,
    )
    licence_holder_email = FCLCharField(
        label="The email address of the person in your organisation who will be responsible for licence compliance",
        max_length=50,
        show_hidden_initial=True,
    )


class OrganizationForm(forms.Form):

    TNA_CONTACTTYPE_CHOICES = [
        "Private limited company",
        "Public limited company",
        "Partnership",
        "Sole trader",
        "Registered Charity",
        "Community interest company",
        "Independent research organisation",
        "Public body",
        "Independent body",
        "Other (please specify)",
    ]

    agent_companyname = FCLCharField(
        label="What is the full legal name of your organisation?", max_length=50
    )
    agent_companyname_other = FCLCharField(
        label="Please enter any other names your organisation is known by",
        max_length=50,
        help_text="If your organisation is not known by any other names, please type <strong>none</strong>.",
    )
    agent_country = FCLChoiceField(
        label="Where is your organisation registered?",
        choices=countries_and_territories,
        widget=forms.Select(attrs={"class": "location-autocomplete"}),
    )

    tna_contacttype = FCLMultipleChoiceField(
        label="What type of organisation is it?",
        help_text="Select all that apply.",
        widget=forms.CheckboxSelectMultiple,
        choices=list_to_choices(TNA_CONTACTTYPE_CHOICES),
    )
    org_other = FCLCharField(max_length=50)
    agent_companyid = FCLCharField(
        max_length=100,
        label="Please provide your organisation identifier (e.g. company number or charity registration number)",
        help_text="If your organisation does not have an identifier, please type <strong>none</strong>.",
    )
    partners = FCLCharField(
        max_length=100,
        label="Please provide the name of any partners or organisations you are working with",
        help_text="If you are not working with any partners or organisations, please type <strong>none</strong>.",
    )


class ProjectPurposeForm(forms.Form):

    PROJECT_PURPOSE_CHOICES = [
        "Publish legal information",
        "Produce summaries and interpretation of the records",
        "Research and develop new technologies",
        "Research activity and trends across records",
        "Deliver a consumer service",
        "Other (please specify)",
    ]

    USER_CHOICES = [
        "Public access (e.g. anyone can freely access)",
        "Restricted access (e.g. only subscribers or research peers)",
        "Internal access (e.g. only colleagues from within your organisation)",
        "Private for personal use only",
    ]

    BENEFIT_CHOICES = [
        "General public",
        "Legal professionals and law firms",
        "Court users (e.g. litigants in person)",
        "The Judiciary",
        "Public bodies",
        "Researchers and academics",
        "A specific community (please specify)",
        "A specific (non-legal) profession (please specify)",
        "Other (please specify)",
    ]

    project_name = FCLCharField(
        label="Please give any project or product name associated with this work",
        max_length=250,
    )
    project_url = FCLCharField(
        label="Please share a link to the project or product site",
        help_text="If you cannot share a link, please type <strong>none</strong>.",
        max_length=250,
    )
    project_purpose = FCLMultipleChoiceField(
        label="What is the main purpose of your project or product?",
        help_text="Select all that apply.",
        widget=forms.CheckboxSelectMultiple,
        choices=list_to_choices(PROJECT_PURPOSE_CHOICES),
    )
    purpose_other = FCLCharField(max_length=50)
    user = FCLChoiceField(
        label="Which one best describes who will be able to access the outcomes of your computational analysis?",
        help_text="Please select one.",
        widget=forms.RadioSelect,
        choices=list_to_choices(USER_CHOICES),
    )
    benefit = FCLMultipleChoiceField(
        label="Which Individuals or communities will benefit from your computational analysis?",
        help_text="Select all that apply.",
        widget=forms.CheckboxSelectMultiple,
        choices=list_to_choices(BENEFIT_CHOICES),
    )
    community_other = FCLCharField(max_length=50)
    profession_other = FCLCharField(max_length=50)
    benefit_other = FCLCharField(max_length=50)


class PublicStatementForm(forms.Form):
    public_statement = FCLCharField(
        label="Please provide a public statement",
        help_text="Please aim for no more than around 150 words.",
        max_length=1500,
        widget=forms.Textarea,
    )


class WorkingPractices1Form(forms.Form):
    focus_on_specific = FCLChoiceField(
        label=" Will the computational analysis focus on specific individuals or specific groups of people?",
        widget=forms.RadioSelect,
        choices=list_to_choices(YES_NO_CHOICES),
    )
    anonymise_individuals = FCLChoiceField(
        label="Will you anonymise individuals before you analyse records?",
        widget=forms.RadioSelect,
        choices=list_to_choices(YES_NO_CHOICES),
    )
    algorithm_review = FCLChoiceField(
        label="Will you regularly review algorithms for bias?",
        widget=forms.RadioSelect,
        choices=list_to_choices(YES_NO_CHOICES),
    )
    code_of_ethics = FCLChoiceField(
        label="Will you abide by a code of ethics?",
        widget=forms.RadioSelect,
        choices=list_to_choices(YES_NO_CHOICES),
    )
    third_party_ethics_review = FCLChoiceField(
        label="Will an impartial party review your work against an ethical framework?",
        help_text="For example, an Ethics Advisory Board (EAB) or Research Ethics Committee (REC).",
        widget=forms.RadioSelect,
        choices=list_to_choices(YES_NO_CHOICES),
    )


class WorkingPractices2Form(forms.Form):

    COMPUTATIONAL_ANALYSIS_TYPE_CHOICES = [
        "Produce fully automated legal advice",
        "Perform automation to anticipate legal decisions directly for a client or consumer",
        "Directly inform or influence the decision of a third-party whether to pursue justice or legal action",
        "None of the above",
    ]

    GENERATIVE_AI_USE_CHOICES = YES_NO_CHOICES + ["Not using Generative AI"]

    entire_record_available = FCLChoiceField(
        label="Will you make the entire record available online?",
        help_text=(
            "For example, you may choose to signpost a full judgment "
            "to users, where you have published or highlighted parts "
            "of a judgment."
        ),
        widget=forms.RadioSelect,
        choices=list_to_choices(YES_NO_CHOICES),
    )
    data_extracted_available = FCLChoiceField(
        label="Will data extracted from these records be published online?",
        help_text="Any statistical analysis, for example: lists of citations or entities from within the records",
        widget=forms.RadioSelect,
        choices=list_to_choices(YES_NO_CHOICES),
    )
    methodology_available = FCLChoiceField(
        label="For transparency, will you make your methodology available to others for scrutiny?",
        widget=forms.RadioSelect,
        choices=list_to_choices(YES_NO_CHOICES),
    )
    publish_findings = FCLChoiceField(
        label="Will you analyse and publish findings online?",
        widget=forms.RadioSelect,
        choices=list_to_choices(YES_NO_CHOICES),
    )
    computational_analysis_type = FCLMultipleChoiceField(
        label="Do you intend to use computational analysis to do any of the following?",
        help_text="Select all that apply.",
        widget=forms.CheckboxSelectMultiple,
        choices=list_to_choices(COMPUTATIONAL_ANALYSIS_TYPE_CHOICES),
    )
    generative_ai_use = FCLChoiceField(
        label="Will you notify people when they are using generative AI services or content?",
        widget=forms.RadioSelect,
        choices=list_to_choices(GENERATIVE_AI_USE_CHOICES),
    )
    explain_limitations = FCLChoiceField(
        label=(
            "Will you explain how the limits of the find case law "
            "collection impacts your computational analysis to users?"
        ),
        widget=forms.RadioSelect,
        choices=list_to_choices(YES_NO_CHOICES),
    )


class NinePrinciplesForm(forms.Form):
    accept_principles = FCLChoiceField(
        label="Licence holders must acknowledge and abide by all the 9 principles. Do you accept this licence term?",
        widget=forms.RadioSelect,
        choices=list_to_choices(YES_NO_CHOICES),
    )

    principles_statement = FCLCharField(
        label="Please describe how you will meet the 9 principles",
        help_text="You should identify any risks and how you will address these risks for each of the 9 principles.",
        max_length=1500,
        widget=forms.Textarea,
    )

    additional_comments = FCLCharField(
        label="Are there any additional comments you would like to make in relation to your application?",
        help_text="This question is optional.",
        max_length=500,
        widget=forms.Textarea,
    )


class ReviewForm(forms.Form):
    # The Review screen has to be a form 'step' with none of its own inputs
    # and a custom tempalte, as once the `done` callback of the form-tools
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
    ("nine-principles", NinePrinciplesForm),
    ("review", ReviewForm),
)
