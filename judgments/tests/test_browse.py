from unittest.mock import patch

from caselawclient.search_parameters import SearchParameters
from django.test import TestCase

from judgments.tests.fixture_data import (
    FakeSearchResponse,
)
from judgments.views.browse import BrowseView


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
        assert response.context_data is not None
        self.assertEqual(
            response.context_data["gtm_data_layer"],
            {
                "page_type": "browse",
            },
        )

    @patch("judgments.views.browse.api_client")
    @patch("judgments.views.browse.search_judgments_and_parse_response")
    def test_year_only_browse_gtm_data_layer(self, mock_search_judgments_and_parse_response, mock_api_client):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        response = self.client.get("/2024")

        assert response.context_data is not None
        self.assertEqual(response.context_data["gtm_data_layer"], {"page_type": "browse"})

    @patch("judgments.views.browse.api_client")
    @patch("judgments.views.browse.search_judgments_and_parse_response")
    def test_browse_with_court_param_sets_gtm_court(self, mock_search_judgments_and_parse_response, mock_api_client):
        mock_search_judgments_and_parse_response.return_value = FakeSearchResponse()
        response = self.client.get("/ewhc/ch")

        assert response.context_data is not None
        self.assertEqual(
            response.context_data["gtm_data_layer"],
            {
                "page_type": "browse",
                "court_code": "EWHC-Chancery",
                "court_type": "court",
            },
        )

    def test_atom_feed_url_uses_tribunal_param_for_nested_tribunal_codes(self):
        view = BrowseView()

        # Top-level tribunal code
        assert view._build_atom_feed_url("eat", None) == "/atom.xml?tribunal=eat"
        # Nested under a group heading (must not be misclassified as court)
        assert view._build_atom_feed_url("ukut/iac", 2024) == (
            "/atom.xml?tribunal=ukut%2Fiac&from_date_2=2024&to_date_2=2024"
        )
        # Court code still uses court param
        assert view._build_atom_feed_url("ewhc/ch", None) == "/atom.xml?court=ewhc%2Fch"
