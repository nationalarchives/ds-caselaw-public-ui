import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase

from judgments.forms.structured_search import DateField

class TestStructuredSearchForm(TestCase):
    def test_date_takes_precedence_over_parts(self):
        pass

    def test_blank_date_is_ignored(self):
        pass

class TestDateField(TestCase):

    def setUp(self):
        self.field = DateField()

    def test_when_a_valid_date_is_provided(self):
        self.assertEqual(self.field.compress(["2021", "01", "01"]), "2021-01-01")

    def test_returns_none_when_no_date_is_provided(self):
        self.assertEqual(self.field.compress(["", "", ""]), None)

    def test_defaults_to_jan_when_no_month_provided(self):
        self.assertEqual(self.field.compress(["2021", "", "01"]), "2021-01-01")

    def test_defaults_to_first_when_no_day_provided(self):
        self.assertEqual(self.field.compress(["2021", "01", ""]), "2021-01-01")

    def test_returns_none_when_no_year_provided(self):
        self.assertEqual(self.field.compress(["", "01", "01"]), None)

    def test_defaults_to_dec_when_no_month_provided_and_default_to_last_set(self):
        field = DateField(default_to_last=True)
        self.assertEqual(field.compress(["2021", "", "01"]), "2021-12-01")

    def test_defaults_to_end_of_month_when_no_month_provided_and_default_to_last_set(self):
        field = DateField(default_to_last=True)
        self.assertEqual(field.compress(["2021", "01", ""]), "2021-01-31")
        self.assertEqual(field.compress(["2021", "02", ""]), "2021-02-28")
        self.assertEqual(field.compress(["2020", "02", ""]), "2020-02-29")

    def test_raises_an_error_on_a_silly_month(self):
        with pytest.raises(ValidationError) as err:
            self.field.compress(["2021", "13", "01"])
        self.assertIn(err.value.args, "month is out of range")

    def test_raises_an_error_on_a_silly_day(self):
        with pytest.raises(ValidationError) as err:
            self.field.compress(["2021", "02", "29"])
        self.assertIn(err.value.args, "day is out of range for month")

    def test_raises_an_error_on_non_numeric_input(self):
        with pytest.raises(ValidationError) as err:
            self.field.compress(["2021", "February", "21"])
        self.assertIn(err.value.args, "please enter a number")