from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase

from judgments.forms.validators import ValidateYearRange


class TestValidators(TestCase):
    def test_validate_year_raises_error_non_integer(self):
        year = "a"
        validator = ValidateYearRange("from")

        with self.assertRaisesMessage(ValidationError, "Enter a valid year"):
            validator(year)

    def test_validate_year_raises_error_out_of_range(self):
        year = 1066

        validator = ValidateYearRange("from")

        with self.assertRaisesMessage(
            ValidationError, f"Year must be after {settings.MINIMUM_ALLOWED_YEAR}"
        ):
            validator(year)
