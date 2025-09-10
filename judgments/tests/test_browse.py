from unittest.mock import patch

from caselawclient.search_parameters import SearchParameters
from django.test import TestCase

from judgments.tests.fixture_data import (
    FakeSearchResponse,
)
from judgments.tests.utils.assertions import (
    assert_contains_html,
)


class TestBrowse(TestCase):
    @patch("judgments.views.browse.api_client")
    @patch("judgments.views.browse.search_judgments_and_parse_response")
    def test_browse_results(self, mock_search_judgments_and_parse_response, mock_api_client):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        response = self.client.get("/ewhc")
        mock_search_judgments_and_parse_response.assert_called_with(
            mock_api_client,
            SearchParameters(
                court="ewhc",
                order="-date",
                page=1,
                page_size=10,
            ),
        )
        self.assertContains(response, "Judgment v Judgement", html=True)
        self.assertContains(response, "/uksc/2025/1")
        self.assertNotContains(response, "d-123456789abcdef")

        expected_html = """
        <div class="search-term-component__container">
            <div class="search-term-component__search-term-container">
            <label for="search_form" class="search-term-component__search-term-label">Search</label>
            <input type="text" name="query" placeholder="Input your search term..." id="search_form" class="search-term-component__search-term-input">
            </div>

            <input type="submit" value="Search" class="button-primary" formaction="/search">
        </div>
        """

        assert_contains_html(response, expected_html)
