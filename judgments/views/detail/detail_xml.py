from django.http import HttpResponse

from judgments.utils import (
    get_published_document_by_uri,
)


def detail_xml(_request, document_uri):
    document = get_published_document_by_uri(document_uri)

    document_xml = document.content_as_xml

    response = HttpResponse(document_xml, content_type="application/xml")
    response["Content-Disposition"] = f"attachment; filename={document.uri}.xml"
    return response
