from unittest.mock import patch

from caselawclient.search_parameters import SearchParameters
from django.test import TestCase

from judgments.tests.fixtures import FakeSearchResponse


class TestBrowseResults(TestCase):
    @patch("judgments.views.browse.api_client")
    @patch("judgments.views.browse.search_judgments_and_parse_response")
    def test_browse_results(
        self, mock_search_judgments_and_parse_response, mock_api_client
    ):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        response = self.client.get("/ewhc/ch/2022")
        mock_search_judgments_and_parse_response.assert_called_with(
            mock_api_client,
            SearchParameters(
                court="ewhc/ch",
                date_from="2022-01-01",
                date_to="2022-12-31",
                order="-date",
                page=1,
                page_size=10,
            ),
        )
        self.assertContains(
            response,
            "A SearchResult name!",
        )


class TestSearchResults(TestCase):
    @patch("judgments.views.results.api_client")
    @patch("judgments.views.results.search_judgments_and_parse_response")
    def test_judgment_results(
        self, mock_search_judgments_and_parse_response, mock_api_client
    ):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        response = self.client.get("/judgments/results?query=waltham+forest")
        mock_search_judgments_and_parse_response.assert_called_with(
            mock_api_client,
            SearchParameters(
                query="waltham forest", page=1, order="-relevance", page_size=10
            ),
        )
        self.assertContains(
            response,
            '<span class="results-search-component__removable-options-value-text">waltham forest</span>',
        )

    @patch("judgments.views.results.preprocess_query")
    @patch("judgments.views.results.search_judgments_and_parse_response")
    def test_jugdment_results_query_preproccesed(
        self,
        mock_search_judgments_and_parse_response,
        fake_preprocess_query,
    ):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        fake_preprocess_query.return_value = "normalised query"
        self.client.get("/judgments/results?query=waltham+forest")

        fake_preprocess_query.assert_called()

    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_judgment_advanced_search(
        self, mock_search_judgments_and_parse_response, mock_api_client
    ):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        response = self.client.get("/judgments/advanced_search?query=waltham+forest")
        self.assertContains(
            response,
            '<span class="results-search-component__removable-options-value-text">waltham forest</span>',
        )
        mock_search_judgments_and_parse_response.assert_called_with(
            mock_api_client,
            SearchParameters(
                query="waltham forest",
                court="",
                judge=None,
                party=None,
                neutral_citation=None,
                specific_keyword=None,
                page=1,
                order="relevance",
                date_from=None,
                date_to=None,
                page_size=10,
            ),
        )

    @patch("judgments.views.advanced_search.preprocess_query")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_judgment_advanced_search_query_preprocessed(
        self,
        mock_search_judgments_and_parse_response,
        fake_preprocess_query,
    ):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        fake_preprocess_query.return_value = "normalised query"
        self.client.get("/judgments/advanced_search?query=waltham+forest")
        fake_preprocess_query.assert_called()
