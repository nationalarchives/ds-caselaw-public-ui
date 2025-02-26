from django import template
from django.utils.text import slugify

register = template.Library()

BASE_TRACKING_CLASS = "analytics"


def trackable_class_name(text):
    return f"{BASE_TRACKING_CLASS}-{slugify(text)}"


@register.inclusion_tag("analytics/trackable_link.html")
def trackable_link(text, **attrs):
    class_name = trackable_class_name(text)

    return {"text": text, "attrs": attrs, "class_name": class_name}
