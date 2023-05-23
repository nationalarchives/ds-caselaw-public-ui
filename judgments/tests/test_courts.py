from unittest.mock import Mock, patch

from django.test import TestCase

from judgments.models import CourtDates
from judgments.templatetags.court_utils import get_court_date_range, get_court_name


def test_get_court_name():
    assert get_court_name("uksc") == "United Kingdom Supreme Court"


def test_get_court_name_non_existent():
    assert get_court_name("ffff") == ""


@patch("judgments.templatetags.court_utils.CourtDates.objects.get")
class TestCourtDatesHelper(TestCase):
    def mock_court_dates(self, start_year, end_year):
        mock = Mock()
        mock.configure_mock(start_year=start_year, end_year=end_year)
        return mock

    def test_when_court_with_param_exists_and_no_dates_in_db_and_start_end_same(
        self, get
    ):
        get.side_effect = CourtDates.DoesNotExist
        court = self.mock_court_dates(2011, 2011)
        self.assertEqual(get_court_date_range(court), "2011")

    def test_when_court_with_param_exists_and_no_dates_in_db_and_start_end_different(
        self, get
    ):
        get.side_effect = CourtDates.DoesNotExist
        court = self.mock_court_dates(2011, 2012)
        self.assertEqual(get_court_date_range(court), "2011&nbsp;to&nbsp;2012")

    def test_when_court_with_param_exists_and_dates_in_db_and_start_end_same(self, get):
        get.return_value = self.mock_court_dates(2013, 2013)
        court = self.mock_court_dates(2011, 2012)
        self.assertEqual(get_court_date_range(court), "2013")

    def test_when_court_with_param_exists_and_dates_in_db_and_start_end_different(
        self, get
    ):
        get.return_value = self.mock_court_dates(2013, 2015)
        court = self.mock_court_dates(2011, 2012)
        self.assertEqual(get_court_date_range(court), "2013&nbsp;to&nbsp;2015")
