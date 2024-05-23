from django import template

register = template.Library()


@register.filter
def error_messages(errors):
    """
    Templatetag to construct the error message for `page-notification-failure`.

    Given a form level error return a generic error.
    Given a field level error append the problem fields into the error message.
    """
    if "__all__" in errors.keys():
        return "Errors in form - see below for details"
    errors = [f"""'{error.replace("_", " ")}'""" for error in list(errors.keys())]
    errors = ", ".join(errors)
    return f"Errors in {errors} - see below for details"
