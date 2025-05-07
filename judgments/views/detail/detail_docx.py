import logging

import requests
from django.http import HttpResponse

from judgments.models.document_file import DocumentDocx


def detail_docx(request, document_uri):
    """
    Response for the legacy data.pdf endpoint, used by data reusers

    If there's a DOCX-derived PDF in the S3 bucket, return that.
    Otherwise fall back and redirect to the weasyprint version."""

    breakpoint()

    docx = DocumentDocx(document_uri)
    response = requests.get(docx.generate_uri())
    logging.debug("Response %s", response.status_code)
    if response.status_code == 200:
        return HttpResponse(
            response.content, content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    if response.status_code != 404:
        logging.warn(f"Unexpected {response.status_code} error on {document_uri} whilst trying to get docx")
