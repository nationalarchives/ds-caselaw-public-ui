from django.utils.safestring import mark_safe

from judgments.models import CourtDates

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