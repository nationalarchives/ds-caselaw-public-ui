from playwright.sync_api import Page


def test_debug_page(page: Page):
    page.goto("/dragondebug")
    assert "prod" not in page.content()
    assert "config.settings.local" in page.content()
    assert "wo: True" in page.content()
