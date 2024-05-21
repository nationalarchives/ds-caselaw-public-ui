import calendar

from django import template

register = template.Library()


@register.filter
def make_query_string(params):
    pairs = []
    for key, value in params.items():
        if isinstance(value, list):
            for value2 in value:
                pairs.append(f"{key}={value2}")
        elif value:
            pairs.append(f"{key}={value}")
        else:
            pairs.append(f"{key}=")
    return "&".join(pairs)


@register.filter
def removable_filter_param(key):
    # This method identifies the parameters in the search which are *removable*
    # in the UI on the search results page. This includes things like court,
    # party, query, but excludes for instance pagination, feature flags, and
    # the individual components of a date, which are presented jointly in the UI.
    excluded = [
        "order",
        "per_page",
        "page",
        "court",
        "tribunal",
        "from_date_0",
        "from_date_1",
        "from_date_2",
        "to_date_0",
        "to_date_1",
        "to_date_2",
    ]
    return key not in excluded


def date_filter_param(key):
    included = ["from", "to"]
    return key in included


@register.filter
def remove_query(query_params, key):
    if date_filter_param(key):
        return remove_date(query_params, key)
    else:
        params = dict(query_params)
        params["page"] = None
        params[key] = None
        return make_query_string(params)


def remove_date(query_params, key):
    params = dict(query_params)
    params["page"] = None
    del params[f"{key}_date_0"]
    del params[f"{key}_date_1"]
    del params[f"{key}_date_2"]
    return make_query_string(params)


@register.filter
def remove_court(query_params, court):
    params = dict(query_params)
    params["page"] = None
    params["court"] = [court2 for court2 in params.get("court", []) if court != court2]
    params["tribunal"] = [
        court2 for court2 in params.get("tribunal", []) if court != court2
    ]
    return make_query_string(params)


@register.filter
def replace_year_in_query(query_params, year):
    params = dict(query_params)
    params.pop("from_date_0", None)
    params.pop("from_date_1", None)
    params.pop("to_date_0", None)
    params.pop("to_date_1", None)
    params["from_date_2"] = year
    params["to_date_2"] = year
    return make_query_string(params)


@register.filter
def replace_integer_with_day(day):
    if day < 10:
        return f"0{day}"
    return str(day)


@register.filter
def replace_integer_with_month(month):
    return calendar.month_name[month][0:3]
