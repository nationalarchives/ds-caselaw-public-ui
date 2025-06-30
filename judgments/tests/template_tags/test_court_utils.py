from datetime import date
from unittest.mock import Mock, patch

from caselawclient.search_parameters import SearchParameters
from django.test import TestCase
from django.utils.safestring import SafeString
from ds_caselaw_utils.courts import CourtNotFoundException, CourtParam

from judgments.models.court_dates import CourtDates
from judgments.templatetags.court_utils import (
    get_court_date_range,
    get_court_judgments_count,
    get_court_name,
    get_first_judgment_year,
    get_last_judgment_year,
)


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


class TestGetLastJudgmentYear(TestCase):
    @patch("judgments.templatetags.court_utils.CourtDates.max_year")
    def test_returns_max_year(self, mock_max_year):
        mock_max_year.return_value = 2022
        result = get_last_judgment_year()
        assert result == 2022

    @patch("judgments.templatetags.court_utils.date")
    @patch("judgments.templatetags.court_utils.logging.warning")
    @patch("judgments.templatetags.court_utils.CourtDates.max_year", return_value=None)
    def test_fallback_to_today_year(self, mock_max_year, mock_logging, mock_date):
        mock_date.today.return_value = date(2024, 1, 1)
        result = get_last_judgment_year()
        assert result == 2024
        mock_logging.assert_called_once_with("CourtDates table is empty! using fallback max_year.")


class TestGetCourtDateRange(TestCase):
    @patch("judgments.templatetags.court_utils.CourtDates.objects.get")
    def test_same_year_returns_single_year(self, mock_get):
        mock_get.return_value = Mock(start_year=2015, end_year=2015)
        param = CourtParam("court-x")
        result = get_court_date_range(param)
        assert result == "2015"

    @patch("judgments.templatetags.court_utils.CourtDates.objects.get")
    def test_different_years_returns_range_with_nbsp(self, mock_get):
        mock_get.return_value = Mock(start_year=2000, end_year=2020)
        param = CourtParam("court-y")
        result = get_court_date_range(param)
        assert isinstance(result, SafeString)
        assert result == "2000&nbsp;to&nbsp;2020"

    @patch("judgments.templatetags.court_utils.all_courts.get_by_param")
    @patch("judgments.templatetags.court_utils.CourtDates.objects.get", side_effect=CourtDates.DoesNotExist)
    def test_fallback_to_all_courts_on_missing_courtdates(self, mock_get, mock_get_by_param):
        mock_get_by_param.return_value = Mock(start_year=1995, end_year=1999)
        param = CourtParam("fallback-court")
        result = get_court_date_range(param)
        assert result == "1995&nbsp;to&nbsp;1999"


class TestGetCourtJudgmentsCount(TestCase):
    @patch("judgments.templatetags.court_utils.search_judgments_and_parse_response")
    def test_returns_total_count_as_int(self, mock_search):
        mock_response = Mock()
        mock_response.total = "42"
        mock_search.return_value = mock_response

        mock_court = Mock()
        mock_court.canonical_param = "some-court"

        result = get_court_judgments_count(mock_court)
        assert result == 42
        mock_search.assert_called_once()
        args, kwargs = mock_search.call_args
        assert isinstance(args[0], object)
        assert isinstance(args[1], SearchParameters)
        assert args[1].court == "some-court"
