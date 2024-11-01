import re

import pytest
from playwright.sync_api import Page, expect

from .utils.assertions import assert_is_accessible

documents = [
    {
        "uri": "/eat/2023/1",
        "title": "Imperial College Healthcare NHS Trust",
        "heading": "IMPERIAL COLLEGE HEALTHCARE NHS TRUST",
        "query": "IMPERIAL",
    }
]


def get_download_pdf_url(document_uri):
    file_name = document_uri.strip("/").replace("/", "_")

    return f"{document_uri}/{file_name}.pdf"


def assert_download_options_link(page):
    download_options_link = page.locator("a", has_text="More download options")

    expect(download_options_link).to_be_visible()
    expect(download_options_link).to_have_attribute("href", "#download-options")


def assert_download_pdf_link(page, uri):
    download_pdf_link = page.locator("a", has_text="Download as PDF")

    expect(download_pdf_link).to_be_visible()

    expect(download_pdf_link).to_have_attribute("href", re.compile(get_download_pdf_url(uri)))


def assert_download_xml_link(page, uri):
    download_as_xml_link = page.locator("a", has_text="Download this judgment as XML")

    expect(download_as_xml_link).to_be_visible()

    expect(download_as_xml_link).to_have_attribute("href", re.compile(f"{uri}/data.xml"))


def assert_has_default_breadcrumbs(page, heading):
    breadcrumb_container = page.locator("[aria-label='Breadcrumb']")

    primary_breadcrumb = breadcrumb_container.locator("a", has_text="Find Case Law")
    secondary_breadcrumb = breadcrumb_container.locator("li", has_text=re.compile(heading, re.IGNORECASE))

    expect(primary_breadcrumb).to_be_visible()
    expect(secondary_breadcrumb).to_be_visible()


def assert_has_search_query_breadcrumb(page, query):
    breadcrumb_container = page.locator("[aria-label='Breadcrumb']")

    search_breadcrumb = breadcrumb_container.locator(
        "a", has_text=re.compile(f'Search results for "{query}"', re.IGNORECASE)
    )

    expect(search_breadcrumb).to_be_visible()


@pytest.mark.parametrize("document", documents)
def test_judgment_page(page: Page, document):
    uri = document.get("uri")
    title = document.get("title")
    heading = document.get("heading")
    query = document.get("query")

    page.goto(uri)

    expect(page).to_have_title(re.compile(title, re.IGNORECASE))
    expect(page.locator("h1")).to_have_text(re.compile(heading, re.IGNORECASE))
    assert_download_options_link(page)
    assert_download_pdf_link(page, uri)
    assert_download_xml_link(page, uri)
    assert_has_default_breadcrumbs(page, heading)

    page.goto(f"{uri}?query={query}")

    assert_has_search_query_breadcrumb(page, query)
    assert_is_accessible(page)
