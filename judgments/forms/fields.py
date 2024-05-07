from calendar import monthrange
from datetime import date
from typing import Literal

from crispy_forms_gds.fields import DateInputField


class DateRangeInputField(DateInputField):
    """
    A custom version of the gds DateInputField which fixes the issue
    preventing us from not requiring all fields to be populated.

    The expected use case for this is to have two of these fields on a given
    form, one being date from and one being date to.

    If a day or month is not provided, default to the minimum or maximum
    date value depending on whether it is to/from.

    e.g. - value of only year provided as from 2010, default to 01/01/2010
         - value of only year provided as to 2010, default to 31/12/2010
         - value of year and month provded as to 02/2010, default to 28/02/2010
    """

    DateType = Literal["from", "to"]

    date_type: DateType

    def __init__(self, date_type, **kwargs):
        self.date_type = date_type
        super().__init__(**kwargs)

    def compress(self, data_list):
        """
        Convert the values entered into the fields as a ``date``.

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
        return date(day=day, month=month, year=year)
