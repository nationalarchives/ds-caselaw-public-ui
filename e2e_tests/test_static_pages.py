import pytest
from playwright.sync_api import Page, expect

from .utils.assertions import assert_is_accessible

static_pages = [
    {"url": "/about-this-service", "title": "About Find Case Law", "heading": "About Find Case Law"},
    {"url": "/accessibility-statement", "title": "Accessibility statement", "heading": "Accessibility statement"},
    {"url": "/contact-us", "title": "Contact Us", "heading": "Contact us"},
    {
        "url": "/courts-and-tribunals",
        "title": "Types of court in England and Wales",
        "heading": "Types of court in England and Wales",
    },
    {"url": "/help-and-guidance", "title": "Help and guidance", "heading": "Help and guidance"},
    {
        "url": "/how-to-search-find-case-law",
        "title": "How to search Find Case Law",
        "heading": "How to search Find Case Law",
    },
    {
        "url": "/how-to-use-this-service",
        "title": "How to use the Find Case Law service",
        "heading": "How to use the Find Case Law service",
    },
    {"url": "/open-justice-licence", "title": "Open Justice Licence", "heading": "Open Justice Licence"},
    {"url": "/privacy-notice", "title": "Privacy Notice", "heading": "Privacy notice"},
    {"url": "/publishing-policy", "title": "Publishing policy", "heading": "Publishing policy"},
    {"url": "/terms-and-policies", "title": "Terms and policies", "heading": "Terms and policies"},
    {"url": "/terms-of-use", "title": "Terms of use", "heading": "Terms of use"},
    {
        "url": "/understanding-judgments-and-decisions",
        "title": "Understanding judgments and decisions",
        "heading": "Understanding judgments and decisions",
    },
]


@pytest.mark.parametrize("static_page", static_pages)
def test_static_pages(page: Page, static_page):
    url = static_page.get("url")
    title = static_page.get("title")
    heading = static_page.get("heading")

    page.goto(url)

    expect(page).to_have_title(f"{title} - Find Case Law - The National Archives")

    expect(page.locator("h1:visible")).to_have_text(heading)

    assert_is_accessible(page)
