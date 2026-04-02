import pytest
from django.test import RequestFactory

from judgments.templatetags.link_tags import trackable_class_name, trackable_link


@pytest.mark.parametrize(
    "input_text, expected_class_name",
    [
        ("Test Text", "analytics-test-text"),
        ("  leading and trailing spaces  ", "analytics-leading-and-trailing-spaces"),
        ("Multiple     Spaces", "analytics-multiple-spaces"),
        ("Special!@#Chars", "analytics-specialchars"),
        ("UPPERCASE", "analytics-uppercase"),
    ],
)
def test_trackable_class_name(input_text, expected_class_name):
    assert trackable_class_name(input_text) == expected_class_name


def test_trackable_link_no_attrs():
    result = trackable_link({}, "Click me")

    assert result == {
        "text": "Click me",
        "attrs": {},
        "class_name": "analytics-click-me",
        "current_path": "",
    }


def test_trackable_link_with_attrs():
    result = trackable_link({}, "Click me", href="/test-url", target="_blank")

    assert result == {
        "text": "Click me",
        "attrs": {"href": "/test-url", "target": "_blank"},
        "class_name": "analytics-click-me",
        "current_path": "",
    }


def test_trackable_link_with_special_characters():
    result = trackable_link({}, "Hello World!", href="/hello-world")

    assert result == {
        "text": "Hello World!",
        "attrs": {"href": "/hello-world"},
        "class_name": "analytics-hello-world",
        "current_path": "",
    }


def test_trackable_link_with_anchor():
    result = trackable_link({}, "Click me", href="/how-to-search-find-case-law#anchor")

    assert result == {
        "text": "Click me",
        "attrs": {"href": "/how-to-search-find-case-law#anchor"},
        "class_name": "analytics-click-me",
        "current_path": "",
    }


def test_trackable_link_includes_current_path_from_request():
    request = RequestFactory().get("/current-page/")
    result = trackable_link({"request": request}, "Click me")

    assert result["current_path"] == "/current-page/"
