from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ValidateYearRange:
    def __init__(self, date_type):
        self.date_type = date_type

    def __call__(self, year):
        try:
            # Validate it is actually an integer first!
            year = int(year)
        except ValueError:
            raise ValidationError("Enter a valid year", code="__all__")
        if year < settings.MINIMUM_ALLOWED_YEAR:
            raise ValidationError(
                f"Year must be after {settings.MINIMUM_ALLOWED_YEAR}",
                code=f"{self.date_type}_date",
            )
