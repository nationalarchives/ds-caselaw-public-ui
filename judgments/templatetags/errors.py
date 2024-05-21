from django import template

register = template.Library()


@register.filter
def error_messages(errors):
    if errors:
        error_message = ""
        for key in errors.keys():
            ", ".join(f"Errors in {key} - see below for details")
        return error_message
