import logging
from datetime import date
from typing import Optional

from caselawclient.client_helpers.search_helpers import (
    search_judgments_and_parse_response,
)
from caselawclient.search_parameters import SearchParameters
from django import template
from django.utils.safestring import mark_safe
from ds_caselaw_utils.courts import Court, CourtNotFoundException, CourtParam
from ds_caselaw_utils.courts import courts as all_courts

from judgments.models.court_dates import CourtDates
from judgments.utils import api_client

register = template.Library()


@register.filter
def get_court_name(court):
    try:
        court_object = all_courts.get_by_param(court)
        return court_object.name
    except CourtNotFoundException:
        pass
    try:
        court_object = all_courts.get_by_code(court)
        return court_object.name
    except CourtNotFoundException:
        return ""


@register.simple_tag
def get_first_judgment_year():
    if min_year := CourtDates.min_year():
        return min_year
    else:
        logging.warning("CourtDates table is empty! using fallback min_year.")
        return min(court.start_year for court in all_courts.get_selectable() if court.start_year)


@register.simple_tag
def get_last_judgment_year() -> int:
    if max_year := CourtDates.max_year():
        return max_year
    else:
        logging.warning("CourtDates table is empty! using fallback max_year.")
        # The dates in all_courts don't work as a fallback, as they can't
        # be relied on to be up to date.
        return date.today().year


@register.filter
def get_court_date_range(court_param: CourtParam) -> str:
    start_year: Optional[int]
    end_year: Optional[int]

    try:
        court_dates = CourtDates.objects.get(pk=court_param)
        start_year = court_dates.start_year
        end_year = court_dates.end_year
    except CourtDates.DoesNotExist:
        court = all_courts.get_by_param(court_param)
        start_year = court.start_year
        end_year = court.end_year
    if start_year == end_year:
        return str(start_year)
    else:
        return mark_safe("%s&nbsp;to&nbsp;%s" % (start_year, end_year))


@register.filter
def get_court_judgments_count(court: Court) -> int:
    return int(
        search_judgments_and_parse_response(api_client, SearchParameters(court=court.canonical_param)).total
    )  # TODO: This should really be an integer coming from the API Client
