from unittest.mock import patch

from django.test import TestCase
from ds_caselaw_utils.courts import CourtNotFoundException


class TestCourtOrTribunalView(TestCase):
    """Test the CourtOrTribunalView handles court not found correctly."""

    @patch("config.views.courts.courts.get_by_param")
    def test_returns_404_when_court_not_found(self, mock_get_by_param):
        """Test that accessing a non-existent court returns a 404 response."""
        mock_get_by_param.side_effect = CourtNotFoundException("Court not found")

        response = self.client.get("/courts-and-tribunals/invalid-param")

        assert response.status_code == 404
