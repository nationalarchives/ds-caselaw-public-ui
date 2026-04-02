import re

import pytest
from playwright.sync_api import Browser, Page, expect

from .utils.assertions import assert_is_accessible, assert_matches_snapshot


@pytest.fixture(scope="class")
def page(browser: Browser, base_url: str) -> Page:
    context = browser.new_context(
        base_url=base_url,
    )
    page = context.new_page()
    yield page
    context.close()


# Pytest tests class methods in the order they are defined
class TestTransactionalLienceForm:
    """
    Test the process to apply for a computational analysis licence.
    We stop on the review page (short of actually submitting the form)
    (which triggers an email to the licensing team): the final step will be tested
    in isolation with a mocked email service."""

    def get_review_row(self, page: Page, label: str):
        return page.locator("dt", has_text=label).locator("..").locator("dd.govuk-summary-list__value")

    def test_preamble_pages(self, page: Page):
        page.goto("/what-you-can-do-freely")

        page.get_by_role("link", name="When you need permission").click()
        page.get_by_text("What you need to apply for a licence").click()
        page.locator("a", has_text="Licence application process").click()

        assert_is_accessible(page)
        assert_matches_snapshot(page, "re_use_find_case_law_records_confirmation_page")

        page.get_by_label("Read the terms of the Open Justice Licence")
        page.get_by_text("Apply now").click()

    def test_contact_details(self, page: Page):
        assert_is_accessible(page)
        assert_matches_snapshot(page, "transactional_license_contact_details_page")
        page.get_by_label("Contact Full Name").fill("Full Name")
        page.get_by_label("Contact Email address").fill("contact@example.com")
        page.get_by_label("This is a different person (please enter their details on the next section)").click()
        page.get_by_label("Licence holder Full Name").fill("Licence Holder")
        page.get_by_label("Licence holder Email").fill("licenceholder@example.com")
        page.get_by_text("Next", exact=True).click()

    def test_organisation_details(self, page: Page):
        assert_is_accessible(page)
        assert_matches_snapshot(page, "transactional_license_organisation_details_page")
        page.get_by_label("What is the full legal name of your organisation?").fill("Organisation name")
        page.get_by_label("Please enter any other names your organisation is known by").fill("Organisation alias")
        page.get_by_label("Which country is your organisation registered in?").fill("Chi")
        page.get_by_role("option", name="Chile").click()
        page.get_by_label("Address line 1").fill("123 Organisation Road")
        page.get_by_label("Address line 2 (optional)").fill("Organisation Street")
        page.get_by_label("Town or city").fill("Organisationville")
        page.get_by_label("County (optional)").fill("Organisationshire")
        page.get_by_label("Postcode").fill("OR12 1GA")
        page.get_by_label("Private limited company").click()
        page.get_by_role("checkbox", name="Other (please specify)")

        page.locator("input[name='organization-tna_contacttype_other']").fill("Other organisation type")
        page.get_by_label(
            "Please provide your organisation identifier (e.g. company number or charity registration number) "
        ).fill("Organisation identifier")
        page.get_by_label("Please provide the name of any partners or organisations you are working with").fill(
            "Partners"
        )
        page.get_by_text("Next", exact=True).click()

    def test_purpose_and_activities(self, page: Page):
        assert_is_accessible(page)
        assert_matches_snapshot(page, "transactional_license_purpose_details_page")

        page.get_by_label("Please give any project or product name associated with this work").fill("Project name")
        page.get_by_label("Please share a link to the project or product site").fill("https://example.com")
        page.get_by_label("Publish legal information").click()

        page.get_by_role("group", name="What is the main purpose").get_by_role(
            "checkbox", name="Other (please specify)"
        ).click()

        page.locator("input[name='project-purpose-project_purpose_other']").fill("Other purpose")
        page.get_by_label("Restricted access (e.g. only subscribers or research peers)").click()
        page.get_by_label("Public bodies").click()

        page.get_by_role("group", name="Which Individuals or communities will benefit").get_by_role(
            "checkbox", name="Other (please specify)"
        ).click()

        page.locator("input[name='project-purpose-benefit_other']").fill("Other benefit")
        page.get_by_text("Next", exact=True).click()

    def test_public_statement(self, page: Page):
        assert_is_accessible(page)
        assert_matches_snapshot(page, "transactional_license_public_statement_page")
        page.get_by_label("Please provide a public statement").fill("Public statement")
        page.get_by_text("Next", exact=True).click()

    def test_working_practices(self, page: Page):
        assert_is_accessible(page)
        assert_matches_snapshot(page, "transactional_license_working_practices_1_page")
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
        page.get_by_text("Next", exact=True).click()

    def test_working_practices_2(self, page: Page):
        assert_is_accessible(page)
        assert_matches_snapshot(page, "transactional_license_working_practices_2_page")
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
        page.get_by_text("Next", exact=True).click()

    def test_nine_principles_1(self, page: Page):
        assert_is_accessible(page)
        assert_matches_snapshot(page, "transactional_license_nine_principles_1_page")
        page.get_by_label("Yes").click()
        page.get_by_text("Next", exact=True).click()

    def test_nine_principles_2(self, page: Page):
        assert_is_accessible(page)
        assert_matches_snapshot(page, "transactional_license_nine_principles_2_page")
        page.get_by_label("Please describe how you will meet the nine principles as terms.").fill(
            "Nine principles statement"
        )
        page.get_by_text("Next", exact=True).click()

    def test_additional_comments(self, page: Page):
        assert_is_accessible(page)
        page.get_by_label(
            "Are there any additional comments you would like us to consider as part of your application?"
        ).fill("Additional comments")
        page.get_by_text("Next", exact=True).click()

    def test_review(self, page: Page):
        assert_is_accessible(page)
        assert_matches_snapshot(page, "transactional_license_review_page")

        expect(self.get_review_row(page, "Contact Full Name")).to_have_text("Full Name")
        expect(self.get_review_row(page, "Contact Email address")).to_have_text("contact@example.com")
        expect(self.get_review_row(page, "We need the contact details of the person")).to_have_text("Yes")
        expect(self.get_review_row(page, "Licence holder full name")).to_have_text("Licence Holder")
        expect(self.get_review_row(page, "Licence holder Email")).to_have_text("licenceholder@example.com")

        expect(self.get_review_row(page, "What is the full legal name")).to_have_text("Organisation name")
        expect(self.get_review_row(page, "Please enter any other names")).to_have_text("Organisation alias")
        expect(self.get_review_row(page, "Address line 1")).to_have_text("123 Organisation Road")
        expect(self.get_review_row(page, "Address line 2 (optional)")).to_have_text("Organisation Street")
        expect(self.get_review_row(page, "Town or city")).to_have_text("Organisationville")
        expect(self.get_review_row(page, "County (optional)")).to_have_text("Organisationshire")
        expect(self.get_review_row(page, "Country")).to_have_text("Chile")
        expect(self.get_review_row(page, "What type of organisation")).to_have_text(
            re.compile("Private limited company")
        )
        expect(self.get_review_row(page, "What type of organisation")).to_have_text(
            re.compile("Other organisation type")
        )

        expect(self.get_review_row(page, "Please provide your organisation identifier")).to_have_text(
            "Organisation identifier"
        )
        expect(self.get_review_row(page, "Please provide the name of any partners or organisations")).to_have_text(
            "Partners"
        )

        expect(
            self.get_review_row(page, "Please give any project or product name associated with this work")
        ).to_have_text("Project name")
        expect(self.get_review_row(page, "Please share a link to the project or product site")).to_have_text(
            "https://example.com"
        )
        expect(self.get_review_row(page, "What is the main purpose")).to_have_text(
            re.compile("Publish legal information")
        )
        expect(self.get_review_row(page, "What is the main purpose")).to_have_text(re.compile("Other purpose"))
        expect(
            self.get_review_row(page, "Which one best describes who will be able to access the outcomes")
        ).to_have_text("Restricted access (e.g. only subscribers or research peers)")
        expect(self.get_review_row(page, "Which individuals or communities")).to_have_text(re.compile("Public bodies"))
        expect(self.get_review_row(page, "Which individuals or communities")).to_have_text(re.compile("Other benefit"))

        expect(self.get_review_row(page, "Please provide a public statement")).to_have_text("Public statement")

        expect(
            self.get_review_row(
                page,
                "Will the computational analysis focus on specific individuals or specific groups of people?",
            )
        ).to_have_text("No")
        expect(self.get_review_row(page, "Will you anonymise individuals before you analyse records?")).to_have_text(
            "Yes"
        )
        expect(self.get_review_row(page, "Will you regularly review algorithms for bias?")).to_have_text("No")
        expect(self.get_review_row(page, "Will you abide by a code of ethics?")).to_have_text("Yes")
        expect(
            self.get_review_row(
                page,
                "Will an impartial party review your work against an ethical framework?",
            )
        ).to_have_text("No")

        expect(self.get_review_row(page, "Will you make the entire record available online?")).to_have_text("No")
        expect(self.get_review_row(page, "Will data extracted from these records be published online?")).to_have_text(
            "Yes"
        )
        expect(
            self.get_review_row(page, "will you make your methodology available to others for scrutiny?")
        ).to_have_text("No")
        expect(self.get_review_row(page, "Will you analyse and publish findings online?")).to_have_text("Yes")
        expect(self.get_review_row(page, "Do you intend to use computational analysis")).to_have_text(
            re.compile("Directly inform or influence the decision of a third-party")
        )
        expect(self.get_review_row(page, "Will you notify people when they are using generative AI")).to_have_text(
            "Not using Generative AI"
        )
        expect(
            self.get_review_row(
                page,
                "Will you explain how the limits of the Find Case Law collection",
            )
        ).to_have_text("No")

        expect(
            self.get_review_row(page, "Licence holders must acknowledge and abide by all the nine principles.")
        ).to_have_text("Yes")

        expect(
            self.get_review_row(page, "Please describe how you will meet the nine principles as terms.")
        ).to_have_text("Nine principles statement")

        expect(
            self.get_review_row(
                page,
                "Are there any additional comments you would like us to consider as part of your application?",
            )
        ).to_have_text("Additional comments")

    def test_editing_responses(self, page: Page):
        assert_is_accessible(page)
        assert_matches_snapshot(page, "transactional_license_edit_responses_page")
        page.locator("dt", has_text="Contact Full Name").locator("..").get_by_text("Change").click()
        page.get_by_label("Contact Full Name").fill("New Full Name")
        page.get_by_text("Next", exact=True).click()
        page.get_by_label("What is the full legal name of your organisation?").fill("New Organisation name")
        page.get_by_text("Save and review").click()

        expect(self.get_review_row(page, "Contact Full Name")).to_have_text("New Full Name")
        expect(self.get_review_row(page, "What is the full legal name")).to_have_text("New Organisation name")

    def test_data_saved_when_going_back(self, page: Page):
        """
        Test the process to apply for a computational analysis licence.
        We stop on the review page (short of actually submitting the form)
        (which triggers an email to the licensing team): the final step will be tested
        in isolation with a mocked email service."""

        # Fill contact details in full
        page.goto("/re-use-find-case-law-records/steps/contact")
        page.get_by_label("Contact Full Name").fill("Full Name")
        page.get_by_label("Contact Email address").fill("contact@example.com")
        page.get_by_label("This is a different person (please enter their details on the next section)").click()
        page.get_by_label("Licence holder Full Name").fill("Licence Holder")
        page.get_by_label("Licence holder Email").fill("licenceholder@example.com")

        # On the next page, fill only 1 field, leaving others blank
        page.get_by_text("Next", exact=True).click()
        page.get_by_label("What is the full legal name of your organisation?").fill("Organisation name")

        # Check previous page has information
        page.get_by_text("Previous").click()
        expect(page.get_by_label("Contact Full Name")).to_have_value("Full Name")

        # Check incomplete next page has information
        page.get_by_text("Next", exact=True).click()
        expect(page.get_by_label("What is the full legal name of your organisation?")).to_have_value(
            "Organisation name"
        )
