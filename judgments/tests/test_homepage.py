from unittest.mock import patch

from caselawclient.search_parameters import SearchParameters
from django.test import TestCase

from judgments.tests.fixture_data import FakeSearchResponse
from judgments.views.index import cached_recent_judgments


class TestHomepage(TestCase):
    @patch("judgments.views.index.cached_recent_judgments")
    def test_homepage(self, mock_cached_recent_judgments):
        mock_cached_recent_judgments.return_value = FakeSearchResponse()
        response = self.client.get("/")
        mock_cached_recent_judgments.assert_called_once()
        self.assertContains(response, "Judgment v Judgement", html=True)

    @patch("judgments.views.index.api_client")
    @patch("judgments.views.index.search_judgments_and_parse_response")
    def test_cached_recent_judgments(self, mock_search_judgments_and_parse_response, mock_api_client):
        cached_recent_judgments(123)
        mock_search_judgments_and_parse_response.assert_called_once_with(
            mock_api_client, SearchParameters(order="-date", page_size=6)
        )
