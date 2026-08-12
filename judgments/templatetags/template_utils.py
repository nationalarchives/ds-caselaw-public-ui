from django.template import TemplateDoesNotExist
from django.template.loader import get_template


def template_exists(template_name: str) -> bool:
    try:
        get_template(template_name, using="jinja")
        return True
    except TemplateDoesNotExist:
        return False
