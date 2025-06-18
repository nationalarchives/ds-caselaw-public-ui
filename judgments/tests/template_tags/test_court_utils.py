from unittest.mock import Mock, patch

from django.test import TestCase
from ds_caselaw_utils.courts import CourtNotFoundException

from judgments.templatetags.court_utils import get_court_name, get_first_judgment_year


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


class TestGetFirstJudgmentYear(TestCase):
    @patch("judgments.templatetags.court_utils.CourtDates.min_year")
    def test_returns_min_year(self, mock_min_year):
        mock_min_year.return_value = 1999
        result = get_first_judgment_year()
        assert result == 1999

    @patch("judgments.templatetags.court_utils.logging.warning")
    @patch("judgments.templatetags.court_utils.CourtDates.min_year", return_value=None)
    @patch("judgments.templatetags.court_utils.all_courts.get_selectable")
    def test_returns_fallback_min_start_year(self, mock_get_selectable, mock_min_year, mock_logging):
        mock_get_selectable.return_value = [
            Mock(start_year=None),
            Mock(start_year=2005),
            Mock(start_year=1998),
            Mock(start_year=2010),
        ]
        result = get_first_judgment_year()
        assert result == 1998
        mock_logging.assert_called_once_with("CourtDates table is empty! using fallback min_year.")
