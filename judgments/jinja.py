from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment, select_autoescape


def environment(**options):
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
            "static": staticfiles_storage.url,
            "url": reverse,
        }
    )
    return env
