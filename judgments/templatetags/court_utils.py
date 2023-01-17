from django import template
from django.utils.safestring import mark_safe
from ds_caselaw_utils import courts as all_courts

from judgments.models import CourtDates

register = template.Library()


@register.filter
def get_court_name(court):
    court_object = all_courts.get_by_param(court)
    if court_object is None:
        return ""
    return court_object.name


@register.filter
def get_court_date_range(court):
    try:
        db_dates = CourtDates.objects.get(pk=court.canonical_param)
        start_year = db_dates.start_year
        end_year = db_dates.end_year
    except CourtDates.DoesNotExist:
        start_year = court.start_year
        end_year = court.end_year
    if start_year == end_year:
        return str(start_year)
    else:
        return mark_safe("%s &ndash; %s" % (start_year, end_year))
