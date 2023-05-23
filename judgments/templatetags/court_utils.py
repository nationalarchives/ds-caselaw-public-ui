import logging
from datetime import date

from django import template
from django.utils.safestring import mark_safe
from ds_caselaw_utils.courts import CourtNotFoundException
from ds_caselaw_utils.courts import courts as all_courts

from judgments.models import CourtDates

register = template.Library()


@register.filter
def get_court_name(court):
    try:
        court_object = all_courts.get_by_param(court)
    except CourtNotFoundException:
        return ""
    return court_object.name


@register.simple_tag
def get_first_judgment_year():
    if min_year := CourtDates.min_year():
        return min_year
    else:
        logging.warning("CourtDates table is empty! using fallback min_year.")
        return min(court.start_year for court in all_courts.get_selectable())


@register.simple_tag
def get_last_judgment_year():
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
        court_dates = CourtDates.objects.get(pk=court.canonical_param)
        start_year = court_dates.start_year
        end_year = court_dates.end_year
    except CourtDates.DoesNotExist:
        start_year = court.start_year
        end_year = court.end_year
    if start_year == end_year:
        return str(start_year)
    else:
        return mark_safe("%s&nbsp;to&nbsp;%s" % (start_year, end_year))
