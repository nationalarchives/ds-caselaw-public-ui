from django import template

register = template.Library()


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
        "text_date_input",
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
