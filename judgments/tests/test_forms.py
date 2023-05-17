import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase

from judgments.forms.structured_search import DateField


def error_messages(errors):
    messages = []
    for error in errors:
        if type(error) == str:
            messages.append(error)
        elif type(error) == ValidationError:
            messages.extend(*error_messages(error.args))
        elif type(error) == list:
            messages.extend(*[error_messages(e) for e in error])
        elif type(error) == tuple:
            messages.extend(*[error_messages(e) for e in error])
        return messages


class TestStructuredSearchForm(TestCase):
    def test_date_takes_precedence_over_parts(self):
        pass

    def test_blank_date_is_ignored(self):
        pass


class TestDateField(TestCase):
    def setUp(self):
        self.field = DateField(required=False)

    def test_when_a_valid_date_is_provided(self):
        self.assertEqual(self.field.clean(["2021", "01", "01"]), "2021-01-01")

    def test_returns_none_when_no_date_is_provided(self):
        self.assertEqual(self.field.clean(["", "", ""]), None)

    def test_defaults_to_jan_when_no_month_provided(self):
        self.assertEqual(self.field.clean(["2021", "", "01"]), "2021-01-01")

    def test_defaults_to_first_when_no_day_provided(self):
        self.assertEqual(self.field.clean(["2021", "01", ""]), "2021-01-01")

    def test_returns_none_when_no_year_provided(self):
        self.assertEqual(self.field.clean(["", "01", "01"]), None)

    def test_defaults_to_dec_when_no_month_provided_and_default_to_last_set(self):
        field = DateField(default_to_last=True)
        self.assertEqual(field.clean(["2021", "", "01"]), "2021-12-01")

    def test_defaults_to_end_of_month_when_no_month_provided_and_default_to_last_set(
        self,
    ):
        field = DateField(default_to_last=True)
        self.assertEqual(field.clean(["2021", "01", ""]), "2021-01-31")
        self.assertEqual(field.clean(["2021", "02", ""]), "2021-02-28")
        self.assertEqual(field.clean(["2020", "02", ""]), "2020-02-29")

    def test_raises_an_error_on_a_silly_month(self):
        with pytest.raises(ValidationError) as err:
            self.field.clean(["2021", "13", "01"])
        self.assertIn("Month must be less than 12", error_messages(err.value))

    def test_raises_an_error_on_a_silly_day(self):
        with pytest.raises(ValidationError) as err:
            self.field.clean(["2021", "02", "29"])
        self.assertIn("day is out of range for month", err.value.args)

    def test_raises_an_error_on_non_numeric_input(self):
        with pytest.raises(ValidationError) as err:
            self.field.clean(["2021", "February", "21"])
        self.assertIn("Please enter a number", error_messages(err.value.args))
