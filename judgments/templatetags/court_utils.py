import logging
from datetime import date

from caselawclient.client_helpers.search_helpers import (
    search_judgments_and_parse_response,
)
from caselawclient.search_parameters import SearchParameters
from django import template
from django.contrib.staticfiles import finders
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from ds_caselaw_utils.courts import CourtNotFoundException
from ds_caselaw_utils.courts import courts as all_courts
from markdown_it import MarkdownIt
from mdit_py_plugins.attrs import attrs_plugin

from judgments.models.court_dates import CourtDates
from judgments.utils import api_client
from ds_caselaw_utils.courts import Court
from typing import Optional

register = template.Library()


@register.filter
def get_court_name(court_param: str) -> str:
    try:
        court_object = all_courts.get_by_param(court_param)
        return court_object.name
    except CourtNotFoundException:
        pass
    try:
        court_object = all_courts.get_by_code(court_param)
        return court_object.name
    except CourtNotFoundException:
        return ""


@register.simple_tag
def get_first_judgment_year() -> int:
    if min_year := CourtDates.min_year():
        return min_year
    else:
        logging.warning("CourtDates table is empty! using fallback min_year.")
        return min(court.start_year for court in all_courts.get_selectable())


@register.simple_tag
def get_last_judgment_year() -> int:
    if max_year := CourtDates.max_year():
        return max_year
    else:
        logging.warning("CourtDates table is empty! using fallback max_year.")
        # The dates in all_courts don't work as a fallback, as they can't
        # be relied on to be up to date.
        return date.today().year


@register.filter
def get_court_date_range(court):
    try:
        court_dates = CourtDates.objects.get(pk=court)
        start_year = court_dates.start_year
        end_year = court_dates.end_year
    except CourtDates.DoesNotExist:
        start_year = all_courts.get_by_param(court).start_year
        end_year = all_courts.get_by_param(court).end_year
    if start_year == end_year:
        return str(start_year)
    else:
        return mark_safe("%s&nbsp;to&nbsp;%s" % (start_year, end_year))


@register.filter
def get_court_judgments_count(court: Court) -> str:
    return search_judgments_and_parse_response(api_client, SearchParameters(court=court.canonical_param)).total


@register.filter
def get_court_intro_text(court: Court) -> Optional[str]:
    def read_markdown(param: str) -> Optional[str]:
        filename = param.replace("/", "_")
        base_path = r"markdown/court_descriptions/{filename}.md"
        path = finders.find(base_path.format(filename=filename))
        md = MarkdownIt("commonmark", {"breaks": True, "html": True}).use(attrs_plugin)
        if path:
            with open(path) as file:
                return md.render(file.read())
        return None

    return read_markdown(court.canonical_param) or read_markdown("default")


@register.filter
def get_court_crest_path(court: Court) -> Optional[str]:
    param = court.canonical_param
    filename = param.replace("/", "_")
    base_path = r"images/court_crests/{filename}.{extension}"
    for extension in ["gif", "png", "jpg", "svg"]:
        path = base_path.format(filename=filename, extension=extension)
        if finders.find(path):
            return static(path)
    return None
