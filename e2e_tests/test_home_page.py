from playwright.sync_api import Page, expect

from .utils.assertions import assert_is_accessible


def test_home_page(page: Page):
    page.goto("/")

    expect(page).to_have_title("Find Case Law - The National Archives")

    expect(page.locator("h1", has_text="Recently published judgments")).to_be_visible()

    assert page.locator(".documents-table tbody tr").count() > 1

    assert_is_accessible(page)
    # TODO: Add this back in when populate_from_caselaw seeds match staging
    # assert_matches_snapshot(page, "home_page")
