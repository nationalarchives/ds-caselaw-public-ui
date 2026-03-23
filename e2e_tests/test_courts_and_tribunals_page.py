from playwright.sync_api import Page, expect

from .utils.assertions import assert_is_accessible, assert_matches_snapshot


def test_courts_and_tribunals_page(page: Page):
    page.goto("/courts-and-tribunals")

    expect(page).to_have_title("Types of courts in England and Wales - Find Case Law - The National Archives")

    expect(page.locator("h1:visible")).to_have_text("Types of courts in England and Wales")

    courts_tab = page.locator("#tab_courts")
    tribunals_tab = page.locator("#tab_tribunals")

    expect(courts_tab).to_be_visible()
    expect(tribunals_tab).to_be_visible()

    expect(courts_tab).to_have_text("Courts")
    expect(tribunals_tab).to_have_text("Tribunals")

    courts_panel = page.locator("#courts")
    tribunals_panel = page.locator("#tribunals")

    expect(courts_panel).to_be_visible()
    expect(tribunals_panel).to_be_hidden()

    expect(courts_panel).to_contain_text("Courts")

    tribunals_tab.click()

    expect(courts_panel).to_be_hidden()
    expect(tribunals_panel).to_be_visible()

    expect(tribunals_panel).to_contain_text("Tribunals")

    courts_tab.click()

    first_court_item = courts_panel.locator(".courts-and-tribunals__item").first
    expect(first_court_item).to_be_visible()

    heading = first_court_item.locator("h2")
    expect(heading).to_be_visible()
    expect(heading).not_to_have_text("")

    summary = first_court_item.locator("summary")
    expect(summary).to_be_visible()
    expect(summary).to_contain_text("About")

    court_search_link = first_court_item.locator('a[href^="/search?court="]').first
    expect(court_search_link).to_be_visible()

    assert_matches_snapshot(page, "courts-and-tribunals_page")
    assert_is_accessible(page)
