from playwright.sync_api import Page, expect

from .utils.assertions import assert_is_accessible, assert_matches_snapshot


def test_courts_and_tribunals_page(page: Page):
    page.goto("/courts-and-tribunals")

    expect(page).to_have_title("Types of courts in England and Wales - Find Case Law - The National Archives")

    expect(page.locator("h1:visible")).to_have_text("Types of courts in England and Wales")

    assert_matches_snapshot(page, "courts-and-tribunals_page")
    assert_is_accessible(page)
