from playwright.sync_api import Page, expect


def test_judgment_page(page: Page):
    page.goto("/ewhc/ch/2024/505")

    main = page.get_by_role("main")
    navigation_judgment_title = main.get_by_text(
        "Nebahat Evyap Işbilen v Selman Turk & Ors"
    )
    expect(navigation_judgment_title).to_be_hidden()

    end_of_document = main.get_by_text("End of document")
    end_of_document.scroll_into_view_if_needed()

    expect(navigation_judgment_title).to_be_visible()
