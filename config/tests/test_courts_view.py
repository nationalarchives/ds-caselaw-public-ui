from unittest.mock import patch

from django.test import RequestFactory, TestCase
from ds_caselaw_utils.courts import CourtNotFoundException

from config.views.courts import CourtOrTribunalView


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

        assert response.context_data["gtm_data_layer"] == {
            "page_type": "court",
            "court_code": "EAT",
            "court_type": "tribunal",
        }
