from playwright.sync_api import Page, expect


def test_home_page(page: Page):
    page.goto("/")

    expect(page).to_have_title("Find Case Law - The National Archives")
