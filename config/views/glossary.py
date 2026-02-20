import string
from dataclasses import dataclass

from django.urls import reverse

from .template_view_with_context import TemplateViewWithContext


@dataclass(frozen=True)
class Term:
    title: str
    meaning: str


TERMS: list[Term] = [
    Term(
        "Anonymisation",
        "The process of removing or replacing names and identifying details in a judgment to protect someone's identity. Courts sometimes use anonymisation in cases involving children or vulnerable people. You might see initials like 'AB' or descriptions like 'the mother' instead of real names.",
    ),
    Term(
        "Appeal",
        "A request to a higher court to review a decision made by a lower court. If you believe a court made a legal mistake in your case, you can appeal. The appeal court doesn't re-hear the whole case - it reviews whether the law was applied correctly.",
    ),
    Term(
        "Appellant",
        "The person or organisation asking a higher court to review a decision made by a lower court. If you disagree with a court's decision and appeal it, you become the appellant.",
    ),
    Term(
        "Breach of contract",
        "When someone fails to do what they agreed to do in a contract. For example, if a builder doesn't complete work they were paid for, this could be a breach of contract. These disputes are heard in civil courts.",
    ),
    Term(
        "Case number",
        "A reference number given to a case by the court. This helps identify and track the case through the court system. Different from a neutral citation, which is assigned when the judgment is published.",
    ),
    Term(
        "Civil case",
        "A legal dispute between individuals, organisations, or both, rather than a criminal prosecution. Civil cases might involve disagreements over contracts, property, money owed, or personal injuries. The person bringing the case is the claimant, not a prosecutor.",
    ),
    Term(
        "Claimant",
        "The person or organisation who brings a case to court in a civil matter. For example, if you're taking someone to court over a dispute, you're the claimant.",
    ),
    Term(
        "Computational analysis",
        "Using computer programmes to automatically process and analyse large numbers of judgments. This includes activities like statistical analysis, text mining, or machine learning. If you want to do computational analysis of Find Case Law records, you need to apply for permission.",
    ),
    Term(
        "Criminal case",
        "A case where someone is accused of committing a crime - an offence against the law. Criminal cases are usually brought by the state (through the Crown Prosecution Service), not by individuals. The accused person is called the defendant.",
    ),
    Term(
        "Criminal offence",
        "An act that breaks the law and can be punished by the state. Criminal offences range from minor offences (like traffic violations) to serious crimes (like theft or assault). The law defines what counts as a criminal offence.",
    ),
    Term(
        "Decision",
        "The outcome reached by a court or tribunal after hearing a case. Often used interchangeably with 'judgment', though 'decision' is more commonly used for tribunal cases.",
    ),
    Term(
        "Defamation",
        "When someone publishes a false statement that damages another person's reputation. This includes libel (written or published defamation) and slander (spoken defamation). Defamation cases are civil matters, not criminal.",
    ),
    Term(
        "Defendant",
        "The person or organisation defending against a claim or accusation in court. In civil cases, this is the party being sued. In criminal cases, this is the person accused of a crime.",
    ),
    Term(
        "Division",
        "A specialist section within a court that handles particular types of cases. For example, the High Court has three divisions: King's Bench Division (general civil claims), Chancery Division (business and property), and Family Division (family matters). Each division has expertise in its area of law.",
    ),
    Term(
        "Ex tempore",
        "A Latin term meaning the judgment was given verbally by the judge in court and may not have been written down. These judgments might not appear on Find Case Law unless they were later transcribed.",
    ),
    Term(
        "Handed down judgment",
        "A written judgment that has been formally released by the court. This is the version you'll find on Find Case Law - it contains the full reasoning for the court's decision.",
    ),
    Term(
        "Inherent jurisdiction",
        "The court's power to deal with matters that aren't specifically covered by law or rules, in order to ensure justice is done. The High Court's inherent jurisdiction is often used in complex cases involving children's welfare or to prevent abuse of the court process.",
    ),
    Term(
        "Judgment",
        "The formal written decision and reasoning given by a court after hearing a case. It explains what the court decided and why. Judgments can be very long and detailed.",
    ),
    Term(
        "Judicial review",
        "A legal process where the High Court reviews whether a decision made by a public body (like a government department, local council or tribunal) was lawful. Judicial review looks at how the decision was made, not whether it was right or wrong. It's used when someone believes a public body has acted unlawfully or unfairly.",
    ),
    Term(
        "Jurisdiction",
        "The authority or power of a court to hear certain types of cases. Jurisdiction can refer to geographic area (for example, courts in England and Wales) or the type of cases a court can hear (for example, the Family Court handles family matters).",
    ),
    Term(
        "Negligence",
        "Failing to take reasonable care, which results in harm or loss to another person. For example, if someone's careless driving causes an accident, this could be negligence. Negligence cases are civil matters where the injured party can claim compensation.",
    ),
    Term(
        "Neutral citation",
        "The official reference number for a published judgment. This is the standard way to identify and cite a specific case. For example, [2024] UKSC 15 is the 15th case published by the UK Supreme Court in 2024.",
    ),
    Term(
        "Open Justice Licence",
        "The licence that allows you to freely use and re-use most judgments from Find Case Law. You can copy, share, and use judgments commercially, as long as you credit the source. The licence has some conditions to protect the administration of justice.",
    ),
    Term(
        "Party / Party name",
        "The people or organisations involved in a case - such as the claimant and defendant. Party names appear at the top of every judgment and can be used to search for specific cases on Find Case Law.",
    ),
    Term(
        "Plaintiff",
        "An older term for claimant - the person bringing a civil case to court. You might see this term in older judgments or in some jurisdictions, but 'claimant' is now the standard term used in England and Wales.",
    ),
    Term(
        "Redaction",
        "The removal or blacking out of sensitive information from a judgment before publication. Courts redact details to protect identities, comply with reporting restrictions, or remove information that shouldn't be public. You might see redacted sections marked with [REDACTED] or black bars.",
    ),
    Term(
        "Reporting restrictions",
        "Court orders that limit what information about a case can be published or shared publicly. Reporting restrictions are used to protect people (especially children and vulnerable adults) or ensure a fair trial. Judgments with reporting restrictions may have names, details, or entire sections removed.",
    ),
    Term(
        "Respondent",
        "The person or organisation responding to an appeal. If someone appeals a decision you won, you become the respondent in the appeal. The respondent usually argues that the original decision should stand.",
    ),
    Term(
        "Rex/Regina",
        "'Rex' is Latin for 'King' and 'Regina' is Latin for 'Queen'. In criminal cases, you'll see case names like 'R v Smith', which means 'The Crown against Smith' - the state prosecuting someone. 'Rex' is used when there's a King on the throne, 'Regina' when there's a Queen. Both are abbreviated as 'R'. The 'v' stands for 'versus' (against).",
    ),
    Term(
        "URI (Uniform Resource Identifier)",
        "The unique web address for each judgment on Find Case Law. The URI ensures each judgment has a permanent link that won't change. For example, /ewca/civ/2024/123 is the URI for a specific Court of Appeal judgment.",
    ),
    Term(
        "Ward of court",
        "A child or young person who has been placed under the protection and control of the High Court. When someone is made a ward of court, important decisions about their life must be approved by the court. This is used in serious cases involving a child's welfare.",
    ),
]


class GlossaryView(TemplateViewWithContext):
    template_engine = "jinja"
    template_name = "pages/glossary.jinja"
    page_title = "Find Case Law Glossary"
    page_canonical_url_name = "glossary"
    page_allow_index = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        letter = (self.request.GET.get("letter") or "a").strip().lower()
        all_terms = sorted(TERMS, key=lambda t: t.title.casefold())

        if len(letter) != 1 or letter not in string.ascii_lowercase:
            letter = "a"

        terms = [t for t in all_terms if t.title[:1].casefold() == letter]

        letters_with_terms = {
            t.title[:1].casefold() for t in all_terms if t.title and t.title[:1].casefold() in string.ascii_lowercase
        }

        letters = [
            {
                "letter": L,
                "has_terms": L.lower() in letters_with_terms,
                "is_active": L.lower() == letter,
                "href": f"?letter={L.lower()}",
            }
            for L in string.ascii_uppercase
        ]

        context["terms"] = terms
        context["letters"] = letters
        context["selected_letter"] = letter
        context["active_navigation_endpoint"] = "help_and_support"
        context["feedback_survey_type"] = "glossary"
        context["page_description"] = (
            "Find Case Law aims to make court judgments accessible to everyone. However, legal language and court terminology can be unfamiliar, even to regular users. This glossary explains common terms you'll encounter when searching for and reading court judgments, helping you understand how our service works."
        )
        context["breadcrumbs"] = [
            {"text": "Help and support", "url": reverse("help_and_support")},
            {"text": "Find Case Law Glossary"},
        ]

        return context
