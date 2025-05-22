from typing import Optional

from caselawclient.types import DocumentURIString
from django.http import Http404, HttpResponse
from django.http.request import HttpRequest
from django.urls import reverse
from django.views.generic import View

from judgments.utils import get_published_document_by_uri


class IdDispatchEngine(View):
    """
    A class to take an absolute object URI (ie something beginning `/id/`) and dispatch the user to the right place.

    At the moment, this can only be a document. We should, however, leave open the possibility of needing to dispatch other things in future.
    """

    def dispatch(
        self,
        request: HttpRequest,
        document_uri: str,
        file_format: Optional[str] = None,
    ):
        document = get_published_document_by_uri(DocumentURIString(document_uri))

        if preferred_id := document.identifiers.preferred():
            response = HttpResponse(content="", status=303)
            response["Location"] = reverse("detail", kwargs={"document_uri": preferred_id.url_slug})
            return response

        raise Http404(f"Document {document_uri} was not found")
