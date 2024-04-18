from calendar import monthrange
import datetime

from ds_caselaw_utils import courts as all_courts

from judgments.models.court_dates import CourtDates

ALL_COURT_CODES = [court.code for court in all_courts.get_all()]


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
        if facet_key in ALL_COURT_CODES and facet_key not in current_courts
    }
    unprocessed_facets = {
        facet_key: facet_value
        for facet_key, facet_value in facets.items()
        if facet_key not in ALL_COURT_CODES
    }

    return unprocessed_facets, _sort_by_number_in_value(court_facets)


def process_year_facets(facets: dict):
    """
    Separates facets dict into non-year facets,
    and year facets
    """
    year_facets = {
        facet_key: facet_value
        for facet_key, facet_value in facets.items()
        if facet_key in _valid_years()
    }
    unprocessed_facets = {
        facet_key: facet_value
        for facet_key, facet_value in facets.items()
        if facet_key not in _valid_years()
    }

    return unprocessed_facets, year_facets

def _parameter_provided(params, parameter_name):
    value = params.get(parameter_name)
    return value and len(value)


def _parse_parameter_as_int(params, parameter_name, default=None):
    if _parameter_provided(params, parameter_name):
        return int(params.get(parameter_name))
    else:
        return default

def parse_date_parameter(
    params, param_name, default_to_last=False,
):
    year_param_name = f"{param_name}_year"
    month_param_name = f"{param_name}_month"
    day_param_name = f"{param_name}_day"

    start_year = CourtDates.min_year()
    end_year = CourtDates.max_year()

    parser_errors = {}

    if _parameter_provided(params, param_name):
        # TODO: Verify that this definitely cannot fail!!!
        return datetime.strptime(params[param_name], "%Y-%m-%d").date(), {}

    elif _parameter_provided(params, year_param_name):
        year = _parse_parameter_as_int(params, year_param_name)

        if start_year and year < start_year:
            year = start_year
            parser_errors[year_param_name] = "This is a date before the start year"

        if end_year and year > end_year:
            year = end_year
            parser_errors[year_param_name] = "This is a date before the current year"

        default_month = 12 if default_to_last else 1
        month = _parse_parameter_as_int(params, month_param_name, default=default_month)

        if month > 12:
            month = 12
            parser_errors[month_param_name] = "This is a month greater than 12"
        if month < 1:
            month = 1
            parser_errors[month_param_name] = "This is a month less than 1"

        default_day = monthrange(year, month)[1] if default_to_last else 1
        day = _parse_parameter_as_int(params, day_param_name, default=default_day)

        if day > 31:
            day = 31
            parser_errors[day_param_name] = "This is a day greater than 31"
        if day < 1:
            day = 1
            parser_errors[day_param_name] = "This is a day less than 1"

        return (datetime.date(year, month, day), parser_errors)
    elif _parameter_provided(params, month_param_name) and _parameter_provided(
        params, day_param_name
    ):
        if param_name == "to_year":
            year = end_year
        else:
            year = start_year
        return datetime.date(year), parser_errors
