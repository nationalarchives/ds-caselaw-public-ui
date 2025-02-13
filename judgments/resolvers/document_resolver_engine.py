from typing import Optional

from caselawclient.types import DocumentIdentifierSlug
from django.http import Http404
from django.http.request import HttpRequest
from django.views.generic import View

from judgments.utils import api_client
from judgments.views.detail import best_pdf, detail_html, detail_xml, generated_pdf
from judgments.views.disambiguation import DisambiguationView


class DocumentResolverEngine(View):
    def dispatch(
        self,
        request: HttpRequest,
        document_uri: str,
        file_format: Optional[str] = None,
    ):
        fileformat_lookup = {
            "data.pdf": best_pdf,
            "generated.pdf": generated_pdf,
            "data.xml": detail_xml,
            "data.html": detail_html,
        }

        resolutions = api_client.resolve_from_identifier_slug(DocumentIdentifierSlug(document_uri))

        if not resolutions:
            msg = f"Unable to find a matching document at {document_uri}"
            raise Http404(msg)

        if len(resolutions) > 1:
            return DisambiguationView.as_view()(
                request, uri=document_uri, resolutions=resolutions, file_format=file_format
            )

        if file_format:
            return fileformat_lookup[file_format](request, document_uri)

        return detail_html(request, resolutions[0].document_uri.as_document_uri())
