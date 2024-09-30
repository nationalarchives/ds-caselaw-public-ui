from unittest.mock import patch

import lxml
from caselawclient.search_parameters import SearchParameters
from django.test import TestCase
from ds_caselaw_utils import courts as all_courts
from ds_caselaw_utils.courts import CourtCode

from judgments.tests.factories import CourtDateFactory
from judgments.tests.fixtures import (
    FakeSearchResponse,
    FakeSearchResponseNoFacets,
    FakeSearchResponseNoResults,
)
from judgments.tests.utils.assertions import (
    assert_contains_html,
    assert_response_contains_text,
    assert_response_not_contains_text,
)


class TestBrowseResults(TestCase):
    @patch("judgments.views.browse.api_client")
    @patch("judgments.views.browse.search_judgments_and_parse_response")
    def test_browse_results(self, mock_search_judgments_and_parse_response, mock_api_client):
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


class TestNoNCN(TestCase):
    @patch("judgments.views.browse.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_browse_results(self, mock_search_judgments_and_parse_response, mock_api_client):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponseNoResults()
        response = self.client.get(r"/judgments/search?query=[2024]%20EAT%209999")
        self.assertContains(
            response, "There is no judgment with the Neutral Citation of [2024] EAT 9999 in our database.", html=True
        )


class TestSearchResults(TestCase):
    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_judgment_advanced_search_with_populated_court_dates(
        self, mock_search_judgments_and_parse_response, mock_api_client
    ):
        """
        GIVEN a client for making HTTP requests
        WHEN a GET request is made to "/judgments/search?query=waltham+forest" and the `CourtDates` model has a row
        THEN the response should contain the expected applied filters HTML excluding the implicitly set minimum date
        AND the `search_judgments_and_parse_response` function should be called with the correct query string and the
        minimum date from CourtDates

        The expected applied filters HTML:
        - Includes a list with class "results-search-component__removable-options"
        - Contains two list items (li) with links (a) representing the applied filters:
        - The first link represents the "Chancery Division of the High Court" filter
        - The second link represents the "Intellectual Property Enterprise Court" filter
        """
        CourtDateFactory()
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()

        response = self.client.get("/judgments/search?query=waltham+forest", {"query": "waltham forest"})

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
                page=1,
                order="relevance",
                date_from="2001-01-01",
                date_to=None,
                page_size=10,
            ),
        )

    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_judgment_advanced_search_without_populated_court_dates(
        self, mock_search_judgments_and_parse_response, mock_api_client
    ):
        """
        GIVEN a client for making HTTP requests
        WHEN a GET request is made to "/judgments/search?query=waltham+forest" and the `CourtDates` model is empty
        THEN the response should contain the expected applied filters HTML excluding the implicitly set minimum date
        AND the `search_judgments_and_parse_response` function should be called with the correct query string and the
        minimum date from `settings.MINIMUM_WARNING_YEAR`

        The expected applied filters HTML:
        - Includes a list with class "results-search-component__removable-options"
        - Contains two list items (li) with links (a) representing the applied filters:
        - The first link represents the "Chancery Division of the High Court" filter
        - The second link represents the "Intellectual Property Enterprise Court" filter
        """
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()

        response = self.client.get("/judgments/search?query=waltham+forest", {"query": "waltham forest"})

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
                page=1,
                order="relevance",
                date_from="2003-01-01",
                date_to=None,
                page_size=10,
            ),
        )

    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_judgment_advanced_search_warns_user_with_date_before_minimum_warning_year(
        self, mock_search_judgments_and_parse_response, mock_api_client
    ):
        """
        GIVEN a client for making HTTP requests
        WHEN a GET request is made to "/judgments/search?query=waltham+forest"
        AND the from_date is before `settings.MINIMUM_WARNING_YEAR`
        AND there's no search results
        THEN the response should contain the expected warning

        The expected applied filters HTML:
        - Includes a div with class `govuk-warning-text` and correct warning text
        """
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()

        response = self.client.get("/judgments/search?from_date_0=1&from_date_1=1&from_date_2=1444")

        expected_text = """
                1444 is before 2003, the date of the oldest record on the Find Case Law service.
        """
        xpath_query = "//div[@class='govuk-warning-text__text']"
        assert_response_contains_text(response, expected_text, xpath_query)

    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_judgment_advanced_search_not_warning_user_with_date_after_minimum_warning_year(
        self, mock_search_judgments_and_parse_response, mock_api_client
    ):
        """
        GIVEN a client for making HTTP requests
        WHEN a GET request is made to "/judgments/search?query=waltham+forest"
        AND the from_date is after `settings.MINIMUM_WARNING_YEAR`
        THEN the response should contain the date range warning

        The expected applied filters HTML:
        - Includes a div with class `advice-message`
        """
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()

        response = self.client.get("/judgments/search?from_date_0=1&from_date_1=1&from_date_2=2011")

        expected_text = """
                2011 is before 2003, the date of the oldest record on the Find Case Law service.
                Showing results from 2003.
        """
        xpath_query = "//div[@class='govuk-warning-text__text']"
        assert_response_not_contains_text(response, expected_text, xpath_query)

    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_judgment_advanced_search_not_warning_user_with_no_results(
        self, mock_search_judgments_and_parse_response, mock_api_client
    ):
        """
        GIVEN a client for making HTTP requests
        WHEN a GET request is made to "/judgments/search?query=waltham+forest"
        AND the from_date is before `settings.MINIMUM_WARNING_YEAR`
        AND there are no results returned
        THEN the response not should contain the date range warning

        The expected applied filters HTML:
        - Includes a div with class `advice-message`
        """
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponseNoResults()

        response = self.client.get("/judgments/search?from_date_0=1&from_date_1=1&from_date_2=1444")

        expected_text = """
                1444 is before 2003, the date of the oldest record on the Find Case Law service.
                Showing results from 2003.
        """
        xpath_query = "//div[@class='govuk-warning-text__text']"
        assert_response_not_contains_text(response, expected_text, xpath_query)

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
        CourtDateFactory()

        expected_applied_filters_html = """
        <ul class="results-search-component__removable-options js-results-facets-applied-filters">
            <li>
              <a role="button"
                 tabindex="0"
                 draggable="false"
                 class="results-search-component__removable-options-link"
                 href="/judgments/search?query=&amp;court=ewhc/ipec&amp;judge=&amp;party=&amp;order=-date&amp;page="
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
                 href="/judgments/search?query=&amp;court=ewhc/ch&amp;judge=&amp;party=&amp;order=-date&amp;page="
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
        response = self.client.get("/judgments/search?court=ewhc/ch&court=ewhc/ipec")

        mock_search_judgments_and_parse_response.assert_called_with(
            mock_api_client,
            SearchParameters(
                query="",
                court="ewhc/ch,ewhc/ipec",
                order="-date",
                judge="",
                party="",
                date_from="2001-01-01",
                date_to=None,
                page=1,
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
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()

        response = self.client.get(
            "/judgments/search?court=ewhc/ch&court=ewhc/ipec&from_date_0=1&from_date_1=1&from_date_2=2011"
        )

        expected_applied_filters_html = """
        <ul class="results-search-component__removable-options js-results-facets-applied-filters">
            <li>
              <a role="button"
                 tabindex="0"
                 draggable="false"
                 class="results-search-component__removable-options-link"
                 href="/judgments/search?query=&amp;court=ewhc/ch&amp;court=ewhc/ipec&amp;judge=&amp;party=&amp;order=-date&amp;page=">
                 <span class="results-search-component__removable-options-key">From:</span>
                 <span class="results-search-component__removable-options-value">
                   <span class="results-search-component__removable-options-value-text"> 01 Jan 2011</span>
                </span>
              </a>
            </li>
            <li>
              <a role="button"
                 tabindex="0"
                 draggable="false"
                 class="results-search-component__removable-options-link"
                 href="/judgments/search?from_date_0=1&amp;from_date_1=1&amp;from_date_2=2011&amp;query=&amp;court=ewhc/ipec&amp;judge=&amp;party=&amp;order=-date&amp;page="
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
                 href="/judgments/search?from_date_0=1&amp;from_date_1=1&amp;from_date_2=2011&amp;query=&amp;court=ewhc/ch&amp;judge=&amp;party=&amp;order=-date&amp;page="
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
                date_from="2011-01-01",
                date_to=None,
                page=1,
                page_size=10,
            ),
        )

        assert_contains_html(response, expected_applied_filters_html)


class TestSearchBreadcrumbs(TestCase):
    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_search_breadcrumbs_without_query_string(self, mock_search_judgments_and_parse_response, mock_api_client):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        response = self.client.get("/judgments/search")
        assert response.context["breadcrumbs"] == [{"text": "Search results"}]

    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_search_breadcrumbs_with_query_string(self, mock_search_judgments_and_parse_response, mock_api_client):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        response = self.client.get("/judgments/search?query=waltham+forest")

        assert response.context["breadcrumbs"] == [{"text": 'Search results for "waltham forest"'}]


class TestSearchFacets(TestCase):
    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_populated_court_facets(self, mock_search_judgments_and_parse_response, mock_api_client):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        court_code = all_courts.get_by_code(CourtCode("EWHC-KBD-TCC"))
        response = self.client.get("/judgments/search?query=example+query")

        # Desired court_facet is present
        assert response.context["court_facets"] == {court_code: "1"}
        # Blank keys are not present
        assert "" not in response.context["court_facets"].keys()
        # Keys that don't match existing courts are not present
        assert "invalid_court" not in response.context["court_facets"].keys()

    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_populated_tribunal_facets(self, mock_search_judgments_and_parse_response, mock_api_client):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        tribunal_code = all_courts.get_by_code(CourtCode("EAT"))
        response = self.client.get("/judgments/search?query=example+query")

        # Desired tribunal_facet is present
        assert response.context["tribunal_facets"] == {tribunal_code: "3"}
        # Blank keys are not present
        assert "" not in response.context["tribunal_facets"].keys()
        # Keys that don't match existing tribunals are not present
        assert "invalid_court" not in response.context["tribunal_facets"].keys()

    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_unpopulated_court_facet_keys(self, mock_search_judgments_and_parse_response, mock_api_client):
        """
        Advanced search only populates court_facets if they are available
        """
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponseNoFacets()
        response = self.client.get("/judgments/search?query=example+query")

        assert response.context["court_facets"] == {}
        assert response.context["tribunal_facets"] == {}

    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_populated_year_facets(self, mock_search_judgments_and_parse_response, mock_api_client):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        response = self.client.get("/judgments/search?query=example+query")

        # Desired year_facet is present
        assert response.context["year_facets"] == {"2010": "103"}
        # Keys that don't match valid years are not present
        assert "1900" not in response.context["year_facets"].keys()

    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_per_page_query_parameter_selected(self, mock_search_judgments_and_parse_response, mock_api_client):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        response = self.client.get("/judgments/search?query=example+query&per_page=50")
        per_page_select_id = lxml.html.fromstring(response.content).xpath('//*[@id="per_page"]')[0]
        option_10_selected = per_page_select_id.xpath("./option[@value=10]/@selected")
        option_50_selected = per_page_select_id.xpath("./option[@value=50]/@selected")

        assert option_50_selected
        assert not option_10_selected

    @patch("judgments.views.advanced_search.api_client")
    @patch("judgments.views.advanced_search.search_judgments_and_parse_response")
    def test_unpopulated_year_facet_keys(self, mock_search_judgments_and_parse_response, mock_api_client):
        """
        Advanced search only populates year_facets if they are available
        """
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponseNoFacets()
        response = self.client.get("/judgments/search?query=example+query")

        assert response.context["year_facets"] == {}
