from unittest.mock import patch

from caselawclient.search_parameters import SearchParameters
from django.test import TestCase

from judgments.tests.fixtures import FakeSearchResponse


class TestHomepage(TestCase):
    @patch("judgments.views.index.api_client")
    @patch("judgments.views.index.search_judgments_and_parse_response")
    def test_homepage(self, mock_search_judgments_and_parse_response, mock_api_client):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        response = self.client.get("/")
        mock_search_judgments_and_parse_response.assert_called_with(
            mock_api_client, SearchParameters(order="-date")
        )
        self.assertContains(response, "A SearchResult name!", html=True)
