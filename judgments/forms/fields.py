from calendar import monthrange
from datetime import date
from typing import Literal

from crispy_forms_gds.fields import DateInputField
from django import forms
from django.core.validators import RegexValidator

from .validators import ValidateYearRange


class DateRangeInputField(DateInputField):
    """
    A custom version of the gds DateInputField which fixes the issue
    preventing some of the sub-fields being set as not required.

    The expected use case for this is to have two of these fields on a given
    form, one being date from and one being date to.

    If a day or month is not provided, default to the minimum or maximum
    date value depending on whether it is to/from.

    If year is missing raise a validation error.

    e.g. - value of only year provided as from 2010, default to 01/01/2010
         - value of only year provided as to 2010, default to 31/12/2010
         - value of year and month provded as to 02/2010, default to 28/02/2010
    """

    DateType = Literal["from", "to"]

    date_type: DateType

    def __init__(self, date_type, **kwargs):
        self.date_type = date_type
        fields = (
            forms.CharField(
                label="Day",
                validators=[RegexValidator(r"^[0-9]+$", "Enter a valid date")],
                required=False,
            ),
            forms.CharField(
                label="Month",
                validators=[RegexValidator(r"^[0-9]+$", "Enter a valid month")],
                required=False,
            ),
            forms.CharField(
                label="Year",
                error_messages={"incomplete": "You must specify a year"},
                validators=[ValidateYearRange(self.date_type)],
                required=True,
            ),
        )
        forms.MultiValueField.__init__(self, fields=fields, **kwargs)

    def compress(self, data_list):
        """
        Convert the values entered into the fields as a ``date``.
        * Return None if year is not provided, raising an error in validation.
        * Default to beginning or end of month if day is not provided depending on
            whether this is a from or to field.
        * Default to the minimum or maximum month depending on whether this is a
            from or a to respectively
        * Default to the minimum month and day if only year is provided and this is a from date,
            and vice-versa for a to date

        Args:
            data_list (tuple): a 3-tuple the of values entered into the fields.

        Returns:
            the ``date`` for the values entered in the day, month and year fields.
                If any of the field are blank then None is returned.

        """
        day, month, year = [int(value) if value else None for value in data_list]
        if not year:
            return None
        if self.date_type == "from":
            if not month:
                month = 1
            if not day:
                day = 1
        if self.date_type == "to":
            if not month:
                month = 12
            if not day:
                day = monthrange(year, month)[1]
        return date(year=year, month=month, day=day)  # type: ignore
