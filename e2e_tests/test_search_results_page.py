import re

import pytest
from playwright.sync_api import Browser, Page, expect

from .utils.assertions import assert_is_accessible, assert_matches_snapshot


@pytest.fixture(scope="module")
def search_results_page(browser: Browser, base_url: str) -> Page:
    context = browser.new_context(
        base_url=base_url,
    )
    page = context.new_page()
    page.goto("/search?query=Imperial")
    yield page
    context.close()


def test_advanced_search_no_results_page(page: Page):
    query = "thisshouldnotgiveanyresults"
    page.goto(f"/search?query={query}")

    expect(page.locator("h2", has_text="No matching results have been found")).to_be_visible()
    expect(page.locator("a", has_text=f"Query: {query}"))


def test_search_results_sorting(search_results_page: Page):
    sort_input = search_results_page.locator("#order_by")
    per_page_input = search_results_page.locator("#per_page")
    sort_button = search_results_page.get_by_role("button", name="Apply")

    sort_input.select_option("Sort by: Newest")
    per_page_input.select_option("25")
    sort_button.click()

    expect(sort_input).to_have_value("-date")
    expect(per_page_input).to_have_value("25")


def test_search_results_page(search_results_page: Page):
    expect(search_results_page.locator("h1")).to_have_text("Search results")

    expect(search_results_page.locator("p", has_text=re.compile(r"\d+\s*results"))).to_be_visible()

    expect(search_results_page.locator("a", has_text="Query: Imperial"))


def test_search_results_page_is_accessible(search_results_page: Page):
    assert_is_accessible(search_results_page)
    assert_matches_snapshot(search_results_page, "search_results_page")
