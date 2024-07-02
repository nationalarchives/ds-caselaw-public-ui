import re

from playwright.sync_api import Page, expect


def test_transactional_licence_form(page: Page):
    """
    Test the process to apply for a computational analysis licence.
    We stop on the review page (short of actually submitting the form)
    (which triggers an email to the licencing team): the final step will be tested
    in isolation with a mocked email service."""

    # Preamble pages
    page.goto("/re-use-find-case-law-records/")
    page.get_by_text("I want to perform computational analysis").click()
    page.get_by_text("What you need to apply for a licence").click()
    page.get_by_role("button", name="Apply for a licence").click()
    page.get_by_text("Apply now").click()

    # Contact details
    page.get_by_label("Contact Full Name").fill("Full Name")
    page.get_by_label("Contact Email address").fill("contact@example.com")
    page.get_by_label("This is a different person (please enter their details below)").click()
    page.get_by_label("Licence holder Full Name").fill("Licence Holder")
    page.get_by_label("Licence holder Email").fill("licenceholder@example.com")
    page.get_by_text("Next").click()

    # Organization details
    page.get_by_label("What is the full legal name of your organisation?").fill("Organisation name")
    page.get_by_label("Please enter any other names your organisation is known by").fill("Organisation alias")
    page.get_by_label("Which country is your organisation registered in?").fill("Chi")
    page.get_by_role("option", name="Chile").click()
    page.get_by_label("Private limited company").click()
    page.get_by_label("Other (please specify)").click()
    page.locator("input[name='organization-tna_contacttype_other']").fill("Other organisation type")
    page.get_by_label(
        "Please provide your organisation identifier (e.g. company number or charity registration number) "
    ).fill("Organisation identifier")
    page.get_by_label("Please provide the name of any partners or organisations you are working with").fill("Partners")
    page.get_by_text("Next").click()

    # Purpose and Activities
    page.get_by_label("Please give any project or product name associated with this work").fill("Project name")
    page.get_by_label("Please share a link to the project or product site").fill("https://example.com")
    page.get_by_label("Publish legal information").click()
    page.get_by_role("group", name="What is the main purpose").get_by_label("Other (please specify)").click()
    page.locator("input[name='project-purpose-project_purpose_other']").fill("Other purpose")
    page.get_by_label("Restricted access (e.g. only subscribers or research peers)").click()
    page.get_by_label("Public bodies").click()
    page.get_by_role("group", name="Which Individuals or communities will benefit").get_by_label(
        "Other (please specify)"
    ).click()
    page.locator("input[name='project-purpose-benefit_other']").fill("Other benefit")
    page.get_by_text("Next").click()

    # Public Sttatement
    page.get_by_label("Please provide a public statement").fill("Public statement")
    page.get_by_text("Next").click()

    # Working practices
    page.get_by_role(
        "group",
        name="Will the computational analysis focus on specific individuals or specific groups of people?",
    ).get_by_label("No").click()
    page.get_by_role("group", name=" Will you anonymise individuals before you analyse records?").get_by_label(
        "Yes"
    ).click()
    page.get_by_role("group", name="Will you regularly review algorithms for bias?").get_by_label("No").click()
    page.get_by_role("group", name="Will you abide by a code of ethics?").get_by_label("Yes").click()
    page.get_by_role(
        "group",
        name="Will an impartial party review your work against an ethical framework?",
    ).get_by_label("No").click()
    page.get_by_text("Next").click()

    # Working practices - 2
    page.get_by_role("group", name="Will you make the entire record available online?").get_by_label("No").click()
    page.get_by_role("group", name="Will data extracted from these records be published online?").get_by_label(
        "Yes"
    ).click()
    page.get_by_role("group", name="will you make your methodology available to others for scrutiny?").get_by_label(
        "No"
    ).click()
    page.get_by_role("group", name="Will you analyse and publish findings online?").get_by_label("Yes").click()
    page.get_by_label("Directly inform or influence the decision of a third-party").click()
    page.get_by_label("Not using Generative AI").click()
    page.get_by_role(
        "group",
        name="Will you explain how the limits of the Find Case Law collection",
    ).get_by_label("No").click()
    page.get_by_text("Next").click()

    # Nine principles - 1
    page.get_by_label("Yes").click()
    page.get_by_text("Next").click()

    # Nine principles - 2
    page.get_by_label("Please describe how you will meet the 9 principles as terms.").fill("Nine principles statement")
    page.get_by_text("Next").click()

    # Additional comments
    page.get_by_label(
        "Are there any additional comments you would like us to consider as part of your application?"
    ).fill("Additional comments")
    page.get_by_text("Next").click()

    # Review
    def get_review_row(page, label):
        return page.locator("dt", has_text=label).locator("..").locator("dd.govuk-summary-list__value")

    expect(get_review_row(page, "Contact Full Name")).to_have_text("Full Name")
    expect(get_review_row(page, "Contact Email address")).to_have_text("contact@example.com")
    expect(get_review_row(page, "We need the contact details of the person")).to_have_text("Yes")
    expect(get_review_row(page, "Licence holder full name")).to_have_text("Licence Holder")
    expect(get_review_row(page, "Licence holder Email")).to_have_text("licenceholder@example.com")

    expect(get_review_row(page, "What is the full legal name")).to_have_text("Organisation name")
    expect(get_review_row(page, "Please enter any other names")).to_have_text("Organisation alias")
    expect(get_review_row(page, "Which country is your organisation")).to_have_text("Chile")
    expect(get_review_row(page, "What type of organisation")).to_have_text(re.compile("Private limited company"))
    expect(get_review_row(page, "What type of organisation")).to_have_text(re.compile("Other organisation type"))

    expect(get_review_row(page, "Please provide your organisation identifier")).to_have_text("Organisation identifier")
    expect(get_review_row(page, "Please provide the name of any partners or organisations")).to_have_text("Partners")

    expect(get_review_row(page, "Please give any project or product name associated with this work")).to_have_text(
        "Project name"
    )
    expect(get_review_row(page, "Please share a link to the project or product site")).to_have_text(
        "https://example.com"
    )
    expect(get_review_row(page, "What is the main purpose")).to_have_text(re.compile("Publish legal information"))
    expect(get_review_row(page, "What is the main purpose")).to_have_text(re.compile("Other purpose"))
    expect(get_review_row(page, "Which one best describes who will be able to access the outcomes")).to_have_text(
        "Restricted access (e.g. only subscribers or research peers)"
    )
    expect(get_review_row(page, "Which individuals or communities")).to_have_text(re.compile("Public bodies"))
    expect(get_review_row(page, "Which individuals or communities")).to_have_text(re.compile("Other benefit"))

    expect(get_review_row(page, "Please provide a public statement")).to_have_text("Public statement")

    expect(
        get_review_row(
            page,
            "Will the computational analysis focus on specific individuals or specific groups of people?",
        )
    ).to_have_text("No")
    expect(get_review_row(page, "Will you anonymise individuals before you analyse records?")).to_have_text("Yes")
    expect(get_review_row(page, "Will you regularly review algorithms for bias?")).to_have_text("No")
    expect(get_review_row(page, "Will you abide by a code of ethics?")).to_have_text("Yes")
    expect(
        get_review_row(
            page,
            "Will an impartial party review your work against an ethical framework?",
        )
    ).to_have_text("No")

    expect(get_review_row(page, "Will you make the entire record available online?")).to_have_text("No")
    expect(get_review_row(page, "Will data extracted from these records be published online?")).to_have_text("Yes")
    expect(get_review_row(page, "will you make your methodology available to others for scrutiny?")).to_have_text("No")
    expect(get_review_row(page, "Will you analyse and publish findings online?")).to_have_text("Yes")
    expect(get_review_row(page, "Do you intend to use computational analysis")).to_have_text(
        re.compile("Directly inform or influence the decision of a third-party")
    )
    expect(get_review_row(page, "Will you notify people when they are using generative AI")).to_have_text(
        "Not using Generative AI"
    )
    expect(
        get_review_row(
            page,
            "Will you explain how the limits of the Find Case Law collection",
        )
    ).to_have_text("No")

    expect(get_review_row(page, "Licence holders must acknowledge and abide by all the 9 principles.")).to_have_text(
        "Yes"
    )

    expect(get_review_row(page, "Please describe how you will meet the 9 principles as terms.")).to_have_text(
        "Nine principles statement"
    )

    expect(
        get_review_row(
            page,
            "Are there any additional comments you would like us to consider as part of your application?",
        )
    ).to_have_text("Additional comments")

    # Editing responses
    page.locator("dt", has_text="Contact Full Name").locator("..").get_by_text("Change").click()
    page.get_by_label("Contact Full Name").fill("New Full Name")
    page.get_by_text("Next").click()
    page.get_by_label("What is the full legal name of your organisation?").fill("New Organisation name")
    page.get_by_text("Save and review").click()

    expect(get_review_row(page, "Contact Full Name")).to_have_text("New Full Name")
    expect(get_review_row(page, "What is the full legal name")).to_have_text("New Organisation name")


def test_data_saved_when_going_back(page: Page):
    """
    Test the process to apply for a computational analysis licence.
    We stop on the review page (short of actually submitting the form)
    (which triggers an email to the licencing team): the final step will be tested
    in isolation with a mocked email service."""

    # Fill contact details in full
    page.goto("/re-use-find-case-law-records/steps/contact")
    page.get_by_label("Contact Full Name").fill("Full Name")
    page.get_by_label("Contact Email address").fill("contact@example.com")
    page.get_by_label("This is a different person (please enter their details below)").click()
    page.get_by_label("Licence holder Full Name").fill("Licence Holder")
    page.get_by_label("Licence holder Email").fill("licenceholder@example.com")

    # On the next page, fill only 1 field, leaving others blank
    page.get_by_text("Next").click()
    page.get_by_label("What is the full legal name of your organisation?").fill("Organisation name")

    # Check previous page has information
    page.get_by_text("Previous").click()
    expect(page.get_by_label("Contact Full Name")).to_have_value("Full Name")

    # Check incomplete next page has information
    page.get_by_text("Next").click()
    expect(page.get_by_label("What is the full legal name of your organisation?")).to_have_value("Organisation name")
