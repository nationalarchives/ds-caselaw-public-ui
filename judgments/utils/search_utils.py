import datetime

from django.conf import settings
from ds_caselaw_utils import courts as all_courts

from judgments.models.court_dates import CourtDates

ALL_COURT_CODES = [court.code for court in all_courts.get_all()]

ALL_LISTABLE_COURT_NAMES = [court.name for court in all_courts.get_listable_courts()]
ALL_LISTABLE_TRIBUNAL_NAMES = [tribunal.name for tribunal in all_courts.get_listable_tribunals()]


def _valid_years():
    """
    Generate a list of valid years as strings.
    """
    today = datetime.date.today()
    valid_years = range(2003, today.year)
    return [f"{year}" for year in valid_years]


def _get_value_as_number(dict_item):
    """
    Given a single facet dictionary {"court_name": "12"},
    return the value as an integer.
    """
    return int(dict_item[1])


def _sort_by_number_in_value(unsorted_dict: dict):
    """
    Sorts a dictionary by value where
    the values contain numbers as strings
    """
    sorted_items = sorted(unsorted_dict.items(), key=_get_value_as_number, reverse=True)
    return dict(sorted_items)


def process_court_facets(facets: dict, current_courts: dict = {}):
    """
    Separates facets dict into non-court facets,
    and court facets.
    """
    court_facets = {
        all_courts.get_by_code(facet_key): facet_value
        for facet_key, facet_value in facets.items()
        if facet_key in ALL_COURT_CODES
        and facet_key not in current_courts
        and all_courts.get_by_code(facet_key).name in ALL_LISTABLE_COURT_NAMES
    }
    tribunal_facets = {
        all_courts.get_by_code(facet_key): facet_value
        for facet_key, facet_value in facets.items()
        if facet_key in ALL_COURT_CODES
        and facet_key not in current_courts
        and all_courts.get_by_code(facet_key).name in ALL_LISTABLE_TRIBUNAL_NAMES
    }
    unprocessed_facets = {
        facet_key: facet_value for facet_key, facet_value in facets.items() if facet_key not in ALL_COURT_CODES
    }

    sorted_court_facets = _sort_by_number_in_value(court_facets)
    sorted_tribunal_facets = _sort_by_number_in_value(tribunal_facets)

    return unprocessed_facets, sorted_court_facets, sorted_tribunal_facets


def process_year_facets(facets: dict):
    """
    Separates facets dict into non-year facets,
    and year facets
    """
    year_facets = {facet_key: facet_value for facet_key, facet_value in facets.items() if facet_key in _valid_years()}
    unprocessed_facets = {
        facet_key: facet_value for facet_key, facet_value in facets.items() if facet_key not in _valid_years()
    }

    return unprocessed_facets, year_facets


def get_minimum_valid_year():
    """
    As `CourtDates.min_year()` would return None if the model is not populated,
    return a sensible default instead.
    """
    return CourtDates.min_year() or settings.MINIMUM_WARNING_YEAR
