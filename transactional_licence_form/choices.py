YES_NO_CHOICES = ["Yes", "No"]

# NOTE: please see comment in transactional_lcence_form.js if
# changing the wording / order of the options for the alternative contact.
ALTERNATIVE_CONTACT_CHOICES = [
    ("No", "This is the same person as the main contact"),
    ("Yes", "This is a different person (please enter their details below)"),
]

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

COMPUTATIONAL_ANALYSIS_TYPE_CHOICES = [
    "Produce fully automated legal advice",
    "Perform automation to anticipate legal decisions directly for a client or consumer",
    "Directly inform or influence the decision of a third-party whether to pursue justice or legal action",
    "None of the above",
]

GENERATIVE_AI_USE_CHOICES = YES_NO_CHOICES + ["Not using Generative AI"]
