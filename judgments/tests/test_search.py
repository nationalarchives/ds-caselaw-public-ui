from datetime import date
from unittest.mock import patch

from caselawclient.search_parameters import SearchParameters
from django.test import TestCase
from ds_caselaw_utils import courts as all_courts

from judgments.tests.factories import CourtDateFactory
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
    def setUp(self):
        CourtDateFactory()

    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_judgment_advanced_search(
        self, mock_search_judgments_and_parse_response, mock_api_client
    ):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()

        response = self.client.get(
            "/judgments/search?query=waltham+forest", {"query": "waltham forest"}
        )

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
                judge="",
                party="",
                page="1",
                order="relevance",
                date_from=date(2001, 1, 1),
                date_to=None,
                page_size=10,
            ),
        )

    # TODO: Move this test coverage to forms!!!
    """
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
    """

    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_judgment_advanced_search_court_filters_no_date(
        self,
        mock_search_judgments_and_parse_response,
        mock_api_client,
    ):
        """
        GIVEN a client for making HTTP requests
        WHEN a GET request is made to "/judgments/search?court=ewhc/ch&court=ewhc/ipec"
        THEN the response should contain the expected applied filters HTML excluding implicitly set date
        AND the `search_judgments_and_parse_response` function should be called with the correct court string.

        The expected applied filters HTML:
        - Includes a list with class "results-search-component__removable-options"
        - Contains two list items (li) with links (a) representing the applied filters:
        - The first link represents the "Chancery Division of the High Court" filter
        - The second link represents the "Intellectual Property Enterprise Court" filter
        """
        response = self.client.get("/judgments/search?courts=ewhc/ch&courts=ewhc/ipec")

        expected_applied_filters_html = """
        <ul class="results-search-component__removable-options js-results-facets-applied-filters">
            <li>
              <a role="button"
                 tabindex="0"
                 draggable="false"
                 class="results-search-component__removable-options-link"
                 href="/judgments/search?query=&amp;courts=ewhc/ipec&amp;judge=&amp;party=&amp;order=-date&amp;page="
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
                 href="/judgments/search?query=&amp;courts=ewhc/ch&amp;judge=&amp;party=&amp;order=-date&amp;page="
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
            SearchParameters(
                query="",
                court="ewhc/ch,ewhc/ipec",
                order="-date",
                judge="",
                party="",
                date_from=date(2001, 1, 1),
                date_to=None,
                page="1",
                page_size=10,
            ),
        )
        assert_contains_html(response, expected_applied_filters_html)

    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_judgment_advanced_search_court_filters_with_from_date(
        self,
        mock_search_judgments_and_parse_response,
        mock_api_client,
    ):
        """
        GIVEN a client for making HTTP requests
        WHEN a GET request is made to:
            "/judgments/search?court=ewhc/ch&court=ewhc/ipec&from_date_0=1&from_date_1=1&from_date_2=1970"
        THEN the response should contain the expected applied filters HTML including explicitly set date
        AND the `search_judgments_and_parse_response` function should be called with the correct court string.

        The expected applied filters HTML:
        - Includes a list with class "results-search-component__removable-options"
        - Contains three list items (li) with links (a) representing the applied filters:
        - The first link represents the provided from date filter
        - The second link represents the "Chancery Division of the High Court" filter
        - The third link represents the "Intellectual Property Enterprise Court" filter
        """
        response = self.client.get(
            "/judgments/search?courts=ewhc/ch&courts=ewhc/ipec&from_date_0=1&from_date_1=1&from_date_2=1970"
        )

        expected_applied_filters_html = """
        <ul class="results-search-component__removable-options js-results-facets-applied-filters">
            <li>
              <a role="button"
                 tabindex="0"
                 draggable="false"
                 class="results-search-component__removable-options-link"
                 href="/judgments/search?query=&amp;courts=ewhc/ch&amp;courts=ewhc/ipec&amp;judge=&amp;party=&amp;order=-date&amp;page=">
                 <span class="results-search-component__removable-options-key">From:</span>
                 <span class="results-search-component__removable-options-value">
                   <span class="results-search-component__removable-options-value-text"> 01 Jan 1970</span>
                </span>
              </a>
            </li>
            <li>
              <a role="button"
                 tabindex="0"
                 draggable="false"
                 class="results-search-component__removable-options-link"
                 href="/judgments/search?from_date_0=1&amp;from_date_1=1&amp;from_date_2=1970&amp;query=&amp;courts=ewhc/ipec&amp;judge=&amp;party=&amp;order=-date&amp;page="
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
                 href="/judgments/search?from_date_0=1&amp;from_date_1=1&amp;from_date_2=1970&amp;query=&amp;courts=ewhc/ch&amp;judge=&amp;party=&amp;order=-date&amp;page="
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
            SearchParameters(
                query="",
                court="ewhc/ch,ewhc/ipec",
                order="-date",
                judge="",
                party="",
                date_from=date(1970, 1, 1),
                date_to=None,
                page="1",
                page_size=10,
            ),
        )
        assert_contains_html(response, expected_applied_filters_html)


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

        breakpoint()
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
