from typing import Optional

from django import template

from judgments import utils

register = template.Library()


@register.filter
def get_title_to_display_in_html(document):
    if not document.name:
        return

    if document.document_noun == "press summary":
        return document.name.removeprefix("Press Summary of ")

    return document.name


@register.simple_tag
def formatted_document_uri(document_uri: str, format: Optional[str] = None):
    return utils.formatted_document_uri(document_uri, format)
