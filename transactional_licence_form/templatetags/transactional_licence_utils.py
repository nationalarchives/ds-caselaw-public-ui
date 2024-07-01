from django import template

from ..utils import countries_and_territories_dict

register = template.Library()


@register.filter
def default_if_empty(value, default):
    if value is not None and len(value.strip()) > 0:
        return value
    else:
        return default


@register.filter
def submit_label_for_step(step):
    match step:
        case "nine-principles":
            return "Review your answers"
        case "review":
            return "Submit your application"
        case _:
            return "Next"


@register.filter
def has_other_field(option_index, other_field_subwidgets):
    return option_index - 1 in other_field_subwidgets.keys()


@register.filter
def get_subwidget_for_other_field(option_index, other_field_subwidgets):
    return other_field_subwidgets[option_index - 1]


@register.filter
def get_field_name(field, field_names):
    return field_names[field]


@register.filter
def get_form(form_key, all_forms):
    return all_forms[form_key]


@register.filter
def get_country_name(code):
    return countries_and_territories_dict().get(code)


@register.filter
def format_value_for_review(value, key):
    if key == "agent_country":
        return get_country_name(value)
    elif isinstance(value, list):
        return ", ".join(value)
    elif isinstance(value, dict):
        return ", ".join([format_value_for_review(value2, key) for value2 in value.values() if len(value2) > 0])
    else:
        return f"{value}"
