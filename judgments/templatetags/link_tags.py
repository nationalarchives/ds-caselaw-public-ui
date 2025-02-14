import re

from django import template

register = template.Library()

BASE_TRACKING_CLASS = "analytics"


def trackable_class_name(text):
    context_class = re.sub(r"\s+", "-", text.strip().lower())

    return f"{BASE_TRACKING_CLASS}-{re.sub(r'[^a-z0-9-]', '', context_class)}"


@register.inclusion_tag("tags/trackable_link.html")
def trackable_link(text, **attrs):
    class_name = trackable_class_name(text)

    return {"text": text, "attrs": attrs, "class_name": class_name}
