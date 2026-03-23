import pytest
from playwright.sync_api import Browser, Locator, Page, expect

VIEWPORTS = {
    "desktop": {"width": 1280, "height": 720},
    "mobile": {"width": 375, "height": 667},
}


def get_navigation(page: Page) -> Locator:
    return page.locator('nav[aria-label="Navigation"]')


def get_navigation_link(navigation: Locator, name: str) -> Locator:
    return navigation.get_by_role("link", name=name, exact=True)


def top_level_navigation_item(navigation: Locator, name: str) -> Locator:
    link = get_navigation_link(navigation, name)
    return link.locator("xpath=ancestor::li[1]")


def submenu_navigation_link(navigation: Locator, parent_name: str, child_name: str) -> Locator:
    parent_li = top_level_navigation_item(navigation, parent_name)
    return parent_li.get_by_role("link", name=child_name, exact=True)


def top_level_navigation_toggle_button(navigation: Locator, name: str) -> Locator:
    parent_li = top_level_navigation_item(navigation, name)
    return parent_li.locator(".navigation__item-icon")


def get_menu_button(navigation: Locator) -> Locator:
    return navigation.get_by_role("button", name="Menu")


@pytest.fixture(scope="module")
def desktop_page(browser: Browser, base_url: str) -> Page:
    context = browser.new_context(
        viewport=VIEWPORTS["desktop"],
        base_url=base_url,
    )
    page = context.new_page()
    page.goto("/")
    yield page
    context.close()


@pytest.fixture(scope="module")
def mobile_page(browser: Browser, base_url: str) -> Page:
    context = browser.new_context(
        viewport=VIEWPORTS["mobile"],
        base_url=base_url,
    )
    page = context.new_page()
    page.goto("/")
    yield page
    context.close()


@pytest.fixture(scope="module")
def desktop_navigation(desktop_page: Page) -> Locator:
    navigation = get_navigation(desktop_page)
    expect(navigation).to_be_visible()
    return navigation


@pytest.fixture(scope="module")
def mobile_navigation(mobile_page: Page) -> Locator:
    navigation = get_navigation(mobile_page)
    expect(navigation).to_be_visible()
    return navigation


@pytest.mark.parametrize(
    "item_name",
    [
        "Home",
        "Understanding case law",
        "Search and browse",
        "About this service",
        "Permissions and licensing",
        "Help and support",
    ],
)
def test_navigation_has_top_level_navigation_items(desktop_navigation: Locator, item_name: str):
    expect(top_level_navigation_item(desktop_navigation, item_name)).to_be_visible()


def test_navigation_shows_submenu_on_hover(desktop_navigation: Locator):
    search_and_browse = top_level_navigation_item(desktop_navigation, "Search and browse")
    advanced_search = submenu_navigation_link(desktop_navigation, "Search and browse", "Advanced search")

    expect(advanced_search).not_to_be_visible()

    search_and_browse.hover()
    expect(advanced_search).to_be_visible()


def test_desktop_navigation_does_not_have_menu_button(desktop_navigation: Locator):
    menu_button = get_menu_button(desktop_navigation)
    expect(menu_button).not_to_be_visible()


def test_mobile_navigation_has_menu_button(mobile_navigation: Locator):
    menu_button = get_menu_button(mobile_navigation)
    expect(menu_button).to_be_visible()


def test_mobile_navigation_menu_button_shows_navigation_container(mobile_navigation: Locator):
    menu_button = get_menu_button(mobile_navigation)
    navigation_container = mobile_navigation.locator(".container")
    expect(navigation_container).not_to_be_visible()

    menu_button.click()
    expect(navigation_container).to_be_visible()


def test_mobile_navigation_shows_submenu_on_focus(mobile_navigation: Locator):
    menu_button = get_menu_button(mobile_navigation)
    menu_button.click()
    advanced_search = submenu_navigation_link(mobile_navigation, "Search and browse", "Advanced search")
    expect(advanced_search).not_to_be_visible()

    search_and_browse_toggle = top_level_navigation_toggle_button(mobile_navigation, "Search and browse")
    search_and_browse_toggle.click()

    expect(advanced_search).to_be_visible()
