import re
from functools import wraps

from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment

from judgments.templatetags import link_tags, navigation_tags


def spaceless(value):
    """Remove whitespace between HTML tags."""
    return re.sub(r">\s+<", "><", value.strip())


def with_context(fn):
    """
    Wraps a Django template tag function that takes context, so it works in Jinja.
    Assumes `request` is in the Jinja template globals.
    """

    @wraps(fn)
    def wrapped(request, *args, **kwargs):
        context = {"request": request}
        return fn(context, *args, **kwargs)

    return wrapped


def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "static": staticfiles_storage.url,
            "url": reverse,
            "navigation_item_class": with_context(navigation_tags.navigation_item_class),
            "trackable_link": with_context(link_tags.trackable_link),
            "waffle_flags": [],  # TODO change how we use waffle flags
        }
    )
    env.filters["spaceless"] = spaceless
    return env
