import os

from django.conf import settings
from django.views.generic.base import TemplateView


def get_attr(object, attribute):
    try:
        return getattr(object, attribute)
    except AttributeError:
        return f"NOPE, nothing named {attribute} on {object}"


class DragonDebugView(TemplateView):
    template_name = "dragondebug.html"

    def get_context_data(self, **kwargs):
        return {
            "DJANGO_SETTINGS_MODULE": os.environ.get("DJANGO_SETTINGS_MODULE"),
            "WAFFLE_OVERRIDE": get_attr(settings, "WAFFLE_OVERRIDE"),
        }
