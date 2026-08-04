"""Timezone helpers: UTC for storage/interchange, Europe/London for presentation."""

from __future__ import annotations

from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo

LONDON = ZoneInfo("Europe/London")
UTC = timezone.utc


def utc_now() -> datetime:
    return datetime.now(tz=UTC)


def london_today() -> date:
    """UK calendar date (Europe/London), including BST when in effect."""
    return datetime.now(tz=LONDON).date()


def as_utc_datetime(value: datetime | str) -> datetime:
    """
    Normalise a datetime or ISO-8601 string to timezone-aware UTC.

    Naive datetimes/strings are treated as UTC (storage-layer contract).
    """
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)
