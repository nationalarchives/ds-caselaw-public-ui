from django import template
from django.template import TemplateDoesNotExist
from django.template.loader import get_template

register = template.Library()


@register.simple_tag
def template_exists(template_name: str) -> bool:
    try:
        get_template(template_name, using="jinja")
        return True
    except TemplateDoesNotExist:
        return False
