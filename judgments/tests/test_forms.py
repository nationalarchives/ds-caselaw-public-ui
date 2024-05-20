from datetime import date

from django.test import TestCase

from judgments.forms import AdvancedSearchForm
from judgments.forms.fields import DateRangeInputField


class TestAdvancedSearchForm(TestCase):
    def test_advanced_search_form_date_validation(self):
        """
        Given a from_date after the to_date, raise
        a validation error
        """
        # Due to this form using an extended version of the Django `SplitDateField``
        # each field is split into field_name_0 through 2, with 0 being day and 2 being year.
        data = {
            "from_date_0": "10",
            "from_date_1": "12",
            "from_date_2": "2012",
            "to_date_0": "9",
            "to_date_1": "10",
            "to_date_2": "2012",
        }

        form = AdvancedSearchForm(data=data)

        self.assertFalse(form.is_valid())


class TestDateRangeInputField(TestCase):
    def test_compress_from_no_day(self):
        field = DateRangeInputField(date_type="from")
        expected_date = date(2012, 1, 1)

        compressed_date = field.compress([None, 1, 2012])

        self.assertEqual(compressed_date, expected_date)

    def test_compress_from_no_month(self):
        field = DateRangeInputField(date_type="from")
        expected_date = date(2012, 1, 1)

        compressed_date = field.compress([1, None, 2012])

        self.assertEqual(compressed_date, expected_date)

    def test_compress_to_no_day(self):
        field = DateRangeInputField(date_type="to")
        expected_date = date(2012, 2, 29)

        compressed_date = field.compress([None, 2, 2012])

        self.assertEqual(compressed_date, expected_date)

    def test_compress_to_no_month(self):
        field = DateRangeInputField(date_type="to")
        expected_date = date(2012, 12, 31)

        compressed_date = field.compress([31, None, 2012])

        self.assertEqual(compressed_date, expected_date)

    def test_compress_no_year(self):
        field = DateRangeInputField(date_type="to")

        self.assertEqual(field.compress([31, 12, None]), None)
