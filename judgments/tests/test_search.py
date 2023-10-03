import html
from unittest.mock import patch

from caselawclient.search_parameters import SearchParameters
from django.test import TestCase
from django.utils.translation import gettext

from judgments.tests.fixtures import FakeSearchResponse
from judgments.tests.utils.assertions import assert_contains_html


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
    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_judgment_advanced_search(
        self, mock_search_judgments_and_parse_response, mock_api_client
    ):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        response = self.client.get("/judgments/search?query=waltham+forest")
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
        fake_preprocess_query.return_value = "normalised query"
        self.client.get("/judgments/search?query=waltham+forest")
        fake_preprocess_query.assert_called()

    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_judgment_advanced_search_court_filters(
        self,
        mock_search_judgments_and_parse_response,
        mock_api_client,
    ):
        """
        GIVEN a client for making HTTP requests
        WHEN a GET request is made to "/judgments/search?court=ewhc/ch&court=ewhc/ipec"
        THEN the response should contain the expected applied filters HTML
        AND the `search_judgments_and_parse_response` function should be called with the correct court string.

        The expected applied filters HTML:
        - Includes a list with class "results-search-component__removable-options"
        - Contains two list items (li) with links (a) representing the applied filters:
        - The first link represents the "Chancery Division of the High Court" filter
        - The second link represents the "Intellectual Property Enterprise Court" filter
        """
        response = self.client.get("/judgments/search?court=ewhc/ch&court=ewhc/ipec")

        expected_applied_filters_html = """
        <ul class="results-search-component__removable-options js-results-facets-applied-filters">
            <li>
              <a role="button"
                 tabindex="0"
                 draggable="false"
                 class="results-search-component__removable-options-link"
                 href="/judgments/search?query=&amp;court=ewhc/ipec&amp;judge=&amp;party=&amp;neutral_citation=&amp;specific_keyword=&amp;order=&amp;from=&amp;from_day=&amp;from_month=&amp;from_year=&amp;to=&amp;to_day=&amp;to_month=&amp;to_year=&amp;per_page=&amp;page="
                 title="Chancery Division of the High Court">
                <span class="results-search-component__removable-options-value">
                  <span class="results-search-component__removable-options-value-text">
                    Chancery Division of the High Court
                  </span>
                </span>
              </a>
            </li>

            <li>
              <a role="button"
                 tabindex="0"
                 draggable="false"
                 class="results-search-component__removable-options-link"
                 href="/judgments/search?query=&amp;court=ewhc/ch&amp;judge=&amp;party=&amp;neutral_citation=&amp;specific_keyword=&amp;order=&amp;from=&amp;from_day=&amp;from_month=&amp;from_year=&amp;to=&amp;to_day=&amp;to_month=&amp;to_year=&amp;per_page=&amp;page="
                 title="Intellectual Property Enterprise Court">
                <span class="results-search-component__removable-options-value">
                  <span class="results-search-component__removable-options-value-text">
                    Intellectual Property Enterprise Court
                  </span>
                </span>
              </a>
            </li>
        </ul>
"""
        mock_search_judgments_and_parse_response.assert_called_with(
            mock_api_client,
            SearchParameters(query="", court="ewhc/ch,ewhc/ipec", order="-date"),
        )
        assert_contains_html(response, expected_applied_filters_html)

    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_judgment_advanced_search_shows_message_with_invalid_from_date(
        self, mock_search_judgments_and_parse_response, mock_api_client
    ):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        response = self.client.get(
            "/judgments/search?from_year=2023&from_month=12&from_day=32"
        )
        message = html.escape(gettext("search.errors.from_date_headline"))
        self.assertContains(
            response, f'<div class="page-notification--failure">{message}</div>'
        )

    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_judgment_advanced_search_shows_message_with_invalid_to_date(
        self, mock_search_judgments_and_parse_response, mock_api_client
    ):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        response = self.client.get(
            "/judgments/search?to_year=2023&to_month=12&to_day=32"
        )
        message = html.escape(gettext("search.errors.to_date_headline"))
        self.assertContains(
            response, f'<div class="page-notification--failure">{message}</div>'
        )

    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_judgment_advanced_search_shows_message_with_crossed_dates(
        self, mock_search_judgments_and_parse_response, mock_api_client
    ):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        response = self.client.get("/judgments/search?to_year=2022&from_year=2023")
        message = html.escape(gettext("search.errors.to_before_from_headline"))
        self.assertContains(
            response, f'<div class="page-notification--failure">{message}</div>'
        )


class TestSearchBreadcrumbs(TestCase):
    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_search_breadcrumbs_without_query_string(
        self, mock_search_judgments_and_parse_response, mock_api_client
    ):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        response = self.client.get("/judgments/search")
        assert response.context["breadcrumbs"] == [{"text": "Search results"}]

    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_search_breadcrumbs_with_query_string(
        self, mock_search_judgments_and_parse_response, mock_api_client
    ):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        response = self.client.get("/judgments/search?query=waltham+forest")
        assert response.context["breadcrumbs"] == [
            {"text": 'Search results for "waltham forest"'}
        ]
