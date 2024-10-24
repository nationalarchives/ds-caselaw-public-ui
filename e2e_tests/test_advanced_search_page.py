from playwright.sync_api import Page, expect

from .utils.assertions import assert_accessible


def test_advanced_search_page(page: Page):
    page.goto("/advanced_search")

    expect(page).to_have_title("Advanced search - Find Case Law - The National Archives")

    expect(page.locator("h1")).to_have_text("Advanced search")

    assert_accessible(page)
