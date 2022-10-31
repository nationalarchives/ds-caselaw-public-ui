from django import template
from ds_caselaw_utils import courts as all_courts

register = template.Library()


@register.filter
def get_court_name(court):
    court_object = all_courts.get_by_param(court)
    if court_object is None:
        return ""
    return court_object.name
