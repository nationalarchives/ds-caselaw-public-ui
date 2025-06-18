from unittest.mock import Mock, patch

from django.test import TestCase
from ds_caselaw_utils.courts import CourtNotFoundException

from judgments.templatetags.court_utils import get_court_name


class TestGetCourtName(TestCase):
    @patch("judgments.templatetags.court_utils.all_courts.get_by_param")
    def test_returns_court_name_when_get_by_param_succeeds(self, mock_get_by_param):
        mock_court = Mock()
        mock_court.name = "Court A"
        mock_get_by_param.return_value = mock_court

        result = get_court_name("court-a")
        assert result == "Court A"

    @patch("judgments.templatetags.court_utils.all_courts.get_by_code")
    @patch("judgments.templatetags.court_utils.all_courts.get_by_param", side_effect=CourtNotFoundException)
    def test_returns_court_name_when_get_by_code_succeeds(self, mock_get_by_param, mock_get_by_code):
        mock_court = Mock()
        mock_court.name = "Court B"
        mock_get_by_code.return_value = mock_court

        result = get_court_name("XYZ")
        assert result == "Court B"

    @patch("judgments.templatetags.court_utils.all_courts.get_by_code", side_effect=CourtNotFoundException)
    @patch("judgments.templatetags.court_utils.all_courts.get_by_param", side_effect=CourtNotFoundException)
    def test_returns_empty_string_when_both_lookups_fail(self, mock_get_by_param, mock_get_by_code):
        result = get_court_name("unknown")
        assert result == ""
