"""
Custom assertion helpers for tests.
"""


def assert_contains_html(response, html):
    """
    Asserts that the given HTML is contained within the response content.

    Raises:
        AssertionError: If the HTML is not found in the response content.
    """
    assert html.replace(" ", "").replace("\n", "") in response.content.decode().replace(" ", "").replace("\n", "")


def assert_not_contains_html(response, html):
    """
    Asserts that the given HTML is not contained within the response content.

    Raises:
        AssertionError: If the HTML is found in the response content.
    """
    assert html.replace(" ", "").replace("\n", "") not in response.content.decode().replace(" ", "").replace("\n", "")
