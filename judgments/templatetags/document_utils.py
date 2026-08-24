from caselawclient.models.documents import Document, DocumentURIString

from judgments import utils


def get_title_to_display_in_html(document: Document) -> str:
    if not document.body.name:
        return ""

    if document.document_noun == "press summary":
        return document.body.name.removeprefix("Press Summary of ")

    return document.body.name


def formatted_document_uri(document_uri: DocumentURIString, format: str | None = None) -> str:
    return utils.formatted_document_uri(document_uri, format)
