import re

import pytest
from playwright.sync_api import Browser, Page, expect

from .utils.assertions import VIEWPORTS, assert_is_accessible, assert_matches_snapshot


@pytest.fixture(scope="module")
def home_page(browser: Browser, base_url: str) -> Page:
    context = browser.new_context(
        base_url=base_url,
    )
    page = context.new_page()
    page.goto("/")
    yield page
    context.close()


@pytest.fixture(scope="module")
def mobile_home_page(browser: Browser, base_url: str) -> Page:
    context = browser.new_context(
        viewport=VIEWPORTS["mobile"],
        base_url=base_url,
    )
    page = context.new_page()
    page.goto("/")
    yield page
    context.close()


def test_home_page_details(home_page: Page):
    expect(home_page).to_have_title("Find Case Law - The National Archives")

    expect(home_page.locator("h2", has_text="Recently published judgments")).to_be_visible()

    assert home_page.locator(".documents-table tbody tr").count() > 1

    assert_is_accessible(home_page)
    assert_matches_snapshot(home_page, "home_page")


def test_home_page_search_form_is_present(home_page: Page):
    search_input = home_page.locator("#search_input")
    expect(search_input).to_be_visible()
    expect(search_input).to_have_attribute("name", "query")


def test_home_page_search_submits_to_correct_action(home_page: Page):
    home_page.fill("#search_input", "Imperial")
    with home_page.expect_navigation():
        home_page.click("input[type=submit][value=Search]")
    expect(home_page).to_have_url(re.compile(r"/search\?query=Imperial"))
    home_page.goto("/")


def test_home_page_judgments_table_has_correct_headers(home_page: Page):
    headers = home_page.locator(".documents-table thead th")

    expect(headers.nth(1)).to_have_text("Neutral citation")
    expect(headers.nth(2)).to_have_text("Handed down")


def test_home_page_judgment_links_are_present_and_have_href(home_page: Page):
    links = home_page.locator(".documents-table tbody a")
    count = links.count()
    assert count > 0

    for i in range(count):
        href = links.nth(i).get_attribute("href")
        assert href and len(href) > 1, f"Judgment link {i} has empty or missing href"


def test_home_page_judgment_rows_have_court_and_date(home_page: Page):
    bodies = home_page.locator(".documents-table tbody")
    count = bodies.count()

    assert count > 0

    for i in range(count):
        tbody = bodies.nth(i)
        meta_cells = tbody.locator("tr").nth(1).locator("td")

        court_text = meta_cells.nth(0).inner_text().strip()
        assert court_text, f"Judgment {i} is missing a court name"

        date_text = meta_cells.nth(2).inner_text().strip()
        assert date_text, f"Judgment {i} is missing a handed-down date"


def test_home_page_cards_are_present_and_link_correctly(home_page: Page):
    expected = [
        ("/understanding-case-law", "New to case law?"),
        ("/search-and-browse", "Ready to search?"),
        ("/help-and-support", "Need help?"),
    ]

    for href, heading in expected:
        card = home_page.locator(f".card[href='{href}']")
        expect(card).to_be_visible()
        expect(card.locator("h3")).to_have_text(heading)


def test_home_page_view_all_judgments_button(home_page: Page):
    btn = home_page.locator("a.button[href='/search']")
    expect(btn).to_be_visible()
    expect(btn).to_contain_text("View all judgments")

    with home_page.expect_navigation():
        btn.click()

    expect(home_page).to_have_url("/search")
    home_page.goto("/")


def test_home_page_about_details_expands(home_page: Page):
    details = home_page.locator("details[data-stateful-details]")
    summary = details.locator("summary")

    expect(details).to_have_attribute("open", "")
    expect(details.locator(".details__text")).to_be_visible()
    summary.click()
    expect(details).not_to_have_attribute("open", "")
    expect(details.locator(".details__text")).not_to_be_visible()


def test_mobile_home_page_judgments_labels(mobile_home_page: Page):
    bodies = mobile_home_page.locator(".documents-table tbody")
    count = bodies.count()

    assert count > 0

    for i in range(count):
        body = bodies.nth(i)
        labels = body.locator(".documents-table__label")

        expect(labels).to_have_text(["Neutral citation", "Handed down"])
