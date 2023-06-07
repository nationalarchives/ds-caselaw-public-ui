from typing import Dict

from django.test import TestCase

from judgments.utils import parse_date_parameter


class TestDateParsing(TestCase):
    def test_when_nothing_is_provided(self):
        """When the given parameter is not provided, either as a complete or
        separate value, don't return anything, and don't raise an error
        """
        params = {"query": "Some other query param"}
        parsed = parse_date_parameter(params, "date")
        self.assertIsNone(parsed)

    def test_when_a_date_is_provided(self):
        """
        When a parameter is provided with the given name, return that value itself.
        """
        params = {"date": "2019-12-02"}
        parsed = parse_date_parameter(params, "date")
        self.assertEqual(parsed, "2019-12-02")

    def test_provided_date_takes_precedence(self):
        """
        When a parameter is provided with the given name, return that value, even if day month and year are provided.
        """
        params = {
            "date": "2019-12-02",
            "date_day": "3",
            "date_month": "1",
            "date_year": "2020",
        }
        parsed = parse_date_parameter(params, "date")
        self.assertEqual(parsed, "2019-12-02")

    def test_a_blank_date_does_not_count_as_provided(self):
        """
        When a blank parameter is provided with the given name, use the day month year parameters for preference.
        """
        params = {"date": "", "date_day": "3", "date_month": "1", "date_year": "2020"}
        parsed = parse_date_parameter(params, "date")
        self.assertEqual(parsed, "2020-01-03")

    def test_constructs_a_date_from_date_parts(self):
        """
        When no date is provided directly, it constructs one from the given day month and year.
        """
        params = {"date_day": "3", "date_month": "1", "date_year": "2020"}
        parsed = parse_date_parameter(params, "date")
        self.assertEqual(parsed, "2020-01-03")

    def test_returns_none_if_no_date_provided(self):
        """
        When no date or date parts are provided, it returns None.
        """
        params: Dict[str, str] = {}
        parsed = parse_date_parameter(params, "date")
        self.assertIsNone(parsed)

    def test_returns_beginning_of_month_when_no_day(self):
        """
        When a year and month are provided, but no day, it defaults to the first day of the month.
        """
        params = {"date_month": "5", "date_year": "2020"}
        parsed = parse_date_parameter(params, "date")
        self.assertEqual(parsed, "2020-05-01")

    def test_returns_january_when_no_month(self):
        """
        When a year is provided but no month or day, it defaults to the first day of January of that year.
        """
        params = {"date_year": "2020"}
        parsed = parse_date_parameter(params, "date")
        self.assertEqual(parsed, "2020-01-01")

    def test_returns_none_if_year_is_blank(self):
        """When a year parameter is provided but empty, it returns none"""
        params = {"date_year": ""}
        parsed = parse_date_parameter(params, "date")
        self.assertIsNone(parsed)

    def test_blank_months_and_days_count_as_undefined(self):
        """Blank months and days are treated as undefined, and default to the first month / day."""
        params = {"date_year": "2009", "date_month": "", "date_day": ""}
        parsed = parse_date_parameter(params, "date")
        self.assertEqual(parsed, "2009-01-01")

    def test_returns_december_when_no_month_and_default_to_last_selected(self):
        """
        When a year is provided but no month or day, and the default_to_last
        option is passed, it defaults to the last day of december of that year.
        """
        params = {"date_year": "2020"}
        parsed = parse_date_parameter(params, "date", default_to_last=True)
        self.assertEqual(parsed, "2020-12-31")

    def test_returns_lastday_long_month_when_year_and_month_given(self):
        """
        When a year and a long 31 days month is provided, but no day, and the default_to_last
        option is passed, it defaults to the last day of the month.
        """
        params = {"date_month": "5", "date_year": "2020"}
        parsed = parse_date_parameter(params, "date", default_to_last=True)
        self.assertEqual(parsed, "2020-05-31")

    def test_returns_lastday_short_month_when_year_and_month_given(self):
        """
        When a year and a short 28 days month is provided, but no day, and the default_to_last
        option is passed, it defaults to the last day of the month.
        """
        params = {"date_month": "2", "date_year": "2021"}
        parsed = parse_date_parameter(params, "date", default_to_last=True)
        self.assertEqual(parsed, "2021-02-28")

    def test_returns_lastday_month_when_leap_year_and_month_given(self):
        """
        When a leap year and month is provided, but no day, and the default_to_last
        option is passed, it defaults to the last day of the month.
        """
        params = {"date_month": "2", "date_year": "2020"}
        parsed = parse_date_parameter(params, "date", default_to_last=True)
        self.assertEqual(parsed, "2020-02-29")

    def test_raises_error_when_a_silly_month_is_given(self):
        """
        When a silly month number (ie >=13) is given, it raises an error.
        """
        params = {"date_month": "13", "date_day": "1", "date_year": "2020"}
        self.assertRaises(ValueError, parse_date_parameter, params, "date")

    def test_raises_error_when_a_silly_day_is_given(self):
        """
        When a silly month number (ie > the number of days in the given month) is given, it raises an error.
        """
        params = {"date_month": "04", "date_day": "31", "date_year": "2020"}
        self.assertRaises(ValueError, parse_date_parameter, params, "date")
