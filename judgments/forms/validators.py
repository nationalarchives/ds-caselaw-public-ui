from datetime import date

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from judgments.utils import get_minimum_valid_year


def validate_year_is_within_sensible_range(year):
    try:
        # Validate it is actually a valid integer first!
        year = int(year)
    except ValueError:
        raise ValidationError("Enter a valid year", code="to_date")
    if year < get_minimum_valid_year() or year > date.today().year:
        raise ValidationError(
            f"Year must be between {get_minimum_valid_year()} and {date.today().year}",
            code="to_date",
        )
