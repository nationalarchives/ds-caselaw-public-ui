from django import template

register = template.Library()


@register.filter
def error_messages(errors):
    error_message = ""
    if errors:
        for key in errors.keys():
            if key == "__all__":
                return "There are errors in the filters, please see below for details"
            else:
                error_message += f"Error in '{key}' - see below for details. "
    return error_message
