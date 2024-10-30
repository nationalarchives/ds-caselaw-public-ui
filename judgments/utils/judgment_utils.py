from typing import Optional

from caselawclient.errors import DocumentNotFoundError, MarklogicNotPermittedError
from caselawclient.models.documents import Document, DocumentURIString
from django.http import Http404

from .utils import get_document_by_uri


def get_published_document_by_uri(
    document_uri: DocumentURIString, cache_if_not_found: bool = False, search_query: Optional[str] = None
) -> Document:
    try:
        document = get_document_by_uri(document_uri, cache_if_not_found=cache_if_not_found, search_query=search_query)
        if not document:
            raise Http404(f"Document {document_uri} was not found")
    except DocumentNotFoundError:
        raise Http404(f"Document {document_uri} was not found")
    except MarklogicNotPermittedError:
        raise Http404(f"Document {document_uri} is not available")

    if not document.is_published:
        raise Http404(f"Document {document_uri} is not available")
    return document
