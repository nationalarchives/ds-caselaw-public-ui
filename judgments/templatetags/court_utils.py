from django import template
from django.utils.safestring import mark_safe
from ds_caselaw_utils import courts as all_courts

from judgments.models import CourtDates

register = template.Library()


@register.filter
def get_court_name(court):
    try:
        court_object = all_courts.get_by_param(court)
    except KeyError:
        return ""
    return court_object.name


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
        return mark_safe("%s &ndash; %s" % (start_year, end_year))
