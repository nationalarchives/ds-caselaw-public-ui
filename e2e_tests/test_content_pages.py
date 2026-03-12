import pytest
from playwright.sync_api import Page, expect

from .utils.assertions import assert_is_accessible, assert_matches_snapshot

about_this_service_pages = [
    {
        "url": "/about-find-case-law",
        "title": "About Find Case Law",
        "heading": "About Find Case Law",
    },
    {"url": "/about-this-service", "title": "About this service", "heading": "About this service"},
    {"url": "/contact-us", "title": "Contact Us", "heading": "Contact us"},
    {"url": "/publishing-policy", "title": "Publishing policy", "heading": "Publishing policy"},
    {
        "url": "/what-we-provide",
        "title": "What we provide",
        "heading": "What we provide",
    },
    {
        "url": "/courts-and-date-coverage",
        "title": "Courts and date coverage",
        "heading": "Courts and date coverage",
    },
    {
        "url": "/courts-and-tribunals-in-fcl",
        "title": "Courts and tribunals in Find Case Law",
        "heading": "Courts and tribunals in Find Case Law",
    },
]

understanding_case_law_pages = [
    {
        "url": "/understanding-case-law",
        "title": "Understanding case law",
        "heading": "Understanding case law",
    },
    {
        "url": "/reading-judgments",
        "title": "Reading judgments",
        "heading": "Reading judgments",
    },
    {
        "url": "/understanding-judgments-and-decisions",
        "title": "Understanding judgments and decisions",
        "heading": "Understanding judgments and decisions",
    },
]

search_and_browse_pages = [
    {
        "url": "/search-and-browse",
        "title": "Search and browse",
        "heading": "Search and browse",
    },
    {
        "url": "/courts-and-tribunals",
        "title": "Types of courts in England and Wales",
        "heading": "Types of courts in England and Wales",
    },
    {
        "url": "/browse-courts-and-tribunals",
        "title": "Browse courts and tribunals",
        "heading": "Browse courts and tribunals",
    },
]

permissions_and_licensing_pages = [
    {
        "url": "/permissions-and-licensing",
        "title": "Permissions and Licensing",
        "heading": "Permissions and Licensing",
    },
    {"url": "/open-justice-licence", "title": "Open Justice Licence", "heading": "Open Justice Licence"},
    {
        "url": "/what-you-can-do-freely",
        "title": "What you can do freely",
        "heading": "What you can do freely",
    },
    {
        "url": "/when-you-need-permission",
        "title": "When you need permission",
        "heading": "When you need permission",
    },
    {
        "url": "/using-find-case-law-records",
        "title": "Using Find Case Law records",
        "heading": "Using Find Case Law records",
    },
    {
        "url": "/what-you-need-to-apply-for-a-licence",
        "title": "What you need to apply for a licence",
        "heading": "What you need to apply for a licence",
    },
    {
        "url": "/how-to-get-permission",
        "title": "How to get permission",
        "heading": "How to get permission",
    },
    {
        "url": "/licence-application-process",
        "title": "Licence application process",
        "heading": "Licence application process",
    },
    {
        "url": "/apply-for-a-licence",
        "title": "Apply for a licence",
        "heading": "Apply for a licence",
    },
    {
        "url": "/legal-framework",
        "title": "Legal framework",
        "heading": "Legal framework",
    },
]

help_and_support_pages = [
    {
        "url": "/feedback",
        "title": "Feedback",
        "heading": "Feedback",
    },
    {
        "url": "/help-and-support",
        "title": "Help and Support",
        "heading": "Help and Support",
    },
    {
        "url": "/how-to-search-find-case-law",
        "title": "How to search Find Case Law",
        "heading": "How to search Find Case Law",
    },
    {
        "url": "/search-tips",
        "title": "Search tips",
        "heading": "Search tips",
    },
    {
        "url": "/glossary",
        "title": "Find Case Law Glossary",
        "heading": "Find Case Law Glossary",
    },
    {"url": "/user-research", "title": "User research", "heading": "User research for Find Case Law"},
]

root_content_pages = [
    {
        "url": "/accessibility-statement",
        "title": "Accessibility statement for Find Case Law",
        "heading": "Accessibility statement for Find Case Law",
    },
    {"url": "/privacy-notice", "title": "Privacy Notice", "heading": "Privacy notice"},
    {"url": "/terms-of-use", "title": "Terms of use", "heading": "Terms of use"},
]


def assert_content_page(page: Page, content_page):
    url = content_page.get("url")
    title = content_page.get("title")
    heading = content_page.get("heading")

    page.goto(url)

    expect(page).to_have_title(f"{title} - Find Case Law - The National Archives")

    expect(page.locator("h1:visible")).to_have_text(heading)

    assert_is_accessible(page)
    assert_matches_snapshot(page, f"{url.replace('/', '')}_page")


@pytest.mark.parametrize("content_page", root_content_pages)
def test_root_content_pages(page: Page, content_page):
    assert_content_page(page, content_page)


@pytest.mark.parametrize("content_page", help_and_support_pages)
def test_help_and_support_pages(page: Page, content_page):
    assert_content_page(page, content_page)


@pytest.mark.parametrize("content_page", permissions_and_licensing_pages)
def test_permissions_and_licensing_pages(page: Page, content_page):
    assert_content_page(page, content_page)


@pytest.mark.parametrize("content_page", search_and_browse_pages)
def test_search_and_browse_pages(page: Page, content_page):
    assert_content_page(page, content_page)


@pytest.mark.parametrize("content_page", understanding_case_law_pages)
def test_understanding_case_law_pages(page: Page, content_page):
    assert_content_page(page, content_page)


@pytest.mark.parametrize("content_page", about_this_service_pages)
def test_about_this_service_pages(page: Page, content_page):
    assert_content_page(page, content_page)
