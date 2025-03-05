from typing import Optional

from caselawclient.types import DocumentIdentifierSlug
from django.http import Http404
from django.http.request import HttpRequest
from django.views.generic import View

from judgments.utils import api_client
from judgments.views.detail import best_pdf, detail_html, detail_xml, generated_pdf


class MultipleResolutionsError(Exception):
    """Multiple pages claim to live at this URL, and we do not yet have a disambiguation mechanic."""


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

        resolved_documents = api_client.resolve_from_identifier_slug(DocumentIdentifierSlug(document_uri))

        if not resolved_documents:
            msg = f"Unable to find a matching document at {document_uri}"
            raise Http404(msg)

        if len(resolved_documents) > 1:
            msg = f"Multiple resolutions found for {document_uri}"
            raise MultipleResolutionsError(msg)

        database_uri = resolved_documents[0].document_uri.as_document_uri()

        if file_format:
            return fileformat_lookup[file_format](request, database_uri)

        return detail_html(request, database_uri)
