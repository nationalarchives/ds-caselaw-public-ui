import unittest
from unittest.mock import Mock

from judgments.templatetags.navigation_tags import navigation_item_class


class TestNavigationTags(unittest.TestCase):
    def test_url_name_equals_path(self):
        mock_request = Mock()
        mock_request.path_info = "/about-this-service"

        mock_context = {"request": mock_request}

        result = navigation_item_class(mock_context, "about_this_service")

        self.assertEqual(result, "govuk-header__navigation-item govuk-header__navigation-item--active")

    def test_url_name_not_equals_path(self):
        mock_request = Mock()
        mock_request.path_info = "/"

        mock_context = {"request": mock_request}

        result = navigation_item_class(mock_context, "about_this_service")

        self.assertEqual(result, "govuk-header__navigation-item")
