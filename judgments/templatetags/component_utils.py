from django import template

register = template.Library()


@register.simple_tag
def component_class_names(*values):
    return " ".join(class_name for value in values if value for class_name in str(value).split())
