import html
from unittest.mock import patch

from caselawclient.search_parameters import SearchParameters
from django.test import TestCase
from django.utils.translation import gettext
from ds_caselaw_utils import courts as all_courts

from judgments.tests.fixtures import FakeSearchResponse, FakeSearchResponseNoFacets
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
        self.assertContains(response, "A SearchResult name!", html=True)


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
            html=True,
        )
        mock_search_judgments_and_parse_response.assert_called_with(
            mock_api_client,
            SearchParameters(
                query="waltham forest",
                court="",
                judge=None,
                party=None,
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
                 href="/judgments/search?query=&amp;court=ewhc/ipec&amp;judge=&amp;party=&amp;order=&amp;from=&amp;from_date_0=&amp;from_date_1=&amp;from_date_2=&amp;to=&amp;to_date_0=&amp;to_date_1=&amp;to_date_2=&amp;per_page=&amp;page="
                 title="High Court (Chancery Division)">
                <span class="results-search-component__removable-options-value">
                  <span class="results-search-component__removable-options-value-text">
                    High Court (Chancery Division)
                  </span>
                </span>
              </a>
            </li>

            <li>
              <a role="button"
                 tabindex="0"
                 draggable="false"
                 class="results-search-component__removable-options-link"
                 href="/judgments/search?query=&amp;court=ewhc/ch&amp;judge=&amp;party=&amp;order=&amp;from=&amp;from_date_0=&amp;from_date_1=&amp;from_date_2=&amp;to=&amp;to_day=&amp;to_month=&amp;to_year=&amp;per_page=&amp;page="
                 title="High Court (Intellectual Property Enterprise Court)">
                <span class="results-search-component__removable-options-value">
                  <span class="results-search-component__removable-options-value-text">
                    High Court (Intellectual Property Enterprise Court)
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
            "/judgments/search?from_date_2=2023&from_date_1=12&from_date_0=32"
        )
        message = html.escape(gettext("search.errors.from_date_headline"))
        self.assertContains(
            response,
            f'<div class="page-notification--failure">{message}</div>',
            html=True,
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
            response,
            f'<div class="page-notification--failure">{message}</div>',
            html=True,
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
            response,
            f'<div class="page-notification--failure">{message}</div>',
            html=True,
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


class TestSearchFacets(TestCase):
    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_populated_court_facets(
        self, mock_search_judgments_and_parse_response, mock_api_client
    ):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        eat_court_code = all_courts.get_by_code("EAT")
        response = self.client.get("/judgments/search?query=example+query")

        # Desired court_facet is present
        assert response.context["context"]["court_facets"] == {eat_court_code: "3"}
        # Blank keys are not present
        assert "" not in response.context["context"]["court_facets"].keys()
        # Keys that don't match existing courts are not present
        assert "invalid_court" not in response.context["context"]["court_facets"].keys()

    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_unpopulated_court_facet_keys(
        self, mock_search_judgments_and_parse_response, mock_api_client
    ):
        """
        Advanced search only populates court_facets if they are available
        """
        mock_search_judgments_and_parse_response.return_value = (
            FakeSearchResponseNoFacets()
        )
        response = self.client.get("/judgments/search?query=example+query")

        assert response.context["context"]["court_facets"] == {}

    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_populated_year_facets(
        self, mock_search_judgments_and_parse_response, mock_api_client
    ):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        response = self.client.get("/judgments/search?query=example+query")

        # Desired year_facet is present
        assert response.context["context"]["year_facets"] == {"2010": "103"}
        # Keys that don't match valid years are not present
        assert "1900" not in response.context["context"]["year_facets"].keys()

    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_unpopulated_year_facet_keys(
        self, mock_search_judgments_and_parse_response, mock_api_client
    ):
        """
        Advanced search only populates year_facets if they are available
        """
        mock_search_judgments_and_parse_response.return_value = (
            FakeSearchResponseNoFacets()
        )
        response = self.client.get("/judgments/search?query=example+query")

        assert response.context["context"]["year_facets"] == {}
