from urllib.parse import quote_plus

from django import template

register = template.Library()


@register.filter
def urlencode(string):
    return quote_plus(string)


@register.filter
def interpolate(template, values):
    return template % values
