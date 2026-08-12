from caselawclient.client_helpers.search_helpers import (
    search_judgments_and_parse_response,
)
from caselawclient.search_parameters import SearchParameters
from django.utils.safestring import mark_safe
from ds_caselaw_utils.courts import Court, CourtNotFoundException, CourtParam
from ds_caselaw_utils.courts import courts as all_courts
from requests.exceptions import RequestException

from judgments.models.court_dates import CourtDates
from judgments.utils import api_client
from judgments.utils.timezones import london_today


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


def get_court_date_range(court_param: CourtParam) -> str:
    start_year: int | None
    end_year: int | None

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
        return mark_safe(f"{start_year}&nbsp;to&nbsp;{end_year}")  # noqa: S308 XSS [safe because years are numbers or None]


def get_court_start_year(court_param: CourtParam) -> int | None:
    try:
        court_dates = CourtDates.objects.get(pk=court_param)
        return court_dates.start_year
    except CourtDates.DoesNotExist:
        try:
            court = all_courts.get_by_param(court_param)
            return court.start_year
        except CourtNotFoundException:
            return None


def get_court_judgments_count(court: Court) -> int:
    try:
        return int(
            search_judgments_and_parse_response(api_client, SearchParameters(court=court.canonical_param)).total
        )  # TODO: This should really be an integer coming from the API Client
    except RequestException:
        return 0


def is_court_ended(court: Court) -> bool:
    current_year = london_today().year

    return court.end_year < current_year
