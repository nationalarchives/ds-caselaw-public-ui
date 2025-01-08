from typing import Optional

from caselawclient.models.documents import DocumentURIString
from caselawclient.types import InvalidDocumentURIException
from django.http import Http404
from django.http.request import HttpRequest
from django.views.generic import View

from judgments.utils.utils import api_client
from judgments.views.detail import best_pdf, detail_html, detail_xml, generated_pdf
from judgments.views.disambiguation import DisambiguationView
from judgments.views.press_summaries import press_summaries


class MarklogicInDocumentClothing(DocumentURIString):
    def __new__(self, value):
        return value.strip("/").replace(".xml", "")


class IdentifierResolverEngine(View):
    # TODO: make this not just a copy-paste

    def dispatch(
        self,
        request: HttpRequest,
        document_uri: str,
        file_format: Optional[str] = None,
        component: Optional[str] = None,
    ):
        fileformat_lookup = {
            "data.pdf": best_pdf,
            "generated.pdf": generated_pdf,
            "data.xml": detail_xml,
            "data.html": detail_html,
        }
        component_lookup = {
            "press-summary": press_summaries,
        }

        if document_uri[-1] == "/":
            raise Http404("Paths cannot end with a slash")
        resolutions = api_client.resolve_from_identifier(document_uri)
        if not resolutions:
            msg = f"No resolutions for {document_uri}"
            raise Http404(msg)
        if len(resolutions) > 1:
            return DisambiguationView.as_view()(
                request, uri=document_uri, resolutions=resolutions, file_format=file_format
            )

        resolution_uri = MarklogicInDocumentClothing(resolutions[0].document_uri)

        if file_format:
            return fileformat_lookup[file_format](request, resolution_uri)

        if component:
            return component_lookup[component](request, resolution_uri)

        return detail_html(request, resolution_uri)


class DocumentResolverEngine(View):
    def dispatch(
        self,
        request: HttpRequest,
        document_uri: str,
        file_format: Optional[str] = None,
        component: Optional[str] = None,
    ):
        fileformat_lookup = {
            "data.pdf": best_pdf,
            "generated.pdf": generated_pdf,
            "data.xml": detail_xml,
            "data.html": detail_html,
        }
        component_lookup = {
            "press-summary": press_summaries,
        }

        try:
            document_uri = DocumentURIString(document_uri)
        except InvalidDocumentURIException:
            raise Http404("Document Resolver recieved an invalid DocumentURIString")

        if file_format:
            return fileformat_lookup[file_format](request, document_uri)

        if component:
            return component_lookup[component](request, document_uri)

        return detail_html(request, document_uri)
