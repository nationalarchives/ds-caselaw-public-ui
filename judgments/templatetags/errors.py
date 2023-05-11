from django import template

register = template.Library()


@register.filter
def has_errors_for_field(errors, field):
    if errors:
        return errors.has_errors(field)
    else:
        return False


@register.filter
def has_errors(errors):
    if errors:
        return errors.has_errors()
    else:
        return False


@register.filter
def error_messages(errors):
    if errors:
        return ",".join(errors.messages)


@register.filter
def errors_for_field(errors, field):
    if errors:
        return ", ".join(errors.fields[field])
