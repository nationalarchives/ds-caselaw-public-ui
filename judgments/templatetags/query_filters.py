from django import template

register = template.Library()


@register.filter
def remove_query(query_params, key):
    params = dict(query_params)
    params[key] = None
    return "&".join([f'{key}={params[key] or ""}' for key in params])


@register.filter
def remove_query_key(query_params, key):
    params = dict(query_params)
    params.pop(key)
    return "&".join([f'{key}={params[key] or ""}' for key in params])
