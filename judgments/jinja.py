from functools import wraps

from crispy_forms.templatetags.crispy_forms_filters import as_crispy_form
from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from django.utils.text import slugify

# from django.middleware.csrf import get_token
from jinja2 import (
    ChoiceLoader,
    Environment,
    PackageLoader,
    PrefixLoader,
    select_autoescape,
)

from judgments.templatetags import (
    court_utils,
    document_utils,
    link_tags,
    navigation_tags,
    query_filters,
    search_results_filters,
)
from transactional_licence_form.templatetags import transactional_licence_utils


def capfirst(value):
    if not value:
        return value
    return value[0].upper() + value[1:]


def formatdate(value, format="%d %b %Y"):
    if value is None:
        return ""
    return value.strftime(format)


def jinja_url(name, *args, **kwargs):
    return reverse(name, args=args or None, kwargs=kwargs or None)


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
            "formatdate": formatdate,
            "url": jinja_url,
            "formatted_document_uri": document_utils.formatted_document_uri,
            "crispy": as_crispy_form,
        }
    )
    env.filters["get_court_judgments_count"] = court_utils.get_court_judgments_count
    env.filters["intcomma"] = intcomma
    env.filters["slugify"] = slugify
    env.filters["show_matches"] = search_results_filters.show_matches
    env.filters["is_exact_ncn_match"] = search_results_filters.is_exact_ncn_match
    env.filters["is_exact_title_match"] = search_results_filters.is_exact_title_match
    env.filters["is_exact_match"] = search_results_filters.is_exact_match
    env.filters["remove_query"] = query_filters.remove_query
    env.filters["remove_court"] = query_filters.remove_court
    env.filters["get_court_name"] = court_utils.get_court_name
    env.filters["removable_filter_param"] = query_filters.removable_filter_param
    env.filters["capfirst"] = capfirst
    env.filters["submit_label_for_step"] = transactional_licence_utils.submit_label_for_step
    env.filters["get_form"] = transactional_licence_utils.get_form
    env.filters["get_field_name"] = transactional_licence_utils.get_field_name
    env.filters["format_value_for_review"] = transactional_licence_utils.format_value_for_review
    env.filters["get_title_to_display_in_html"] = document_utils.get_title_to_display_in_html
    env.filters["get_court_date_range"] = court_utils.get_court_date_range
    return env
