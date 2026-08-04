from datetime import date, datetime
from unittest.mock import Mock

import pytest
from django.conf import settings
from django.test import SimpleTestCase

from judgments.feeds import JudgmentsFeed
from judgments.jinja import formatdate
from judgments.utils.timezones import LONDON, UTC, as_utc_datetime, london_today, utc_now

# UK DST transitions in 2025:
# - clocks go forward 2025-03-30 01:00 GMT -> 02:00 BST
# - clocks go back   2025-10-26 02:00 BST -> 01:00 GMT


def test_django_keeps_storage_utc_and_presents_london():
    assert settings.USE_TZ is True
    assert settings.TIME_ZONE == "Europe/London"


def test_utc_now_is_timezone_aware_utc():
    now = utc_now()
    assert now.tzinfo is not None
    assert now.utcoffset() == UTC.utcoffset(None)


def test_london_today_returns_date():
    assert isinstance(london_today(), date)


def test_as_utc_datetime_parses_offset_string():
    result = as_utc_datetime("2025-01-01 01:23:00+00:00")
    assert result == datetime(2025, 1, 1, 1, 23, tzinfo=UTC)


def test_as_utc_datetime_parses_zulu_string():
    result = as_utc_datetime("2025-01-01T01:23:00Z")
    assert result == datetime(2025, 1, 1, 1, 23, tzinfo=UTC)


def test_as_utc_datetime_treats_naive_as_utc():
    result = as_utc_datetime(datetime(2025, 1, 1, 12, 0, 0))  # noqa: DTZ001
    assert result == datetime(2025, 1, 1, 12, 0, 0, tzinfo=UTC)


def test_as_utc_datetime_converts_london_to_utc_in_bst():
    # BST: 2025-07-01 13:00 London == 12:00 UTC
    result = as_utc_datetime(datetime(2025, 7, 1, 13, 0, 0, tzinfo=LONDON))
    assert result == datetime(2025, 7, 1, 12, 0, 0, tzinfo=UTC)


def test_as_utc_datetime_converts_london_to_utc_in_gmt():
    # Winter: London == UTC
    result = as_utc_datetime(datetime(2025, 1, 15, 13, 0, 0, tzinfo=LONDON))
    assert result == datetime(2025, 1, 15, 13, 0, 0, tzinfo=UTC)


def test_as_utc_datetime_across_spring_forward():
    # After the gap: 02:30 BST on spring-forward day is 01:30 UTC
    result = as_utc_datetime(datetime(2025, 3, 30, 2, 30, 0, tzinfo=LONDON))
    assert result == datetime(2025, 3, 30, 1, 30, 0, tzinfo=UTC)
    assert result.utcoffset() == UTC.utcoffset(None)


def test_as_utc_datetime_across_fall_back():
    # First 01:30 (BST, fold=0) is 00:30 UTC; second 01:30 (GMT, fold=1) is 01:30 UTC
    bst_occurrence = datetime(2025, 10, 26, 1, 30, 0, tzinfo=LONDON, fold=0)
    gmt_occurrence = datetime(2025, 10, 26, 1, 30, 0, tzinfo=LONDON, fold=1)

    assert as_utc_datetime(bst_occurrence) == datetime(2025, 10, 26, 0, 30, 0, tzinfo=UTC)
    assert as_utc_datetime(gmt_occurrence) == datetime(2025, 10, 26, 1, 30, 0, tzinfo=UTC)


def test_storage_calendar_date_stays_utc_when_london_is_next_day():
    """During BST, late UTC evening is already the next calendar day in London."""
    utc_instant = datetime(2025, 7, 1, 23, 30, 0, tzinfo=UTC)

    assert utc_instant.date() == date(2025, 7, 1)
    assert utc_instant.astimezone(LONDON).date() == date(2025, 7, 2)
    # Sitemap lastmod / API storage date must follow UTC, not London presentation
    assert as_utc_datetime(utc_instant).date() == date(2025, 7, 1)
    assert as_utc_datetime(utc_instant.isoformat()).date() == date(2025, 7, 1)


def test_formatdate_shows_london_calendar_day_for_aware_utc_datetime():
    # 23:30 UTC on 1 Jul is already 2 Jul in London (BST)
    utc_instant = datetime(2025, 7, 1, 23, 30, 0, tzinfo=UTC)
    assert formatdate(utc_instant) == "02 Jul 2025"
    assert formatdate(utc_instant, "%Y-%m-%d %H:%M") == "2025-07-02 00:30"


def test_formatdate_winter_matches_utc_clock():
    utc_instant = datetime(2025, 1, 15, 14, 0, 0, tzinfo=UTC)
    assert formatdate(utc_instant, "%Y-%m-%d %H:%M") == "2025-01-15 14:00"


def test_formatdate_leaves_naive_date_unchanged():
    assert formatdate(date(2025, 7, 1)) == "01 Jul 2025"


def test_formatdate_across_spring_forward_gap():
    # 01:30 UTC on spring-forward morning displays as 02:30 BST in London
    utc_instant = datetime(2025, 3, 30, 1, 30, 0, tzinfo=UTC)
    assert formatdate(utc_instant, "%Y-%m-%d %H:%M %Z") == "2025-03-30 02:30 BST"


class TestFeedTimestampsRemainUtc(SimpleTestCase):
    def setUp(self):
        self.feed = JudgmentsFeed()

    def test_item_updateddate_returns_aware_utc(self):
        item = Mock(transformation_date="2025-07-01 23:30:00+00:00")
        result = self.feed.item_updateddate(item)

        assert result == datetime(2025, 7, 1, 23, 30, 0, tzinfo=UTC)
        assert result.utcoffset() == UTC.utcoffset(None)
        # Must not silently shift to London for the Atom wire format
        assert result.isoformat() == "2025-07-01T23:30:00+00:00"

    def test_item_updateddate_parses_client_factory_style_string(self):
        item = Mock(transformation_date="2023-02-03 12:34:00+00:00")
        result = self.feed.item_updateddate(item)
        assert result == datetime(2023, 2, 3, 12, 34, 0, tzinfo=UTC)

    def test_item_pubdate_normalises_aware_client_datetime_to_utc(self):
        # Client may hand back an aware UTC datetime (factory default)
        item = Mock(date=datetime(2023, 2, 3, 0, 0, 0, tzinfo=UTC))
        result = self.feed.item_pubdate(item)
        assert result == datetime(2023, 2, 3, 0, 0, 0, tzinfo=UTC)
        assert result.utcoffset() == UTC.utcoffset(None)

    def test_item_pubdate_treats_naive_client_datetime_as_utc(self):
        # SearchResult.date can still be naive when MarkLogic omits an offset
        item = Mock(date=datetime(2023, 2, 3, 0, 0, 0))  # noqa: DTZ001
        result = self.feed.item_pubdate(item)
        assert result == datetime(2023, 2, 3, 0, 0, 0, tzinfo=UTC)

    def test_item_pubdate_none(self):
        assert self.feed.item_pubdate(Mock(date=None)) is None


@pytest.mark.parametrize(
    ("london_local", "expected_utc"),
    [
        # Immediately before spring forward (still GMT)
        (datetime(2025, 3, 30, 0, 30, 0, tzinfo=LONDON), datetime(2025, 3, 30, 0, 30, 0, tzinfo=UTC)),
        # Immediately after spring forward (BST)
        (datetime(2025, 3, 30, 2, 30, 0, tzinfo=LONDON), datetime(2025, 3, 30, 1, 30, 0, tzinfo=UTC)),
        # Midsummer BST
        (datetime(2025, 7, 1, 12, 0, 0, tzinfo=LONDON), datetime(2025, 7, 1, 11, 0, 0, tzinfo=UTC)),
        # Midwinter GMT
        (datetime(2025, 1, 15, 12, 0, 0, tzinfo=LONDON), datetime(2025, 1, 15, 12, 0, 0, tzinfo=UTC)),
    ],
)
def test_round_trip_london_local_to_utc_storage(london_local, expected_utc):
    stored = as_utc_datetime(london_local)
    assert stored == expected_utc
    assert stored.tzinfo == UTC or stored.utcoffset() == UTC.utcoffset(None)
    # Presentation must be able to recover the London wall clock
    assert stored.astimezone(LONDON).strftime("%Y-%m-%d %H:%M") == london_local.strftime("%Y-%m-%d %H:%M")
