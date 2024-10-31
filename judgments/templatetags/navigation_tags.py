from django import template
from django.urls import resolve

register = template.Library()


@register.simple_tag(takes_context=True)
def navigation_item_class(context, path):
    request = context.get("request")

    if request and resolve(request.path_info).url_name == path:
        return "govuk-header__navigation-item govuk-header__navigation-item--active"

    return "govuk-header__navigation-item"
