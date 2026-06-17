import re
from urllib.parse import urlencode

import pytest
from playwright.sync_api import Browser, Page, expect

from .utils.assertions import assert_is_accessible, assert_matches_snapshot

JUDGMENT_URI = "/eat/2023/1"
JUDGMENT_SEARCH_QUERY = "IMPERIAL"
JUDGMENT_TITLE = "Imperial College Healthcare NHS Trust"
JUDGMENT_HEADING = "IMPERIAL COLLEGE HEALTHCARE NHS TRUST"


@pytest.fixture(scope="module")
def judgment_page(browser: Browser, base_url: str) -> Page:
    context = browser.new_context(
        base_url=base_url,
    )
    page = context.new_page()
    page.goto(JUDGMENT_URI)
    yield page
    context.close()


@pytest.fixture(autouse=True)
def reset_judgment_page(judgment_page: Page, base_url: str):
    yield

    expected_url = f"{base_url.rstrip('/')}{JUDGMENT_URI}"

    if judgment_page.url != expected_url:
        judgment_page.goto(JUDGMENT_URI)


def get_download_pdf_url(document_uri):
    return f"{document_uri}/data.pdf"


def test_judgment_page_has_download_options_link(judgment_page: Page):
    download_options_link = judgment_page.locator("a", has_text="View download options")

    expect(download_options_link).to_be_visible()
    expect(download_options_link).to_have_attribute("href", "#download-options")


def test_judgment_page_has_download_options_title(judgment_page: Page):
    expect(judgment_page.get_by_role("heading", name="Document download options")).to_be_visible()


def test_judgment_page_has_download_pdf_link(judgment_page: Page):
    download_pdf_link = judgment_page.locator("a", has_text="Download PDF")

    expect(download_pdf_link).to_be_visible()
    expect(download_pdf_link).to_have_attribute("href", re.compile(get_download_pdf_url(JUDGMENT_URI)))


def test_judgment_page_has_download_xml_link(judgment_page: Page):
    download_as_xml_link = judgment_page.locator("a", has_text="Download XML")

    expect(download_as_xml_link).to_be_visible()
    expect(download_as_xml_link).to_have_attribute("href", re.compile(f"{JUDGMENT_URI}/data.xml"))


def test_judgment_page_has_default_breadcrumbs(judgment_page: Page):
    breadcrumb_container = judgment_page.locator("[aria-label='Breadcrumb']")

    primary_breadcrumb = breadcrumb_container.locator("a", has_text="Home")
    secondary_breadcrumb = breadcrumb_container.locator("li", has_text=re.compile(JUDGMENT_HEADING, re.IGNORECASE))

    expect(primary_breadcrumb).to_be_visible()
    expect(secondary_breadcrumb).to_be_visible()


def test_judgment_page_has_search_query_breadcrumb(judgment_page: Page):
    query_string = urlencode({"query": JUDGMENT_SEARCH_QUERY})
    judgment_page.goto(f"{JUDGMENT_URI}?{query_string}")
    breadcrumb_container = judgment_page.locator("[aria-label='Breadcrumb']")

    search_breadcrumb = breadcrumb_container.locator(
        "a", has_text=re.compile(f'Search results for "{JUDGMENT_SEARCH_QUERY}"', re.IGNORECASE)
    )

    expect(search_breadcrumb).to_be_visible()


def test_judgment_page_has_title(judgment_page: Page):
    expect(judgment_page).to_have_title(re.compile(JUDGMENT_TITLE, re.IGNORECASE))
    expect(judgment_page.locator("h1")).to_have_text(re.compile(JUDGMENT_HEADING, re.IGNORECASE))


def test_judgment_page_details(judgment_page: Page):
    query_string = urlencode({"query": JUDGMENT_SEARCH_QUERY})
    judgment_page.goto(f"{JUDGMENT_URI}?{query_string}")
    assert_is_accessible(judgment_page)
    assert_matches_snapshot(judgment_page, "judgment_page")
