from datetime import datetime
from unittest.mock import patch

from caselawclient.factories import SearchResultFactory
from django.test import TestCase
from django.urls import reverse

from config.views.sitemaps import SitemapStaticView
from judgments.models import CourtDates
from judgments.tests.fixture_data import FakeSearchResponse, FakeSearchResponseBaseClass


class MockCourtYearSearchResult(FakeSearchResponseBaseClass):
    results = [
        SearchResultFactory.build(
            uri="d-a1b2c3", slug="test/2025/123", transformation_date=datetime(2025, 1, 1, 1, 23).isoformat()
        ),
        SearchResultFactory.build(
            uri="d-d4e5f6", slug="test/2025/456", transformation_date=datetime(2025, 2, 2, 4, 56).isoformat()
        ),
    ]


class TestSitemaps(TestCase):
    def setUp(self):
        CourtDates.objects.create(param="testcourt", start_year=2023, end_year=2025)
        CourtDates.objects.create(param="testcourt/b", start_year=2025, end_year=2025)

    def test_sitemap_index_returns_expected_values(self):
        response = self.client.get("/sitemap.xml")

        assert response.status_code == 200

        self.assertContains(response, "sitemap-static.xml")
        self.assertContains(response, "sitemap-courts.xml")
        self.assertContains(response, "sitemap-court-testcourt-2023.xml")
        self.assertContains(response, "sitemap-court-testcourt-2024.xml")
        self.assertContains(response, "sitemap-court-testcourt-2025.xml")
        self.assertContains(response, "sitemap-court-testcourt/b-2025.xml")

    def test_sitemap_static(self):
        response = self.client.get("/sitemap-static.xml")

        assert response.status_code == 200

    def test_sitemap_courts(self):
        response = self.client.get("/sitemap-courts.xml")

        assert response.status_code == 200

        self.assertContains(response, "courts-and-tribunals/testcourt")
        self.assertContains(response, "courts-and-tribunals/testcourt/b")

    @patch("config.views.sitemaps.search_judgments_and_parse_response")
    def test_sitemap_court_year(self, mock_search_judgments_and_parse_response):
        mock_search_judgments_and_parse_response.return_value = MockCourtYearSearchResult()

        response = self.client.get("/sitemap-court-testcourt/b-2025.xml")

        assert response.status_code == 200

        self.assertContains(response, "/test/2025/123")
        self.assertNotContains(response, "d-a1b2c3")
        self.assertContains(response, "2025-01-01")

        self.assertContains(response, "/test/2025/456")
        self.assertNotContains(response, "d-d4e5f6")
        self.assertContains(response, "2025-02-02")

    @patch("judgments.templatetags.court_utils.search_judgments_and_parse_response")
    @patch("judgments.views.index.search_judgments_and_parse_response")
    def test_static_sitemaps_do_not_redirect(self, mock_search_judgments_index, mock_search_judgments_template):
        """Test that all static page URL names in the sitemap resolve with status 200, and do not redirect or 404."""
        mock_search_judgments_index.return_value = FakeSearchResponse()
        mock_search_judgments_template.return_value = FakeSearchResponse()
        for url_name in SitemapStaticView.url_names:
            with self.subTest(url_name=url_name):
                url = reverse(url_name)
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code,
                    200,
                    f"URL name '{url_name}' resolved to '{url}' but returned status {response.status_code}",
                )
