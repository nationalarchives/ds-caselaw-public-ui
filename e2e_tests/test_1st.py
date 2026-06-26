import pytest
from playwright.sync_api import Page


@pytest.mark.must_pass
def test_is_e2e_working(page: Page):
    response = page.goto("/")
    assert response.status <= 299

    page.locator("h1")
    breakpoint()
