from playwright.sync_api import Page, expect

from .utils.assertions import assert_is_accessible, assert_matches_snapshot


def test_court_page(page: Page):
    page.goto("/courts-and-tribunals/ukpc")

    expect(page).to_have_title("Privy Council - Find Case Law - The National Archives")

    expect(page.locator("h1:visible")).to_have_text("Privy Council")

    assert_matches_snapshot(page, "court_page")
    assert_is_accessible(page)
