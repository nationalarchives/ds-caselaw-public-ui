from types import SimpleNamespace
from unittest.mock import patch

from django.template.response import TemplateResponse
from django.test import RequestFactory, TestCase
from ds_caselaw_utils.courts import CourtNotFoundException

from config.views.courts import CourtOrTribunalView, CourtsTribunalsListView
from judgments.models.court_dates import CourtDates


class TestCourtsTribunalsListView(TestCase):
    @patch("config.views.courts.get_court_judgments_count")
    def test_decorate_court_group_adds_dates_and_document_counts(self, mock_get_court_judgments_count):

        def judgment_count(court):
            if court.canonical_param == "court-with-data":
                return 123
            else:
                return 0

        mock_get_court_judgments_count.side_effect = judgment_count
        CourtDates.objects.create(param="court-with-data", start_year=2020, end_year=2024)

        court_with_data = SimpleNamespace(canonical_param="court-with-data", start_year=None, end_year=None)
        court_without_data = SimpleNamespace(canonical_param="court-without-data", start_year=1999, end_year=2001)
        group = SimpleNamespace(courts=[court_with_data, court_without_data])

        decorated_group = CourtsTribunalsListView().decorate_court_group(
            group,
        )

        assert decorated_group == group
        assert court_with_data.start_year == 2020
        assert court_with_data.end_year == 2024
        assert court_with_data.documents_count == 123
        assert court_without_data.start_year == 1999
        assert court_without_data.end_year == 2001
        assert court_without_data.documents_count == 0


class TestCourtOrTribunalView(TestCase):
    """Test the CourtOrTribunalView handles court not found correctly."""

    @patch("config.views.courts.courts.get_by_param")
    def test_returns_404_when_court_not_found(self, mock_get_by_param):
        """Test that accessing a non-existent court returns a 404 response."""
        mock_get_by_param.side_effect = CourtNotFoundException("Court not found")

        response = self.client.get("/courts-and-tribunals/invalid-param")

        assert response.status_code == 404

    @patch("config.views.courts.CourtOrTribunalView._get_search_response")
    def test_gtm_data_layer_for_tribunal(self, mock_search_response):
        mock_search_response.return_value = type("Resp", (), {"results": []})()
        request = RequestFactory().get("/courts-and-tribunals/eat")

        response = CourtOrTribunalView.as_view()(request, param="eat")

        assert isinstance(response, TemplateResponse)
        assert response.context_data is not None
        assert response.context_data["gtm_data_layer"] == {
            "page_type": "court",
            "court_code": "EAT",
            "court_type": "tribunal",
        }
