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
