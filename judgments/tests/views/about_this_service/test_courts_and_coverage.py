from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, TestCase

from judgments.views.about_this_service.courts_and_coverage import CourtsAndCoverageView


class TestCourtsAndCoverageView(TestCase):
    @patch("judgments.views.about_this_service.courts_and_coverage.courts.get_grouped_show_in_public_directory_courts")
    def test_context_uses_public_directory_courts(self, mock_get_grouped_show_in_public_directory_courts):
        courts = [SimpleNamespace(name="Public directory court")]
        mock_get_grouped_show_in_public_directory_courts.return_value = courts
        view = CourtsAndCoverageView()
        view.setup(RequestFactory().get("/courts-and-coverage"))

        context = view.get_context_data()

        assert context["courts"] == courts
        mock_get_grouped_show_in_public_directory_courts.assert_called_once_with()
