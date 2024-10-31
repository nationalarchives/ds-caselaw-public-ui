from django import template
from django.urls import Resolver404, resolve

register = template.Library()


@register.simple_tag(takes_context=True)
def navigation_item_class(context, path):
    request = context.get("request")

    if request:
        try:
            request_path = resolve(request.path_info).url_name
        except Resolver404:
            request_path = None

        if request and request_path and request_path == path:
            return "govuk-header__navigation-item govuk-header__navigation-item--active"

    return "govuk-header__navigation-item"
