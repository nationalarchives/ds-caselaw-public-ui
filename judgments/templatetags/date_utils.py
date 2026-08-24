from datetime import datetime

from judgments.utils.timezones import LONDON


def formatdate(value, format="%d %b %Y"):
    if value is None:
        return ""
    # Aware datetimes are shown in Europe/London; date-only values are calendar days.
    if isinstance(value, datetime) and value.tzinfo is not None:
        value = value.astimezone(LONDON)
    return value.strftime(format)
