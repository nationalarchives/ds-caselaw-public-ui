from datetime import datetime

from judgments.templatetags.date_utils import formatdate
from judgments.utils.timezones import UTC


def test_formatdate_formats_value_with_default_format():
    result = formatdate(datetime(2025, 1, 15, 14, 0, 0, tzinfo=UTC))

    assert result == "15 Jan 2025"
