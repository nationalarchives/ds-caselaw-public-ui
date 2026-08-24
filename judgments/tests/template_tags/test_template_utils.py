from unittest.mock import patch

from django.template import TemplateDoesNotExist

from judgments.templatetags.template_utils import template_exists


@patch("judgments.templatetags.template_utils.get_template")
def test_template_exists_returns_true_when_template_can_be_loaded(mock_get_template):
    assert template_exists("content/courts/uksc.jinja")
    mock_get_template.assert_called_once_with("content/courts/uksc.jinja", using="jinja")


@patch("judgments.templatetags.template_utils.get_template", side_effect=TemplateDoesNotExist("missing.jinja"))
def test_template_exists_returns_false_when_template_cannot_be_loaded(mock_get_template):
    assert not template_exists("missing.jinja")
