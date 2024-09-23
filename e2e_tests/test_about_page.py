from playwright.sync_api import Page, expect


def test_about_page(page: Page):
    """
    A minimum-viable-integration test of a page
    that doesn't talk to marklogic or any other
    external services.
    """
    page.goto("/about-this-service")

    expect(page).to_have_title("About this service - Find Case Law - The National Archives")
