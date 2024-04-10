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
        "court",
        "from_day",
        "from_month",
        "from_year",
        "to_day",
        "to_month",
        "to_year",
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
    params[key] = None
    params[f"{key}_day"] = None
    params[f"{key}_month"] = None
    params[f"{key}_year"] = None
    return make_query_string(params)


@register.filter
def remove_court(query_params, court):
    params = dict(query_params)
    params["page"] = None
    params["court"] = [court2 for court2 in params.get("court", []) if court != court2]
    return make_query_string(params)


@register.filter
def replace_year_in_query(query_params, year):
    params = dict(query_params)
    del params["from"]
    del params["from_day"]
    del params["from_month"]
    del params["to"]
    del params["to_day"]
    del params["to_month"]
    params["from_year"] = year
    params["to_year"] = year
    return make_query_string(params)
