import pytest
from django.test import TestCase

from judgments.tests.utils.assertions import (
    assert_contains_html,
    assert_not_contains_html,
    assert_response_contains_text,
    assert_response_not_contains_text,
)


class MockResponse:
    def __init__(self, content):
        self.content = content.encode()


class TestAssertions(TestCase):
    contained_html = "<title>Judgment A - Find case law - The National Archives</title>"
    response_contains = MockResponse("<html>" + contained_html + "</html>")
    response_not_contains = MockResponse("<html>Something else</html>")

    def test_assert_contains_html(self):
        try:
            assert_contains_html(self.response_contains, self.contained_html)
        except AssertionError:
            pytest.fail("assert_contains_html raised an AssertionError - html not contained within response")

    def test_assert_not_contains_html(self):
        try:
            assert_not_contains_html(self.response_not_contains, self.contained_html)
        except AssertionError:
            pytest.fail("assert_not_contains_html raised an AssertionError")

    def test_assert_contains_html_fails(self):
        with pytest.raises(AssertionError):
            assert_contains_html(self.response_not_contains, self.contained_html)

    def test_assert_not_contains_html_fails(self):
        with pytest.raises(AssertionError):
            assert_not_contains_html(self.response_contains, self.contained_html)

    def test_assert_contains_nested_html(self):
        contained_html = "<li><span>Item 2</span></li>"
        response = MockResponse(
            "<html><ul><li><span>Item 1</span></li>" + contained_html + "<li><span>Item 3</span></li></html>",
        )

        try:
            assert_contains_html(response, contained_html)
        except AssertionError:
            pytest.fail("assert_contains_html raised AssertionError with nested HTML")

    def test_assert_not_contains_nested_html(self):
        contained_html = "<li><span>Item 2</span></li>"
        response = MockResponse("<html><ul><li><span>Item 1</span></li><li><span>Item 3</span></li></html>")

        try:
            assert_not_contains_html(response, contained_html)
        except AssertionError:
            pytest.fail("assert_contains_html raised AssertionError with nested HTML")

    def test_assert_response_contains_text(self):
        contained_text = "Server Error"
        xpath_query = "//div[@class='breadcrumbs']"

        response = MockResponse("<html><div class='breadcrumbs'><ul><li>Server Error</li></ul></div></html>")

        try:
            assert_response_contains_text(response, contained_text, xpath_query)
        except AssertionError:
            pytest.fail("assert_response_contains_text raised AssertionError")

    def test_assert_response_not_contains_text(self):
        contained_text = "Not there"
        xpath_query = "//div[@class='breadcrumbs']"

        response = MockResponse("<html><div class='breadcrumbs'><ul><li>Server Error</li></ul></div></html>")

        try:
            assert_response_not_contains_text(response, contained_text, xpath_query)
        except AssertionError:
            pytest.fail("assert_response_not_contains_text raised AssertionError")
