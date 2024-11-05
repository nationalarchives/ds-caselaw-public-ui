from playwright.sync_api import Page, expect


def test_style_guide_page(page: Page):
    page.goto("/style-guide")

    expect(page).to_have_title("Style Guide - The National Archives")

    expect(page.locator("h1", has_text="Find Case Law UI Style Guide")).to_be_visible()
