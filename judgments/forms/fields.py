from calendar import monthrange
from datetime import date

from crispy_forms_gds.fields import DateInputField


class DateRangeInputField(DateInputField):
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
        if self.label == "From Date":
            if not month:
                month = 1
            if not day:
                day = 1
        if self.label == "To Date":
            if not month:
                month = 12
            if not day:
                day = monthrange(year, month)[1]
        return date(day=day, month=month, year=year)
