from django import template

import judgments.utils
from judgments.utils import preprocess_title

register = template.Library()


@register.filter(name='addcss')
def addcss(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter
def is_exact_match(result, query):
    return is_exact_title_match(result, query) or is_exact_ncn_match(result, query)


@register.filter
def is_exact_title_match(result, query):
    return preprocess_title(query) == preprocess_title(result.name)


@register.filter
def is_exact_ncn_match(result, query):
    return judgments.utils.is_exact_ncn_match(result, query)


@register.filter
def show_matches(result, query):
    return result.matches and not is_exact_match(result, query)
