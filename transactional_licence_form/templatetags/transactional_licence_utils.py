from django import template

register = template.Library()


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
