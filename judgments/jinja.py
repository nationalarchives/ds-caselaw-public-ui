from crispy_forms.templatetags.crispy_forms_filters import as_crispy_form
from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.l10n import unlocalize
from django.utils.html import json_script
from django.utils.text import slugify
from jinja2 import (
    ChoiceLoader,
    Environment,
    PackageLoader,
    PrefixLoader,
    select_autoescape,
)

from judgments.jinja_helpers import jinja_url, with_context
from judgments.templatetags import (
    component_utils,
    court_utils,
    date_utils,
    document_utils,
    errors,
    link_tags,
    query_filters,
    search_results_filters,
    template_utils,
    text_utils,
)
from transactional_licence_form.templatetags import transactional_licence_utils


def build_loader(base_loader):
    govuk_loader = PrefixLoader(
        {
            "govuk_frontend_jinja": PackageLoader("govuk_frontend_jinja"),
        }
    )

    tna_loader = PackageLoader("tna_frontend_jinja")

    loaders = []

    if base_loader:
        loaders.append(base_loader)

    loaders.extend([govuk_loader, tna_loader])

    return ChoiceLoader(loaders)


def build_environment(options):
    options = dict(options)
    options["loader"] = build_loader(options.get("loader"))
    options.pop("autoescape", None)

    return Environment(
        autoescape=select_autoescape(
            enabled_extensions=("jinja"),
            default_for_string=True,
            default=True,
        ),
        **options,
    )


def get_globals():
    return {
        "static": staticfiles_storage.url,
        "trackable_link": with_context(link_tags.trackable_link),
        "trackable_class_name": link_tags.trackable_class_name,
        "formatdate": date_utils.formatdate,
        "url": jinja_url,
        "formatted_document_uri": document_utils.formatted_document_uri,
        "crispy": as_crispy_form,
        "unlocalize": unlocalize,
        "has_other_field": transactional_licence_utils.has_other_field,
        "template_exists": template_utils.template_exists,
        "get_subwidget_for_other_field": transactional_licence_utils.get_subwidget_for_other_field,
        "mailto_with_subject_href": transactional_licence_utils.mailto_with_subject_href,
        "component_class_names": component_utils.component_class_names,
    }


def get_filters():
    return {
        "error_messages": errors.error_messages,
        "get_court_judgments_count": court_utils.get_court_judgments_count,
        "intcomma": intcomma,
        "slugify": slugify,
        "show_matches": search_results_filters.show_matches,
        "remove_query": query_filters.remove_query,
        "remove_court": query_filters.remove_court,
        "replace_integer_with_day": query_filters.replace_integer_with_day,
        "replace_integer_with_month": query_filters.replace_integer_with_month,
        "get_court_name": court_utils.get_court_name,
        "removable_filter_param": query_filters.removable_filter_param,
        "capfirst": text_utils.capfirst,
        "submit_label_for_step": transactional_licence_utils.submit_label_for_step,
        "get_form": transactional_licence_utils.get_form,
        "get_field_name": transactional_licence_utils.get_field_name,
        "format_value_for_review": transactional_licence_utils.format_value_for_review,
        "get_title_to_display_in_html": document_utils.get_title_to_display_in_html,
        "get_court_date_range": court_utils.get_court_date_range,
        "get_court_start_year": court_utils.get_court_start_year,
        "hyphenate": text_utils.hyphenate,
        "is_court_ended": court_utils.is_court_ended,
        "json_script": json_script,
    }


def register_globals(env):
    env.globals.update(get_globals())


def register_filters(env):
    env.filters.update(get_filters())


def environment(**options):
    env = build_environment(options)
    register_globals(env)
    register_filters(env)
    return env
