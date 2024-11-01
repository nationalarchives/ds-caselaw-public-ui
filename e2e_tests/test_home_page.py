from playwright.sync_api import Page, expect

from .utils.assertions import assert_is_accessible


def test_home_page(page: Page):
    page.goto("/")

    expect(page).to_have_title("Find Case Law - The National Archives")

    expect(page.locator("h2", has_text="Recently published judgments")).to_be_visible()

    assert page.locator(".recent-judgments ul li").count() > 1

    assert_is_accessible(page)
