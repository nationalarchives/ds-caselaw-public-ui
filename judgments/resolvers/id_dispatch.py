from typing import Optional

from caselawclient.models.documents import DocumentURIString
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.urls import reverse
from django.views.generic import View

from judgments.utils import get_published_document_by_uri

_HTML_TYPES = ("text/html", "application/xhtml+xml")
_XML_TYPES = ("application/akn+xml", "application/xml")
_PDF_TYPES = ("application/pdf",)

# Order matters when Accept is */* or otherwise unconstrained: HTML first.
_OFFERED_TYPES = _HTML_TYPES + _XML_TYPES + _PDF_TYPES


def representation_kind_from_accept(request: HttpRequest) -> Optional[str]:
    """
    Choose a document representation from Accept.

    Returns one of: "html", "xml", "pdf", or None when Accept matches none of
    our representations (caller should respond 406).

    Missing Accept is treated by Django as */*, which selects HTML.
    """
    preferred = request.get_preferred_type(_OFFERED_TYPES)
    if preferred is None:
        return None
    if preferred in _XML_TYPES:
        return "xml"
    if preferred in _PDF_TYPES:
        return "pdf"
    return "html"


def location_for_representation(slug: str, kind: str) -> str:
    if kind == "xml":
        return reverse("detail", kwargs={"document_uri": slug, "file_format": "data.xml"})
    if kind == "pdf":
        return reverse("detail", kwargs={"document_uri": slug, "file_format": "data.pdf"})
    return reverse("detail", kwargs={"document_uri": slug})


class IdDispatchEngine(View):
    """
    Dereference an identity URL under `/id/` to a current representation.

    `/id/{document_uri}` identifies the document (the work), not a particular
    HTML/XML/PDF expression. We 303 to the preferred-slug representation chosen
    from Accept (HTML by default), or 406 if Accept matches nothing we offer.
    """

    def get(self, request: HttpRequest, document_uri: str) -> HttpResponse:
        document = get_published_document_by_uri(DocumentURIString(document_uri))

        # document.slug raises RuntimeError if there is no preferred identifier —
        # that is broken published data on our side, so a 500 is appropriate.
        slug = document.slug

        kind = representation_kind_from_accept(request)
        if kind is None:
            response = HttpResponse(status=406)
        else:
            response = HttpResponse(content="", status=303)
            response["Location"] = location_for_representation(slug, kind)

        response["Vary"] = "Accept"
        return response
