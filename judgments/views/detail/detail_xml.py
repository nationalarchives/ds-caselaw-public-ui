from caselawclient.models.documents import DocumentURIString
from django.http import HttpResponse
from django.urls import resolve

from judgments.utils import (
    get_published_document_by_uri,
)


def filename(request) -> str:
    return resolve(request.path).captured_kwargs["document_uri"].replace("/", "_")


def detail_xml(request, document_uri: DocumentURIString) -> HttpResponse:
    document = get_published_document_by_uri(document_uri)

    document_xml = document.body.content_as_xml

    response = HttpResponse(document_xml, content_type="application/xml")
    response["Content-Disposition"] = f"attachment; filename={filename(request)}.xml"
    return response
