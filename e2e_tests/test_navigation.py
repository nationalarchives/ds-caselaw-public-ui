import pytest
from playwright.sync_api import Browser, Locator, Page, expect

from .utils.assertions import VIEWPORTS, assert_matches_snapshot


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
    return navigation.locator("label.navigation__menu-button")


@pytest.fixture(scope="function")
def desktop_page(browser: Browser, base_url: str) -> Page:
    context = browser.new_context(
        viewport=VIEWPORTS["desktop"],
        base_url=base_url,
    )
    page = context.new_page()
    page.goto("/")
    yield page
    context.close()


@pytest.fixture(scope="function")
def mobile_page(browser: Browser, base_url: str) -> Page:
    context = browser.new_context(
        viewport=VIEWPORTS["mobile"],
        base_url=base_url,
    )
    page = context.new_page()
    page.goto("/")
    yield page
    context.close()


@pytest.fixture(scope="function")
def desktop_navigation(desktop_page: Page) -> Locator:
    navigation = get_navigation(desktop_page)
    expect(navigation).to_be_visible()
    return navigation


@pytest.fixture(scope="function")
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


def test_desktop_submenu_closes_on_mouse_leave(desktop_page: Page, desktop_navigation: Locator):
    search_and_browse = top_level_navigation_item(desktop_navigation, "Search and browse")
    advanced_search = submenu_navigation_link(desktop_navigation, "Search and browse", "Advanced search")

    search_and_browse.hover()
    expect(advanced_search).to_be_visible()

    desktop_page.mouse.move(0, 0)
    expect(advanced_search).not_to_be_visible()


def test_desktop_submenu_open_snapshot(desktop_page: Page, desktop_navigation: Locator):
    search_and_browse = top_level_navigation_item(desktop_navigation, "Search and browse")

    search_and_browse.hover()

    assert_matches_snapshot(desktop_page, "navigation_open", "desktop")


def test_mobile_navigation_has_menu_button(mobile_navigation: Locator):
    menu_button = get_menu_button(mobile_navigation)
    expect(menu_button).to_be_visible()


def test_mobile_navigation_menu_button_shows_navigation_container(mobile_navigation: Locator):
    menu_button = get_menu_button(mobile_navigation)
    navigation_container = mobile_navigation.locator(".container")
    expect(navigation_container).not_to_be_visible()

    menu_button.click()
    expect(navigation_container).to_be_visible()


def test_mobile_navigation_shows_submenu_on_click(mobile_page: Page, mobile_navigation: Locator):
    menu_button = get_menu_button(mobile_navigation)
    menu_button.click()
    advanced_search = submenu_navigation_link(mobile_navigation, "Search and browse", "Advanced search")
    expect(advanced_search).not_to_be_visible()

    search_and_browse_toggle = top_level_navigation_toggle_button(mobile_navigation, "Search and browse")
    search_and_browse_toggle.click()

    expect(advanced_search).to_be_visible()


def test_mobile_navigation_menu_button_closes_navigation(mobile_page: Page, mobile_navigation: Locator):
    menu_button = get_menu_button(mobile_navigation)
    navigation_container = mobile_navigation.locator(".container")

    menu_button.click()
    expect(navigation_container).to_be_visible()

    menu_button.click()
    expect(navigation_container).not_to_be_visible()


def test_mobile_navigation_closes_on_overlay_click(mobile_page: Page, mobile_navigation: Locator):
    menu_button = get_menu_button(mobile_navigation)
    navigation_container = mobile_navigation.locator(".container")

    menu_button.click()
    expect(navigation_container).to_be_visible()

    mobile_page.locator(".navigation__overlay").click(force=True)
    expect(navigation_container).not_to_be_visible()


def test_mobile_navigation_submenu_collapses_on_second_click(mobile_page: Page, mobile_navigation: Locator):
    get_menu_button(mobile_navigation).click()

    advanced_search = submenu_navigation_link(mobile_navigation, "Search and browse", "Advanced search")
    toggle = top_level_navigation_toggle_button(mobile_navigation, "Search and browse")

    toggle.click()
    expect(advanced_search).to_be_visible()

    toggle.click()
    expect(advanced_search).not_to_be_visible()


def test_mobile_submenu_open_snapshot(mobile_page: Page, mobile_navigation: Locator):
    get_menu_button(mobile_navigation).click()

    toggle = top_level_navigation_toggle_button(mobile_navigation, "Search and browse")
    toggle.click()

    assert_matches_snapshot(mobile_page, "navigation_open", "mobile")
