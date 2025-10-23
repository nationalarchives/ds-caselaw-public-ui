from functools import wraps

from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import (
    ChoiceLoader,
    Environment,
    PackageLoader,
    PrefixLoader,
    select_autoescape,
)

from judgments.templatetags import link_tags, navigation_tags


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
    base_loader = options.get("loader")
    govuk_loader = PrefixLoader(
        {
            "govuk_frontend_jinja": PackageLoader("govuk_frontend_jinja"),
        }
    )

    combined_loader = ChoiceLoader([base_loader, govuk_loader]) if base_loader else govuk_loader

    options["loader"] = combined_loader

    options.pop("autoescape", None)
    env = Environment(
        autoescape=select_autoescape(
            enabled_extensions=("jinja"),
            default_for_string=True,
            default=True,
        ),
        **options,
    )
    env.globals.update(
        {
            "navigation_item_class": with_context(navigation_tags.navigation_item_class),
            "static": staticfiles_storage.url,
            "trackable_link": with_context(link_tags.trackable_link),
            "url": reverse,
        }
    )
    return env
