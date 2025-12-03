from typing import Optional

from caselawclient.types import DocumentIdentifierSlug
from django.http import Http404
from django.http.request import HttpRequest
from django.views.generic import View

from judgments.utils import api_client
from judgments.views.detail import best_pdf, detail_html, detail_jinja, detail_xml, generated_pdf


class MultipleResolutionsError(Exception):
    """Multiple pages claim to live at this URL, and we do not yet have a disambiguation mechanic."""


class DocumentResolverEngine(View):
    def get_default_renderer(self):
        return detail_html

    def get_fileformat_renderer(self, file_format: str):
        lookup = {
            "data.pdf": best_pdf,
            "generated.pdf": generated_pdf,
            "data.xml": detail_xml,
            "data.html": detail_html,
        }
        return lookup[file_format]

    def dispatch(
        self,
        request: HttpRequest,
        document_uri: str,
        file_format: Optional[str] = None,
    ):
        resolved_documents = api_client.resolve_from_identifier_slug(DocumentIdentifierSlug(document_uri))

        if not resolved_documents:
            msg = f"Unable to find a matching document at {document_uri}"
            raise Http404(msg)

        if len(resolved_documents) > 1:
            slugs = [resolution.document_uri for resolution in resolved_documents]
            msg = f"Multiple resolutions found for {document_uri}: {', '.join(slugs)}"
            raise MultipleResolutionsError(msg)

        database_uri = resolved_documents[0].document_uri.as_document_uri()

        if file_format:
            renderer = self.get_fileformat_renderer(file_format)
            return renderer(request, database_uri)

        renderer = self.get_default_renderer()
        return renderer(request, database_uri)


class JinjaDocumentResolverEngine(DocumentResolverEngine):
    def get_default_renderer(self):
        return detail_jinja

    def get_fileformat_renderer(self, file_format: str):
        lookup = {
            "data.pdf": best_pdf,
            "generated.pdf": generated_pdf,
            "data.xml": detail_xml,
            "data.html": detail_jinja,
        }
        return lookup[file_format]
