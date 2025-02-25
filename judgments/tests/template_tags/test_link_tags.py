import pytest
from django.template import Context, Template

from judgments.templatetags.link_tags import trackable_class_name


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


@pytest.mark.django_db
def test_trackable_link_tag_no_attrs():
    template = Template("{% load link_tags %}{% trackable_link 'Click me' %}")
    rendered = template.render(Context())

    assert "<a " in rendered
    assert 'class="analytics-click-me"' in rendered
    assert "Click me" in rendered


@pytest.mark.django_db
def test_trackable_link_tag_with_attrs():
    template = Template("{% load link_tags %}{% trackable_link 'Click me' href='/test-url' target='_blank' %}")
    rendered = template.render(Context())

    assert "<a " in rendered
    assert 'class="analytics-click-me"' in rendered
    assert 'href="/test-url"' in rendered
    assert 'target="_blank"' in rendered
    assert "Click me" in rendered


@pytest.mark.django_db
def test_trackable_link_tag_with_special_characters():
    template = Template("{% load link_tags %}{% trackable_link 'Hello World!' href='/hello-world' %}")
    rendered = template.render(Context())

    assert "<a " in rendered
    assert 'class="analytics-hello-world"' in rendered
    assert 'href="/hello-world"' in rendered
    assert "Hello World!" in rendered


@pytest.mark.django_db
def test_trackable_link_tag_with_anchor():
    template = Template(
        "{% load link_tags %}{% url 'how_to_use_this_service' as my_url %}{% trackable_link 'Click me' href=my_url|add:'#anchor' %}"
    )
    context = Context()
    rendered = template.render(context)

    assert "<a " in rendered
    assert 'href="/how-to-use-this-service#anchor"' in rendered
    assert "Click me" in rendered
