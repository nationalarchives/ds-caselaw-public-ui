from django import template

register = template.Library()


def make_query_string(params):
    pairs = []
    for (key, value) in params.items():
        if isinstance(value, list):
            for value2 in value:
                pairs.append(f"{key}={value2}")
        elif value:
            pairs.append(f"{key}={value}")
        else:
            pairs.append(f"{key}=")
    return "&".join(pairs)


@register.filter
def remove_query(query_params, key):
    params = dict(query_params)
    params["page"] = None
    params[key] = None
    return make_query_string(params)


@register.filter
def remove_court(query_params, court):
    params = dict(query_params)
    params["page"] = None
    params["court"] = [court2 for court2 in params.get("court", []) if court != court2]
    return make_query_string(params)
