from typing import Optional

from caselawclient.models.documents import Document, DocumentURIString
from django import template

from judgments import utils

register = template.Library()


@register.filter
def get_title_to_display_in_html(document: Document) -> str:
    if not document.name:
        return ""

    if document.document_noun == "press summary":
        return document.name.removeprefix("Press Summary of ")

    return document.name


@register.simple_tag
def formatted_document_uri(document_uri: DocumentURIString, format: Optional[str] = None) -> str:
    return utils.formatted_document_uri(document_uri, format)
