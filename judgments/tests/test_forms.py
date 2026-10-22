from datetime import date
from unittest.mock import Mock, patch

from django.conf import settings
from django.test import TestCase
from ds_caselaw_utils.courts import Court
from lxml import html

from judgments.forms import AdvancedSearchForm
from judgments.forms.fields import DateRangeInputField
from judgments.forms.search_forms import _get_scope_choices


class TestAdvancedSearchForm(TestCase):
    @patch("judgments.forms.search_forms.TRIBUNAL_CHOICES", {})
    @patch(
        "judgments.forms.search_forms.COURT_CHOICES",
        {"uksc": "Supreme Court", "Court of Appeal": {"ewca/crim": "Criminal Division", "ewca/civ": "civil Division"}},
    )
    def test_scope_choices_are_alphabetical_at_each_level(self):
        courts: list[Court] = [
            Mock(canonical_param="uksc"),
            Mock(canonical_param="ewca/crim"),
            Mock(canonical_param="ewca/civ"),
            Mock(canonical_param="ewcc"),
        ]
        courts[-1].name = "county Court"

        choices = _get_scope_choices(courts)

        self.assertEqual(list(choices), ["ewcc", "Court of Appeal", "uksc"])
        self.assertEqual(list(choices["Court of Appeal"]), ["ewca/civ", "ewca/crim"])

    def test_scopes_take_priority_over_individual_courts(self):
        form = AdvancedSearchForm(data={"scope": ["higher_courts", "other_courts"], "court": ["uksc"]})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["scope"], ["all_courts"])
        self.assertNotIn("court", form.cleaned_data)
        root = html.fromstring(str(form["court"]))
        self.assertEqual(root.xpath('//input[@name="scope"][@checked]/@value'), ["higher_courts", "other_courts"])

    def test_scope_normalisation(self):
        for scopes, expected in [
            (["higher_courts", "higher_courts"], ["higher_courts"]),
            (["other_courts"], ["other_courts"]),
            (["other_courts", "higher_courts"], ["all_courts"]),
            (["all_courts", "higher_courts"], ["all_courts"]),
        ]:
            with self.subTest(scopes=scopes):
                form = AdvancedSearchForm(data={"scope": scopes})
                self.assertTrue(form.is_valid())
                self.assertEqual(form.cleaned_data["scope"], expected)

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
        # Since this validation is done at a form level, rather than a field level,
        # the errors will be at the __all__ key.
        self.assertEqual(form.errors, {"__all__": ["Please enter a 'to' date after the 'from' date"]})

    def test_advanced_search_form_date_limit(self):
        """
        We have a hard limit on the minimum date allowed, ensure
        an error is raised if we try to submit a date before that!
        """
        data = {
            "from_date_0": "10",
            "from_date_1": "12",
            "from_date_2": "979",
            "to_date_0": "9",
            "to_date_1": "10",
            "to_date_2": "999",
        }
        expected_warning = f"Year must be after {settings.MINIMUM_ALLOWED_YEAR}"

        form = AdvancedSearchForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {"from_date": [expected_warning], "to_date": [expected_warning]},
        )

    def test_advanced_search_form_accepts_dummy_date(self):
        data = {
            "from_date_0": "1",
            "from_date_1": "1",
            "from_date_2": "1000",
            "to_date_0": "1",
            "to_date_1": "1",
            "to_date_2": "1000",
        }

        form = AdvancedSearchForm(data=data)

        self.assertTrue(form.is_valid())

    def test_order_valid_choice_accepted(self):
        form = AdvancedSearchForm(data={"order": "-date"})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["order"], "-date")

    def test_order_invalid_choice_rejected(self):
        form = AdvancedSearchForm(data={"order": "modified"})

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                "order": [
                    (
                        "Sort order should be one of relevance, -date, date, "
                        "-transformation, transformation, -updated, updated"
                    )
                ]
            },
        )

    def test_order_blank_treated_as_unset(self):
        form = AdvancedSearchForm(data={"order": ""})

        self.assertTrue(form.is_valid())
        self.assertNotIn("order", form.cleaned_data)

    def test_order_missing_treated_as_unset(self):
        form = AdvancedSearchForm(data={})

        self.assertTrue(form.is_valid())
        self.assertNotIn("order", form.cleaned_data)


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
