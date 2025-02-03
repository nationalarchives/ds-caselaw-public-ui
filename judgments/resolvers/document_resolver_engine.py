from typing import Optional

from caselawclient.models.documents import DocumentURIString
from caselawclient.types import InvalidDocumentURIException
from django.http import Http404
from django.http.request import HttpRequest
from django.views.generic import View

from judgments.views.detail import best_pdf, detail_html, detail_xml, generated_pdf
from judgments.views.press_summaries import press_summaries


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
