import re

import pytest
from playwright.sync_api import Page, expect

from .utils.assertions import assert_is_accessible, assert_matches_snapshot


def query_input(page: Page):
    return page.locator("#search_input")


def submit_button(page: Page):
    return page.get_by_role("button", name="Search")


def update_filters_button(page: Page):
    return page.get_by_role("button", name="Update filters")


court_filters = [
    "United Kingdom Supreme Court",
    "Privy Council",
    "Civil Division",
    "Criminal Division",
    "Administrative Court",
    "Admiralty Court",
    "Chancery Division",
    "Commercial Court",
    "Family Division",
    "Intellectual Property Enterprise Court",
    "King's / Queen's Bench Division",
    "Mercantile Court",
    "Patents Court",
    "Senior Courts Costs Office",
    "Technology and Construction Court",
    "Family Court",
    "Court of Protection",
]


@pytest.mark.parametrize("filter", court_filters)
def test_advanced_search_court_filters(page: Page, filter):
    page.goto("/search/advanced")

    page.locator("label", has_text=f"{filter}").click()

    update_filters_button(page).click()

    form = page.locator("#analytics-search-form")

    expect(form.locator("a", has_text=f"{filter}")).to_be_visible()
    expect(page.locator("p", has_text=re.compile(r"\d+\s*documents found"))).to_be_visible()


def test_advanced_search_before_2003(page: Page):
    page.goto("/search/advanced")

    page.locator("#id_from_date_0").fill("01")
    page.locator("#id_from_date_1").fill("01")
    page.locator("#id_from_date_2").fill("2002")

    update_filters_button(page).click()

    expect(
        page.get_by_text("2002 is before 2003, the date of the oldest record on the Find Case Law service.")
    ).to_be_visible()


def test_advanced_search_basic_query_page(page: Page):
    query = "Imperial"
    page.goto("/search/advanced")

    expect(page).to_have_title("Advanced search - Find Case Law - The National Archives")

    expect(page.locator("h1")).to_have_text("Advanced search")

    query_input(page).fill(query)
    submit_button(page).click()

    expect(page.locator("h1")).to_have_text("Search results")

    expect(page.locator("p", has_text=re.compile(r"\d+\s*documents found"))).to_be_visible()

    expect(page.locator("a", has_text=f"Query: {query}"))


def test_advanced_search_page_is_accessible(page: Page):
    page.goto("/search/advanced")
    assert_is_accessible(page)
    assert_matches_snapshot(page, "advanced_search_page")
